import pytest


@pytest.mark.parametrize("name", ["Joe", "Jane"])
def test_isolation(create_user, user_model, fake_session_maker, name):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = create_user(name)
    assert result == "success"
    with fake_session_maker() as session:
        assert session.query(user_model.id, user_model.name).all() == [(1, name)]


@pytest.mark.parametrize("name", ["Joe", "Jane"])
def test_commit(create_user_with_commit, user_model, fake_session_maker, name):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = create_user_with_commit(name)
    assert result == "success"
    with fake_session_maker() as session:
        assert session.query(user_model.id, user_model.name).all() == [(1, name)]


def test_auto_rollback(
    create_user_joe, read_user_with_auto_rollback, user_model, fake_session_maker
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = read_user_with_auto_rollback()
    assert len(result) == 1
    with fake_session_maker() as session:
        assert session.query(user_model.id, user_model.name).all() == [(1, "Joe")]


@pytest.mark.parametrize(["name1", "name2"], [["Joe", "Jane"], ["Jane", "Joe"]])
def test_rollback_commit_rollback(
    create_user_rollback_commit_rollback,
    user_model,
    fake_session_maker,
    namespace,
    name1,
    name2,
):
    create_user_rollback_commit_rollback(name1, name2)
    with fake_session_maker() as session:
        assert session.query(user_model.id, user_model.name).all() == [(1, name2)]
    create_user_rollback_commit_rollback(name1, name2)
    with fake_session_maker() as session:
        assert session.query(user_model.id, user_model.name).all() == [
            (1, name2),
            (2, name2),
        ]
