import hashlib
import hmac
import json
import logging
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

SECRET = os.environ["WEBHOOK_SECRET"].encode()
REPO_URL = os.environ["REPO_URL"]


def verify_signature(payload: bytes, header: str) -> bool:
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header[7:])


class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info(format % args)

    def do_POST(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        sig = self.headers.get("X-Hub-Signature-256", "")

        if not verify_signature(body, sig):
            logging.warning("Invalid webhook signature")
            self.send_response(403)
            self.end_headers()
            return

        try:
            event = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        ref = event.get("ref", "")
        if ref != "refs/heads/main":
            logging.info("Ignoring push to %s", ref)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ignored")
            return

        logging.info("Push to main — starting hugo-builder")
        subprocess.Popen([
            "docker", "compose", "run", "--rm", "hugo-builder",
        ], cwd="/project")

        self.send_response(202)
        self.end_headers()
        self.wfile.write(b"accepted")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9000), WebhookHandler)
    logging.info("Webhook listener running on :9000")
    server.serve_forever()
