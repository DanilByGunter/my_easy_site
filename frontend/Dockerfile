# This Dockerfile is not used in the current setup
# Static files are served directly by nginx container via volume mount
# Keeping this file for potential future use

FROM nginx:alpine

# Copy static files
COPY . /usr/share/nginx/html

# Create custom error pages
RUN echo '<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>404 - Page Not Found</h1><p>The requested page could not be found.</p></body></html>' > /usr/share/nginx/html/404.html
RUN echo '<!DOCTYPE html><html><head><title>Server Error</title></head><body><h1>500 - Server Error</h1><p>Something went wrong on our end.</p></body></html>' > /usr/share/nginx/html/50x.html

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]