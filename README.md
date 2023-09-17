# Household-Account-Book-App

This app is a simple household account book.
It is assumed that the following configuration will be used.

## composition
- OS：Linux(CentOS)
- Python:3.11.5
- Python Library：fastapi,uvicorn,gunicorn,SQLAlchemy
- WebServer: Nginx

## procedure
```bash
git clone https://github.com/nw-engineer/Household-Account-Book-App.git
cd Household-Account-Book-App
mv build.tar.gz /var/www/html/
cd /var/www/html/
tar zxvf build.tar.gz && chown -R nginx:nginx build
cd Household-Account-Book-App
systemctl restart nginx
uvicorn main:app --reload
```
If you run it using the systemctl command, please rewrite the main.py path in the fastapi-app.service file appropriately.

## setting file
You can decide what day of the month you want to start the month on.
```json
{
  "day_threshold": 25
}
```
Changing the value of day_threshold will also change the WebUI aggregation period.

## screen image
![画像](/webui.png)
