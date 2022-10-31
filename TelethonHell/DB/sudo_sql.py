from sqlalchemy import Column, String
from TelethonHell.DB import BASE, SESSION


class Sudo(BASE):
    __tablename__ = "sudo"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Sudo.__table__.create(checkfirst=True)


def in_sudo(chat_id):
    try:
        return SESSION.query(Sudo).filter(Sudo.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_sudo(chat_id):
    adder = Sudo(str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def rem_sudo(chat_id):
    rem = SESSION.query(Sudo).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def all_sudo():
    rem = SESSION.query(Sudo).all()
    SESSION.close()
    if rem:
        return rem
    else:
        return 1234
