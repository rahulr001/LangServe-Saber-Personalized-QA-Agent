from core.app import engine
from core.app.api.models import Users

Users.Base.metadata.create_all(engine)
