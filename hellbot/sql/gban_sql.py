from . import SESSION, BASE
from sqlalchemy import Column, String


class GBan(BASE):
    __tablename__ = "gban"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


GBan.__table__.create(checkfirst=True)


def is_gbanned(chat_id):
    try:
        return SESSION.query(GBan).filter(GBan.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gbaner(chat_id):
    adder = GBan(str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def ungbaner(chat_id):
    rem = SESSION.query(GBan).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def all_gbanned():
    rem = SESSION.query(GBan).all()
    SESSION.close()
    return rem
