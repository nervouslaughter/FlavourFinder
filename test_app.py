import app

def test_home():
    with app.test_client() as client:
        # Simulate a user who is not logged in
        response = client.get('/home')
        assert response.status_code == 200  # Check that the response is successful
        with open('homepage.html', 'rb') as f:
            expected_html = f.read()
        assert expected_html == response.data  # Check that the response contains the expected HTML

        # Simulate a logged-in user
        with client.session_transaction() as session:
            session['user_id'] = 1
        response = client.get('/home')
        assert response.status_code == 200  # Check that the response is successful
        with open('homepage.html', 'rb') as f:
            expected_html = f.read()
        assert expected_html == response.data  # Check that the response contains the expected HTML

# def test_restaurant(client, app, db):
#     # Add a new restaurant to the database
#     restaurant = Restaurant(name='Test Restaurant')
#     db.session.add(restaurant)
#     db.session.commit()

#     # Send a POST request to add a review to the restaurant
#     response = client.post(f'/restaurant/{restaurant.id}', data={
#         'rating': 5,
#         'comment': 'Great food!'
#     })
#     assert response.status_code == 302  # Check that the response is a redirect

#     # Retrieve the updated restaurant from the database
#     updated_restaurant = Restaurant.query.get(restaurant.id)

#     # Check that the restaurant's rating has been updated
#     assert updated_restaurant.rating == 5.0

#     # Send a GET request to retrieve the restaurant's page
#     response = client.get(f'/restaurant/{restaurant.id}')
#     assert response.status_code == 200

#     # Check that the restaurant's name is displayed on the page
#     assert b'Test Restaurant' in response.data

#     # Check that the review has been added to the page
#     assert b'Great food!' in response.data

# def test_signup(client, app, db):
#     # Send a GET request to retrieve the signup page
#     response = client.get('/signup-page')
#     assert response.status_code == 200

#     # Send a POST request to create a new user
#     data = {
#         'usname': 'testuser',
#         'email': 'testuser@example.com',
#         'password': 'testpassword'
#     }
#     response = client.post('/signup-page', data=data)
#     assert response.status_code == 302  # Check that the response is a redirect

#     # Check that the user has been added to the database
#     user = User.query.filter_by(username='testuser').first()
#     assert user is not None

#     # Check that the user's information is correct
#     assert user.username == 'testuser'
#     assert user.email == 'testuser@example.com'

#     # Check that the user's password is hashed
#     assert user.password != 'testpassword'

#     # Check that the user is logged in after signing up
#     with client.session_transaction() as session:
#         assert session['user_id'] == user.user_id

# def test_login():
#     with app.test_request_context('/login-page', method='POST', data={
#         'usname': 'testuser',
#         'password': 'testpassword'
#     }):
#         response = login()
#         assert response.status_code == 302  # Check that the response is a redirect
#         assert session['user_id'] == 1  # Check that the user is logged in

#     with app.test_request_context('/login-page', method='POST', data={
#         'usname': 'testuser',
#         'password': 'wrongpassword'
#     }):
#         response = login()
#         assert 'Invalid email or password' in response.data.decode('utf-8')  # Check that the error message is displayed

#     with app.test_request_context('/login-page', method='GET'):
#         response = login()
#         assert response.status_code == 200  # Check that the login page is rendered

# def test_logout():
#     with app.test_client() as client:
#         # Login a user
#         with client.session_transaction() as session:
#             session['user_id'] = 1

#         # Logout the user
#         response = client.get('/logout')
#         assert response.status_code == 302  # Check that the response is a redirect
#         assert 'user_id' not in session  # Check that the user is logged out
