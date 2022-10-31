from sqlalchemy import Column, String, UnicodeText
from TelethonHell.DB import BASE, SESSION


class Gvar(BASE):
    __tablename__ = "gvar"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = value


Gvar.__table__.create(checkfirst=True)


def gvarstat(variable):
    try:
        return SESSION.query(Gvar).filter(Gvar.variable == str(variable)).first().value
    except BaseException:
        return None
    finally:
        SESSION.close()


def addgvar(variable, value):
    if SESSION.query(Gvar).filter(Gvar.variable == str(variable)).one_or_none():
        delgvar(variable)
    adder = Gvar(str(variable), value)
    SESSION.add(adder)
    SESSION.commit()


def delgvar(variable):
    rem = (
        SESSION.query(Gvar)
        .filter(Gvar.variable == str(variable))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.commit()
