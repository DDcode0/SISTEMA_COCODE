# creando cruds para las tablas de la base de datos



#inportar la base de datos y el modelo de la tabla persona

# Importamos la instancia de la base de datos

import logging
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Persona, Derecho, Cuota, Pago, Ingreso, Egreso, PersonaDerecho
from app.utils.validaciones import (
    validar_persona, validar_derecho, validar_cuota, validar_pago, validar_ingreso, 
    validar_egreso, validar_persona_derecho)





# Crear un Blueprint para las rutas relacionadas con personas
personas_bp = Blueprint('personas', __name__)

# Ruta para crear una persona
@personas_bp.route('/personas', methods=['POST'])
def crear_persona():
    
    datos = request.get_json()
    
    errores = validar_persona(datos)
    if errores:
        logging.error(f"Error al crear persona: {errores}")  # Log de error

        return jsonify({'errores': errores}), 400

    nueva_persona = Persona(
        DPI=datos.get('DPI'),
        Nombre=datos.get('Nombre'),
        Direccion=datos.get('Direccion'),
        Telefono=datos.get('Telefono'),
        Email=datos.get('Email'),
        Rol=datos.get('Rol'),
        Estado=datos.get('Estado', True)
    )
    db.session.add(nueva_persona)
    db.session.commit()
    
    ## Log de éxito
    logging.info(f"Persona creada exitosamente: DPI={datos['DPI']}")  # Log de éxito
    
    mensaje = f"La persona {datos['Nombre']} ha sido registrada exitosamente con el rol '{datos['Rol']}'."
    
    return jsonify({
        'mensaje': mensaje,
        'persona': {
            'ID_Persona': nueva_persona.ID_Persona,
            'Nombre': nueva_persona.Nombre,
            'Rol': nueva_persona.Rol
        }
    }), 201


# Ruta para obtener todas las personas
@personas_bp.route('/personas', methods=['GET'])
def obtener_personas():
    personas = Persona.query.all()
    resultado = [
        {
            'ID_Persona': persona.ID_Persona,
            'DPI': persona.DPI,
            'Nombre': persona.Nombre,
            'Direccion': persona.Direccion,
            'Telefono': persona.Telefono,
            'Email': persona.Email,
            'Rol': persona.Rol,
            'Estado': persona.Estado
        }
        for persona in personas
    ]
    return jsonify(resultado), 200

# Ruta para obtener una persona específica
@personas_bp.route('/personas/<int:id_persona>', methods=['GET'])
def obtener_persona(id_persona):
    persona = Persona.query.get_or_404(id_persona)
    return jsonify({
        'ID_Persona': persona.ID_Persona,
        'DPI': persona.DPI,
        'Nombre': persona.Nombre,
        'Direccion': persona.Direccion,
        'Telefono': persona.Telefono,
        'Email': persona.Email,
        'Rol': persona.Rol,
        'Estado': persona.Estado
    }), 200

# Ruta para actualizar una persona
@personas_bp.route('/personas/<int:id_persona>', methods=['PUT'])
def actualizar_persona(id_persona):
    persona = Persona.query.get_or_404(id_persona)
    datos = request.get_json()
    persona.DPI = datos.get('DPI', persona.DPI)
    persona.Nombre = datos.get('Nombre', persona.Nombre)
    persona.Direccion = datos.get('Direccion', persona.Direccion)
    persona.Telefono = datos.get('Telefono', persona.Telefono)
    persona.Email = datos.get('Email', persona.Email)
    persona.Rol = datos.get('Rol', persona.Rol)
    persona.Estado = datos.get('Estado', persona.Estado)
    db.session.commit()
    return jsonify({'mensaje': 'Persona actualizada exitosamente'}), 200

# Ruta para eliminar una persona
@personas_bp.route('/personas/<int:id_persona>', methods=['DELETE'])
def eliminar_persona(id_persona):
    persona = Persona.query.get_or_404(id_persona)
    db.session.delete(persona)
    db.session.commit()
    return jsonify({'mensaje': 'Persona eliminada exitosamente'}), 200


#==========================================================================================================
#rutas para la tabla derechos


# Crear un Blueprint para las rutas de derechos
derechos_bp = Blueprint('derechos', __name__)

# Ruta para crear un derecho
@derechos_bp.route('/derechos', methods=['POST'])
def crear_derecho():
    datos = request.get_json()
    
    # Validar los datos de entrada
    errores = validar_derecho(datos)
    
    if errores:
        logging.error(f"Error al crear derecho: {errores}")  # Log de error

        return jsonify({'errores': errores}), 400

    nuevo_derecho = Derecho(Nombre=datos.get('Nombre'))
    db.session.add(nuevo_derecho)
    db.session.commit()
    logging.info(f"Derecho creado exitosamente: Nombre={datos['Nombre']}")  # Log de éxito

    return jsonify({'mensaje': 'Derecho creado exitosamente', 'derecho': {'ID_Derecho': nuevo_derecho.ID_Derecho, 'Nombre': nuevo_derecho.Nombre}}), 201

# Ruta para obtener todos los derechos
@derechos_bp.route('/derechos', methods=['GET'])
def obtener_derechos():
    derechos = Derecho.query.all()
    resultado = [{'ID_Derecho': derecho.ID_Derecho, 'Nombre': derecho.Nombre} for derecho in derechos]
    return jsonify(resultado), 200

# Ruta para obtener un derecho específico
@derechos_bp.route('/derechos/<int:id_derecho>', methods=['GET'])
def obtener_derecho(id_derecho):
    derecho = db.session.get(Derecho, id_derecho)
    if derecho:
        return jsonify({'ID_Derecho': derecho.ID_Derecho, 'Nombre': derecho.Nombre}), 200
    else:
        return jsonify({'mensaje': 'Derecho no encontrado'}), 404

# Ruta para actualizar un derecho
@derechos_bp.route('/derechos/<int:id_derecho>', methods=['PUT'])
def actualizar_derecho(id_derecho):
    derecho = db.session.get(Derecho, id_derecho)
    if not derecho:
        return jsonify({'mensaje': 'Derecho no encontrado'}), 404

    datos = request.get_json()
    derecho.Nombre = datos.get('Nombre', derecho.Nombre)
    db.session.commit()
    return jsonify({'mensaje': 'Derecho actualizado exitosamente'}), 200

# Ruta para eliminar un derecho
@derechos_bp.route('/derechos/<int:id_derecho>', methods=['DELETE'])
def eliminar_derecho(id_derecho):
    derecho = db.session.get(Derecho, id_derecho)
    if not derecho:
        return jsonify({'mensaje': 'Derecho no encontrado'}), 404

    db.session.delete(derecho)
    db.session.commit()
    return jsonify({'mensaje': 'Derecho eliminado exitosamente'}), 200




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Crear un Blueprint para las rutas de cuotas
cuotas_bp = Blueprint('cuotas', __name__)

# Ruta para crear una cuota
@cuotas_bp.route('/cuotas', methods=['POST'])
def crear_cuota():
    datos = request.get_json()
    
    # Validar los datos de entrada
    errores = validar_cuota(datos)
    if errores:
        logging.error(f"Error al crear cuota: {errores}")  # Log de error

        return jsonify({'errores': errores}), 400

    
    nueva_cuota = Cuota(
        Descripcion=datos.get('Descripcion'),
        Monto=datos.get('Monto'),
        Fecha_Limite=datos.get('Fecha_Limite')
    )
    db.session.add(nueva_cuota)
    db.session.commit()
    
    
    logging.info(f"Cuota creada exitosamente: Descripcion={datos['Descripcion']}") # Log de éxito
    return jsonify({'mensaje': 'Cuota creada exitosamente', 'cuota': {'ID_Cuota': nueva_cuota.ID_Cuota, 'Descripcion': nueva_cuota.Descripcion}}), 201

# Ruta para obtener todas las cuotas
@cuotas_bp.route('/cuotas', methods=['GET'])
def obtener_cuotas():
    cuotas = Cuota.query.all()
    resultado = [{'ID_Cuota': cuota.ID_Cuota, 'Descripcion': cuota.Descripcion, 'Monto': str(cuota.Monto), 'Fecha_Limite': str(cuota.Fecha_Limite)} for cuota in cuotas]
    return jsonify(resultado), 200

# Ruta para obtener una cuota específica
@cuotas_bp.route('/cuotas/<int:id_cuota>', methods=['GET'])
def obtener_cuota(id_cuota):
    cuota = db.session.get(Cuota, id_cuota)
    if cuota:
        return jsonify({'ID_Cuota': cuota.ID_Cuota, 'Descripcion': cuota.Descripcion, 'Monto': str(cuota.Monto), 'Fecha_Limite': str(cuota.Fecha_Limite)}), 200
    else:
        return jsonify({'mensaje': 'Cuota no encontrada'}), 404

# Ruta para actualizar una cuota
@cuotas_bp.route('/cuotas/<int:id_cuota>', methods=['PUT'])
def actualizar_cuota(id_cuota):
    cuota = db.session.get(Cuota, id_cuota)
    if not cuota:
        return jsonify({'mensaje': 'Cuota no encontrada'}), 404

    datos = request.get_json()
    cuota.Descripcion = datos.get('Descripcion', cuota.Descripcion)
    cuota.Monto = datos.get('Monto', cuota.Monto)
    cuota.Fecha_Limite = datos.get('Fecha_Limite', cuota.Fecha_Limite)
    db.session.commit()
    return jsonify({'mensaje': 'Cuota actualizada exitosamente'}), 200

# Ruta para eliminar una cuota
@cuotas_bp.route('/cuotas/<int:id_cuota>', methods=['DELETE'])
def eliminar_cuota(id_cuota):
    cuota = db.session.get(Cuota, id_cuota)
    if not cuota:
        return jsonify({'mensaje': 'Cuota no encontrada'}), 404

    db.session.delete(cuota)
    db.session.commit()
    return jsonify({'mensaje': 'Cuota eliminada exitosamente'}), 200


#_____________________________________________________________________________

# Crear un Blueprint para las rutas de pagos
pagos_bp = Blueprint('pagos', __name__)

# Ruta para crear un pago
@pagos_bp.route('/pagos', methods=['POST'])
def crear_pago():
    datos = request.get_json()
    errores = validar_pago(datos)
    if errores:
        logging.error(f"Error al registrar pago: {errores}")  # Log de error

        return jsonify({'errores': errores}), 400

    cuota = Cuota.query.get(datos['ID_Cuota'])
    persona = Persona.query.get(datos['ID_Persona'])  # Recuperar la persona para observaciones

    if not cuota:
        return jsonify({'error': 'Cuota no encontrada.'}), 404
    
    if not persona:
        return jsonify({'error': 'Persona no encontrada.'}), 404


    # Calcular pagos realizados para la persona y cuota específica
    pagos_previos = db.session.query(db.func.sum(Pago.Monto_Pagado)).filter(
        Pago.ID_Cuota == datos['ID_Cuota'], Pago.ID_Persona == datos['ID_Persona']
    ).scalar() or 0

    pagos_totales = pagos_previos + datos['Monto_Pagado']
    if pagos_totales > cuota.Monto:
        return jsonify({'error': f'El monto total no puede exceder el monto restante de la cuota: Q{cuota.Monto - pagos_previos}.'}), 400

    # Verificar si existe un registro previo
    pago_existente = Pago.query.filter_by(ID_Persona=datos['ID_Persona'], ID_Cuota=datos['ID_Cuota']).first()


    # Si detectamos un pago previo, verificamos su contexto
    
    if pago_existente:
        # Calcular la diferencia en el monto pagado
        diferencia_monto = datos['Monto_Pagado'] - pago_existente.Monto_Pagado


        # Actualizar el pago existente
        pago_existente.Monto_Pagado += datos['Monto_Pagado']
        pago_existente.Fecha_Pago = datos['Fecha_Pago']
        pago_existente.Estado = 'Completado' if pagos_totales >= cuota.Monto else 'Pendiente'
        db.session.commit()
        
        # Registrar el ingreso correspondiente al nuevo pago
        nuevo_ingreso = Ingreso(
            Fecha=datos['Fecha_Pago'],
            Monto=datos['Monto_Pagado'] ,
            Fuente=f'Tipo de Cuota: {cuota.Descripcion}',
            Observaciones=f'Pago realizado por {persona.Nombre}. Estado de la cuota: {pago_existente.Estado}.'
        
        )
        db.session.add(nuevo_ingreso)
        db.session.commit()

        
        
        logging.info(f"Pago actualizado exitosamente: Persona={datos['ID_Persona']}, Cuota={datos['ID_Cuota']}, Estado={pago_existente.Estado}")
        return jsonify({'mensaje': 'Pago actualizado exitosamente', 'estado': pago_existente.Estado, 'monto_restante': cuota.Monto - pagos_totales}), 200

    # Registrar un nuevo pago
    nuevo_pago = Pago(
        ID_Persona=datos['ID_Persona'],
        ID_Cuota=datos['ID_Cuota'],
        Fecha_Pago=datos['Fecha_Pago'],
        Monto_Pagado=datos['Monto_Pagado'],
        Estado='Completado' if pagos_totales >= cuota.Monto else 'Pendiente'
    )
    db.session.add(nuevo_pago)
    # Registrar el ingreso correspondiente al nuevo pago
    nuevo_ingreso = Ingreso(
        Fecha=datos['Fecha_Pago'],
        Monto=datos['Monto_Pagado'],
        Fuente=f'Tipo de Cuota: {cuota.Descripcion}',
        Observaciones=f'Pago registrado por {persona.Nombre}. Estado de la cuota: {nuevo_pago.Estado}.'
    
    )
    db.session.add(nuevo_ingreso)

    db.session.commit()
    logging.info(f"Pago registrado exitosamente: Persona={datos['ID_Persona']}, Cuota={datos['ID_Cuota']}")
    return jsonify({'mensaje': 'Pago registrado exitosamente', 'estado': nuevo_pago.Estado, 'monto_restante': cuota.Monto - pagos_totales}), 201

# Ruta para obtener todos los pagos
@pagos_bp.route('/pagos', methods=['GET'])
def obtener_pagos():
    pagos = Pago.query.all()
    resultado = [
        {
            'ID_Pago': pago.ID_Pago,
            'ID_Persona': pago.ID_Persona,
            'ID_Cuota': pago.ID_Cuota,
            'Fecha_Pago': str(pago.Fecha_Pago),
            'Monto_Pagado': str(pago.Monto_Pagado),
            'Estado': pago.Estado
        }
        for pago in pagos
    ]
    return jsonify(resultado), 200

# Ruta para obtener un pago específico
@pagos_bp.route('/pagos/<int:id_pago>', methods=['GET'])
def obtener_pago(id_pago):
    pago = db.session.get(Pago, id_pago)
    if pago:
        return jsonify({
            'ID_Pago': pago.ID_Pago,
            'ID_Persona': pago.ID_Persona,
            'ID_Cuota': pago.ID_Cuota,
            'Fecha_Pago': str(pago.Fecha_Pago),
            'Monto_Pagado': str(pago.Monto_Pagado),
            'Estado': pago.Estado
        }), 200
    else:
        return jsonify({'mensaje': 'Pago no encontrado'}), 404
    

# Ruta para actualizar un pago
@pagos_bp.route('/pagos/<int:id_pago>', methods=['PUT'])
def actualizar_pago(id_pago):
    pago = db.session.get(Pago, id_pago)
    if not pago:
        return jsonify({'mensaje': 'Pago no encontrado'}), 404

    datos = request.get_json()
    pago.ID_Persona = datos.get('ID_Persona', pago.ID_Persona)
    pago.ID_Cuota = datos.get('ID_Cuota', pago.ID_Cuota)
    pago.Fecha_Pago = datos.get('Fecha_Pago', pago.Fecha_Pago)
    pago.Monto_Pagado = datos.get('Monto_Pagado', pago.Monto_Pagado)
    pago.Estado = datos.get('Estado', pago.Estado)
    db.session.commit()
    return jsonify({'mensaje': 'Pago actualizado exitosamente'}), 200

# Ruta para eliminar un pago
@pagos_bp.route('/pagos/<int:id_pago>', methods=['DELETE'])
def eliminar_pago(id_pago):
    pago = db.session.get(Pago, id_pago)
    if not pago:
        return jsonify({'mensaje': 'Pago no encontrado'}), 404

    db.session.delete(pago)
    db.session.commit()
    return jsonify({'mensaje': 'Pago eliminado exitosamente'}), 200


@pagos_bp.route('/pagos/cuota/<int:id_cuota>', methods=['GET'])
def obtener_estado_cuota(id_cuota):
    # Validar que el parámetro ID_Persona esté presente
    id_persona = request.args.get('ID_Persona')
    if not id_persona:
        return jsonify({'error': 'ID_Persona es obligatorio para consultar el estado de la cuota.'}), 400

    cuota = Cuota.query.get(id_cuota)
    if not cuota:
        return jsonify({'error': 'Cuota no encontrada'}), 404

    # Calcular los pagos realizados para esta cuota y persona específica
    pagos_totales = db.session.query(db.func.sum(Pago.Monto_Pagado)).filter(
        Pago.ID_Cuota == id_cuota, Pago.ID_Persona == id_persona
    ).scalar() or 0

    # Calcular el monto restante
    monto_restante = cuota.Monto - pagos_totales

    return jsonify({
        'ID_Cuota': cuota.ID_Cuota,
        'Descripcion': cuota.Descripcion,
        'Monto': cuota.Monto,
        'PagosRealizados': pagos_totales,
        'MontoRestante': monto_restante,
        'Estado': 'Completado' if pagos_totales >= cuota.Monto else 'Pendiente'
    }), 200

#--____________________________________________________________________________________
#--____________________________________________________________________________________

# Crear un Blueprint para las rutas de ingresos
ingresos_bp = Blueprint('ingresos', __name__)

# Ruta para crear un ingreso
@ingresos_bp.route('/ingresos', methods=['POST'])
def crear_ingreso():
    datos = request.get_json()
    errores = validar_ingreso(datos)
    if errores:
        logging.error(f"Error al registrar ingreso: {errores}")  # Log de error

        return jsonify({'errores': errores}), 400

    nuevo_ingreso = Ingreso(
        Fecha=datos.get('Fecha'),
        Monto=datos.get('Monto'),
        Fuente=datos.get('Fuente'),
        Observaciones=datos.get('Observaciones')
    )
    db.session.add(nuevo_ingreso)
    db.session.commit()
    logging.info(f"Ingreso registrado exitosamente: Fuente={datos['Fuente']}, Monto={datos['Monto']}")
    return jsonify({'mensaje': 'Ingreso creado exitosamente', 'ingreso': {'ID_Ingreso': nuevo_ingreso.ID_Ingreso, 'Monto': str(nuevo_ingreso.Monto)}}), 201

# Ruta para obtener todos los ingresos
@ingresos_bp.route('/ingresos', methods=['GET'])
def obtener_ingresos():
    ingresos = Ingreso.query.all()
    resultado = [
        {
            'ID_Ingreso': ingreso.ID_Ingreso,
            'Fecha': str(ingreso.Fecha),
            'Monto': str(ingreso.Monto),
            'Fuente': ingreso.Fuente,
            'Observaciones': ingreso.Observaciones
        }
        for ingreso in ingresos
    ]
    return jsonify(resultado), 200

# Ruta para obtener un ingreso específico
@ingresos_bp.route('/ingresos/<int:id_ingreso>', methods=['GET'])
def obtener_ingreso(id_ingreso):
    ingreso = db.session.get(Ingreso, id_ingreso)
    if ingreso:
        return jsonify({
            'ID_Ingreso': ingreso.ID_Ingreso,
            'Fecha': str(ingreso.Fecha),
            'Monto': str(ingreso.Monto),
            'Fuente': ingreso.Fuente,
            'Observaciones': ingreso.Observaciones
        }), 200
    else:
        return jsonify({'mensaje': 'Ingreso no encontrado'}), 404

@ingresos_bp.route('/ingresos/total', methods=['GET'])
def obtener_total_ingresos():
    total = db.session.query(db.func.sum(Ingreso.Monto)).scalar() or 0
    return jsonify({'total_ingresos': float(total)}), 200


# Ruta para actualizar un ingreso
@ingresos_bp.route('/ingresos/<int:id_ingreso>', methods=['PUT'])
def actualizar_ingreso(id_ingreso):
    ingreso = db.session.get(Ingreso, id_ingreso)
    if not ingreso:
        return jsonify({'mensaje': 'Ingreso no encontrado'}), 404

    datos = request.get_json()
    ingreso.Fecha = datos.get('Fecha', ingreso.Fecha)
    ingreso.Monto = datos.get('Monto', ingreso.Monto)
    ingreso.Fuente = datos.get('Fuente', ingreso.Fuente)
    ingreso.Observaciones = datos.get('Observaciones', ingreso.Observaciones)
    db.session.commit()
    return jsonify({'mensaje': 'Ingreso actualizado exitosamente'}), 200

# Ruta para eliminar un ingreso
@ingresos_bp.route('/ingresos/<int:id_ingreso>', methods=['DELETE'])
def eliminar_ingreso(id_ingreso):
    ingreso = db.session.get(Ingreso, id_ingreso)
    if not ingreso:
        return jsonify({'mensaje': 'Ingreso no encontrado'}), 404

    db.session.delete(ingreso)
    db.session.commit()
    return jsonify({'mensaje': 'Ingreso eliminado exitosamente'}), 200



#--____________________________________________________________________________________
#--____________________________________________________________________________________


# Crear un Blueprint para las rutas de egresos
egresos_bp = Blueprint('egresos', __name__)

# Ruta para crear un egreso
@egresos_bp.route('/egresos', methods=['POST'])
def crear_egreso():
    datos = request.get_json()
    errores = validar_egreso(datos)
    if errores:
        logging.error(f"Error al registrar egreso: {errores}")
        return jsonify({'errores': errores}), 400

    try:
        # Obtener los fondos disponibles desde la lógica interna
        total_ingresos = db.session.query(db.func.sum(Ingreso.Monto)).scalar() or 0
        total_egresos = db.session.query(db.func.sum(Egreso.Monto)).scalar() or 0
        fondos_disponibles = total_ingresos - total_egresos

        # Validar fondos suficientes
        if datos['Monto'] > fondos_disponibles:
            mensaje_error = f"Fondos insuficientes. Disponible: Q{fondos_disponibles:.2f}. Egreso solicitado: Q{datos['Monto']:.2f}."
            logging.error(mensaje_error)
            return jsonify({'errores': [mensaje_error]}), 400

        # Registrar el nuevo egreso
        nuevo_egreso = Egreso(
            Fecha=datos.get('Fecha'),
            Monto=datos.get('Monto'),
            Descripcion=datos.get('Descripcion')
        )
        db.session.add(nuevo_egreso)
        db.session.commit()
        logging.info(f"Egreso registrado exitosamente: Descripcion={datos['Descripcion']}, Monto={datos['Monto']}")

        return jsonify({'mensaje': 'Egreso creado exitosamente', 'egreso': {'ID_Egreso': nuevo_egreso.ID_Egreso, 'Monto': str(nuevo_egreso.Monto)}}), 201
    except Exception as e:
        logging.error(f"Error interno al registrar egreso: {str(e)}")
        return jsonify({'error': 'Error interno al registrar egreso.'}), 500
    
    
    

# Ruta para obtener todos los egresos
@egresos_bp.route('/egresos', methods=['GET'])
def obtener_egresos():
    egresos = Egreso.query.all()
    resultado = [
        {
            'ID_Egreso': egreso.ID_Egreso,
            'Fecha': str(egreso.Fecha),
            'Monto': str(egreso.Monto),
            'Descripcion': egreso.Descripcion
        }
        for egreso in egresos
    ]
    return jsonify(resultado), 200

# Ruta para obtener un egreso específico
@egresos_bp.route('/egresos/<int:id_egreso>', methods=['GET'])
def obtener_egreso(id_egreso):
    egreso = db.session.get(Egreso, id_egreso)
    if egreso:
        return jsonify({
            'ID_Egreso': egreso.ID_Egreso,
            'Fecha': str(egreso.Fecha),
            'Monto': str(egreso.Monto),
            'Descripcion': egreso.Descripcion
        }), 200
    else:
        return jsonify({'mensaje': 'Egreso no encontrado'}), 404

# Ruta para actualizar un egreso
@egresos_bp.route('/egresos/<int:id_egreso>', methods=['PUT'])
def actualizar_egreso(id_egreso):
    egreso = db.session.get(Egreso, id_egreso)
    if not egreso:
        return jsonify({'mensaje': 'Egreso no encontrado'}), 404

    datos = request.get_json()
    egreso.Fecha = datos.get('Fecha', egreso.Fecha)
    egreso.Monto = datos.get('Monto', egreso.Monto)
    egreso.Descripcion = datos.get('Descripcion', egreso.Descripcion)
    db.session.commit()
    return jsonify({'mensaje': 'Egreso actualizado exitosamente'}), 200

# Ruta para eliminar un egreso
@egresos_bp.route('/egresos/<int:id_egreso>', methods=['DELETE'])
def eliminar_egreso(id_egreso):
    egreso = db.session.get(Egreso, id_egreso)
    if not egreso:
        return jsonify({'mensaje': 'Egreso no encontrado'}), 404

    db.session.delete(egreso)
    db.session.commit()
    return jsonify({'mensaje': 'Egreso eliminado exitosamente'}), 200

@egresos_bp.route('/fondos/disponibles', methods=['GET'])
def obtener_fondos_disponibles():
    try:
        # Total de ingresos
        total_ingresos = db.session.query(db.func.sum(Ingreso.Monto)).scalar() or 0
        # Total de egresos
        total_egresos = db.session.query(db.func.sum(Egreso.Monto)).scalar() or 0
        # Fondos disponibles
        fondos_disponibles = total_ingresos - total_egresos
        return jsonify({'fondos_disponibles': float(fondos_disponibles)}), 200  # Convertir explícitamente a float
    except Exception as e:
        logging.error(f"Error al calcular fondos disponibles: {str(e)}")
        return jsonify({'error': 'Error al calcular fondos disponibles.'}), 500
    
    
@egresos_bp.route('/egresos/total', methods=['GET'])
def obtener_total_egresos():
    try:
        total_egresos = db.session.query(db.func.sum(Egreso.Monto)).scalar() or 0
        return jsonify({'total_egresos': float(total_egresos)}), 200
    except Exception as e:
        logging.error(f"Error al calcular total de egresos: {str(e)}")
        return jsonify({'error': 'Error interno al calcular total de egresos.'}), 500

#==========================================================================================================
#==========================================================================================================

# Crear un Blueprint para las rutas de Persona_Derecho
persona_derecho_bp = Blueprint('persona_derecho', __name__)

# Ruta para asignar un derecho a una persona
@persona_derecho_bp.route('/persona_derecho', methods=['POST'])
def asignar_derecho():
    datos = request.get_json()
    errores = validar_persona_derecho(datos)
    if errores:
        logging.error(f"Error al asignar derecho: {errores}")  # Log de error

        return jsonify({'errores': errores}), 400

    nueva_asignacion = PersonaDerecho(
        ID_Persona=datos.get('ID_Persona'),
        ID_Derecho=datos.get('ID_Derecho'),
        Fecha_Inicio=datos.get('Fecha_Inicio'),
        Fecha_Fin=datos.get('Fecha_Fin')
    )
    db.session.add(nueva_asignacion)
    db.session.commit()
    logging.info(f"Derecho asignado exitosamente: ID_Persona={datos['ID_Persona']}, ID_Derecho={datos['ID_Derecho']}")
    return jsonify({'mensaje': 'Derecho asignado exitosamente', 'asignacion': {
        'ID_Persona': nueva_asignacion.ID_Persona,
        'ID_Derecho': nueva_asignacion.ID_Derecho,
        'Fecha_Inicio': str(nueva_asignacion.Fecha_Inicio),
        'Fecha_Fin': str(nueva_asignacion.Fecha_Fin)
    }}), 201

# Ruta para obtener todas las asignaciones de derechos
@persona_derecho_bp.route('/persona_derecho', methods=['GET'])
def obtener_asignaciones():
    asignaciones = PersonaDerecho.query.all()
    resultado = [
        {
            'ID_Persona': asignacion.ID_Persona,
            'ID_Derecho': asignacion.ID_Derecho,
            'Fecha_Inicio': str(asignacion.Fecha_Inicio),
            'Fecha_Fin': str(asignacion.Fecha_Fin)
        }
        for asignacion in asignaciones
    ]
    return jsonify(resultado), 200

# Ruta para obtener una asignación específica
@persona_derecho_bp.route('/persona_derecho/<int:id_persona>/<int:id_derecho>', methods=['GET'])
def obtener_asignacion(id_persona, id_derecho):
    asignacion = PersonaDerecho.query.filter_by(ID_Persona=id_persona, ID_Derecho=id_derecho).first()
    if asignacion:
        return jsonify({
            'ID_Persona': asignacion.ID_Persona,
            'ID_Derecho': asignacion.ID_Derecho,
            'Fecha_Inicio': str(asignacion.Fecha_Inicio),
            'Fecha_Fin': str(asignacion.Fecha_Fin)
        }), 200
    else:
        return jsonify({'mensaje': 'Asignación no encontrada'}), 404

# Ruta para actualizar una asignación
@persona_derecho_bp.route('/persona_derecho/<int:id_persona>/<int:id_derecho>', methods=['PUT'])
def actualizar_asignacion(id_persona, id_derecho):
    asignacion = PersonaDerecho.query.filter_by(ID_Persona=id_persona, ID_Derecho=id_derecho).first()
    if not asignacion:
        return jsonify({'mensaje': 'Asignación no encontrada'}), 404

    datos = request.get_json()
    asignacion.Fecha_Inicio = datos.get('Fecha_Inicio', asignacion.Fecha_Inicio)
    asignacion.Fecha_Fin = datos.get('Fecha_Fin', asignacion.Fecha_Fin)
    db.session.commit()
    return jsonify({'mensaje': 'Asignación actualizada exitosamente'}), 200

# Ruta para eliminar una asignación
@persona_derecho_bp.route('/persona_derecho/<int:id_persona>/<int:id_derecho>', methods=['DELETE'])
def eliminar_asignacion(id_persona, id_derecho):
    asignacion = PersonaDerecho.query.filter_by(ID_Persona=id_persona, ID_Derecho=id_derecho).first()
    if not asignacion:
        return jsonify({'mensaje': 'Asignación no encontrada'}), 404

    db.session.delete(asignacion)
    db.session.commit()
    return jsonify({'mensaje': 'Asignación eliminada exitosamente'}), 200

@persona_derecho_bp.route('/persona_derecho/resumen', methods=['GET'])
def obtener_resumen_personas_derechos():
    try:
        resultado = db.session.query(
            Persona.Nombre,
            Persona.DPI,
            Persona.Rol,
            Derecho.Nombre.label('Nombre_Derecho'),
            Cuota.Descripcion.label('Descripcion_Cuota'),
            Cuota.Monto,
            db.func.sum(Pago.Monto_Pagado).label('PagosRealizados')
        ).join(PersonaDerecho, Persona.ID_Persona == PersonaDerecho.ID_Persona)\
         .join(Derecho, PersonaDerecho.ID_Derecho == Derecho.ID_Derecho)\
         .outerjoin(Cuota, Cuota.ID_Cuota == Pago.ID_Cuota)\
         .outerjoin(Pago, Cuota.ID_Cuota == Pago.ID_Cuota)\
         .group_by(Persona.Nombre, Persona.DPI, Persona.Rol, Derecho.Nombre, Cuota.Descripcion, Cuota.Monto).all()

        resumen = [
            {
                'Nombre': persona.Nombre,
                'DPI': persona.DPI,
                'Rol': persona.Rol,
                'Nombre_Derecho': derecho.Nombre_Derecho,
                'Descripcion_Cuota': cuota.Descripcion_Cuota,
                'Monto': cuota.Monto,
                'PagosRealizados': cuota.PagosRealizados or 0,
                'Estado': 'Completado' if cuota.PagosRealizados and cuota.PagosRealizados >= cuota.Monto else 'Pendiente'
            } for persona, derecho, cuota in resultado
        ]
        return jsonify(resumen), 200
    except Exception as e:
        logging.error(f"Error al obtener resumen de personas con derechos: {str(e)}")
     
    
@persona_derecho_bp.route('/persona_derecho/detalle', methods=['GET'])
def obtener_detalle_personas_derechos():
    try:
        # Obtener parámetros de búsqueda
        nombre = request.args.get('Nombre')
        dpi = request.args.get('DPI')
        derecho = request.args.get('Derecho')

        # Construir la consulta base
        query = db.session.query(
            Persona.ID_Persona,
            Persona.Nombre,
            Persona.DPI,
            Persona.Rol,
            Persona.Telefono,
            Persona.Email,
            PersonaDerecho.Fecha_Inicio,
            PersonaDerecho.Fecha_Fin,
            Derecho.ID_Derecho,
            Derecho.Nombre.label('Descripcion_Derecho')
        ).join(PersonaDerecho, Persona.ID_Persona == PersonaDerecho.ID_Persona)\
         .join(Derecho, PersonaDerecho.ID_Derecho == Derecho.ID_Derecho)

        # Aplicar filtros según parámetros
        if nombre:
            query = query.filter(Persona.Nombre.ilike(f'%{nombre}%'))
        if dpi:
            query = query.filter(Persona.DPI == dpi)
        if derecho:
            query = query.filter(Derecho.Nombre.ilike(f'%{derecho}%'))

        # Ejecutar la consulta
        resultado = query.all()

        # Procesar los datos
        asignaciones = [
            {
                'ID_Persona': fila.ID_Persona,
                'Nombre': fila.Nombre,
                'DPI': fila.DPI,
                'Rol': fila.Rol,
                'Telefono': fila.Telefono,
                'Email': fila.Email,
                'ID_Derecho': fila.ID_Derecho,
                'Descripcion_Derecho': fila.Descripcion_Derecho,
                'Fecha_Inicio': str(fila.Fecha_Inicio),
                'Fecha_Fin': str(fila.Fecha_Fin) if fila.Fecha_Fin else 'Sin vencimiento'
            } for fila in resultado
        ]
        return jsonify(asignaciones), 200
    except Exception as e:
        logging.error(f"Error al obtener detalle de personas con derechos: {str(e)}")
        return jsonify({'error': 'Error interno al obtener datos.'}), 500
    
@persona_derecho_bp.route('/persona_derecho/sin_derechos', methods=['GET'])
def obtener_personas_sin_derechos():
    try:
        # Consultar personas sin derechos asignados
        personas_sin_derechos = db.session.query(Persona).outerjoin(
            PersonaDerecho, Persona.ID_Persona == PersonaDerecho.ID_Persona
        ).filter(PersonaDerecho.ID_Derecho == None).all()

        resultado = [
            {
                'ID_Persona': persona.ID_Persona,
                'Nombre': persona.Nombre,
                'DPI': persona.DPI,
                'Email': persona.Email,
                'Telefono': persona.Telefono,
                'Rol': persona.Rol,
                'Estado': persona.Estado
            } for persona in personas_sin_derechos
        ]
        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error al obtener personas sin derechos: {str(e)}")
        return jsonify({'error': 'Error interno al obtener personas sin derechos.'}), 500 

@cuotas_bp.route('/cuotas/estado', methods=['GET'])
def obtener_cuotas_estado():
    try:
        cuotas = db.session.query(
            Cuota.ID_Cuota,
            Cuota.Descripcion,
            Cuota.Monto,
            db.func.sum(Pago.Monto_Pagado).label('PagosRealizados')
        ).outerjoin(Pago, Cuota.ID_Cuota == Pago.ID_Cuota).group_by(Cuota.ID_Cuota, Cuota.Descripcion, Cuota.Monto).all()

        resultado = [
            {
                'ID_Cuota': cuota.ID_Cuota,
                'Descripcion': cuota.Descripcion,
                'Monto': cuota.Monto,
                'PagosRealizados': cuota.PagosRealizados or 0,
                'Estado': 'Completado' if cuota.PagosRealizados and cuota.PagosRealizados >= cuota.Monto else 'Pendiente'
            } for cuota in cuotas
        ]
        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error al obtener cuotas con estado: {str(e)}")
        return jsonify({'error': 'Error interno al obtener datos de cuotas.'}), 500
    
    
@persona_derecho_bp.route('/persona_derecho/detalle_combinado', methods=['GET'])
def obtener_detalle_combinado_personas():
    try:
        # Obtener parámetros de búsqueda
        nombre = request.args.get('Nombre')
        dpi = request.args.get('DPI')
        derecho = request.args.get('Derecho')

        # Personas con derechos asignados
        query_con_derechos = db.session.query(
            Persona.ID_Persona,
            Persona.Nombre,
            Persona.DPI,
            Persona.Rol,
            Persona.Telefono,
            Persona.Email,
            PersonaDerecho.Fecha_Inicio,
            PersonaDerecho.Fecha_Fin,
            Derecho.ID_Derecho,
            Derecho.Nombre.label('Descripcion_Derecho')
        ).join(PersonaDerecho, Persona.ID_Persona == PersonaDerecho.ID_Persona)\
         .join(Derecho, PersonaDerecho.ID_Derecho == Derecho.ID_Derecho)

        # Aplicar filtros a personas con derechos
        if nombre:
            query_con_derechos = query_con_derechos.filter(Persona.Nombre.ilike(f'%{nombre}%'))
        if dpi:
            query_con_derechos = query_con_derechos.filter(Persona.DPI == dpi)
        if derecho and derecho.lower() != 'sin derechos':
            query_con_derechos = query_con_derechos.filter(Derecho.Nombre.ilike(f'%{derecho}%'))

        personas_con_derechos = query_con_derechos.all()

        # Personas sin derechos asignados
        query_sin_derechos = db.session.query(Persona).outerjoin(
            PersonaDerecho, Persona.ID_Persona == PersonaDerecho.ID_Persona
        ).filter(PersonaDerecho.ID_Derecho == None)

        # Aplicar filtros a personas sin derechos
        if derecho and derecho.lower() == 'sin derechos':
            if nombre:
                query_sin_derechos = query_sin_derechos.filter(Persona.Nombre.ilike(f'%{nombre}%'))
            if dpi:
                query_sin_derechos = query_sin_derechos.filter(Persona.DPI == dpi)

        personas_sin_derechos = query_sin_derechos.all()

        # Formatear resultados
        con_derechos = [
            {
                'ID_Persona': fila.ID_Persona,
                'Nombre': fila.Nombre,
                'DPI': fila.DPI,
                'Rol': fila.Rol,
                'Telefono': fila.Telefono,
                'Email': fila.Email,
                'ID_Derecho': fila.ID_Derecho,
                'Descripcion_Derecho': fila.Descripcion_Derecho,
                'Fecha_Inicio': str(fila.Fecha_Inicio),
                'Fecha_Fin': str(fila.Fecha_Fin) if fila.Fecha_Fin else 'Sin vencimiento'
            } for fila in personas_con_derechos
        ]

        sin_derechos = [
            {
                'ID_Persona': persona.ID_Persona,
                'Nombre': persona.Nombre,
                'DPI': persona.DPI,
                'Rol': persona.Rol,
                'Telefono': persona.Telefono,
                'Email': persona.Email,
                'Descripcion_Derecho': 'Sin derechos',
                'Fecha_Inicio': 'N/A',
                'Fecha_Fin': 'N/A'
            } for persona in personas_sin_derechos
        ]

        # Decidir qué lista retornar
        if derecho and derecho.lower() == 'sin derechos':
            resultado = sin_derechos
        elif derecho:
            resultado = con_derechos
        else:
            resultado = con_derechos + sin_derechos

        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error al obtener detalle combinado de personas: {str(e)}")
        return jsonify({'error': 'Error interno al obtener datos.'}), 500
    
@cuotas_bp.route('/cuotas/estado/mejorado', methods=['GET'])
def obtener_cuotas_mejoradas():
    try:
        # Consultar cuotas con detalles avanzados
        cuotas = db.session.query(
            Cuota.ID_Cuota,
            Cuota.Descripcion,
            Cuota.Monto,
            Cuota.Fecha_Inicio,
            Cuota.Fecha_Vencimiento,
            db.func.sum(Pago.Monto_Pagado).label('PagosRealizados'),
            db.func.count(Pago.ID_Persona).label('Participantes')
        ).outerjoin(Pago, Cuota.ID_Cuota == Pago.ID_Cuota).group_by(
            Cuota.ID_Cuota, Cuota.Descripcion, Cuota.Monto, Cuota.Fecha_Inicio, Cuota.Fecha_Vencimiento
        ).all()

        # Formatear resultados
        resultado = [
            {
                'ID_Cuota': cuota.ID_Cuota,
                'Descripcion': cuota.Descripcion,
                'Monto': cuota.Monto,
                'PagosRealizados': cuota.PagosRealizados or 0,
                'MontoPendiente': cuota.Monto - (cuota.PagosRealizados or 0),
                'Estado': 'Completado' if cuota.PagosRealizados and cuota.PagosRealizados >= cuota.Monto else 'Pendiente',
                'Fecha_Inicio': str(cuota.Fecha_Inicio),
                'Fecha_Vencimiento': str(cuota.Fecha_Vencimiento) if cuota.Fecha_Vencimiento else 'Sin vencimiento',
                'Participantes': cuota.Participantes
            } for cuota in cuotas
        ]

        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error al obtener cuotas mejoradas: {str(e)}")
        return jsonify({'error': 'Error interno al obtener datos de cuotas.'}), 500
    
    
    
@cuotas_bp.route('/cuotas/detalladas', methods=['GET'])
def obtener_cuotas_detalladas():
    try:
        # Consultar cuotas
        cuotas = db.session.query(
            Cuota.ID_Cuota,
            Cuota.Descripcion,
            Cuota.Monto,
            Cuota.Fecha_Inicio,
            Cuota.Fecha_Vencimiento,
            db.func.sum(Pago.Monto_Pagado).label('PagosRealizados'),
            db.func.count(Pago.ID_Persona).label('Participantes')
        ).outerjoin(Pago, Cuota.ID_Cuota == Pago.ID_Cuota).group_by(
            Cuota.ID_Cuota, Cuota.Descripcion, Cuota.Monto, Cuota.Fecha_Inicio, Cuota.Fecha_Vencimiento
        ).all()

        # Formatear los resultados
        resultado = [
            {
                'ID_Cuota': cuota.ID_Cuota,
                'Descripcion': cuota.Descripcion,
                'Monto': float(cuota.Monto) if cuota.Monto else 0.0,
                'PagosRealizados': float(cuota.PagosRealizados) if cuota.PagosRealizados else 0.0,
                'MontoPendiente': (float(cuota.Monto) - float(cuota.PagosRealizados)) if cuota.Monto and cuota.PagosRealizados else 0.0,
                'Estado': 'Completado' if cuota.PagosRealizados and cuota.PagosRealizados >= cuota.Monto else 'Pendiente',
                'Fecha_Inicio': str(cuota.Fecha_Inicio) if cuota.Fecha_Inicio else 'No definida',
                'Fecha_Vencimiento': str(cuota.Fecha_Vencimiento) if cuota.Fecha_Vencimiento else 'Sin vencimiento',
                'Participantes': cuota.Participantes or 0
            } for cuota in cuotas
        ]

        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error al obtener cuotas detalladas: {str(e)}")
        return jsonify({'error': 'Error interno al obtener datos de cuotas.'}), 500
    
    
@cuotas_bp.route('/cuotas/con-pagos', methods=['GET'])
def obtener_cuotas_con_pagos():
    try:
        # Consultar cuotas con sus respectivos pagos realizados
        cuotas = db.session.query(
            Cuota.ID_Cuota,
            Cuota.Descripcion,
            Cuota.Monto,
            Cuota.Fecha_Limite,
            db.func.sum(Pago.Monto_Pagado).label('PagosRealizados'),
            db.func.count(Pago.ID_Persona).label('Participantes')
        ).outerjoin(Pago, Cuota.ID_Cuota == Pago.ID_Cuota).group_by(
            Cuota.ID_Cuota, Cuota.Descripcion, Cuota.Monto, Cuota.Fecha_Limite
        ).all()

        # Formatear los resultados
        resultado = [
            {
                'ID_Cuota': cuota.ID_Cuota,
                'Descripcion': cuota.Descripcion,
                'Monto': float(cuota.Monto),
                'PagosRealizados': float(cuota.PagosRealizados) if cuota.PagosRealizados else 0.0,
                'MontoPendiente': (float(cuota.Monto) - float(cuota.PagosRealizados)) if cuota.PagosRealizados else float(cuota.Monto),
                'Estado': 'Completado' if cuota.PagosRealizados and cuota.PagosRealizados >= cuota.Monto else 'Pendiente',
                'Fecha_Limite': str(cuota.Fecha_Limite),
                'Participantes': cuota.Participantes or 0
            } for cuota in cuotas
        ]

        return jsonify(resultado), 200
    except Exception as e:
        logging.error(f"Error al obtener cuotas con pagos: {str(e)}")
        return jsonify({'error': 'Error interno al obtener datos de cuotas y pagos.'}), 500