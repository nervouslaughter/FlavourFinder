import mysql.connector
import csv
import random


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="flavourfinder"
)


cursor = mydb.cursor()

cursor.execute("SELECT restaurant_id FROM restaurants")
restaurant_ids = [id[0] for id in cursor.fetchall()]

cursor.execute("SELECT user_id FROM users")
user_ids = [id[0] for id in cursor.fetchall()]

with open('Restaurant_Reviews.tsv', newline='', encoding='utf-8') as csvfile:
    
    reader = csv.reader(csvfile, delimiter='\t')
    next(reader) 
    num_reviews = sum(1 for row in reader) - 5
    print(num_reviews)
    csvfile.seek(0)

    
    x =0
    for restaurant_id in restaurant_ids:
        if x%500==0:
            print(x)
        x+=1
        reviews_assigned = random.randint(3,4)
        for i in range(reviews_assigned):
           
            user_id = random.choice(user_ids)
            review_data = next(reader)

            if reader.line_num%(num_reviews + 1) ==0:
                    csvfile.seek(0)
                    next(reader)
                    review_data = next(reader)

            print(reader.line_num)
                    
            dummy_rating=0
            
            if (review_data[1]=='Liked'):
                 dummy_rating = 4
            
            elif (int(review_data[1])>0):
                dummy_rating = 5
            
                 
                 
            sql = "INSERT INTO reviews (user_id, restaurant_id, rating, comment) VALUES (%s, %s, %s, %s)"
            val = (user_id, restaurant_id, dummy_rating, review_data[0])
            cursor.execute(sql, val)

           
    mydb.commit()
