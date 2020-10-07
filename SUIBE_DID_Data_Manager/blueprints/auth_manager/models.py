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

class Authentication(Model):
    __tablename__ = "authentication"
    publicKey = db.Column(db.String(88), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(20), nullable=False)

class PublicKey(Model):
    __tablename__ = "publickey"
    id = db.Column(db.String(88), primary_key=True)
    owner = db.Column(db.String(88), nullable=False)
    publicKey = db.Column(db.String(300), nullable=False)
    type = db.Column(db.String(20), nullable=False)

class DidDoc(Model):
    __tablename__ = "diddoc"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.Integer)

    authentication_publickey = db.Column(db.String(88), nullable=False)
    authentication_revoked = db.Column(db.Boolean, nullable=False)
    authentication_type = db.Column(db.String(20), nullable=False)

    publickey_id = db.Column(db.String(88), nullable=False)
    publickey_owner = db.Column(db.String(88), nullable=False)
    publickey_publickey = db.Column(db.String(300), nullable=False)
    publickey_revoked = db.Column(db.Boolean, nullable=False)
    publickey_type = db.Column(db.String(20), nullable=False)

    service = db.Column(db.JSON)
