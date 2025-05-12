
# app/utils/validaciones.py
# Validaciones actualizadas para coincidir con los modelos y claves JSON

import logging
from app.models import Persona, Derecho, Cuota, Pago, Ingreso, Egreso, PersonaDerecho
from app.extensions import db
from datetime import datetime

# VALIDA DATOS DE PERSONA
# app/utils/validaciones.py

def validar_persona(datos: dict, actualizacion: bool = False) -> list[str]:
    """
    Valida los datos de una persona.
    - Si actualizacion=False (creación), exige DPI presente y único.
    - Si actualizacion=True, solo valida el DPI si viene en datos.
    """
    errores = []
    dpi = datos.get('DPI')

    # 1) Validar DPI
    if not actualizacion:
        # En creación: DPI obligatorio y único
        if not dpi or len(dpi) != 13 or not dpi.isdigit():
            errores.append('DPI debe ser un número de 13 dígitos.')
        elif Persona.query.filter_by(dpi=dpi).first():
            errores.append('El DPI ya está registrado.')
    else:
        # En actualización: si envían DPI, validarlo
        if 'DPI' in datos and dpi:
            if len(dpi) != 13 or not dpi.isdigit():
                errores.append('DPI debe ser un número de 13 dígitos.')
            else:
                # Si cambian el DPI, asegurarse de no colisionar con otro registro
                id_persona = datos.get('ID_Persona')
                existente = Persona.query.filter_by(dpi=dpi).first()
                if existente and existente.id_persona != id_persona:
                    errores.append('El DPI ya está registrado en otra persona.')

    # 2) Validar email
    correo = datos.get('Email')
    if correo and ('@' not in correo or '.' not in correo):
        errores.append('Correo electrónico inválido.')

    # 3) Validar estado
    estado = datos.get('Estado')
    if estado and estado not in ['Activo', 'Inactivo']:
        errores.append('El estado debe ser Activo o Inactivo.')

    # 4) Validar teléfono
    telefono = datos.get('Telefono')
    if telefono and (not telefono.isdigit() or not (7 <= len(telefono) <= 15)):
        errores.append('El teléfono debe ser numérico con una longitud válida.')

    # 5) Validar rol único
    rol = datos.get('Rol')
    roles_unicos = ['Presidente', 'Vicepresidente', 'Secretario', 'Tesorero',
                    'Vocal I', 'Vocal II', 'Vocal III']
    if rol in roles_unicos:
        existente = Persona.query.filter_by(rol=rol).first()
        # Si es actualización, permitir si es la misma persona
        if existente and (not datos.get('ID_Persona') or existente.id_persona != datos['ID_Persona']):
            errores.append(f"El rol '{rol}' ya está asignado a otra persona.")

    return errores


# VALIDA DATOS DE DERECHO
def validar_derecho(datos):
    errores = []
    nombre = datos.get('Nombre')
    if not nombre:
        errores.append('El nombre del derecho es obligatorio.')
    else:
        if Derecho.query.filter_by(nombre=nombre).first():
            errores.append('Este derecho ya existe.')
    return errores

# VALIDA DATOS DE CUOTA
def validar_cuota(datos):
    errores = []
    desc = datos.get('Descripcion')
    if not desc:
        errores.append('La descripción es obligatoria.')
    monto = datos.get('Monto')
    if monto is None or not isinstance(monto, (int, float)) or monto <= 0:
        errores.append('El monto debe ser un número positivo.')
    if not datos.get('Fecha_Limite'):
        errores.append('La fecha límite es obligatoria.')
    else:
        # Verifica formato YYYY-MM-DD
        try:
            datetime.strptime(datos['Fecha_Limite'], '%Y-%m-%d')
        except ValueError:
            errores.append('Fecha_Limite debe ser YYYY-MM-DD.')
    return errores

# VALIDA DATOS DE PAGO
def validar_pago(datos):
    errores = []
    # Persona
    id_persona = datos.get('ID_Persona')
    if not id_persona or not Persona.query.get(id_persona):
        errores.append('Persona inválida.')
    # Cuota
    id_cuota = datos.get('ID_Cuota')
    cuota = Cuota.query.get(id_cuota)
    if not cuota:
        errores.append('Cuota inválida.')
    # Fecha Pago
    fecha_pago = datos.get('Fecha_Pago')
    if not fecha_pago:
        errores.append('La fecha de pago es obligatoria.')
    else:
        try:
            datetime.strptime(fecha_pago, '%Y-%m-%d')
        except ValueError:
            errores.append('Fecha_Pago debe ser YYYY-MM-DD.')
    # Monto Pagado
    monto_pagado = datos.get('Monto_Pagado', 0)
    if monto_pagado <= 0:
        errores.append('El monto pagado debe ser mayor a cero.')
    # Lógica de saldo
    if cuota and id_persona:
        pagos_previos = db.session.query(db.func.sum(Pago.monto_pagado))\
            .filter(Pago.id_persona==id_persona, Pago.id_cuota==id_cuota).scalar() or 0
        if pagos_previos >= cuota.monto:
            errores.append('Esta cuota ya está completamente pagada.')
        elif monto_pagado + pagos_previos > cuota.monto:
            faltante = float(cuota.monto - pagos_previos)
            errores.append(f'El monto no puede exceder Q{faltante}.')
    return errores

# VALIDA DATOS DE INGRESO
def validar_ingreso(datos):
    errores = []
    # Fecha
    if not datos.get('Fecha'):
        errores.append('La fecha es obligatoria.')
    else:
        try:
            datetime.strptime(datos['Fecha'], '%Y-%m-%d')
        except ValueError:
            errores.append('Fecha debe ser YYYY-MM-DD.')
    # Monto
    try:
        monto = float(datos.get('Monto', 0))
        if monto <= 0:
            errores.append('El monto debe ser positivo.')
    except:
        errores.append('El monto debe ser un número válido.')
    # Fuente
    if not datos.get('Fuente'):
        errores.append('La fuente es obligatoria.')
    return errores



# VALIDA PERSONA_DERECHO
def validar_persona_derecho(datos):
    errores = []
    # ID_Persona y ID_Derecho
    if not datos.get('ID_Persona'):
        errores.append('ID_Persona es obligatorio.')
    if not datos.get('ID_Derecho'):
        errores.append('ID_Derecho es obligatorio.')
    # Fechas inicio/vencimiento
    fi = datos.get('Fecha_Inicio')
    ff = datos.get('Fecha_Fin')
    if not fi:
        errores.append('Fecha_Inicio obligatoria.')
    else:
        try:
            datetime.strptime(fi, '%Y-%m-%d')
        except:
            errores.append('Fecha_Inicio debe ser YYYY-MM-DD.')
    if ff:
        try:
            datetime.strptime(ff, '%Y-%m-%d')
        except:
            errores.append('Fecha_Fin debe ser YYYY-MM-DD.')
    if fi and ff and fi > ff:
        errores.append('Fecha_Inicio no puede ser posterior a Fecha_Fin.')
    return errores





def validar_egreso(datos: dict) -> list[str]:
    """
    Valida los datos para crear un egreso:
    1) Monto positivo y numérico.
    2) Fecha obligatoria.
    3) Descripción obligatoria y no duplicada.
    4) Fondos suficientes: (SUM ingresos) - (SUM egresos existentes).
    """
    errores = []

    # 1) Validación de Monto
    try:
        monto = float(datos.get('Monto', 0))
        if monto <= 0:
            errores.append('El monto debe ser un número positivo.')
    except (TypeError, ValueError):
        errores.append('El monto debe ser un número válido.')

    # 2) Validación de Fecha
    if not datos.get('Fecha'):
        errores.append('La fecha es obligatoria.')
        logging.error("Validación fallida en Egreso: Fecha faltante.")

    # 3) Validación de Descripción
    descripcion = datos.get('Descripcion')
    if not descripcion:
        errores.append('La descripción es obligatoria.')
        logging.error("Validación fallida en Egreso: Descripción faltante.")
    else:
        # Evitar duplicados exactos por fecha+descripción
        if datos.get('Fecha') and Egreso.query.filter_by(
            fecha=datos['Fecha'],
            descripcion=descripcion
        ).first():
            errores.append('Ya existe un egreso registrado con esta fecha y descripción.')

    # 4) Validación de fondos disponibles
    # Solo procedemos si no hay errores previos
    if not errores:
        total_ingresos = db.session.query(db.func.sum(Ingreso.monto)).scalar() or 0
        total_egresos  = db.session.query(db.func.sum(Egreso.monto)).scalar()  or 0
        fondos_disp    = total_ingresos - total_egresos

        if monto > fondos_disp:
            errores.append(
                f'Fondos insuficientes. Disponible: Q{fondos_disp:.2f}. '
                f'Egreso solicitado: Q{monto:.2f}.'
            )
            logging.error(
                f"Validación fallida en Egreso: fondos insuficientes "
                f"(disp={fondos_disp}, sol={monto})."
            )

    return errores