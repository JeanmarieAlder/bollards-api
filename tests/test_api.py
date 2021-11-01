
from tests.utils.api_responses import (bollards_details_resp,
                                       bollards_list_resp,
                                       bollards_markers_resp)

API_ENDPOINT = "/api/v1"

def test_bollards_list(client):
    rv = client.get(API_ENDPOINT + "/bollards/list")
    resp = rv.data
    print(resp)
    assert bollards_list_resp in resp


def test_bollards_markers(client):
    rv = client.get(API_ENDPOINT + "/bollards/markers")
    resp = rv.data
    print(resp)
    assert bollards_markers_resp in resp


def test_bollards_details(client):
    rv = client.get(API_ENDPOINT + "/bollards/details/2")
    resp = rv.data
    print(resp)
    assert bollards_details_resp in resp
