import datetime as dt

from SUIBE_DID_Data_Manager.database import (
    Column,
    Model,
    db,
)

class Did(Model):
    """A user of the app."""

    __tablename__ = "did"
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
