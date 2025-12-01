from app import create_app
from app.extensions import db
from app.models.users import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Verificar si el usuario ya existe
    existing_user = User.query.filter_by(email="admin@example.com").first()
    
    if not existing_user:
        new_user = User(
            name="Administrador",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(new_user)
        db.session.commit()
        print("✅ Usuario creado exitosamente!")
        print("📧 Email: admin@example.com")
        print("🔑 Contraseña: admin123")
    else:
        print("⚠️ El usuario ya existe")