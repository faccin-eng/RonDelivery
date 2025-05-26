from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user, login_user

from app.forms import FormLogin, FormCadastro, EnderecoForm
from app.models import Empresa, Usuario, Product, Endereco
from app.extensions import bcrypt, db

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

@usuario_bp.route("/login", methods=["GET","POST"])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario= Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("usuario.perfil", usuario=current_user))
    return render_template("usuario/login.html", form=formlogin)

@usuario_bp.route("/cadastro", methods=["GET","POST"])
def cadastro():
    formcadastro = FormCadastro()
    if formcadastro.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcadastro.senha.data)
        usuario = Usuario(username=formcadastro.username.data, senha=senha, email=formcadastro.email.data)

        db.session.add(usuario)
        db.session.commit()
        login_user(usuario, remember=True)
        # db.session.refresh(usuario)
        return redirect(url_for("usuario.perfil", usuario=current_user))
    return render_template("usuario/cadastro.html", form=formcadastro)

@usuario_bp.route("/perfil")
@login_required
def perfil():
    return render_template("usuario/perfil.html", user=current_user) 

@usuario_bp.route("/perfil/enderecos", methods=["GET","POST"])
@login_required
def gerenciar_enderecos():
    form = EnderecoForm()
    if form.validate_on_submit():
        novo_end = Endereco(
            usuario_id=current_user.id,
            tipo_end=form.tipo_end.data,
            endereco=form.endereco.data,
            numero=form.numero.data,
            bairro=form.bairro.data,
            complemento=form.complemento.data,
        )
        db.session.add(novo_end)
        db.session.commit()
        return redirect(url_for("usuario.gerenciar_enderecos"))
    enderecos = Endereco.query.filter_by(usuario_id=current_user.id).all()
    return render_template(
        "usuario/enderecos.html",
        form=form,
        enderecos=enderecos,
        user=current_user)


@usuario_bp.route("/produtos/<int:id_empresa>", methods=["GET", "POST"])
def produtos(id_empresa):
    empresa = Empresa.query.get_or_404(id_empresa)
    produtos = empresa.produtos
    return render_template("usuario/produtos.html", empresa=empresa, produtos=empresa.produtos)

@usuario_bp.route("/inicio")
def inicio():
    empresas = Empresa.query.filter_by(aberto=True).all()
    return render_template("usuario/inicio.html", empresas=empresas)

@usuario_bp.route("/carrinho") #, methods=['POST']
@login_required
def carrinho():
    return render_template("usuario/carrinho.html")

@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user() #ele já sabe que precisa deslogar o current user
    return render_template("usuario/logout.html")