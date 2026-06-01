FROM python:3.12-alpine

RUN apk add --no-cache docker-cli docker-cli-compose

WORKDIR /app
COPY server.py .

CMD ["python", "-u", "server.py"]
