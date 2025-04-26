from app import create_app, db

app = create_app()

# --- Make sure context exists before accessing db ---
with app.app_context():
    from app.models import User, SharedAccess, Photo, Comment  # <-- Add your models here
    db.create_all()
    print("✅ Database checked/created successfully.")

# --- Local run if needed ---
if __name__ == "__main__":
    app.run()
