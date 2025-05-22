from flask import Flask
from .extensions import database, bcrypt, login_manager, migrate
import os

def create_app():
    app = Flask(__name__) 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mkojil8809@localhost:5432/capim_limao'
    app.config["SECRET_KEY"] = "bddfaa05e05bcd560b8f8a239352802b" #SECRET
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'fotos_prod')

    database.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # migrate(app, database) 

    # database = SQLAlchemy(app)
    # bcrypt = Bcrypt(app)
    # login_manager = LoginManager(app)

    from app.routes.usuario import usuario_bp
    from app.routes.empresa import empresa_bp
    from app.routes.geral import geral_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(empresa_bp)
    app.register_blueprint(geral_bp)
    # app.register_blueprint(entregador_bp)

    @app.context_processor
    def inject_empresa():
        from flask import session
        from app.models import Empresa
        empresa_id = session.get("empresa_id")
        empresa = Empresa.query.get(empresa_id) if empresa_id else None
        return {"empresa_logada": empresa}
    
    return app