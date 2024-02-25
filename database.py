import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

DATABASE_URl = "postgresql://myuser:19971997@localhost/ecommerce"

engine = _sql.create_engine(DATABASE_URl)

sessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind = engine)

base = _declarative.declarative_base()

