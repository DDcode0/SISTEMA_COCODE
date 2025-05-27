
# app/routes.py
# Todas las rutas unificadas en un solo archivo
# Prefijo común: /api

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import (
    Persona, Derecho, PersonaDerecho,
    Cuota, DerechoCuota, PersonaCuota,
    Pago, Ingreso, Egreso
)


from app.utils.validaciones import (
    validar_persona,
    validar_derecho,
    validar_cuota,
    validar_persona_derecho,
    validar_pago,
    validar_ingreso,
    validar_egreso
)


api = Blueprint('api', __name__, url_prefix='/api')

# --------------------- Personas ---------------------
@api.route('/personas', methods=['GET'])
def get_personas():
    personas = Persona.query.all()
    return jsonify([{
        'ID_Persona': p.id_persona,
        'DPI': p.dpi,
        'Nombre': p.nombre,
        'Direccion': p.direccion,
        'Telefono': p.telefono,
        'Email': p.email,
        'Rol': p.rol,
        'Estado': p.estado
    } for p in personas]), 200

@api.route('/personas/<int:id>', methods=['GET'])
def get_persona(id):
    p = Persona.query.get_or_404(id)
    return jsonify({
        'ID_Persona': p.id_persona,
        'DPI': p.dpi,
        'Nombre': p.nombre,
        'Direccion': p.direccion,
        'Telefono': p.telefono,
        'Email': p.email,
        'Rol': p.rol,
        'Estado': p.estado
    }), 200

@api.route('/personas', methods=['POST'])
def post_persona():
    datos = request.get_json()
    datos.setdefault('Estado', 'Activo')
    datos.setdefault('Rol', 'Sin rol')

    errores = validar_persona({
        'DPI': datos.get('DPI'),
        'Nombre': datos.get('Nombre'),
        'Email': datos.get('Email'),
        'Telefono': datos.get('Telefono'),
        'Direccion': datos.get('Direccion'),
        'Rol': datos.get('Rol'),
        'Estado': datos.get('Estado')
    })
    if errores:
        return jsonify({'errores': errores}), 400

    p = Persona(
        dpi=datos['DPI'], nombre=datos['Nombre'], email=datos.get('Email'),
        telefono=datos.get('Telefono'), direccion=datos.get('Direccion'),
        rol=datos.get('Rol'), estado=datos.get('Estado')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'mensaje': 'Persona creada', 'ID_Persona': p.id_persona}), 201



@api.route('/personas/<int:id>', methods=['PUT'])
def put_persona(id):
    datos = request.get_json()
    # Añadir el ID al payload para validaciones de duplicado
    datos['ID_Persona'] = id

    # Llamar al validador en modo actualización
    errores = validar_persona({
        'DPI': datos.get('DPI'),
        'Nombre': datos.get('Nombre'),
        'Email': datos.get('Email'),
        'Telefono': datos.get('Telefono'),
        'Direccion': datos.get('Direccion'),
        'Rol': datos.get('Rol'),
        'Estado': datos.get('Estado'),
        'ID_Persona': id
    }, actualizacion=True)

    if errores:
        return jsonify({'errores': errores}), 400

    p = Persona.query.get_or_404(id)
    # Solo sobrescribimos los campos que vienen en datos
    for key, attr in [
        ('DPI','dpi'),('Nombre','nombre'),
        ('Email','email'),('Telefono','telefono'),
        ('Direccion','direccion'),('Rol','rol'),
        ('Estado','estado')
    ]:
        if key in datos and datos[key] is not None:
            setattr(p, attr, datos[key])
    db.session.commit()
    return jsonify({'mensaje': 'Persona actualizada'}), 200





@api.route('/personas/<int:id>', methods=['DELETE'])
def delete_persona(id):
    p = Persona.query.get_or_404(id)
    p.estado = 'Inactivo'
    p.rol = 'Sin rol'                 # <-- liberamos el rol
    db.session.commit()
    return jsonify({'mensaje':'Persona inactivada y rol liberado'}), 200



# --------------------- Derechos ---------------------
@api.route('/derechos', methods=['GET'])
def get_derechos():
    lista = Derecho.query.all()
    return jsonify([{'ID_Derecho': d.ID_Derecho, 'Nombre': d.Nombre} for d in lista]), 200

@api.route('/derechos/<int:id>', methods=['GET'])
def get_derecho(id):
    d = Derecho.query.get_or_404(id)
    return jsonify({'ID_Derecho': d.id_derecho, 'Nombre': d.nombre}), 200

@api.route('/derechos', methods=['POST'])
def post_derecho():
    datos = request.get_json()
    errores = validar_derecho({'Nombre': datos.get('Nombre')})
    if errores:
        return jsonify({'errores': errores}), 400
    d = Derecho(nombre=datos['Nombre'])
    db.session.add(d)
    db.session.commit()
    return jsonify({'mensaje':'Derecho creado','ID_Derecho': d.id_derecho}),201

@api.route('/derechos/<int:id>', methods=['PUT'])
def put_derecho(id):
    obj = Derecho.query.get_or_404(id)
    d = request.get_json()
    if 'Nombre' in d: obj.nombre = d['Nombre']
    db.session.commit()
    return jsonify({'mensaje': 'Derecho actualizado'}), 200

@api.route('/derechos/<int:id>', methods=['DELETE'])
def delete_derecho(id):
    obj = Derecho.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    return jsonify({'mensaje': 'Derecho eliminado'}), 200

# --------------------- Cuotas ---------------------
@api.route('/cuotas', methods=['GET'])
def get_cuotas():
    lista = Cuota.query.all()
    return jsonify([
    {
        'ID_Cuota': c.ID_Cuota,
        'Descripcion': c.Descripcion,
        'Monto': float(c.Monto),
        'Fecha_Limite': str(c.Fecha_Limite)
    }
        for c in lista
    ]), 200

@api.route('/cuotas/<int:id>', methods=['GET'])
def get_cuota(id):
    c = Cuota.query.get_or_404(id)
    return jsonify({
        'ID_Cuota': c.id_cuota,
        'Descripcion': c.descripcion,
        'Monto': float(c.monto),
        'Fecha_Limite': str(c.fecha_limite)
    }), 200

@api.route('/cuotas', methods=['POST'])
def post_cuota():
    datos = request.get_json()
    errores = validar_cuota({
        'Descripcion': datos.get('Descripcion'),
        'Monto': datos.get('Monto'),
        'Fecha_Limite': datos.get('Fecha_Limite')
    })
    if errores:
        return jsonify({'errores': errores}), 400
    c = Cuota(descripcion=datos['Descripcion'], monto=datos['Monto'], fecha_limite=datos['Fecha_Limite'])
    db.session.add(c)
    db.session.commit()
    return jsonify({'mensaje':'Cuota creada','ID_Cuota': c.id_cuota}),201

@api.route('/cuotas/<int:id>', methods=['PUT'])
def put_cuota(id):
    datos = request.get_json()
    errores = validar_cuota({
        'Descripcion': datos.get('Descripcion'),
        'Monto': datos.get('Monto'),
        'Fecha_Limite': datos.get('Fecha_Limite')
    })
    if errores:
        return jsonify({'errores': errores}),400
    c = Cuota.query.get_or_404(id)
    for key, attr in [('Descripcion','descripcion'),('Monto','monto'),('Fecha_Limite','fecha_limite')]:
        if datos.get(key) is not None:
            setattr(c, attr, datos[key])
    db.session.commit()
    return jsonify({'mensaje':'Cuota actualizada'}),200

@api.route('/cuotas/<int:id>', methods=['DELETE'])
def delete_cuota(id):
    c = Cuota.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'mensaje': 'Cuota eliminada'}), 200

# Opcionales: /cuotas/estado, /cuotas/con-pagos (igual que antes)

# --------------------- Asignación Derechos → PersonaCuota ---------------------
@api.route('/persona_derecho', methods=['GET'])
def list_persona_derecho():
    lista = PersonaDerecho.query.all()
    return jsonify([{
        'ID_Persona': pd.id_persona,
        'ID_Derecho': pd.id_derecho,
        'Fecha_Inicio': str(pd.fecha_inicio),
        'Fecha_Fin': str(pd.fecha_fin) if pd.fecha_fin else None
    } for pd in lista]), 200

@api.route('/persona_derecho/<int:pe>/<int:de>', methods=['GET'])
def get_persona_derecho(pe, de):
    pd = PersonaDerecho.query.get_or_404((pe, de))
    return jsonify({
        'ID_Persona': pd.id_persona,
        'ID_Derecho': pd.id_derecho,
        'Fecha_Inicio': str(pd.fecha_inicio),
        'Fecha_Fin': str(pd.fecha_fin) if pd.fecha_fin else None
    }), 200




@api.route('/persona_derecho/<int:pe>/<int:de>', methods=['PUT'])
def put_persona_derecho(pe, de):
    pd = PersonaDerecho.query.get_or_404((pe, de))
    d = request.get_json()
    if 'Fecha_Inicio' in d: pd.fecha_inicio = d['Fecha_Inicio']
    if 'Fecha_Fin' in d: pd.fecha_fin = d['Fecha_Fin']
    db.session.commit()
    return jsonify({'mensaje': 'Asignación actualizada'}), 200

@api.route('/persona_derecho/<int:pe>/<int:de>', methods=['DELETE'])
def delete_persona_derecho(pe, de):
    pd = PersonaDerecho.query.get_or_404((pe, de))
    db.session.delete(pd)
    db.session.commit()
    return jsonify({'mensaje': 'Asignación eliminada'}), 200

# --------------------- Pagos ---------------------
@api.route('/pagos', methods=['GET'])
def get_pagos():
    pagos = Pago.query.all()
    return jsonify([{
        'ID_Pago': p.id_pago,
        'ID_Persona': p.id_persona,
        'ID_Cuota': p.id_cuota,
        'Fecha_Pago': str(p.fecha_pago),
        'Monto_Pagado': float(p.monto_pagado),
        'Estado': p.estado
    } for p in pagos]), 200

@api.route('/pagos/<int:id>', methods=['GET'])
def get_pago(id):
    p = Pago.query.get_or_404(id)
    return jsonify({
        'ID_Pago': p.id_pago,
        'ID_Persona': p.id_persona,
        'ID_Cuota': p.id_cuota,
        'Fecha_Pago': str(p.fecha_pago),
        'Monto_Pagado': float(p.monto_pagado),
        'Estado': p.estado
    }), 200

@api.route('/pagos', methods=['POST'])
def post_pago():
    datos = request.get_json()
    errores = validar_pago(datos)
    if errores:
        return jsonify({'errores': errores}),400
    pago = Pago.registrar_pago(
        datos['ID_Persona'], datos['ID_Cuota'], datos['Fecha_Pago'], datos['Monto_Pagado']
    )
    return jsonify({'mensaje':'Pago registrado','ID_Pago': pago.id_pago}),201

@api.route('/pagos/<int:id>', methods=['PUT'])
def put_pago(id):
    p = Pago.query.get_or_404(id)
    d = request.get_json()
    for key, attr in [('ID_Persona','id_persona'),('ID_Cuota','id_cuota'),('Fecha_Pago','fecha_pago'),('Monto_Pagado','monto_pagado'),('Estado','estado')]:
        if key in d: setattr(p, attr, d[key])
    db.session.commit()
    return jsonify({'mensaje': 'Pago actualizado'}), 200

@api.route('/pagos/<int:id>', methods=['DELETE'])
def delete_pago(id):
    p = Pago.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'mensaje': 'Pago eliminado'}), 200

@api.route('/pagos/cuota/<int:cuota_id>', methods=['GET'])
def estado_cuota(cuota_id):
    persona_id = request.args.get('ID_Persona')
    if not persona_id:
        return jsonify({'error': 'ID_Persona requerido'}), 400
    pc = PersonaCuota.query.get((int(persona_id), cuota_id))
    if not pc:
        return jsonify({'error': 'Asignación no encontrada'}), 404
    total_pagado = (db.session.query(db.func.sum(Pago.monto_pagado)).filter(Pago.id_persona == persona_id, Pago.id_cuota == cuota_id).scalar() or 0)

    restante = pc.cuota.monto - total_pagado
    return jsonify({'ID_Cuota':cuota_id, 'PagosRealizados':float(total_pagado), 'MontoRestante':float(restante), 'Estado':pc.estado}), 200

# --------------------- Ingresos ---------------------
@api.route('/ingresos', methods=['GET'])
def get_ingresos():
    ingresos = Ingreso.query.all()
    return jsonify([{
        'ID_Ingreso': i.id_ingreso,
        'Fecha': str(i.fecha),
        'Monto': float(i.monto),
        'Fuente': i.fuente,
        'Observaciones': i.observaciones,
        'ID_Pago': i.id_pago
    } for i in ingresos]), 200

@api.route('/ingresos/<int:id>', methods=['GET'])
def get_ingreso(id):
    i = Ingreso.query.get_or_404(id)
    return jsonify({
        'ID_Ingreso': i.id_ingreso,
        'Fecha': str(i.fecha),
        'Monto': float(i.monto),
        'Fuente': i.fuente,
        'Observaciones': i.observaciones,
        'ID_Pago': i.id_pago
    }), 200

@api.route('/ingresos', methods=['POST'])
def post_ingreso():
    datos = request.get_json()
    errores = validar_ingreso(datos)
    if errores:
        return jsonify({'errores': errores}),400
    ing = Ingreso(
        fecha=datos['Fecha'], monto=datos['Monto'], fuente=datos.get('Fuente'),
        observaciones=datos.get('Observaciones'), id_pago=datos.get('ID_Pago')
    )
    db.session.add(ing)
    db.session.commit()
    return jsonify({'mensaje':'Ingreso creado','ID_Ingreso': ing.id_ingreso}),201

@api.route('/ingresos/<int:id>', methods=['PUT'])
def put_ingreso(id):
    ing = Ingreso.query.get_or_404(id)
    d = request.get_json()
    for key, attr in [('Fecha','fecha'),('Monto','monto'),('Fuente','fuente'),('Observaciones','observaciones')]:
        if key in d: setattr(ing, attr, d[key])
    db.session.commit()
    return jsonify({'mensaje':'Ingreso actualizado'}),200

@api.route('/ingresos/<int:id>', methods=['DELETE'])
def delete_ingreso(id):
    ing = Ingreso.query.get_or_404(id)
    db.session.delete(ing)
    db.session.commit()
    return jsonify({'mensaje':'Ingreso eliminado'}),200

@api.route('/ingresos/total', methods=['GET'])
def total_ingresos():
    total = db.session.query(db.func.sum(Ingreso.monto)).scalar() or 0
    return jsonify({'total_ingresos': float(total)}), 200

# --------------------- Egresos ---------------------
@api.route('/egresos', methods=['GET'])
def get_egresos():
    lista = Egreso.query.all()
    return jsonify([{
        'ID_Egreso': e.id_egreso,
        'Fecha': str(e.fecha),
        'Monto': float(e.monto),
        'Descripcion': e.descripcion
    } for e in lista]),200

@api.route('/egresos/<int:id>', methods=['GET'])
def get_egreso(id):
    e = Egreso.query.get_or_404(id)
    return jsonify({
        'ID_Egreso': e.id_egreso,
        'Fecha': str(e.fecha),
        'Monto': float(e.monto),
        'Descripcion': e.descripcion
    }),200

@api.route('/egresos', methods=['POST'])
def post_egreso():
    datos = request.get_json()
    errores = validar_egreso(datos)
    if errores:
        return jsonify({'errores': errores}), 400

    eg = Egreso(
        fecha=datos['Fecha'],
        monto=datos['Monto'],
        descripcion=datos['Descripcion']
    )
    db.session.add(eg)
    db.session.commit()
    return jsonify({'mensaje':'Egreso creado','ID_Egreso': eg.id_egreso}),201


@api.route('/egresos/<int:id>', methods=['PUT'])
def put_egreso(id):
    eg = Egreso.query.get_or_404(id)
    d = request.get_json()
    for key, attr in [('Fecha','fecha'),('Monto','monto'),('Descripcion','descripcion')]:
        if key in d: setattr(eg, attr, d[key])
    db.session.commit()
    return jsonify({'mensaje':'Egreso actualizado'}),200

@api.route('/egresos/<int:id>', methods=['DELETE'])
def delete_egreso(id):
    eg = Egreso.query.get_or_404(id)
    db.session.delete(eg)
    db.session.commit()
    return jsonify({'mensaje':'Egreso eliminado'}),200

@api.route('/fondos/disponibles', methods=['GET'])
def fondos_disponibles():
    total_i = db.session.query(db.func.sum(Ingreso.monto)).scalar() or 0
    total_e = db.session.query(db.func.sum(Egreso.monto)).scalar() or 0
    return jsonify({'fondos_disponibles': float(total_i - total_e)}),200

@api.route('/egresos/total', methods=['GET'])
def total_egresos():
    total = db.session.query(db.func.sum(Egreso.monto)).scalar() or 0
    return jsonify({'total_egresos': float(total)}),200



# --------------------- Vincular Derecho ↔ Cuota ---------------------
@api.route('/derechos/<int:id_derecho>/vincular-cuota', methods=['POST'])
def vincular_cuota_a_derecho(id_derecho):
    datos = request.get_json()
    id_cuota = datos.get('ID_Cuota')
    # 1) Validaciones básicas
    if not id_cuota:
        return jsonify({'errores': ['ID_Cuota es obligatorio.']}), 400
    # Verificar que existan los registros
    derecho = Derecho.query.get(id_derecho)
    if not derecho:
        return jsonify({'errores': [f'Derecho {id_derecho} no encontrado.']}), 404
    cuota = Cuota.query.get(id_cuota)
    if not cuota:
        return jsonify({'errores': [f'Cuota {id_cuota} no encontrada.']}), 404

    # 2) Evitar duplicados
    existe = DerechoCuota.query.filter_by(
        ID_Derecho=id_derecho, ID_Cuota=id_cuota
    ).first()
    if existe:
        return jsonify({'errores': ['Esta cuota ya está vinculada a este derecho.']}), 400

    # 3) Crear la relación
    enlace = DerechoCuota(ID_Derecho=id_derecho, ID_Cuota=id_cuota)
    db.session.add(enlace)
    db.session.commit()
    return jsonify({
        'mensaje': 'Cuota vinculada al derecho exitosamente',
        'ID_Derecho': id_derecho,
        'ID_Cuota': id_cuota
    }), 201


@api.route('/derecho_cuota', methods=['POST'])
def post_derecho_cuota():
    datos = request.get_json()
    id_d  = datos.get('ID_Derecho')
    id_c  = datos.get('ID_Cuota')
    # Validar existencia
    derecho = Derecho.query.get_or_404(id_d)
    cuota   = Cuota.query.get_or_404(id_c)

    # Evitar duplicados
    existe = DerechoCuota.query.filter_by(ID_Derecho=id_d, ID_Cuota=id_c).first()
    if existe:
        return jsonify({'mensaje':'Ya está vinculada'}), 400

    enlace = DerechoCuota(ID_Derecho=id_d, ID_Cuota=id_c)
    db.session.add(enlace)
    db.session.commit()
    return jsonify({
        'mensaje':'Vinculación creada',
        'ID_Derecho': id_d,
        'ID_Cuota': id_c
    }), 201


@api.route('/persona_derecho', methods=['POST'])
def post_persona_derecho():
    datos = request.get_json()
    # 1) Validar datos básicos
    errores = validar_persona_derecho(datos)
    if errores:
        return jsonify({'errores': errores}), 400

    # 2) Recuperar la persona. Si no existe, Flask dará 404 automáticamente.
    persona = Persona.query.get_or_404(datos['ID_Persona'])

    # 3) Crear el registro en Persona_Derecho
    pd = PersonaDerecho(
        ID_Persona   = datos['ID_Persona'],
        ID_Derecho   = datos['ID_Derecho'],
        Fecha_Inicio = datos['Fecha_Inicio'],
        Fecha_Fin    = datos.get('Fecha_Fin')  # opcional
    )
    db.session.add(pd)

    # 4) **Parte NUEVA**: por cada cuota vinculada al derecho,
    #    creamos un PersonaCuota con estado 'Pendiente'
    #    Suponemos que en PersonaDerecho tienes relación con Derecho:
    #    pd.derecho → instancia de Derecho
    for enlace in pd.derecho.cuotas_asociadas:
        pc = PersonaCuota(
            ID_Persona = persona.ID_Persona,
            ID_Cuota   = enlace.ID_Cuota,
            Fecha_Asig = datos['Fecha_Inicio'],
            Estado     = 'Pendiente'
        )
        db.session.add(pc)

    # 5) Guardar todo en la base de datos
    db.session.commit()

    # 6) Responder con éxito
    return jsonify({
        'mensaje': 'Asignación creada y cuotas preasignadas',
        'ID_Persona': persona.ID_Persona,
        'ID_Derecho': datos['ID_Derecho']
    }), 201

    


