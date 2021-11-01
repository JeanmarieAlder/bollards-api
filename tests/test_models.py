from bollards_api.models import Information, User, Bimage, Bollard

def test_user_model_repr():
    user = User(username='noob', password="password")
    resp = str(user)
    print(resp)
    assert "User('noob')" in resp


def test_bollard_model_repr():
    bimage1 = Bimage(uri="test_bollard_1.jpeg")
    bollard1 = Bollard(
        b_number=1, 
        b_name="Test Bollard 1", 
        comment="Test comment for bollard 1.", 
        image_icon="test_bollard_icon_1.jpeg")
    bollard1.images.append(bimage1)
    resp = str(bollard1)
    print(resp)
    assert "Bollard('1', 'Test Bollard 1', 'Test comment for bollard 1.', 'test_bollard_icon_1.jpeg')" in resp


def test_bimage_model_repr():
    bimage1 = Bimage(uri="test_bollard_1.jpeg")
    resp = str(bimage1)
    print(resp)
    assert "Bimage('test_bollard_1.jpeg', 'None')" in resp


def test_information_model_repr():
    info1 = Information(information="Le test info.")
    resp = str(info1)
    print(resp)
    assert "Information('Le test info.', 'None')" in resp