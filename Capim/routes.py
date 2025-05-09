from flask import render_template, url_for, redirect, session, abort
from Capim import app, database, bcrypt
from Capim.models import Usuario, Empresa
from flask_login import login_required, login_user, logout_user, current_user
from Capim.forms import FormLogin, FormCadastro, FormLogin_Emp, FormCadastro_Emp, FormProduto

@app.route("/")
def homepage():
    return render_template("homepage.html")

# --------------------
# Cliente (Usuario)
# --------------------

@app.route("/login", methods=["GET","POST"])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario= Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", usuario=current_user))
    return render_template("login.html", form=formlogin)

@app.route("/cadastro", methods=["GET","POST"])
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

@app.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", user=current_user) # current_user já disponível no template, posso remover?

# --------------------
# Empresa
# --------------------

@app.route("/empresa/cadastro", methods=["GET","POST"])
def cadastro_empresa():
    form = FormCadastro_Emp()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.senha.data)
        emp = Empresa(
            username=form.username.data,
            senha=hashed,
            email=form.email.data
            )
        database.session.add(emp)
        database.session.commit()

        session["empresa_id"] = emp.id
        return redirect(url_for("produtos", id_empresa=emp.id))
    return render_template("e_cadastro.html", form=form)

@app.route("/empresa/login", methods=["GET", "POST"])
def login_empresa():
    form = FormLogin_Emp()
    if form.validate_on_submit():
        emp = Empresa.query.filter_by(email=form.email.data).first()
        if emp  and bcrypt.check_password_hash(emp.senha, form.senha.data):
            session["empresa_id"] = emp.id
            return redirect(url_for("produtos", id_empresa=emp.id))
    return render_template("e_login.html", form=form)


@app.route("/produtos/<int:id_empresa>", methods=["GET", "POST"])
def produtos(id_empresa):
    emp = Empresa.query.get_or_404(id_empresa)
    form = FormProduto()
    
    if session.get("empresa_id") == emp.id and form.validate_on_submit():
        novo = Product(
            name=form.nome.data,
            description = form.descricao.data,
            price=form.preco.data,
            imagem=form.imagem.data,  # adapte conforme upload
            empresa_id=emp.id
        )
        database.session.add(novo)
        database.session.commit()
        return redirect(url_for("produtos", id_empresa=emp.id))

    return render_template(
        "produtos.html", empresa=emp, produtos=emp.produtos, form=form if session.get("empresa_id") == emp.id else None)


@app.route("/pesquisa")
def pesquisa():
    return render_template("pesquisa.html")

@app.route("/carrinho") #, methods=['POST']
@login_required
def carrinho():
    return render_template("carrinho.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/logout")
@login_required
def logout():
    logout_user() #ele já sabe que precisa deslogar o current user
    return render_template("logout.html")

@app.route("/empresa/logout")
def logout_empresa():
    session.pop("empresa_id", None)
    return redirect(url_for("homepage"))
