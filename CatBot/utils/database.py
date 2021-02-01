# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from typing import Optional, List

from sqlalchemy import create_engine, Column, BigInteger, String, Date, Text, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from CatBot.settings import Settings

_engine = create_engine(Settings().database_url)
_Session = sessionmaker()
_Session.configure(bind=_engine)

Base = declarative_base()


class Flex(Base):
    __tablename__ = 'flexes'
    flex_id = Column(BigInteger, primary_key=True)
    user_id = Column(String('18'))
    flex_date = Column(Date)
    reason = Column(Text)


def get_flex(user_id: int) -> Optional[Flex]:
    session = _Session()
    try:
        return session.query(Flex).filter_by(user_id=str(user_id)).one_or_none()
    finally:
        session.close()


def get_flexes(user_id: int) -> Optional[List[Flex]]:
    session = _Session()
    try:
        return list(session.query(Flex).filter_by(user_id=str(user_id)).limit(10))
    finally:
        session.close()


def get_top_flexes(last_x_days: int = 30) -> Optional[List[Flex]]:
    session = _Session()
    if last_x_days < 1:
        last_x_days = 30
    try:
        flex_date_filter = datetime.today() - timedelta(days=last_x_days)
        return list(session.query(
            Flex.user_id, func.count(Flex.user_id))
                    .group_by(Flex.user_id)
                    .filter(Flex.flex_date >= flex_date_filter)
                    .limit(3))
    finally:
        session.close()


def add_flex(user_id: int, reason: str) -> Optional[Flex]:
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
