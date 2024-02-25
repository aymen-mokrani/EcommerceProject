import datetime as _dt
import sqlalchemy as _sql
import database as _database

class order_status(_database.base):
    __tablename__ = "order_status"
    id = _sql.Column(_sql.INTEGER, primary_key=True,index=True)
    status = _sql.Column(_sql.VARCHAR(200))