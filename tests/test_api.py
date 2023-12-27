
API_ENDPOINT = "/api/v1"

def test_bollards_list(client):
    rv = client.get(API_ENDPOINT + "/bollards/list")
    resp = rv.data
    print(resp)
    assert resp is not None


def test_bollards_markers(client):
    rv = client.get(API_ENDPOINT + "/bollards/markers")
    resp = rv.data
    print(resp)
    assert resp is not None


def test_bollards_details(client):
    rv = client.get(API_ENDPOINT + "/bollards/details/2")
    resp = rv.data
    print(resp)
    assert resp is not None
