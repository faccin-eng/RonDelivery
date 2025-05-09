from Capim import database, login_manager
from datetime import datetime
from flask_login import UserMixin

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

    orders = database.relationship("Order", backref="usuario", lazy=True)

class Empresa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

    produtos = database.relationship("Product", backref="empresa", lazy=True)

class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120))
    descricao = database.Column(database.Text)
    imagem = database.Column(database.String(255), default="default.png")
    price = database.Column(database.Float)
    empresa_id = database.Column(database.Integer, database.ForeignKey("empresa.id"), nullable=False)

class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)
    criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

    itens = database.relationship("Carrinho", backref="order", lazy=True)

class Carrinho(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    order_id = database.Column(database.Integer, database.ForeignKey("order.id"), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey("product.id"), nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)

    produto = database.relationship("Product", backref="carrinhos")

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))