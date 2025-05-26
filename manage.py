from app import create_app, db
from app.extensions import migrate

app = create_app()
migrate.init_app(app, db)