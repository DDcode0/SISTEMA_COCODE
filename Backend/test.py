from app import create_app
from app.extensions import db
from app.models import Persona

# Crear una instancia de la aplicación
app = create_app()

# Operaciones CRUD
with app.app_context():
    # **Leer una persona específica (SELECT ONE)**
    print("\nConsultando una persona específica (ID = 1)...")

    # Usar `db.session.get()` en lugar de `Persona.query.get()`
    persona_especifica = db.session.get(Persona, 1)  # `Persona` es el modelo, `1` es el ID
    if persona_especifica:
        print(f"Persona encontrada: Nombre: {persona_especifica.Nombre}, DPI: {persona_especifica.DPI}")
    else:
        print("Persona no encontrada.")