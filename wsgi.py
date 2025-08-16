from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

@app.shell_context_processor
def ctx():
    return {"db": db, "app": app, "User": User}
