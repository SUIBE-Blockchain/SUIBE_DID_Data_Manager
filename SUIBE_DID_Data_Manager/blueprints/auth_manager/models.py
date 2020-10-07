# -*- coding: utf-8 -*-
"""User models."""
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
from SUIBE_DID_Data_Manager.extensions import bcrypt


class DidDoc(Model):
    __tablename__ = "diddoc"
    id = db.Column(db.Integer, primary_key=True)
    did = db.Column(db.String(88), nullable=False)
