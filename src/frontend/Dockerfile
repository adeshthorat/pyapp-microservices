# Use lightweight Nginx to serve static files
ARG type="alpine"
FROM nginx:${type}
LABEL app="frontendService"

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

RUN rm -rf /etc/nginx/conf.d/*

# Copy your static site into Nginx's web directory
COPY index.html /usr/share/nginx/html/

COPY default.conf /etc/nginx/conf.d/

# Expose HTTP port
EXPOSE 80

# Default command runs nginx
CMD ["nginx", "-g", "daemon off;"]
