import datetime as dt

from flask_login import UserMixin

from SUIBE_DID_Data_Manager.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)

class Data(Model):
    """A user of the app."""

    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)

class CPT(Model):
    """A user of the app."""

    __tablename__ = "cpt"
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
