from app.models import Persona, Derecho, Cuota, Pago, Ingreso, Egreso, PersonaDerecho
import logging
from app.extensions import db

# Función de validación para Personas
def validar_persona(datos):
    errores = []
    if not datos.get('DPI') or len(datos['DPI']) != 13 or not datos['DPI'].isdigit():
        

        errores.append('DPI debe ser un número de 13 dígitos.')
        logging.error(f"Validación fallida en Persona: {'DPI'} no válido.")
        
    elif Persona.query.filter_by(DPI=datos['DPI']).first():
        errores.append('El DPI ya está registrado.')
        logging.error(f"Validación fallida en Persona: el dpi ya registrado.")

    if datos.get('Correo') and ('@' not in datos['Correo'] or '.' not in datos['Correo']):
        errores.append('Correo electrónico inválido.')
    if datos.get('Estado') and datos['Estado'] not in ['Activo', 'Inactivo']:
        errores.append('El estado debe ser Activo o Inactivo.')
    if datos.get('Telefono') and (not datos['Telefono'].isdigit() or not (7 <= len(datos['Telefono']) <= 15)):
        errores.append('El teléfono debe ser numérico con una longitud válida.')
        
    if datos.get('Rol') and datos['Rol'] in [
        'Presidente', 'Vicepresidente', 'Secretario', 'Tesorero',
        'Vocal I', 'Vocal II', 'Vocal III'
    ]:
        persona_existente = Persona.query.filter_by(Rol=datos['Rol']).first()
        if persona_existente:
            errores.append(f"El rol '{datos['Rol']}' ya está asignado a otra persona.")
            logging.error(f"Validación fallida en Persona: el rol '{datos['Rol']}' ya está ocupado.")


    return errores

# Función de validación para Derechos
def validar_derecho(datos):
    errores = []
    if not datos.get('Nombre'):
        errores.append('El nombre del derecho es obligatorio.')
        logging.error(f"Validación fallida en Derecho: nombre obiligatorio.")

    elif Derecho.query.filter_by(Nombre=datos['Nombre']).first():
        
        errores.append('Este derecho ya existe.')
        logging.error(f"Validación fallida en Derecho: Ya existe.")

    return errores

# Función de validación para Cuotas
def validar_cuota(datos):
    errores = []
    if not datos.get('Descripcion'):
        errores.append('La descripción es obligatoria.')
        
    if not isinstance(datos.get('Monto'), (int, float)) or datos['Monto'] <= 0:
        errores.append('El monto debe ser un número positivo.')
    if not datos.get('Fecha_Limite'):
        errores.append('La fecha límite es obligatoria.')
    return errores


def validar_pago(datos):
    errores = []

    # Validación de Persona
    if not datos.get('ID_Persona') or not Persona.query.get(datos['ID_Persona']):
        errores.append('Persona inválida.')
        logging.error(f"Validación fallida en Cuota: ID_Persona inválido.")

    

    # Validación de Cuota
    cuota = Cuota.query.get(datos.get('ID_Cuota'))
    if not cuota:
        errores.append('Cuota inválida.')
        logging.error("Validación fallida: ID_Cuota inválido.")
    else:
        # Calcular el monto restante
        
        pagos_previos = db.session.query(db.func.sum(Pago.Monto_Pagado)).filter(
            Pago.ID_Cuota == cuota.ID_Cuota, Pago.ID_Persona == datos['ID_Persona']
        ).scalar() or 0

        monto_restante = cuota.Monto - pagos_previos

        #validar que el monto pagado no sea cero
        if datos.get('Monto_Pagado', 0) <= 0:
            errores.append('El monto pagado debe ser mayor a cero.')
            logging.error(f"Validación fallida: Monto_Pagado no puede ser cero o negativo.")
        
        #validar si el monto previo es igual al monto de la cuota porque entonces ya esta pagado
        
        
        if pagos_previos >= cuota.Monto:
            errores.append('Esta cuota ya ha sido pagada completamente. No se pueden realizar más pagos.')
            logging.error("Validación fallida: Cuota completamente pagada.")

        # Validar que el monto pagado no exceda el monto restante
        elif datos.get('Monto_Pagado', 0) > monto_restante:
            errores.append(f'El monto pagado no puede exceder el monto restante: Q{monto_restante}.')
            logging.error(f"Validación fallida: Monto pagado ({datos['Monto_Pagado']}) excede el restante ({monto_restante}).")



    # Validación de Fecha de Pago
    if not datos.get('Fecha_Pago'):
        errores.append('La fecha de pago es obligatoria.')
        logging.error("Validación fallida: Fecha_Pago faltante.")



    return errores


def validar_ingreso(datos):
    errores = []

    # Validación de Monto
    try:
        
        monto = float(datos.get('Monto', 0))  # Intentar convertir a número
        
        if monto <= 0:
            errores.append('El monto debe ser un número positivo.')
    except ValueError:
        errores.append('El monto debe ser un número válido.')


    # Validación de Fecha
    if not datos.get('Fecha'):
        errores.append('La fecha es obligatoria.')

    # Validación de Fuente
    if not datos.get('Fuente'):
        errores.append('La fuente es obligatoria.')
        
    elif Ingreso.query.filter_by(Fecha=datos['Fecha'], Fuente=datos['Fuente']).first():
        errores.append('Ya existe un ingreso registrado con esta fecha y fuente.')


    return errores

def validar_egreso(datos):
    errores = []

    # Validación de Monto
    try:
        monto = float(datos.get('Monto', 0))  # Convertir a número
        if monto <= 0:
            errores.append('El monto debe ser un número positivo.')
    except ValueError:
        errores.append('El monto debe ser un número válido.')

    # Validación de Fecha
    if not datos.get('Fecha'):
        errores.append('La fecha es obligatoria.')
        logging.error(f"Validación fallida en Pago: Fecha faltante.")

    # Validación de Descripción
    if not datos.get('Descripcion'):
        errores.append('La descripción es obligatoria.')
        logging.error(f"Validación fallida en Pago: Descripción faltante.")
    elif Egreso.query.filter_by(Fecha=datos['Fecha'], Descripcion=datos['Descripcion']).first():
        errores.append('Ya existe un egreso registrado con esta fecha y descripción.')

    return errores



def validar_persona_derecho(datos):
    errores = []

    if 'ID_Persona' not in datos:
        errores.append('ID_Persona es requerida.')
        logging.error("Validación fallida: falta ID_Persona en los datos.")
        return errores

    if 'ID_Derecho' not in datos:
        errores.append('ID_Derecho es requerido.')
        logging.error("Validación fallida: falta ID_Derecho en los datos.")
        return errores

    # Validación de Persona
    if not datos.get('ID_Persona') or not Persona.query.get(datos['ID_Persona']):
        errores.append('Persona inválida.')
        logging.error(f"Validación fallida en persona derecho: ")

    # Validación de Derecho
    if not datos.get('ID_Derecho') or not Derecho.query.get(datos['ID_Derecho']):
        errores.append('Derecho inválido.')
        logging.error(f"Validación fallida en persona derecho: ")

    # Validación de Fechas
    if not datos.get('Fecha_Inicio') or not datos.get('Fecha_Fin'):
        errores.append('Las fechas de inicio y fin son obligatorias.')
        logging.error(f"Validación fallida en persona derecho: ")
    elif datos['Fecha_Inicio'] > datos['Fecha_Fin']:
        errores.append('La fecha de inicio no puede ser posterior a la fecha de fin.')
        logging.error(f"Validación fallida en persona derecho: ")

    if PersonaDerecho.query.filter_by(ID_Persona=datos['ID_Persona'], ID_Derecho=datos['ID_Derecho']).first():
        errores.append('La relación entre esta Persona y este Derecho ya existe.')

    return errores