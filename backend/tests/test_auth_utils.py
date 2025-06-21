from types import SimpleNamespace
from app.auth import utils
from jose import jwt


def test_hash_and_verify_password():
    password = "secret"
    hashed = utils.hash_password(password)
    assert hashed != password
    assert utils.verify_password(password, hashed)
    assert not utils.verify_password("wrong", hashed)


def test_access_token_contains_subject():
    token = utils.create_access_token({"sub": "42"})
    decoded = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
    assert decoded["sub"] == "42"


def test_reset_token_roundtrip():
    user = SimpleNamespace(email="foo@example.com")
    token = utils.create_reset_token(user)
    assert utils.verify_reset_token(token) == user.email


def test_reset_token_invalid():
    assert utils.verify_reset_token("invalid") is None


def test_send_reset_email(capsys):
    utils.send_reset_email("user@example.com", "tok123")
    captured = capsys.readouterr().out
    assert "user@example.com" in captured
    assert "tok123" in captured
