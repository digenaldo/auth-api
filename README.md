Tutorial Inicial

1) preparar ambiente

# (se usa asdf e viu "No version is set for command python3")
asdf install python 3.11.9
asdf local python 3.11.9

mkdir auth-api && cd auth-api
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask_sqlalchemy flask_migrate flask-jwt-extended bcrypt python-dotenv

2) estrutura de pastas

mkdir -p app/{routes,auth}
touch app/__init__.py app/extensions.py app/models.py app/routes/__init__.py app/routes/users.py app/auth/service.py config.py wsgi.py .flaskenv .gitignore

3) arquivos
.flaskenv (facilita flask run)

FLASK_APP=wsgi.py
FLASK_DEBUG=1

Codar o Config.py

Codar o app/extensions.py

Codar o app/models.py

Codar o app/auth/service.py

Codar o app/routes/users.py

Codar app/models.py

Codar app/auth/service.py

Codar app/routes/users.py

Codar app/__init__.py

Codar wsgi.py

4) inicializar banco e rodar

flask db init
flask db migrate -m "init: users"
flask db upgrade
flask run