# test_derecho_cuota.py
from app import create_app
from app.extensions import db
from app.models import (
    Persona, Derecho, Cuota,
    DerechoCuota, PersonaCuota, PersonaDerecho
)

def main():
    app = create_app()
    with app.app_context():
        # 1) Limpiar TODO rastro de pruebas anteriores
        
        # Borrar asignaciones de cuotas y derechos
        PersonaCuota.query.filter_by(ID_Persona=9999).delete()
        PersonaDerecho.query.filter_by(ID_Persona=9999).delete()
        DerechoCuota.query.filter_by(ID_Derecho=9999).delete()
        
        # Borrar la persona de prueba por DPI
        Persona.query.filter_by(dpi='9999999999999').delete()
        
        # Borrar derecho y cuota de prueba por sus claves
        Derecho.query.filter_by(ID_Derecho=9999).delete()
        Cuota.query.filter_by(Descripcion='TestCuota').delete()
        
        db.session.commit()
        print("→ Datos previos limpiados.")

        # 2) Crear nueva Persona, Derecho y Cuota
        p = Persona(
            dpi='9999999999999',
            nombre='TestUser',
            estado='Activo'
        )
        d = Derecho(
            ID_Derecho=9999,
            Nombre='TestDerecho'
        )
        c = Cuota(
            ID_Cuota=9999,
            Descripcion='TestCuota',
            Monto=50.0,
            Fecha_Limite='2025-12-31'
        )
        db.session.add_all([p, d, c])
        db.session.commit()
        print(f"→ Creado Persona (DPI={p.dpi}), Derecho ID={d.ID_Derecho}, Cuota ID={c.ID_Cuota}")

        # 3) Enlazar Derecho ↔ Cuota
        enlace = DerechoCuota(ID_Derecho=d.ID_Derecho, ID_Cuota=c.ID_Cuota)
        db.session.add(enlace)
        db.session.commit()
        print("→ DerechoCuota creado correctamente.")

        # 4) Asignar derecho y generar PersonaCuota
        p.asignar_derecho(d.ID_Derecho, fecha_asig='2025-05-15')
        print("→ Llamada a asignar_derecho() realizada.")

        # 5) Verificar existencia de exactamente un PersonaCuota
        pcs = PersonaCuota.query.filter_by(
            ID_Persona=p.id_persona,
            ID_Cuota=c.ID_Cuota
        ).all()
        assert len(pcs) == 1, "❌ No se creó la cuota para la persona"
        print("✅ Prueba OK: PersonaCuota creada correctamente.")

        # 6) Limpiar registros de prueba otra vez
        PersonaCuota.query.filter_by(ID_Persona=p.id_persona).delete()
        PersonaDerecho.query.filter_by(ID_Persona=p.id_persona).delete()
        DerechoCuota.query.filter_by(ID_Derecho=d.ID_Derecho).delete()
        Persona.query.filter_by(dpi=p.dpi).delete()
        Derecho.query.filter_by(ID_Derecho=d.ID_Derecho).delete()
        Cuota.query.filter_by(ID_Cuota=c.ID_Cuota).delete()
        db.session.commit()
        print("→ Registros de prueba eliminados. Todo OK.")

if __name__ == '__main__':
    main()
