from router.router import urls_blueprint
from router.web import web_blueprint
from app.manage import app

def create_app():
    
    app.register_blueprint(urls_blueprint, url_prefix='/v1')
    app.register_blueprint(web_blueprint, url_prefix='/')
    return app