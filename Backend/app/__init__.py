

"""# Configuración de la base de datos
DB_CONFIG = {
    'server': 'localhost\\SQLEXPRESS',  # Cambia esto según el nombre de tu servidor SQL
    'database': 'COCODE_Gestion',       # El nombre de tu base de datos
    'username': 'cocode_Presidente',    # Usuario de SQL Server
    'password': 'cocode_Gest!ion'      # Contraseña del usuario
}"""
from flask_migrate import Migrate
import logging
from flask_cors import CORS

from flask import Flask
from app.extensions import db  # Importar la instancia de SQLAlchemy desde extensions

from app.routes import api

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})



    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://cocode_Presidente:cocode_Gest!ion@localhost\\SQLEXPRESS/COCODE_Gestion?driver=ODBC+Driver+17+for+SQL+Server"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar alertas innecesarias

    # Inicializar extensiones
    db.init_app(app)
    app.register_blueprint(api) 

    migrate = Migrate(app, db)
    # Registrar Blueprints
    
    
    
    #Configurar el sistema de logging global
    logging.basicConfig(
        level=logging.INFO,  # Nivel de registro (INFO, WARNING, ERROR)
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("system.log"),  # Guardar logs en archivo
            logging.StreamHandler()            # Mostrar logs en la consola
        ]
    )
    
    
    
    return app

