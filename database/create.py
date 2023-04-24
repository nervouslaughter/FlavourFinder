import csv
import mysql.connector


with open('Bangalore_Restaurants.csv', newline='', encoding='utf-8') as csvfile:


    data = csv.DictReader(csvfile)


    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='flavourfinder'
    )

    
    cursor = db.cursor()

   
    for row in data:
        name = row['Restaurant_Name']
        category = row['Category']
        price = row['Pricing_for_2']
        locality = row['Locality']
        rating = 4.5
        website = row['Website']
        address = row['Address']
        phone = row['Phone_No']
        lat = row['Latitude']
        lng = row['Longitude']
        tags = row['Category']

        
        query = "INSERT INTO restaurants (name, category, pricing_for_two, locality, rating, website, address, contact_number, latitude, longitude, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, category, price, locality, rating, website, address, phone, lat, lng, tags)

       
        cursor.execute(query, values)


    db.commit()

 
    cursor.close()
    db.close()

