# Use lightweight Nginx to serve static files
FROM nginx:alpine

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy your static site into Nginx's web directory
COPY index.html /usr/share/nginx/html/

# Expose HTTP port
EXPOSE 80

# Default command runs nginx
CMD ["nginx", "-g", "daemon off;"]
