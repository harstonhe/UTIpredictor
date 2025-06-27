# Use a lightweight Nginx image
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy application files to the web root
COPY utipredictor.html /usr/share/nginx/html/
COPY utipredictor.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/

# Create utipredictor directory and copy files there too
RUN mkdir -p /usr/share/nginx/html/utipredictor
COPY utipredictor.html /usr/share/nginx/html/utipredictor/
COPY utipredictor.html /usr/share/nginx/html/utipredictor/index.html
COPY styles.css /usr/share/nginx/html/utipredictor/

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"] 