# app/models.py
# -*- coding: utf-8 -*-

from datetime import date
from app.extensions import db

# Modelo Personas
class Persona(db.Model):
    __tablename__ = 'Personas'
    id_persona = db.Column('ID_Persona', db.Integer, primary_key=True)
    dpi        = db.Column('DPI',        db.String(13), nullable=False, unique=True)
    nombre     = db.Column('Nombre',     db.String(100), nullable=False)
    direccion  = db.Column('Direccion',  db.String(200), nullable=True)
    telefono   = db.Column('Telefono',   db.String(15),  nullable=True)
    email      = db.Column('Email',      db.String(100), nullable=True)
    rol        = db.Column('Rol',        db.String(50),  nullable=True)
    estado     = db.Column('Estado',     db.String(10),  nullable=False)

    def __repr__(self):
        return f"<Persona {self.nombre}>"

# Modelo Derechos
class Derecho(db.Model):
    __tablename__ = 'Derechos'
    id_derecho = db.Column('ID_Derecho', db.Integer, primary_key=True)
    nombre     = db.Column('Nombre',     db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Derecho {self.nombre}>"

# Modelo Persona_Derecho
class PersonaDerecho(db.Model):
    __tablename__ = 'Persona_Derecho'
    id_persona   = db.Column('ID_Persona',   db.Integer, db.ForeignKey('Personas.ID_Persona'), primary_key=True)
    id_derecho   = db.Column('ID_Derecho',   db.Integer, db.ForeignKey('Derechos.ID_Derecho'), primary_key=True)
    fecha_inicio = db.Column('Fecha_Inicio', db.Date,    nullable=False)
    fecha_fin    = db.Column('Fecha_Fin',    db.Date,    nullable=True)

    def __repr__(self):
        return f"<PersonaDerecho persona={self.id_persona} derecho={self.id_derecho}>"

# Modelo Cuotas
class Cuota(db.Model):
    __tablename__ = 'Cuotas'
    id_cuota     = db.Column('ID_Cuota',     db.Integer, primary_key=True)
    descripcion  = db.Column('Descripcion',  db.String(100), nullable=False)
    monto        = db.Column('Monto',        db.Numeric(9,2), nullable=False)
    fecha_limite = db.Column('Fecha_Limite', db.Date,    nullable=False)

    def __repr__(self):
        return f"<Cuota {self.descripcion} Q{self.monto}>"

# Modelo intermedio Derecho_Cuota
class DerechoCuota(db.Model):
    __tablename__ = 'Derecho_Cuota'
    id_derecho = db.Column('ID_Derecho', db.Integer, db.ForeignKey('Derechos.ID_Derecho'), primary_key=True)
    id_cuota   = db.Column('ID_Cuota',   db.Integer, db.ForeignKey('Cuotas.ID_Cuota'),     primary_key=True)

# Modelo intermedio Persona_Cuota
class PersonaCuota(db.Model):
    __tablename__ = 'Persona_Cuota'
    id_persona = db.Column('ID_Persona', db.Integer, db.ForeignKey('Personas.ID_Persona'), primary_key=True)
    id_cuota   = db.Column('ID_Cuota',   db.Integer, db.ForeignKey('Cuotas.ID_Cuota'),     primary_key=True)
    fecha_asig = db.Column('Fecha_Asig', db.Date,    nullable=False)
    estado     = db.Column('Estado',     db.String(20), nullable=False, default='Pendiente')

    persona = db.relationship('Persona', backref='cuotas_asignadas')
    cuota   = db.relationship('Cuota',   backref='personas_asignadas')

# Modelo Pagos
class Pago(db.Model):
    __tablename__ = 'Pagos'
    id_pago      = db.Column('ID_Pago',      db.Integer, primary_key=True)
    id_persona   = db.Column('ID_Persona',   db.Integer, nullable=False)
    id_cuota     = db.Column('ID_Cuota',     db.Integer, nullable=False)
    fecha_pago   = db.Column('Fecha_Pago',   db.Date,    nullable=False)
    monto_pagado = db.Column('Monto_Pagado', db.Numeric(9,2), nullable=False)
    estado       = db.Column('Estado',       db.String(50),  nullable=False)

    @staticmethod
    def registrar_pago(id_persona, id_cuota, fecha_pago, monto_pagado):
        pago = Pago(
            id_persona   = id_persona,
            id_cuota     = id_cuota,
            fecha_pago   = fecha_pago,
            monto_pagado = monto_pagado,
            estado       = 'Pendiente'
        )
        db.session.add(pago)
        db.session.flush()

        pc = PersonaCuota.query.get((id_persona, id_cuota))
        if pc:
            pc.estado = 'Completado' if monto_pagado >= pc.cuota.monto else 'Pendiente'

        from app.models import Ingreso
        ingreso = Ingreso(
            fecha   = fecha_pago,
            monto   = monto_pagado,
            id_pago = pago.id_pago
        )
        db.session.add(ingreso)
        db.session.commit()
        return pago

# Modelo Ingresos
class Ingreso(db.Model):
    __tablename__ = 'Ingresos'
    id_ingreso    = db.Column('ID_Ingreso',    db.Integer, primary_key=True)
    fecha         = db.Column('Fecha',         db.Date,    nullable=False)
    monto         = db.Column('Monto',         db.Numeric(9,2), nullable=False)
    fuente        = db.Column('Fuente',        db.String(100), nullable=True)
    observaciones = db.Column('Observaciones', db.Text,    nullable=True)
    id_pago       = db.Column('ID_Pago',       db.Integer, db.ForeignKey('Pagos.ID_Pago'), nullable=True)

    pago = db.relationship('Pago', backref='ingresos')

# Modelo Egresos
class Egreso(db.Model):
    __tablename__ = 'Egresos'
    id_egreso   = db.Column('ID_Egreso',   db.Integer, primary_key=True)
    fecha       = db.Column('Fecha',       db.Date,    nullable=False)
    monto       = db.Column('Monto',       db.Numeric(9,2), nullable=False)
    descripcion = db.Column('Descripcion', db.Text,    nullable=False)

    def __repr__(self):
        return f"<Egreso Q{self.monto}>"

