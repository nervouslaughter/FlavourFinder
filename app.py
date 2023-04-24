from flask import Flask, make_response, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import base64
import json
import requests
from werkzeug import *
from math import sin, cos, sqrt, atan2, radians


from base64 import b64encode


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flavourfinder'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy()
bcrypt = Bcrypt(app)
db.init_app(app)
class User(UserMixin, db.Model):
    __tablename__='users'
    username = db.Column('username',db.String(255), unique=True, nullable=False)
    email = db.Column('email',db.String(255), nullable=False)
    password = db.Column('password',db.String(255), nullable=False)
    user_id = db.Column('user_id',db.Integer, primary_key=True,autoincrement=True)

class restaurant(db.Model) :
    __tablename__='restaurants'
    restaurant_id = db.Column('restaurant_id',db.Integer, primary_key = True)
    name = db.Column('name',db.String(255))
    category = db.Column('category',db.String(255))
    locality = db.Column('locality',db.String(255))
    address = db.Column('address',db.Text())
    tags = db.Column('tags',db.String(255))
    rating = db.Column('rating',db.Float())
    website = db.Column('website',db.String())
    contact_number = db.Column('contact_number',db.String())
    latitude = db.Column('latitude',db.Float())
    longitude = db.Column('longitude',db.Float())
    pricing_for_two = db.Column('pricing_for_two',db.Integer())

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column('review_id',db.Integer, primary_key=True,autoincrement=True,default=0)
    restaurant_id = db.Column('restaurant_id',db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    rating = db.Column('rating',db.Integer, nullable=False)
    comment = db.Column('comment',db.Text(), nullable=False)
    upvote_count = db.Column('upvote_count',db.Integer, default=0,nullable=True)
class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    image_url=db.Column(db.String(255), nullable=False)
@app.route('/search-page',methods=['POST','GET'])
def search():
    if (request.method=='GET'):
        return render_template('search-page.html')
    query_string=request.form.get('query',False)
    if (query_string == False):
        return make_response('Query string cannot be empty', 400)
    items = [x.name for x in restaurant.query.filter(restaurant.name.like('%'+query_string+'%')).limit(5).all()]
    return render_template("search-page.html",restaurants=items)
def finddistance(lat1,lon1,lat2,lon2):
    R=6370.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
@app.route('/find_nearest', methods=['GET'])
def find_nearest():
    target_lat = request.form.get('lat',False)
    if (target_lat == False):
        return make_response('Latitude cannot be empty', 400)
    target_lon = request.form.get('lon')
    if (target_lon == False):
        return make_response('Longitude cannot be empty', 400)
    limit = request.form.get('limit', 5, type=int)
    if (limit == False):
        return make_response('Limit cannot be empty', 400)
    query = db.session.query(restaurant).order_by(
        db.func.sqrt(
            db.func.pow(restaurant.latitude - target_lat, 2) +
            db.func.pow(restaurant.longitude - target_lon, 2)
        )
    ).limit(limit)
    results = query.all()
    nearest = []
    for row in results:
        distance = finddistance(target_lat, target_lon, row.latitude, row.longitude)
        nearest.append((row, distance))
    nearest = sorted(nearest, key=lambda x: x[1])
    return {'results': [r[0] for r in nearest]}





@app.route('/restaurant/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurantid(restaurant_id):
    
        # Retrieve restaurant from database
        restauranttemp = restaurant.query.get(restaurant_id)
        if (restauranttemp == None):
            return make_response('Restaurant not found', 404)
        # Render restaurant's HTML page
        print(Image.query.filter_by(restaurant_id=restaurant_id).all())
        return render_template('restaurant-page.html', restaurant=restauranttemp,num_reviews=Review.query.filter_by(restaurant_id=restaurant_id).count(),reviews=Review.query.filter_by(restaurant_id=restaurant_id).all(),images=Image.query.filter_by(restaurant_id=restaurant_id).all())

@app.route('/signup-page', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        username = request.form.get('usname',False)
        if (username == False):
            return make_response(render_template('signup-page.html', error='Username cannot be empty'), 400)
        email = request.form.get('email',False)
        if (email == False):
            return make_response(render_template('signup-page.html', error='Email cannot be empty'), 400)
        password = request.form.get('password',False)
        if (password == False):
            return make_response(render_template('signup-page.html', error='Password cannot be empty'), 400)
        if (User.query.filter_by(username=username).first()):
            return make_response(render_template('signup-page.html', error='Username already exists'), 400)
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        session['logged_in'] = True
        return redirect('/home-page')
    else:
        return render_template('signup-page.html')
@app.route('/addimage', methods=[ 'POST'])
def addimage():
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id',False)
        if (restaurant_id==False):
            return make_response('Restaurant not found', 404)
        image = request.files.get('image',False)
        if (image==False):
            return make_response('Image not found', 404)
        headers = {"Authorization": "Client-ID db886f20c5da9f2"}

        api_key = 'e86eff8c1b826b265c544c9e383933ca1375c743'

        url = "https://api.imgur.com/3/upload.json"

        j1=requests.post(url, headers=headers, files={'image':image})
        data = json.loads(j1.text)['data']
        imagelink = data['link']
        
        image = Image(restaurant_id=restaurant_id, image_url=imagelink)
        db.session.add(image)
        db.session.commit()
        return redirect('/restaurant/'+restaurant_id)
    else:
        return render_template('addimage.html')


@app.route('/login-page', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usname = request.form.get('usname',False)
        if (usname == False):
            return make_response(render_template('login-page.html', error='Username cannot be empty'), 400)
        
        password = request.form.get('password',False)
        if (password == False):
            return make_response(render_template('login-page.html', error='Password cannot be empty'), 400)
        
        user = User.query.filter_by(username=usname).first()
        
        if (user and user.password==password):
            session['user_id'] = user.user_id
            session['logged_in']=True
            return redirect('/homepage')
        else:
            return make_response(render_template('login-page.html', error='Invalid email or password'), 401)
    if ('logged_in' in session and session['logged_in']==True):
        return redirect('/homepage')
    return render_template('login-page.html')

@app.route('/logout')
def logout():
    session['logged_in']=False
    session['user_id']=None
    return redirect('/homepage')
@app.route('/about-us')
def aboutus():
    return render_template('about-us.html')
@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/homepage')
def home():
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        return (render_template('homepage.html'))
    else:
        return render_template('homepage.html')
def find_restaurants_by_rating(min_rating):
    # Query the database for all restaurants with a rating greater than or equal to min_rating
    restaurants = restaurant.query.filter(restaurant.rating >= min_rating).all()
    
    # Return the list of matching restaurants
    return restaurants
@app.route('/restaurants/min/<float:min_rating>')
def restaurants_by_rating(min_rating):
    # Call the find_restaurants_by_rating method to get a list of matching restaurants
    restaurants = find_restaurants_by_rating(min_rating)
    
    # Render the results in a template
    return render_template('search-page.html', restaurants=restaurants)
@app.route('/restaurants-by-tags', methods=['GET'])
def restaurants_by_tags():
    # Retrieve tags from form
    tags = request.form.get('tags',False)
    
    if (tags==False):
        return make_response('Tags cannot be empty', 400)
    
    
    # Split tags string into list of individual tags
    tag_list = tags.split(', ')
    print(tag_list)
    
    # Query the database for restaurants that match any of the tags
    restaurants = restaurant.query.filter(restaurant.tags.in_(tag_list)).all()
    
    # Render the results in a template
    return [x.name for x in restaurants]
def get_restaurant_by_id(id):
    # Query the database for a restaurant with a matching ID
    restauranttemp = restaurant.query.get(id)
    ##
    
    # Return the restaurant
    return restauranttemp


def get_user_profile(user_id=None):
    
    user = User.query.filter_by(user_id=user_id)
    if not user:
        return None
    user=user.first()

    

    profile = {
        'username': user.username,
        'email': user.email,
        'user_id': user.user_id,
    }

    return profile
@app.route('/restaurant/<int:restaurant_id>/reviewwrite', methods=['POST'])
def reviewwrite(restaurant_id):
        rating = request.form['rating']
        comment = request.form['comment']
        
        # Create new review object
        new_review = Review(
            restaurant_id=restaurant_id,
            rating=rating,
            comment=comment
        )
        
        # Add review to database
        db.session.add(new_review)
        db.session.commit()
        
        # Update restaurant rating
        restauranttemp = restaurant.query.get(restaurant_id)
        num_reviews = len(restauranttemp.reviews)
        total_rating = sum([review.rating for review in restauranttemp.reviews])
        restauranttemp.rating = total_rating / num_reviews
        db.session.commit()
        
        # Redirect to restaurant's HTML page
        return redirect('/restaurant/restaurant_id')

@app.route('/profile-page')
def profile():
    return render_template('profile-page.html',user=get_user_profile(session['user_id']))
# @app.route('/profile/<int:user_id>')
# def profileuser():
#     user = User.query.get(user_id=user_id)
#     if (user)
#     return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
