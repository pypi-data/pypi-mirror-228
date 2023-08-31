import contextlib
import typing

import pytest
import sqlalchemy.event
import sqlalchemy.orm


@contextlib.contextmanager
def fsm(
    db_url: str,
    namespace: typing.Any,
    symbol_name: str,
    *,
    create_engine_kwargs: typing.Optional[typing.Mapping] = None,
) -> typing.Generator:
    """
    :param db_url: url of the test.py database
    :param namespace: namespace where the original session_maker is located
    :param symbol_name: name of the original session_maker symbol
    :param create_engine_kwargs: keyword arguments to pass to sqlalchemy.create_engine
    :return: a context manager that can be used as a session_maker
    """
    if create_engine_kwargs is None:
        create_engine_kwargs = {}

    engine = sqlalchemy.create_engine(
        url=db_url,
        echo=True,
        **create_engine_kwargs,
    )

    if db_url.startswith("sqlite"):

        @sqlalchemy.event.listens_for(engine, "connect")
        def do_connect(dbapi_connection: typing.Any, _: typing.Any) -> None:
            # disable pysqlite's emitting of the "BEGIN" statement entirely.
            # also stops it from emitting COMMIT before any DDL.
            dbapi_connection.isolation_level = None

        @sqlalchemy.event.listens_for(engine, "begin")
        def do_begin(connexion: sqlalchemy.engine.Connection) -> None:
            # emit our own "BEGIN"
            connexion.exec_driver_sql("BEGIN")

    with engine.connect() as conn, conn.begin() as transaction:
        session_maker = sqlalchemy.orm.sessionmaker(
            bind=conn,
            join_transaction_mode="create_savepoint",
        )

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(namespace, symbol_name, session_maker)
            yield session_maker

        transaction.rollback()
