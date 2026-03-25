FROM mysql:8.0.34-debian

ARG MYSQL_VERSION=8.0.34

# Keep only non-secret configuration baked into image
ENV MYSQL_DATABASE=userdb

# Copy initialization SQL and set ownership to mysql user
COPY --chown=mysql:mysql init.sql /docker-entrypoint-initdb.d/

# Healthcheck for orchestrators
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD mysqladmin ping -h 127.0.0.1 --silent || exit 1

# EXPOSE is informational; actual networking controlled by orchestration
EXPOSE 3306

# Notes:
# - Do NOT set MYSQL_ROOT_PASSWORD or MYSQL_PASSWORD here. Provide them at runtime via secrets.
# - Use a pinned tag or digest in CI/CD.