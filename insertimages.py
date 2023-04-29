import random
import mysql.connector

# establish connection to MySQL database
cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='flavourfinder')
cursor = cnx.cursor()

# define list of links
links = ["https://i.imgur.com/8leLcsF.jpg","https://i.imgur.com/Evpph5P.jpg" ,"https://i.imgur.com/BUQQAFy.jpg" ,"https://i.imgur.com/ODMpZzJ.jpg" ,"https://i.imgur.com/pSnEbJK.jpg" ,"https://i.imgur.com/PhK2vhk.jpg" 
,"https://i.imgur.com/AR524OS.jpg","https://i.imgur.com/QNbePGe.jpg","https://i.imgur.com/mFDZReN.jpg"]

# query to get list of valid restaurant_ids
get_restaurant_ids_query = """SELECT review_id FROM reviews;"""

# execute query to get list of valid restaurant_ids
cursor.execute(get_restaurant_ids_query)

restaurant_ids = cursor.fetchall()

# loop through each valid restaurant_id
for restaurant_id in restaurant_ids:
    # randomly select 5 links from the list of links
    x = random.randint(1,3)
    random_links = random.sample(links, x)
    # insert each link into the image table with the current restaurant_id
    
    for link in random_links:
        insert_query = """ INSERT INTO review_images (review_id, image_url) VALUES (%s, %s); """
        cursor.execute(insert_query, (restaurant_id[0], link))
        cnx.commit()

# close cursor and database connection
cursor.close()
cnx.close()



