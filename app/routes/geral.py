from flask import Blueprint, render_template, redirect, url_for
from flask import render_template, url_for, redirect, session
from flask_login import login_required, current_user
from app.models import Empresa
#from templates.

geral_bp = Blueprint("geral", __name__)

@geral_bp.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for("usuario.perfil"))
    elif "empresa_id" in session:
        emp = Empresa.query.get(session["empresa_id"])
        if emp:
            return redirect(url_for("empresa.e_perfil", id_empresa=emp.id))
    return render_template("geral/homepage.html")


@geral_bp.route("/pesquisa")
def pesquisa():
    return render_template("geral/pesquisa.html")

@geral_bp.route("/sobre")
def sobre():
    return render_template("geral/sobre.html")

