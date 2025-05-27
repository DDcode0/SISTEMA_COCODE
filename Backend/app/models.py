# app/models.py
# -*- coding: utf-8 -*-

from datetime import date
from app.extensions import db

# --------------------- Personas ---------------------
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


        # Relación con PersonaDerecho
    derechos_asignados = db.relationship(
        'PersonaDerecho',
        back_populates='persona',
        cascade='all, delete-orphan'
    )

    # Relación con PersonaCuota
    cuotas_asignadas = db.relationship(
        'PersonaCuota',
        back_populates='persona',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Persona {self.nombre}>"

    def asignar_derecho(self, id_derecho, fecha_asig):
        """
        1) Crea la relación PersonaDerecho
        2) Por cada cuota vinculada al derecho, crea un registro PersonaCuota
        """
        from app.models import PersonaDerecho, DerechoCuota, PersonaCuota

        # 1) Asignar el derecho
        pd = PersonaDerecho(
            ID_Persona   = self.id_persona,
            ID_Derecho   = id_derecho,
            Fecha_Inicio = fecha_asig,
            Fecha_Fin    = None
        )
        db.session.add(pd)

        # 2) Generar las cuotas automáticas
        enlaces = DerechoCuota.query.filter_by(ID_Derecho=id_derecho).all()
        for enlace in enlaces:
            pc = PersonaCuota(
                ID_Persona = self.id_persona,
                ID_Cuota   = enlace.ID_Cuota,
                Fecha_Asig = fecha_asig,
                Estado     = 'Pendiente'
            )
            db.session.add(pc)

        db.session.commit()


# --------------------- Derechos ---------------------
class Derecho(db.Model):
    __tablename__ = 'Derechos'
    ID_Derecho = db.Column('ID_Derecho', db.Integer, primary_key=True)
    Nombre     = db.Column('Nombre',     db.String(50), nullable=False)

    # Relaciones
    cuotas_asociadas    = db.relationship(
        'DerechoCuota',
        back_populates='derecho',
        cascade='all, delete-orphan'
    )
    personas_derechos = db.relationship(
        'PersonaDerecho',
        back_populates='derecho',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Derecho {self.Nombre}>"

# --------------------- Persona_Derecho ---------------------
class PersonaDerecho(db.Model):
    __tablename__ = 'Persona_Derecho'
    ID_Persona   = db.Column('ID_Persona',   db.Integer, db.ForeignKey('Personas.ID_Persona'),   primary_key=True)
    ID_Derecho   = db.Column('ID_Derecho',   db.Integer, db.ForeignKey('Derechos.ID_Derecho'),   primary_key=True)
    Fecha_Inicio = db.Column('Fecha_Inicio', db.Date,    nullable=False)
    Fecha_Fin    = db.Column('Fecha_Fin',    db.Date,    nullable=True)

    # Relaciones
    persona = db.relationship('Persona',  back_populates='derechos_asignados')
    derecho = db.relationship('Derecho',  back_populates='personas_derechos')

    def __repr__(self):
        return f"<PersonaDerecho Persona={self.ID_Persona} Derecho={self.ID_Derecho}>"

# --------------------- Cuotas ---------------------
class Cuota(db.Model):
    __tablename__ = 'Cuotas'
    ID_Cuota     = db.Column('ID_Cuota',     db.Integer, primary_key=True)
    Descripcion  = db.Column('Descripcion',  db.String(100), nullable=False, unique=True)
    Monto        = db.Column('Monto',        db.Numeric(9, 2), nullable=False)
    Fecha_Limite = db.Column('Fecha_Limite', db.Date,          nullable=False)

    # Relaciones
    derechos_asociados = db.relationship(
        'DerechoCuota',
        back_populates='cuota',
        cascade='all, delete-orphan'
    )
    personas_asignadas = db.relationship(
        'PersonaCuota',
        back_populates='cuota',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Cuota {self.Descripcion} Q{self.Monto}>"

# --------------------- Derecho_Cuota intermedia ---------------------
class DerechoCuota(db.Model):
    __tablename__ = 'Derecho_Cuota'
    ID_Derecho = db.Column('ID_Derecho', db.Integer, db.ForeignKey('Derechos.ID_Derecho'), primary_key=True)
    ID_Cuota   = db.Column('ID_Cuota',   db.Integer, db.ForeignKey('Cuotas.ID_Cuota'),     primary_key=True)

    # Relaciones
    derecho = db.relationship('Derecho', back_populates='cuotas_asociadas')
    cuota   = db.relationship('Cuota',   back_populates='derechos_asociados')

    def __repr__(self):
        return f"<DerechoCuota Derecho={self.ID_Derecho} Cuota={self.ID_Cuota}>"

# --------------------- Persona_Cuota intermedia ---------------------
class PersonaCuota(db.Model):
    __tablename__ = 'Persona_Cuota'
    ID_Persona = db.Column('ID_Persona', db.Integer, db.ForeignKey('Personas.ID_Persona'), primary_key=True)
    ID_Cuota   = db.Column('ID_Cuota',   db.Integer, db.ForeignKey('Cuotas.ID_Cuota'),     primary_key=True)
    Fecha_Asig = db.Column('Fecha_Asig', db.Date,    nullable=False)
    Estado     = db.Column('Estado',     db.String(20), nullable=False, default='Pendiente')

    # Relaciones
    persona = db.relationship('Persona', back_populates='cuotas_asignadas')
    cuota   = db.relationship('Cuota',   back_populates='personas_asignadas')

    def __repr__(self):
        return f"<PersonaCuota Persona={self.ID_Persona} Cuota={self.ID_Cuota} Estado={self.Estado}>"

# --------------------- Pagos ---------------------
class Pago(db.Model):
    __tablename__ = 'Pagos'
    ID_Pago      = db.Column('ID_Pago',      db.Integer, primary_key=True)
    ID_Persona   = db.Column('ID_Persona',   db.Integer, db.ForeignKey('Personas.ID_Persona'), nullable=False)
    ID_Cuota     = db.Column('ID_Cuota',     db.Integer, db.ForeignKey('Cuotas.ID_Cuota'),     nullable=False)
    Fecha_Pago   = db.Column('Fecha_Pago',   db.Date,    nullable=False)
    Monto_Pagado = db.Column('Monto_Pagado', db.Numeric(9,2), nullable=False)
    Estado       = db.Column('Estado',       db.String(50),  nullable=False)

    # Relaciones
    persona = db.relationship('Persona',  backref='pagos')
    cuota   = db.relationship('Cuota',    backref='pagos')
    ingresos= db.relationship('Ingreso',  back_populates='pago', cascade='all, delete-orphan')

    @staticmethod
    def registrar_pago(id_persona, id_cuota, fecha_pago, monto_pagado):
        pago = Pago(
            ID_Persona   = id_persona,
            ID_Cuota     = id_cuota,
            Fecha_Pago   = fecha_pago,
            Monto_Pagado = monto_pagado,
            Estado       = 'Pendiente'
        )
        db.session.add(pago)
        db.session.flush()

        # Actualiza el estado en PersonaCuota
        pc = PersonaCuota.query.get((id_persona, id_cuota))
        if pc:
            pc.Estado = 'Completado' if monto_pagado >= pc.cuota.Monto else 'Pendiente'

        # Genera ingreso asociado
        ingreso = Ingreso(
            Fecha        = fecha_pago,
            Monto        = monto_pagado,
            ID_Pago      = pago.ID_Pago
        )
        db.session.add(ingreso)
        db.session.commit()
        return pago

    def __repr__(self):
        return f"<Pago Persona={self.ID_Persona} Cuota={self.ID_Cuota} Monto={self.Monto_Pagado}>"

# --------------------- Ingresos ---------------------
class Ingreso(db.Model):
    __tablename__ = 'Ingresos'
    ID_Ingreso    = db.Column('ID_Ingreso',    db.Integer, primary_key=True)
    Fecha         = db.Column('Fecha',         db.Date,    nullable=False)
    Monto         = db.Column('Monto',         db.Numeric(9,2), nullable=False)
    Fuente        = db.Column('Fuente',        db.String(100), nullable=True)
    Observaciones = db.Column('Observaciones', db.Text,    nullable=True)
    ID_Pago       = db.Column('ID_Pago',       db.Integer, db.ForeignKey('Pagos.ID_Pago'), nullable=True)

    pago = db.relationship('Pago', back_populates='ingresos')

    def __repr__(self):
        return f"<Ingreso Q{self.Monto} Fecha={self.Fecha}>"

# --------------------- Egresos ---------------------
class Egreso(db.Model):
    __tablename__ = 'Egresos'
    ID_Egreso   = db.Column('ID_Egreso',   db.Integer, primary_key=True)
    Fecha       = db.Column('Fecha',       db.Date,    nullable=False)
    Monto       = db.Column('Monto',       db.Numeric(9,2), nullable=False)
    Descripcion = db.Column('Descripcion', db.Text,    nullable=False)

    def __repr__(self):
        return f"<Egreso Q{self.Monto} Fecha={self.Fecha}>"
