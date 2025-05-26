from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.LargeBinary(60), nullable=False)
    criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    orders = db.relationship("Order", backref="usuario", lazy=True)

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.LargeBinary(60), nullable=False)
    criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    aberto = db.Column(db.Boolean, default=False, nullable=False)

    produtos = db.relationship("Product", backref="empresa", lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255), default="default.png")
    price = db.Column(db.Float)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    itens = db.relationship("Carrinho", backref="order", lazy=True)

class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    produto = db.relationship("Product", backref="carrinhos")

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    tipo_end = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    complemento = db.Column(db.String(120))
    criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="enderecos")


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))