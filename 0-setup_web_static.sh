#!/usr/bin/env bash
# A Bash script that sets up web servers for the deployment of web_static

# Install Nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Create necessary folders and files
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '/\blocation \/ {/a\
\    location /hbnb_static {\
\        alias /data/web_static/current/;\
\    }' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

# Exit successfully
exit 0
