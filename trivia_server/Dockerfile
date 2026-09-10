FROM python:3.8-slim

WORKDIR /app

# build-essential + libjpeg/zlib: needed by Pillow (avatar image uploads).
# PyMySQL is pure-Python, so no MySQL client headers are required.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
