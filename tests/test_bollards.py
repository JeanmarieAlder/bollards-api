from io import BytesIO
from pytest_mock import MockerFixture


def test_list_page(client):
    """Test that list page displays correctly"""

    rv = client.get('/list')
    resp = rv.data
    print(resp)
    assert b'<h1 class="m-2">Bollards List</h1>' in resp
    assert b'<b>No 3a</b>' in resp
    assert b'<b>No 1</b>' in resp


def test_list_page_sort_by_ascending(client):
    rv = client.get('/list?sort=nasc')
    resp = rv.data
    print(resp)
    assert resp.find(b'No 1') < resp.find(b'No 2')


def test_list_page_sort_by_descending(client):
    rv = client.get('/list?sort=ndesc')
    resp = rv.data
    print(resp)
    assert resp.find(b'No 1') > resp.find(b'No 2')


def test_manage_page(client, auth):
    auth.login()
    rv = client.get("/manage/1", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b"<h1>Manage Bollard</h1>" in resp


def test_modify_bollard(client, auth):
    auth.login()
    rv = client.post("/manage/1", data=dict(
        b_number = 42,
        b_letter = "z",
        b_type = "Special",
        images = (None, '')
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1 class="m-2">Bollards List</h1>' in resp
    assert b'<b>No 42z</b>' in resp
    assert b'Bollard No 42 has been updated' in resp


def test_modify_bollard_main_image(client, auth, mocker: MockerFixture):
    mocker.patch('PIL.Image.Image.save')
    auth.login()
    with open("tests/img/test-bollard.jpg", 'rb') as img:
        imgStringIO = BytesIO(img.read())
    rv = client.post("/manage/1", data=dict(
        b_number = 42,
        b_letter = "z",
        b_type = "Special",
        main_image = (imgStringIO, 'new-main-image.jpg'),
        images = (None, '')
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1 class="m-2">Bollards List</h1>' in resp
    assert b'<b>No 42z</b>' in resp
    assert b'test_bollard_icon_1.jpeg' not in resp
    assert b'Bollard No 42 has been updated' in resp


def test_modify_bollard_images(client, auth, mocker: MockerFixture):
    mocker.patch('PIL.Image.Image.save')
    auth.login()
    with open("tests/img/test-bollard.jpg", 'rb') as img:
        imgStringIO = BytesIO(img.read())
    rv = client.post("/manage/1", data=dict(
        b_number = 42,
        b_letter = "z",
        b_type = "Special",
        images = (imgStringIO, 'test-bollard.jpg')
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1 class="m-2">Bollards List</h1>' in resp
    assert b'Bollard No 42 has been updated' in resp


def test_delete_bollard(client, auth):
    auth.login()
    rv = client.post("/delete/1", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Bollard deleted successfully.' in resp
    assert b'<b>No 1</b>' not in resp


def test_add_bollard_page(client, auth):
    auth.login()
    rv = client.get("/add", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'<h1 style="float: left;">New Bollard</h1>' in resp
    assert b'<input autocomplete="off" class="form-control form-control-sm" id="b_number" name="b_number" required type="number" value="">' in resp


def test_add_simple_bollard(client, auth):
    auth.login()
    rv = client.post("/add", data=dict(
        b_number=69,
        b_type="Custom",
        b_letter=""
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Bollard No 69 Created' in resp
    assert b'<td style="vertical-align: middle;"><b>No 69</b></td>' in resp


def test_add_bollard_with_images(client, auth, mocker: MockerFixture):
    mocker.patch('PIL.Image.Image.save')
    with open("tests/img/test-bollard-landscape.jpg", 'rb') as img:
        imgMainStringIO = BytesIO(img.read())
    with open("tests/img/test-bollard.jpg", 'rb') as img2:
        imgStringIO = BytesIO(img2.read())
    auth.login()
    rv = client.post("/add", data=dict(
        b_number=69,
        b_type="Custom",
        b_letter="",
        main_image=(imgMainStringIO, "main-bollard.jpg"),
        images=(imgStringIO, "other-bollard.jpg")
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Bollard No 69 Created' in resp
    assert b'<td style="vertical-align: middle;"><b>No 69</b></td>' in resp

def test_add_existing_bollard_fails(client, auth):
    auth.login()
    rv = client.post("/add", data=dict(
        b_number=1,
        b_type="Custom",
        b_letter=""
    ), follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Bollard No 1 Created' not in resp
    assert b'Bollard No 1 allready exists' in resp
    assert b'<title>Bollards API - Add</title>' in resp


def test_delete_image_from_bollard(client, auth):
    auth.login()
    rv = client.post('/delete/image/1/1', follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b'Image deleted successfully.' in resp
    assert b'<h1>Manage Bollard</h1>' in resp
    assert b'test_bollard_1.jpeg' not in resp