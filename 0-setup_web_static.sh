#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static
sudo apt-get -y update

# Install nginx
sudo apt-get install nginx

# Create folders
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Add custom HTML content
echo "Here we go" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -fs /data/web_static/releases/test/ /data/web_static/current

# Directory and file permissions
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
sudo sed -i '54 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default

# Restart nginx
sudo service nginx restart
