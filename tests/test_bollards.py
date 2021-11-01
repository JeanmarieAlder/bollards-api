def test_list_page(client):
    """Test that list page displays correctly"""

    rv = client.get('/list')
    resp = rv.data
    print(resp)
    assert b'<h1 class="m-2">Bollards List</h1>' in resp
    assert b'<b>No 3a</b>' in resp
    assert b'<b>No 1</b>' in resp


def test_manage_page(client, auth):
    auth.login()
    rv = client.get("/manage/1", follow_redirects=True)
    resp = rv.data
    print(resp)
    assert b"<h1>Manage Bollard</h1>" in resp