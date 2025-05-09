from Capim import database, app
from Capim.models import Usuario, Empresa, Product, Order, Carrinho

with app.app_context():
    database.create_all()