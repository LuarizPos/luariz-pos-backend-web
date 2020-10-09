from router.router import urls_blueprint
from app.manage import app

def create_app():
    
    app.register_blueprint(urls_blueprint, url_prefix='/v1')
    return app