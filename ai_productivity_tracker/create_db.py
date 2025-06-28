from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

from app import db, create_app
from sqlalchemy import text

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(task);"))
        for row in result:
            print(row)
