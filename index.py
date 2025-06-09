# instalar Flask
from flask import Flask, render_template, request, redirect, url_for, flash

# importar todos ls controladores
from Business.controlador_usuarios import usuario


app = Flask(__name__, template_folder='Presentacion')
app.secret_key = 'clave_secreta_segura'

# agregar rutas 
app.register_blueprint(usuario)

if __name__=='__main__':
    app.run(debug=True)

