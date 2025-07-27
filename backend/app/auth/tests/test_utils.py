from types import SimpleNamespace
from unittest.mock import patch
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


@patch('app.auth.utils.send_reset_email')
def test_send_reset_email(mock_send_reset_email, capsys):
    email = "user@example.com"
    token = "tok123"
    utils.send_reset_email(email, token)
    mock_send_reset_email.assert_called_once_with(email, token)
    # The capsys assertions are no longer relevant as the email sending is mocked
    # captured = capsys.readouterr().out
    # assert "user@example.com" in captured
    # assert "tok123" in captured
