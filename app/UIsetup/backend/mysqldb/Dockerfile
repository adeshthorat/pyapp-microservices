FROM mysql:8.0-debian

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=userdb
ENV MYSQL_USER=myuser
ENV MYSQL_PASSWORD=mypass

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306
