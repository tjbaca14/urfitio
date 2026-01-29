sudo nano /etc/nginx/conf.d/urfit.io.conf; # edit nginx 
sudo nginx -t; # test nginx conf
sudo systemctl reload nginx; # reload nginx