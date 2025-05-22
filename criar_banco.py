from App import database, app
from App.models import Usuario, Empresa, Product, Order, Carrinho

with app.app_context():
    database.create_all()