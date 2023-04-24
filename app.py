from flask import Flask, make_response, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt


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


@app.route('/restaurant/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurantid(restaurant_id):
    
        # Retrieve restaurant from database
        restauranttemp = restaurant.query.get(restaurant_id)
        
        # Render restaurant's HTML page
        return render_template('restaurant-page.html', restaurant=restauranttemp,num_reviews=Review.query.filter_by(restaurant_id=restaurant_id).count(),reviews=Review.query.filter_by(restaurant_id=restaurant_id).all())

@app.route('/signup-page', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        username = request.form['usname']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        entries = User.query.order_by(User.user_id.desc()).limit(10).all()
        print(entries)
        return redirect('/login-page')
    else:
        return render_template('signup-page.html')

@app.route('/login-page', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usname = request.form['usname']
        password = request.form['password']
        user = User.query.filter_by(username=usname).first()
        
        if (user and user.password==password):
            session['user_id'] = user.user_id
            session['logged_in']=True
            return redirect('/homepage')
        else:
            return render_template('login-page.html', error='Invalid email or password')
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
@app.route('/restaurants/<float:min_rating>')
def restaurants_by_rating(min_rating):
    # Call the find_restaurants_by_rating method to get a list of matching restaurants
    restaurants = find_restaurants_by_rating(min_rating)
    
    # Render the results in a template
    return render_template('restaurants.html', restaurants=restaurants)
@app.route('/restaurants-by-tags', methods=['GET'])
def restaurants_by_tags():
    # Retrieve tags from form
    tags = request.form['tags']
    
    # Split tags string into list of individual tags
    tag_list = tags.split(',')
    
    # Query the database for restaurants that match any of the tags
    restaurants = restaurant.query.filter(restaurant.tags.in_(tag_list)).all()
    
    # Render the results in a template
    return render_template('restaurants.html', restaurant=restaurants)
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
        return new_review

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
