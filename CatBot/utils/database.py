# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import create_engine, Column, BigInteger, String, Date, Text, \
    func, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from CatBot.settings import database_url

_engine = create_engine(database_url())
_Session = sessionmaker()
_Session.configure(bind=_engine)

Base = declarative_base()


class NoRecords:
    """Used when database is working, but user has no records."""

    def __repr__(self):
        return "<NoFlexes: database OK, but no records>"


class Flex(Base):
    __tablename__ = 'flexes'
    flex_id = Column(BigInteger, primary_key=True)
    user_id = Column(String('18'))
    flex_date = Column(Date)
    reason = Column(Text)


def get_flex(user_id: int) -> Flex or None:
    session = _Session()
    try:
        return session.query(Flex).filter_by(
            user_id=str(user_id)
        ).one_or_none() or NoRecords()
    finally:
        session.close()


def get_flexes(user_id: int) -> list[Flex]:
    session = _Session()
    try:
        return list(session.query(Flex).filter_by(user_id=str(user_id))
                    .order_by(desc(Flex.flex_date)).limit(10))
    finally:
        session.close()


def get_top_flexes(last_x_days: int = 30) -> list[tuple[Any, ...]]:
    session = _Session()
    if last_x_days < 1:
        last_x_days = 30
    try:
        flex_date_filter = datetime.today() - timedelta(days=last_x_days)
        return list(session.query(
            Flex.user_id, func.count(Flex.user_id))
                    .group_by(Flex.user_id)
                    .order_by(func.count(Flex.user_id).desc())
                    .filter(Flex.flex_date >= flex_date_filter)
                    .limit(3))
    finally:
        session.close()


def add_flex(user_id: int, reason: str) -> Flex or None:
    session = _Session()
    new_flex = Flex(
        user_id=str(user_id),
        flex_date=date.today(),
        reason=reason
    )
    try:
        session.add(new_flex)
        session.commit()
        return new_flex
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


class Counter(Base):
    __tablename__ = 'counters'
    counter_id = Column(BigInteger, primary_key=True)
    user_id = Column(String(18))
    counter_date = Column(Date)


def get_counters(user_id: int) -> int:
    session = _Session()
    try:
        return session.query(Counter).filter_by(user_id=str(user_id)).count()
    finally:
        session.close()


def add_counter(user_id: int) -> Counter or None:
    session = _Session()
    new_counter = Counter(
        user_id=str(user_id),
        counter_date=date.today()
    )
    try:
        session.add(new_counter)
        session.commit()
        return new_counter
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


class Interrupt(Base):
    __tablename__ = 'interrupts'
    interrupt_id = Column(BigInteger, primary_key=True)
    user_id = Column(String(18))
    interrupt_date = Column(Date)


def get_interrupts(user_id: int) -> int:
    session = _Session()
    try:
        return session.query(Interrupt).filter_by(user_id=str(user_id)).count()
    finally:
        session.close()


def add_interrupt(user_id: int) -> Interrupt or None:
    session = _Session()
    new_interrupt = Interrupt(
        user_id=str(user_id),
        interrupt_date=date.today()
    )
    try:
        session.add(new_interrupt)
        session.commit()
        return new_interrupt
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


class Bonk(Base):
    __tablename__ = 'bonks'
    bonk_id = Column(BigInteger, primary_key=True)
    user_id = Column(String(18))
    bonk_date = Column(Date)


def get_bonks(user_id: int) -> int:
    session = _Session()
    try:
        return session.query(Bonk).filter_by(user_id=str(user_id)).count()
    finally:
        session.close()


def add_bonk(user_id: int) -> Bonk or None:
    session = _Session()
    new_bonk = Bonk(
        user_id=str(user_id),
        bonk_date=date.today()
    )
    try:
        session.add(new_bonk)
        session.commit()
        return new_bonk
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()
