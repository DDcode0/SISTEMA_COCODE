

# PREDEFINIMOS MODELOS DE LA BASE DE DATOS
# Aquí definimos los modelos de la base de datos utilizando SQLAlchemy
# Cada modelo representa una tabla en la base de datos y sus atributos representan las columnas de esa tabla.
# En este caso, definimos un modelo para la tabla "Personas" que contiene información sobre los miembros de la comunidad.


from app.extensions import db  # Importar `db` desde extensions

# Modelo para la tabla Personas
class Persona(db.Model):
    __tablename__ = 'Personas'

    ID_Persona = db.Column(db.Integer, primary_key=True)
    DPI = db.Column(db.String(13), nullable=False, unique=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Direccion = db.Column(db.String(200), nullable=True)
    Telefono = db.Column(db.String(15), nullable=True)
    Email = db.Column(db.String(100), nullable=True)
    Rol = db.Column(db.String(50), nullable=True)
    Estado = db.Column(db.String(10), nullable=False) 
    def __repr__(self):
        return f'<Persona {self.Nombre}>'

# Modelo para la tabla Derechos
class Derecho(db.Model):
    __tablename__ = 'Derechos'

    ID_Derecho = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Derecho {self.Nombre}>'

# Modelo para la tabla Persona_Derecho
class PersonaDerecho(db.Model):
    __tablename__ = 'Persona_Derecho'

    ID_Persona = db.Column(db.Integer, db.ForeignKey('Personas.ID_Persona'), primary_key=True)
    ID_Derecho = db.Column(db.Integer, db.ForeignKey('Derechos.ID_Derecho'), primary_key=True)
    Fecha_Inicio = db.Column(db.Date, nullable=False)
    Fecha_Fin = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<PersonaDerecho ID_Persona={self.ID_Persona}, ID_Derecho={self.ID_Derecho}>'

# Modelo para la tabla Cuotas
class Cuota(db.Model):
    __tablename__ = 'Cuotas'

    ID_Cuota = db.Column(db.Integer, primary_key=True)
    Descripcion = db.Column(db.String(100), nullable=False)
    Monto = db.Column(db.Numeric(10, 2), nullable=False)
    Fecha_Limite = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Cuota {self.Descripcion}, Monto={self.Monto}>'

# Modelo para la tabla Pagos
class Pago(db.Model):
    __tablename__ = 'Pagos'

    ID_Pago = db.Column(db.Integer, primary_key=True)
    ID_Persona = db.Column(db.Integer, db.ForeignKey('Personas.ID_Persona'), nullable=False)
    ID_Cuota = db.Column(db.Integer, db.ForeignKey('Cuotas.ID_Cuota'), nullable=False)
    Fecha_Pago = db.Column(db.Date, nullable=False)
    Monto_Pagado = db.Column(db.Numeric(10, 2), nullable=False)
    Estado = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Pago ID_Persona={self.ID_Persona}, Monto={self.Monto_Pagado}>'

# Modelo para la tabla Ingresos
class Ingreso(db.Model):
    __tablename__ = 'Ingresos'

    ID_Ingreso = db.Column(db.Integer, primary_key=True)
    Fecha = db.Column(db.Date, nullable=False)
    Monto = db.Column(db.Numeric(10, 2), nullable=False)
    Fuente = db.Column(db.String(100), nullable=True)
    Observaciones = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Ingreso Monto={self.Monto}, Fuente={self.Fuente}>'

# Modelo para la tabla Egresos
class Egreso(db.Model):
    __tablename__ = 'Egresos'

    ID_Egreso = db.Column(db.Integer, primary_key=True)
    Fecha = db.Column(db.Date, nullable=False)
    Monto = db.Column(db.Numeric(10, 2), nullable=False)
    Descripcion = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Egreso Monto={self.Monto}, Descripcion={self.Descripcion}>'
    
    

