import pytest
from app import app
import io

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

def test_home():
    with app.test_client() as client:
        # Simulate a user who is not logged in
        response = client.get('/homepage')
        assert response.status_code == 200  # Check that the response is successful

        # Simulate a logged-in user
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.get('/homepage')
        assert response.status_code == 200 
        # print(response.data.decode())
        # Check that the response is successful


def test_signup_login():
        with app.test_client() as client:
            response = client.post('/signup-page', method ='POST', data = {
                'usname' : 'hqerty',
                'email' : 'COPsucks@gmail.com',
                'password' : 'COPsucks',
            })
            assert response.status_code == 400
            # print(response.data.decode())
            # test check for signup. 
            # this check whether this signup has been successfully been added.
            response = client.post('/login-page', method='POST', data={
                'usname': 'cooldude4',
                'password': 'cooldudefour',
            })
            assert response.status_code == 302
            # print(response.data.decode())

def test_restaurantid() :
    with app.test_client() as client : 
            response = client.get('/restaurant/100', method='GET')
            assert response.status_code == 200
            # print(response.data.decode())


# def test_addimage():
#     with app.test_client() as client : 
#         response = client.post('/addimage', method='POST', data = {
#             'restaurant_id' : '4',
#             'image' : '10-downing-street-bhopal.jpg'
#         })
#         assert response.status_code == 302


def test_logout():
    with app.test_client() as client:
        response = client.get('/logout')
        assert response.status_code == 302
        # print(response.data.decode())

def test_aboutus() :
    with app.test_client() as client:
        response = client.get('/about-us')  
        assert response.status_code == 200 
        # print(response.data.decode())

def test_categories():
    with app.test_client() as client:
        response = client.get('/categories')
        assert response.status_code == 200
        # print(response.data.decode())



def test_restaurants_by_tags():
    with app.test_client() as client:
            response = client.get('restaurant-by-tags', method='GET', data = {
                'tags' : 'Pizza, Salad',
            })
            # assert response.status_code == 200
            print(response.data.decode())

def test_reviewwrite() :
    with app.test_client() as client:
        response = client.post('/restaurant/1/reviewwrite', method = 'POST', data = {
            'rating' : '4',
            'comment' : 'this restaurant sucks big time'
        })
        assert response.status_code == 302
        print(response.data.decode())

def test_profile():
    with app.test_client() as client:
        response = client.post('/login-page', method='POST', data={
            'usname': 'cooldude4',
            'password': 'cooldudefour',
        })
        # data = app.session['user_id']
        # print(data)
        response = client.get('/profile-page')
        assert response.status_code == 200
        # print(response.data.decode())


def test_increaseupvotes() :
    with app.test_client() as client:
        response = client.post('/login-page', method='POST', data={
            'usname': 'cooldude4',
            'password': 'cooldudefour',
        })
        assert response.status_code == 302
        response = client.post('/restaurant/100/1', method='POST')
        # response = client.post('/restaurant/1/1', method='POST')
        response.status_code == 302

def test_search() :
    with app.test_client() as client:
        response = client.post('/search-page', method='POST', data = {
            'query'  : 'Italian',
        })
        assert response.status_code == 200

def test_translatereview():
    with app.test_client() as client : 
        response = client.post('/translate', method='POST')
        assert response.status_code == 302
        response = client.post('/login-page', method='POST', data={
            'usname': 'cooldude4',
            'password': 'cooldudefour',
        })
        assert response.status_code == 302
        response = client.post('/translate', method='POST')
        response = client.post('/translate', method='POST',data={'review_id': 1})

        # clarify review_id


def test_search():
    with app.test_client() as client : 
        response = client.post('/search-page', method='POST', data = {
            'query' : '#Name of restaurant'
        })
        assert response.status_code == 200

def test_searchcat():
    with app.test_client() as client :
        response = client.get('/search-page/fast', method='GET')
        assert response.status_code == 200