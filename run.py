from app import create_app, db
import os

app = create_app()

# --- Automatic database creation if missing ---
if not os.path.exists("app.db"):
    with app.app_context():
        db.create_all()
        print("✅ Database created successfully.")

# --- Run app if executed locally (optional) ---
if __name__ == "__main__":
    app.run()
