from app import create_app, database
from app.extensions import migrate

app = create_app()
migrate.init_app(app, database)