

"""# Configuración de la base de datos
DB_CONFIG = {
    'server': 'localhost\\SQLEXPRESS',  # Cambia esto según el nombre de tu servidor SQL
    'database': 'COCODE_Gestion',       # El nombre de tu base de datos
    'username': 'cocode_Presidente',    # Usuario de SQL Server
    'password': 'cocode_Gest!ion'      # Contraseña del usuario
}"""

import logging
from flask_cors import CORS

from flask import Flask
from app.extensions import db  # Importar la instancia de SQLAlchemy desde extensions
from app.routes import personas_bp, derechos_bp, cuotas_bp, pagos_bp, ingresos_bp, egresos_bp, persona_derecho_bp# Importar los Blueprints

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})



    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://cocode_Presidente:cocode_Gest!ion@localhost\\SQLEXPRESS/COCODE_Gestion?driver=ODBC+Driver+17+for+SQL+Server"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar alertas innecesarias

    # Inicializar extensiones
    db.init_app(app)

    # Registrar Blueprints
    
    app.register_blueprint(personas_bp, url_prefix='/api')  # Opcional: Usar prefijo '/api'
    app.register_blueprint(derechos_bp, url_prefix='/api')  # Nuevo Blueprint para derechos
    app.register_blueprint(cuotas_bp, url_prefix='/api')
    app.register_blueprint(pagos_bp, url_prefix='/api')
    app.register_blueprint(ingresos_bp, url_prefix='/api')
    app.register_blueprint(egresos_bp, url_prefix='/api')
    app.register_blueprint(persona_derecho_bp, url_prefix='/api')
    
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

