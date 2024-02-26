import sqlalchemy as _sql
import database as _database

class order_status(_database.base):
    __tablename__ = "order_status"
    id = _sql.Column(_sql.INTEGER, primary_key=True,index=True)
    status = _sql.Column(_sql.VARCHAR(200))

class product(_database.base):
    __tablename__ = "product"
    id = _sql.Column(_sql.INTEGER, primary_key=True,index=True)
    category_id = _sql.Column(_sql.INTEGER)
    name = _sql.Column(_sql.VARCHAR)
    description = _sql.Column(_sql.TEXT)