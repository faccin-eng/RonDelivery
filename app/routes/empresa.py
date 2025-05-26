from flask import Blueprint, render_template, redirect, url_for, session, abort, current_app, request
from werkzeug.utils import secure_filename

from app.forms import FormCadastro_Emp, FormLogin_Emp, FormProduto
from app.models import Empresa, Product, Order
from app.extensions import bcrypt, db
from app.decorators import empresa_login_required
from flask_login import login_required

import os


empresa_bp = Blueprint("empresa", __name__, url_prefix="/empresa")

@empresa_bp.route("/empresa/cadastro", methods=["GET","POST"])
def cadastro_empresa():
    form = FormCadastro_Emp()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.senha.data)
        emp = Empresa(
            username=form.username.data,
            senha=hashed,
            email=form.email.data
            )
        db.session.add(emp)
        db.session.commit()

        session["empresa_id"] = emp.id
        return redirect(url_for("empresa.e_perfil", id_empresa=emp.id))
    return render_template("empresa/e_cadastro.html", form=form)

@empresa_bp.route("/empresa/login", methods=["GET", "POST"])
def login_empresa():
    form = FormLogin_Emp()

    if form.validate_on_submit():
        emp = Empresa.query.filter_by(email=form.email.data).first()
        if emp and bcrypt.check_password_hash(emp.senha, form.senha.data):
            session["empresa_id"] = emp.id
            return redirect(url_for("empresa.e_perfil", id_empresa=emp.id))
    return render_template("empresa/e_login.html", form=form)


@empresa_bp.route("/add_produtos/<int:id_empresa>", methods=["GET", "POST"])
@empresa_login_required
def add_produtos(id_empresa):
    emp = Empresa.query.get_or_404(id_empresa)
    form = FormProduto()
    
    if session.get("empresa_id") == emp.id and form.validate_on_submit():
        imagem = form.imagem.data
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        novo = Product(
            name=form.nome.data,
            descricao = form.descricao.data,
            price=form.preco.data,
            imagem=filename,  # somente nome ou caminho
            empresa_id=emp.id
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("empresa.add_produtos", id_empresa=emp.id))

    return render_template(
        "empresa/e_produtos.html", empresa=emp, produtos=emp.produtos, form=form if session.get("empresa_id") == emp.id else None)

@empresa_bp.route("/e_perfil/<int:id_empresa>")
@empresa_login_required
def e_perfil(id_empresa):
    empresa = Empresa.query.get_or_404(id_empresa)

    # Só permite se a empresa logada for a dona do perfil
    if session.get("empresa_id") != empresa.id:
        abort(403)

    ordens = Order.query.filter_by(empresa_id=empresa.id).all()

    return render_template("empresa/e_perfil.html", empresa=empresa, ordens=ordens)

@empresa_bp.route("/empresa/logout")
def logout_empresa():
    session.pop("empresa_id", None)
    return redirect(url_for("geral.homepage"))

@empresa_bp.route('/toggle_status/<int:empresa_id>', methods=['POST'])
@empresa_login_required
def toggle_status(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    empresa.aberto = not empresa.aberto
    db.session.commit()
    return redirect(request.referrer or url_for('empresa.e_perfil', empresa_id=empresa_id))