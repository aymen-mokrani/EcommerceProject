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

class address(_database.base):
    __tablename__ = "address"
    id = _sql.Column(_sql.INTEGER, primary_key=True,index=True)
    unit_number = _sql.Column(_sql.VARCHAR(200))
    street_number = _sql.Column(_sql.VARCHAR(200))
    address_line = _sql.Column(_sql.VARCHAR(200))
    city = _sql.Column(_sql.VARCHAR(200))
    region = _sql.Column(_sql.VARCHAR(200))
    postal_code = _sql.Column(_sql.INTEGER)
    country_id = _sql.Column(_sql.INTEGER)