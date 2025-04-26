from app import create_app, db

app = create_app()

# --- Always try creating missing tables (safe, idempotent) ---
with app.app_context():
    db.create_all()
    print("✅ Database checked/created successfully.")

# --- Local run if needed ---
if __name__ == "__main__":
    app.run()
