from flask import Flask

# Crie a instância do Flask
flask_app = Flask(__name__)

@flask_app.route('/')
def hello_world():
    return 'Hello from Flask!'

# Caso deseje rodar Flask separadamente ou configurar o Django para servi-lo.
