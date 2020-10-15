import datetime as dt

from SUIBE_DID_Data_Manager.database import (
    Column,
    Model,
    db,
)

class DID(Model):
    __tablename__ = "did"
    type = db.Column(db.String(22), nullable=False)
    id = db.Column(db.String(88), nullable=False)
    # privkeyHex
    privkey_hex = db.Column(db.String(355), nullable=False)
    privkey_int = db.Column(db.String(355), nullable=False)

    publickey_hex = db.Column(db.String(355), nullable=True)
    publickey_int = db.Column(db.String(355), nullable=True)
