FROM itzg/minecraft-server:latest

USER root
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates python3; \
    curl -sSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o /tmp/ngrok.tgz; \
    tar -xzf /tmp/ngrok.tgz -C /usr/local/bin; rm /tmp/ngrok.tgz; \
    apt-get clean; rm -rf /var/lib/apt/lists/*

ENV EULA="TRUE" \
    TYPE="FABRIC" \
    VERSION="1.21.11" \
    MEMORY="3G" \
    ONLINE_MODE="false" \
    ENFORCE_SECURE_PROFILE="false" \
    MODRINTH_PROJECTS="lithium?,ferrite-core?,worldedit,c2me-fabric?,krypton?,noisium?"

COPY status.py /usr/local/bin/status.py
COPY hf-entrypoint.sh /usr/local/bin/hf-entrypoint.sh
RUN chmod +x /usr/local/bin/hf-entrypoint.sh && chmod -R 777 /data

ENTRYPOINT ["/usr/local/bin/hf-entrypoint.sh"]
