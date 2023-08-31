import pathlib
import sqlite3

import pytest
import sqlalchemy.orm

from fake_session_maker import fsm


@pytest.fixture(autouse=True, scope="session")
def db_migrate():
    db = pathlib.Path("./tests/test.sqlite")
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
        )
        con.commit()
    yield
    db.unlink()


@pytest.fixture
def namespace():
    class Namespace:
        engine = sqlalchemy.create_engine(
            "sqlite:///tests/test.sqlite",
            echo=True,
        )
        session_maker = sqlalchemy.orm.sessionmaker(bind=engine)

    return Namespace


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


@pytest.fixture(scope="session")
def user_model():
    class User(Base):
        __tablename__ = "users"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String)

    return User


@pytest.fixture
def create_user(namespace, user_model):
    """
    this fixture is used to test a function that rely on the auto-commit feature
    of the session_maker begin method
    """

    def create_user_(name: str):
        with namespace.session_maker.begin() as session:
            session.add(user_model(name=name))
        return "success"

    return create_user_


@pytest.fixture
def create_user_with_commit(namespace, user_model):
    """
    this fixture is used to test a function that do a manual commit
    """

    def create_user_(name: str):
        with namespace.session_maker() as session:
            session.add(user_model(name=name))
            session.commit()
        return "success"

    return create_user_


@pytest.fixture
def read_user_with_auto_rollback(namespace, user_model):
    """
    this fixture is used to test a function that rely on the auto-rollback feature
    """

    def read_users():
        with namespace.session_maker() as session:
            users = session.query(user_model.id, user_model.name).all()
        return users

    return read_users


@pytest.fixture
def create_user_rollback_commit_rollback(namespace, user_model):
    def create_user_(name1: str, name2: str):
        with namespace.session_maker() as session:
            session.add(user_model(name=name1))
            session.rollback()
            session.add(user_model(name=name2))
            session.commit()
            session.add(user_model(name=name1))
            session.rollback()

    return create_user_


@pytest.fixture
def fake_session_maker(namespace) -> sqlalchemy.orm.sessionmaker:
    with fsm(
        db_url="sqlite:///tests/test.sqlite",
        namespace=namespace,
        symbol_name="session_maker",
    ) as fake_session_maker_:
        yield fake_session_maker_


@pytest.fixture
def create_user_joe(namespace, user_model, fake_session_maker):
    with namespace.session_maker.begin() as session:
        session.add(user_model(name="Joe"))
