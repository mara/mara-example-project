# Flask autodiscovery file: Flask >1.0 will automatically use the wsgi.py file in the root directory
from app.app import create_app

app = create_app()

# from werkzeug.contrib.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='/tmp/')

wsgi_app = app.wsgi_app
