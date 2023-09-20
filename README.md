# Household-Account-Book-App
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/nw-engineer/Household-Account-Book-App/blob/main/LICENSE.txt) 
[![](https://img.shields.io/badge/Pypi-0.0.1-FF9E0F.svg?logo=pypi&style=popout)](https://pypi.org/project/Household-Account-Book-App/)
![](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&style=popout)
[![Downloads](https://static.pepy.tech/badge/Household-Account-Book-App)](https://pepy.tech/project/Household-Account-Book-App)

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
tar zxvf build.tar.gz && chown -R nginx:nginx build && rm -rf build.tar.gz
cd Household-Account-Book-App
cp app.conf /etc/nginx/conf.d/
systemctl restart nginx
uvicorn main:app --reload
```
If you run it using the systemctl command, please rewrite the main.py path in the fastapi-app.service file appropriately.

The API server can also be started using the following method.

```bassh
pip3 install Household_Account_Book_App
cp Household-Account-Book-App/config.json ./
Household_Account_Book_App
```

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
