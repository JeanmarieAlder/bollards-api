
from bollards_api.main.forms import ContactForm

def test_home_page(client):
    """Test that home page displays correctly"""

    rv = client.get('/')
    assert b'<h1 class="text-center">Welcome to Bollards API</h1>' in rv.data
    assert b'<p class="card-text">Discover all bollards between Vaud, Switzerland and France.</p>' in rv.data
    assert b'Welcome to the bollards.ch API.' in rv.data

    # /home should be equal to /
    rv_home = client.get('/home')
    assert rv_home.data == rv.data


def test_about_page(client):
    rv = client.get('/about')
    assert b'42' in rv.data
    

def test_about_page2(client):
    rv = client.get('/about')
    assert b'42' in rv.data
    
def test_contact_form_works(app):
    """Currently not in use"""
    with app.app_context():
        contactForm = ContactForm()
    assert True


def test_404_on_bad_request(client):
    rv = client.get('/randomlink')
    assert b'<h1>Looks like you ran into 404.</h1>' in rv.data