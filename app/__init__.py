from router.router import urls_blueprint
from router.web import web_blueprint
from app.manage import app

def create_app():
    
    app.register_blueprint(urls_blueprint)
    app.register_blueprint(web_blueprint)
    return app