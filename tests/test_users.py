from io import BytesIO
import os

def test_register_page_layout(client):
    rv = client.get("/register")
    resp = rv.data
    assert b'<title>Bollards API - Register</title>' in resp
    assert b'<h1>Register as a guest</h1>' in resp
    assert b'Note: To get editing permissions, contact the author.' in resp


def test_register_correctly(client):
    rv = client.post("/register", data=dict(
        username="newuser",
        password="newpassword",
        confirm_password="newpassword",
        secret_phrase=os.environ['TEST_REGISTRATION_SECRET_PHRASE']
    ), follow_redirects=True)
    resp = rv.data
    assert b'Account created. Welcome newuser. Please log in.' in resp
    assert b'<h1>Login</h1>' in resp


def test_register_fails_without_arguments(client):
    rv = client.post("/register", data=dict(
        username="badguy",
        password="misterbadguy",
        confirm_password="misterbadguy"
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Account created.' not in resp
    assert b'<h1>Login</h1>' not in resp
    assert b'<h1>Register as a guest</h1>' in resp


def test_register_fails_with_different_passwords(client):
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


def test_register_fails_with_existing_user(client):
    rv = client.post("/register", data=dict(
        username="noob",
        password="misterbadguy",
        confirm_password="misterbadguy",
        secret_phrase=os.environ['TEST_REGISTRATION_SECRET_PHRASE']
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Account created. Welcome newuser. Please log in.' not in resp
    assert b'<h1>Login</h1>' not in resp
    assert b'<h1>Register as a guest</h1>' in resp
    assert b'<span>Username already taken</span>' in resp


def test_register_fails_with_wrong_secret_phrase(client):
    rv = client.post("/register", data=dict(
        username="badguy",
        password="misterbadguy",
        confirm_password="misterbadguy",
        secret_phrase="wrongsecretphraselol"
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Account creation is limited. Please contact the author for specific access' in resp
    assert b'<h1>Login</h1>' not in resp
    assert b'<h1>Register as a guest</h1>' in resp

def test_register_redirects_if_allready_logged_in(client, auth):
    auth.login()
    rv = client.get("/register", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1 class="text-center">Welcome to Bollards API</h1>' in resp


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


def test_login_redirects_if_logged_in(client, auth):
    auth.login()
    rv = client.get("/login", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1 class="text-center">Welcome to Bollards API</h1>' in resp


def test_logout(client, auth):
    auth.login()
    rv = client.get("/logout", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<a class="nav-item nav-link" href="/login">Login</a>' in resp


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
    assert b'<h1>Account</h1>' in resp
    assert b'<h2>Logged in as <b>noob</b></h2>' in resp

def test_username_changes_correctly(client, auth):
    auth.login()
    rv = client.post("/account", data=dict(
        username='noobylol',
        submit_account=True
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1>Account</h1>' in resp
    assert b'Accound updated, your username is now noobylol.' in resp
    assert b'<div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordion-account">' in resp
    assert b'<input class="form-control form-control-lg" id="username" name="username" required type="text" value="noobylol">' in resp


def test_username_change_existing_username_error(client, auth):
    auth.login()
    rv = client.post("/account", data=dict(
        username='user2',
        submit_account=True
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1>Account</h1>' in resp
    assert b'<span>Username already taken</span>' in resp
    assert b'<input class="form-control form-control-lg is-invalid" id="username" name="username" required type="text" value="noob">' in resp


def test_account_image_updates_correctly(client, auth):
    auth.login()
    with open("tests/img/test-profile-pic.jpg", 'rb') as img:
        imgStringIO = BytesIO(img.read())
    rv = client.post("/account", data=dict(
        username='noob',
        profile_pic=(imgStringIO, 'newpic.jpg'),
        submit_account=True
        ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert False



def test_password_changes_correctly(client, auth):
    auth.login()
    rv = client.post("/account", data=dict(
        old_password='password',
        new_password='newpassword',
        confirm_password='newpassword',
        submit_password=True
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1>Account</h1>' in resp
    assert b'Account password updated successfully.' in resp
    assert b'<div id="collapseTwo" class="accordion-collapse collapse show" aria-labelledby="headingTwo" data-bs-parent="#accordion-account">' in resp


def test_wrong_old_password_error(client, auth):
    auth.login()
    rv = client.post("/account", data=dict(
        old_password='badpassword',
        new_password='newpassword',
        confirm_password='newpassword',
        submit_password=True
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1>Account</h1>' in resp
    assert b'An error occured when changing the password, please try again.' in resp
    assert b'<div id="collapseTwo" class="accordion-collapse collapse show" aria-labelledby="headingTwo" data-bs-parent="#accordion-account">' in resp
