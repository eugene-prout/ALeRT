from config import settings

bind = settings.gunicornbind
accesslog = settings.gunicornaccesslog
access_log_format = settings.gunicornaccesslogformat

workers = settings.gunicornworkers
threads = settings.gunicornthreads

reload = settings.gunicornreload
