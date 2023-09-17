bind = "127.0.0.1:8000"
workers = 1
accesslog = '/logs/applog/access.log'
errorlog = '/logs/applog/error.log'
worker_class = 'uvicorn.workers.UvicornWorker'
pidfile = '/var/run/gunicorn.pid'
