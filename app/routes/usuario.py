from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user

from app.forms import FormLogin, FormCadastro
from app.models import Empresa, Usuario, Product
from app.extensions import bcrypt, database

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

@usuario_bp.route("/login", methods=["GET","POST"])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario= Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", usuario=current_user))
    return render_template("login.html", form=formlogin)

@usuario_bp.route("/cadastro", methods=["GET","POST"])
def cadastro():
    formcadastro = FormCadastro()
    if formcadastro.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcadastro.senha.data)
        usuario = Usuario(username=formcadastro.username.data, senha=senha, email=formcadastro.email.data)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        # database.session.refresh(usuario)
        return redirect(url_for("perfil", usuario=current_user))
    return render_template("cadastro.html", form=formcadastro)

@usuario_bp.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", user=current_user) 
@usuario_bp.route("/perfil/enderecos", methods=["GET","POST"])

@login_required
def gerenciar_enderecos():
    form = Endereco()
    if form.validate_on_submit():
        novo_end = Endereco(
            usuario_id=current_user.id,
            tipo_end=form.tipo_end.data,
            endereco=form.endereco.data,
            numero=form.numero.data,
            bairro=form.bairro.data,
            complemento=form.complemento.data,
        )
        database.session.add(novo_end)
        database.session.commit()
        return redirect(url_for("gerenciar_enderecos"))
    enderecos = current_user.enderecos 
    return render_template("enderecos.html", form=form, enderecos=enderecos)


@usuario_bp.route("/produtos/<int:id_empresa>", methods=["GET", "POST"])
def produtos(id_empresa):
    emp = Empresa.query.get_or_404(id_empresa)
    return render_template("produtos.html", empresa=emp, produtos=emp.produtos)
