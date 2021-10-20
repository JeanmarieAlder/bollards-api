import os
from bollards_api.models import User
from flask_wtf.csrf import generate_csrf

def test_register_page_layout(client):
    rv = client.get("/register")
    resp = rv.data
    assert b'<title>Bollards API - Register</title>' in resp
    assert b'<h1>Register as a guest</h1>' in resp
    assert b'<input class="form-control form-control-lg" id="username" name="username" required type="text" value="">' in resp
    assert b'<input class="form-control form-control-lg" id="password" name="password" required type="password" value="">' in resp
    assert b'<input class="form-control form-control-lg" id="confirm_password" name="confirm_password" required type="password" value="">' in resp
    assert b'<input class="form-control form-control-lg" id="secret_phrase" name="secret_phrase" required type="password" value="">' in resp
    assert b'<input class="btn btn-outline-info" id="submit" name="submit" type="submit" value="Register">' in resp
    assert b'Note: To get editing permissions, contact the author.' in resp


def test_register_correctly(client, app):
    rv = client.post("/register", data=dict(
        username="newuser",
        password="newpassword",
        confirm_password="newpassword",
        secret_phrase=os.environ['TEST_REGISTRATION_SECRET_PHRASE']
    ), follow_redirects=True)
    resp = rv.data
    assert b'Account created. Welcome newuser. Please log in.' in resp
    assert b'<h1>Login</h1>' in resp


def test_register_fails_without_arguments(client, app):
    rv = client.post("/register", data=dict(
        username="badguy",
        password="misterbadguy",
        confirm_password="misterbadguy",
        secret_phrase="Completelywrongsecretphrase"
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Account created. Welcome newuser. Please log in.' not in resp
    assert b'<h1>Login</h1>' not in resp
    assert b'Account creation is limited. Please contact the author for specific access' in resp
    assert b'<h1>Register as a guest</h1>' in resp


def test_register_fails_with_different_passwords(client, app):
    rv = client.post("/register", data=dict(
        username="badguy",
        password="misterbadguy",
        confirm_password="misterbadguydoesntknowpassword",
        secret_phrase=os.environ['TEST_REGISTRATION_SECRET_PHRASE']
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Account created. Welcome newuser. Please log in.' not in resp
    assert b'<h1>Login</h1>' not in resp
    assert b'<h1>Register as a guest</h1>' in resp
    assert b'<span>Field must be equal to password.</span>' in resp


def test_login_with_correct_credentials(client):
    rv = client.post("/login", data=dict(
        username='noob',
        password='password'
    ), follow_redirects=True)
    resp = rv.data
    assert b'<title>Bollards API</title>' in resp
    assert b'Login successful. Welcome noob!' in resp


def test_login_with_incorrect_username(client):
    rv = client.post("/login", data=dict(
        username='noobylol',
        password='password'
    ), follow_redirects=True)
    resp = rv.data
    assert b'<title>Bollards API</title>' not in resp
    assert b'Login successful.' not in resp


def test_account_page_redirects_without_account(client):
    rv = client.get("/account", follow_redirects=True)
    print(rv.data)
    resp = rv.data
    assert b'Please log in to access this page.' in resp
    assert b'<h1>Login</h1>' in resp

def test_account_page_displays_user(client, auth):
    auth.login()
    rv = client.get("/account")
    print(rv.data)
    resp = rv.data
    assert False