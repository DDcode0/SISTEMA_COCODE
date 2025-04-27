from app import create_app
from app.extensions import db
from app.models import Persona, Derecho, Cuota, Pago, Ingreso, Egreso, PersonaDerecho

app = create_app()

with app.app_context():
    # Eliminar todos los datos existentes (para pruebas)
    db.session.query(Pago).delete()
    db.session.query(Cuota).delete()
    db.session.query(PersonaDerecho).delete()
    db.session.query(Derecho).delete()
    db.session.query(Persona).delete()
    db.session.query(Ingreso).delete()
    db.session.query(Egreso).delete()
    db.session.commit()

    # Insertar datos de prueba
    nueva_persona = Persona(DPI='1112223334445', Nombre='Darwin López', Direccion='Zona 1', Telefono='555111222', Email='darwin@email.com', Rol='Presidente', Estado=True)
    nuevo_derecho = Derecho(Nombre='Agua potable')
    nueva_cuota = Cuota(Descripcion='Cuota de agua potable', Monto=50.00, Fecha_Limite='2023-07-01')
    nuevo_pago = Pago(ID_Persona=1, ID_Cuota=1, Fecha_Pago='2023-06-30', Monto_Pagado=50.00, Estado='Completado')
    nuevo_ingreso = Ingreso(Fecha='2023-06-30', Monto=50.00, Fuente='Pago de agua potable')
    nuevo_egreso = Egreso(Fecha='2023-07-01', Monto=30.00, Descripcion='Reparación de tuberías')

    # Agregar los datos
    db.session.add(nueva_persona)
    db.session.add(nuevo_derecho)
    db.session.add(nueva_cuota)
    db.session.add(nuevo_pago)
    db.session.add(nuevo_ingreso)
    db.session.add(nuevo_egreso)
    db.session.commit()

    # Consultar los datos y mostrar resultados
    personas = Persona.query.all()
    derechos = Derecho.query.all()
    cuotas = Cuota.query.all()
    pagos = Pago.query.all()
    ingresos = Ingreso.query.all()
    egresos = Egreso.query.all()

    print("Personas:")
    for persona in personas:
        print(persona)

    print("\nDerechos:")
    for derecho in derechos:
        print(derecho)

    print("\nCuotas:")
    for cuota in cuotas:
        print(cuota)

    print("\nPagos:")
    for pago in pagos:
        print(pago)

    print("\nIngresos:")
    for ingreso in ingresos:
        print(ingreso)

    print("\nEgresos:")
    for egreso in egresos:
        print(egreso)