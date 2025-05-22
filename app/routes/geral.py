from flask import Blueprint, render_template, redirect, url_for
from flask import render_template, url_for, redirect, session
from flask_login import login_required, current_user
from app.models import Empresa

geral_bp = Blueprint("geral", __name__, url_prefix="/geral")

@geral_bp.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for("perfil", usuario=current_user))
    elif "empresa_id" in session:
        emp = Empresa.query.get(session["empresa_id"])
        if emp:
            return redirect(url_for("e_perfil", id_empresa=emp.id))
    return render_template("homepage.html")

@geral_bp.route("/inicio")
def inicio():
    return render_template("inicio.html")

@geral_bp.route("/pesquisa")
def pesquisa():
    return render_template("pesquisa.html")

@geral_bp.route("/carrinho") #, methods=['POST']
@login_required
def carrinho():
    return render_template("carrinho.html")

@geral_bp.route("/sobre")
def sobre():
    return render_template("sobre.html")

