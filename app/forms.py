from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, SubmitField, DecimalField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import Usuario, Empresa, Product

class FormLogin_Emp(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")
    
class FormCadastro_Emp(FlaskForm):
    username = StringField("Nome da Empresa", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Cadastrar Empresa")
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first() or Empresa.query.filter_by(email=email.data).first():
            raise ValidationError("Email já cadastrado")
        
class FormProduto(FlaskForm):
    nome = StringField("Titulo", validators=[DataRequired()])
    descricao = StringField("Texto", validators=[DataRequired()])
    preco = DecimalField("Valor (R$)", validators=[DataRequired()])
    imagem = FileField("Imagem", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")

# --------------------
# Cliente (Usuario)
# --------------------

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")
        
class FormCadastro(FlaskForm):
    username = StringField("Nome do usuário", validators=[DataRequired()])
    email =StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Fazer Cadastro")
    def validate_email(self, email):
        usuario= Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("Email já cadastrado")

class EnderecoForm(FlaskForm):
    tipo_end = SelectField(
        "Tipo de Endereço",
        choices=[("principal", "Principal"),
                 ("trabalho", "Trabalho"),
                 ("outro", "Outro")])
    endereco = StringField("Logradouro", validators=[DataRequired()])
    numero = IntegerField("Número", validators=[DataRequired()])
    bairro = StringField("Bairro", validators=[DataRequired()])
    complemento = StringField("Complemento (opcional)")
    submit = SubmitField("Salvar Endereço")

