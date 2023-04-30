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

from google.cloud import translate_v2 as translate

# Initialize the client
def translate_review(rev, target_language = "en"):
    translate_client = translate.Client.from_service_account_json('credents.json')
    text = rev
    result = translate_client.detect_language(text)
    source_lang = result["language"]
    if (source_lang == "en"):
        return rev
    translation = translate_client.translate(text, source_language=source_lang, target_language=target_language)
    return (translation['translatedText'])



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
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    review_id = db.Column('review_id',db.Integer, primary_key=True,autoincrement=True,default=0)
    restaurant_id = db.Column('restaurant_id',db.Integer,db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    rating = db.Column('rating',db.Integer, nullable=False)
    comment = db.Column('comment',db.Text(), nullable=False)
    upvote_count = db.Column('upvote_count',db.Integer, default=0)
class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    image_url=db.Column(db.String(255))
class review_images(db.Model):
    __tablename__ = 'review_images'
    image_id=db.Column(db.Integer, db.ForeignKey('images.image_id'), primary_key=True)
    review_id=db.Column(db.Integer, db.ForeignKey('reviews.review_id'), primary_key=True)
    image_url=db.Column(db.String(255))
class reviewtouser(db.Model):
    __tablename__ = 'reviewstouser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column(db.Integer,db.ForeignKey('reviews.review_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'),default=0)
@app.route('/translate',methods=['POST'])
def translatereview():
    if (not('logged_in' in session) or  session['logged_in']==False):
        return redirect('/login-page')
    print(session['user_id'])
    review_id=request.form.get('review_id',False)
    if (review_id==False or review_id==""):
        return make_response('Review ID cannot be empty', 400)
    restaurant_id=Review.query.filter_by(review_id=review_id).first().restaurant_id
    review = Review.query.get(review_id)
    newtext =translate_review(review.comment)
    print("HERE")
    print(session['user_id'])

    review.comment = newtext
    db.session.commit()
    return redirect('/restaurant/'+str(restaurant_id))
@app.route('/search-page',methods=['GET','POST'])
def search():
    
    query_string=request.form.get('query',"By Location")
    print(request.form)
    
    if (query_string==""):
        query_string="by location"
    
    restaurants=restaurant.query.filter(restaurant.name.like('%'+query_string+'%')).limit(5).all()
    # restaurant1={
    #         'name':restaurants[0].name,
    #         # 'comment':reviews.first().comment,
    #         # 'id':reviews.first().review_id,
    #         'upvote_count':reviews.first().upvote_count,
    #         'restaurant':restaurant.query.filter_by(restaurant_id=reviews[0].restaurant_id).first(),
    #         'imagerest':Image.query.filter_by(restaurant_id=reviews[0].restaurant_id).first().image_url,

    #         'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews.first().review_id).all()]
            
    # }
    # review2={
    #         'name':User.query.get(reviews[1].user_id).username,
    #         'comment':reviews[1].comment,
    #         'id':reviews[1].review_id,
    #         'upvote_count':reviews[1].upvote_count,
    #         'restaurant':restaurant.query.filter_by(restaurant_id=reviews[1].restaurant_id).first(),
    #         'imagerest':Image.query.filter_by(restaurant_id=reviews[1].restaurant_id).first().image_url,

    #         'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews[1].review_id).all()]
            
    # }
    images=[]
    for r in restaurants:
        images=images+[Image.query.filter_by(restaurant_id=r.restaurant_id).first().image_url]
    
    

    return render_template("search-page.html",restaurants=restaurants,query=query_string,images=images)
@app.route('/search-page/<category>',methods=['GET'])
def searchcat(category):
    
    
    tag_list =[str(category)]
    print(tag_list)
    
    # Query the database for restaurants that match any of the tags
    restaurants2=restaurant.query.filter(restaurant.name.like('%'+category+'%')).limit(5).all()

    restaurants = restaurant.query.filter(restaurant.tags.like('%'+category+'%')).limit(5).all()
    
    
    # restaurant1={
    #         'name':restaurants[0].name,
    #         # 'comment':reviews.first().comment,
    #         # 'id':reviews.first().review_id,
    #         'upvote_count':reviews.first().upvote_count,
    #         'restaurant':restaurant.query.filter_by(restaurant_id=reviews[0].restaurant_id).first(),
    #         'imagerest':Image.query.filter_by(restaurant_id=reviews[0].restaurant_id).first().image_url,

    #         'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews.first().review_id).all()]
            
    # }
    # review2={
    #         'name':User.query.get(reviews[1].user_id).username,
    #         'comment':reviews[1].comment,
    #         'id':reviews[1].review_id,
    #         'upvote_count':reviews[1].upvote_count,
    #         'restaurant':restaurant.query.filter_by(restaurant_id=reviews[1].restaurant_id).first(),
    #         'imagerest':Image.query.filter_by(restaurant_id=reviews[1].restaurant_id).first().image_url,

    #         'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews[1].review_id).all()]
            
    # }

    if (len(restaurants)<2):
        restaurants=restaurants2
    
    images=[]
    for r in restaurants:
        images=images+[Image.query.filter_by(restaurant_id=r.restaurant_id).first().image_url]

    return render_template("search-page.html",restaurants=restaurants,query=category,images=images)

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
    return [x.name for x in query.all()]





@app.route('/restaurant/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurantid(restaurant_id):
    
        # Retrieve restaurant from database
        restauranttemp = restaurant.query.get(restaurant_id)
        if (restauranttemp == None):
            return make_response('Restaurant not found', 404)
        # Render restaurant's HTML page
        reviews=Review.query.filter_by(restaurant_id=restaurant_id).order_by(Review.upvote_count.desc())
        reviews2=Review.query.filter_by(restaurant_id=restaurant_id).order_by(Review.upvote_count.asc())

        reviewtop={
            'name':User.query.get(reviews.first().user_id).username,
            'comment':reviews.first().comment,
            'id':reviews.first().review_id,
            'upvote_count':reviews.first().upvote_count,
            'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews.first().review_id).all()]
            
        }
        
        print("HERE")
        print(reviewtop['images'])
        reviewbot={
            'name':User.query.get(reviews2.first().user_id).username,
            'comment':reviews2.first().comment,
            'upvote_count':reviews2.first().upvote_count,
            'id':reviews2.first().review_id,
            'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews.first().review_id).all()]

        }
        return render_template('restaurant-page.html', restaurant=restauranttemp,num_reviews=Review.query.filter_by(restaurant_id=restaurant_id).count(),reviewtop=reviewtop,reviewbot=reviewbot,images=[x.image_url for x in Image.query.filter_by(restaurant_id=restaurant_id).all()])

@app.route('/signup-page', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname=request.form.get('fname',False)
        if (firstname == False or firstname==""):
            return make_response(render_template('signup-page.html', error='First name cannot be empty'), 400)
        lastname=request.form.get('lname',False)
        if (lastname == False or lastname==""):
            return make_response(render_template('signup-page.html', error='Last name cannot be empty'), 400)
        username = request.form.get('usname',False)
        if (username == False or username==""):
            return make_response(render_template('signup-page.html', error='Username cannot be empty'), 400)
        email = request.form.get('email',False)
        if (email == False or email==""):
            return make_response(render_template('signup-page.html', error='Email cannot be empty'), 400)
        password = request.form.get('password',False)
        if (password == False or password==""):
            return make_response(render_template('signup-page.html', error='Password cannot be empty'), 400)
        confpassword=request.form.get('confpassword',False)
        if (confpassword == False or confpassword==""):
            return make_response(render_template('signup-page.html', error='Confirm password cannot be empty'), 400)
        if (User.query.filter_by(username=username).first()):
            print("user exists")
            return make_response(render_template('signup-page.html', error='Username already exists'), 400)
        if (password!=confpassword):
            
            return make_response(render_template('signup-page.html', error='Passwords do not match'), 400)
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        session['logged_in'] = True
        session['loginlink']='/logout'
        session['logintext']='Logout'
        return redirect('/homepage')
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
        print(usname)
        if (usname == False or usname==""):
            return make_response(render_template('login-page.html', error='Username cannot be empty'), 400)
        
        password = request.form.get('password',False)
        print(password)
        if (password == False or password==""):
            return make_response(render_template('login-page.html', error='Password cannot be empty'), 400)
        
        user = User.query.filter_by(username=usname).first()
        
        if (user and user.password==password):
            session['user_id'] = user.user_id
            session['logged_in'] = True
            session['loginlink']='/logout'
            session['logintext']='Logout'
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
    session['loginlink']='/login-page'
    session['logintext']='Login'
    return redirect('/homepage')
@app.route('/about-us')
def aboutus():
    return render_template('about-us.html')
@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/homepage')
def home():
    if (not ('loggedin' in session) or not('user_id' in session)):
        session['loggedin']=False
        session['user_id']=None
        session['logintext']='Login'
        session['loginlink']='/login-page'
    reviews=Review.query.order_by(Review.upvote_count.desc())
    review1={
            'name':User.query.get(reviews.first().user_id).username,
            'comment':reviews.first().comment,
            'id':reviews.first().review_id,
            'upvote_count':reviews.first().upvote_count,
            'restaurant':restaurant.query.filter_by(restaurant_id=reviews[0].restaurant_id).first(),
            'imagerest':Image.query.filter_by(restaurant_id=reviews[0].restaurant_id).first().image_url,

            'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews.first().review_id).all()]
            
    }
    review2={
            'name':User.query.get(reviews[1].user_id).username,
            'comment':reviews[1].comment,
            'id':reviews[1].review_id,
            'upvote_count':reviews[1].upvote_count,
            'restaurant':restaurant.query.filter_by(restaurant_id=reviews[1].restaurant_id).first(),
            'imagerest':Image.query.filter_by(restaurant_id=reviews[1].restaurant_id).first().image_url,

            'images':[x.image_url for x in review_images.query.filter_by(review_id=reviews[1].review_id).all()]
            
    }

    if 'user_id' in session and session['user_id']!=None:
        return (render_template('homepage.html',loginlink='/logout',loginlinktext='LOGOUT',user=User.query.get(session['user_id']),review1=review1,review2=review2))
    else:
        return render_template('homepage.html',loginlink='/login-page',loginlinktext='LOGIN',review1=review1,review2=review2)


@app.route('/restaurant_by_tags', methods=['POST'])
def restaurants_by_tags():
    # Retrieve tags from form
    tags=request.form.get('tags',False)
    if (tags=="" or tags==False):
        return make_response('Tags cannot be empty', 400)
    
    
    # Split tags string into list of individual tags
    tag_list = tags.split(', ')

    print(tag_list)
    
    # Query the database for restaurants that match any of the tags
    restaurants = restaurant.query.filter(restaurant.tags.in_(tag_list)).limit(5).all()
    # if (len(restaurants)<2):
    #     return make_response('Not enough restaurants', 400)
    # image1=Image.query.filter_by(restaurant_id=restaurants[0].restaurant_id).first()
    # if (image1==None):
    #     return make_response('Not enough restaurants', 400)
    # image1=image1.image_url
    # image2=Image.query.filter_by(restaurant_id=restaurants[1].restaurant_id).first()
    # if (image2==None):
    #     return make_response('Not enough restaurants', 400)
    # image2=image2.image_url
    images=[]
    for r in restaurants:
        images=images+[Image.query.filter_by(restaurant_id=r.restaurant_id).first().image_url]

    return render_template("search-page.html",restaurants=restaurants,query=tags,images=images)
    
    # Render the results in a template
def get_restaurant_by_id(id):
    # Query the database for a restaurant with a matching ID
    restauranttemp = restaurant.query.get(id)
    ##
    
    # Return the restaurant
    return restauranttemp


def get_user_profile(user_id=None):
    
    user = User.query.filter_by(user_id=user_id)
    
    if not user.first():
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
        rating = request.form.get('rating',False)
        if (rating==False):
            return make_response('Rating cannot be empty', 400)
        comment = request.form.get('comment',False)
        if (comment==False):
            return make_response('Comment cannot be empty', 400)
        if (session['logged_in']==False):
            return redirect('/login-page')
        
        # Create new review object
        new_review = Review(
            user_id=session['user_id'],
            restaurant_id=restaurant_id,
            rating=rating,
            comment=comment,
            upvote_count=0,
            
            
        )
        
        # Add review to database
        db.session.add(new_review)
        
        # Update restaurant rating
        db.session.commit()
        
        # Redirect to restaurant's HTML page
        return redirect('/restaurant/restaurant_id')
@app.route('/upvote',methods=['POST'])
def increaseupvotes():
    if (session['logged_in']==False):
        
        return redirect('/login-page')
    print(session['user_id'])
    review_id=request.form.get('review_id',False)
    if (review_id==False or review_id==""):
        return make_response('Review ID cannot be empty', 400)
    restaurant_id=Review.query.filter_by(review_id=review_id).first().restaurant_id
    if (reviewtouser.query.filter_by(review_id=review_id,user_id=session['user_id']).first()):
        
        return redirect('/restaurant/'+str(restaurant_id))
    else:
        print("HERE")
        print(session['user_id'])
        newreviewtouser=reviewtouser(review_id=review_id,user_id=session['user_id'])
        review = Review.query.get(review_id)
        if (review.upvote_count==None):
            review.upvote_count=0
        review.upvote_count += 1

        db.session.add(newreviewtouser)
        db.session.commit()
        return redirect('/restaurant/'+str(restaurant_id))

@app.route('/profile-page')
def profile():
    if (get_user_profile(session['user_id'])==None):
        return redirect('/login-page')
    return render_template('profile-page.html',user=get_user_profile(session['user_id']))
# @app.route('/profile/<int:user_id>')
# def profileuser():
#     user = User.query.get(user_id=user_id)
#     if (user)
#     return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True,host='')
