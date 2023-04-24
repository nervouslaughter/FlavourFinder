import csv
with open('Restaurant_Reviews.tsv', newline='', encoding='utf-8') as csvfile:
    
    reader = csv.reader(csvfile, delimiter='\t')
    next(reader) 

    data= next(reader)
    print(data)