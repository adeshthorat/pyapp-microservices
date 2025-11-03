FROM mysql:8.0-debian

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/
COPY mysql.cnf /etc/mysql/conf.d/

EXPOSE 3306
