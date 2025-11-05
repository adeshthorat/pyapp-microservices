#Global argument for Python version
ARG MYSQL_VER="8.0-debian"

#Can be overridden at build time
FROM mysql:${MYSQL_VER}

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

COPY my.cnf /etc/mysql/conf.d/

EXPOSE 3306
