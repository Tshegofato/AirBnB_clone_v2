#!/usr/bin/env bash
# Script to set up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create fake HTML file for testing Nginx configuration
echo "<html>
  <head>
    <title>Test Page</title>
  </head>
  <body>
    <p>This is a test page for Nginx configuration.</p>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config="server {
    listen 80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
    }
    error_page 404 /404.html;
    location = /404.html {
        internal;
        root /usr/share/nginx/html;
    }
    add_header X-Served-By \$HOSTNAME;
}"
echo "$config" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restart Nginx
sudo service nginx restart

# Exit successfully
exit 0
