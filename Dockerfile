# Single dev container with both the Python/Django backend and the
# Node/Vue frontend toolchains, so one VS Code window (one container)
# can edit and run both trivia_server and trivia_front.
FROM python:3.8-slim

# --- Node.js 16.x (matches what trivia_front was built/tested against) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg build-essential libjpeg-dev zlib1g-dev \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Pre-install backend deps (kept separate from the bind mount so a
# `docker compose up --build` doesn't need to reinstall every time the
# source changes).
COPY trivia_server/requirements.txt trivia_server/requirements.txt
RUN pip install --no-cache-dir -r trivia_server/requirements.txt

# Pre-install frontend deps into the image; the node_modules volume in
# docker-compose.yml keeps this from being hidden by the bind mount.
COPY trivia_front/package.json trivia_front/package-lock.json trivia_front/
RUN cd trivia_front && npm install

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000 8080
ENTRYPOINT ["/workspace/entrypoint.sh"]
