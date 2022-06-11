import persian
import requests
from bs4 import BeautifulSoup
import mysql.connector


mydb = mysql.connector.connect(user='root',
                              password='your_password',
                              host='127.0.0.1',
                              database='database_name')

#x = persian.convert_fa_numbers("۱۳۷۱۳۷۱۱۳۷۱۱")
#print(x)
mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE car")
#mycursor.execute("CREATE TABLE cars (name_car VARCHAR(255), model VARCHAR(255), Mileage VARCHAR(255), city VARCHAR(255), Price VARCHAR(255))")

for i in range(1,3):
    r = requests.get('https://mashinbank.com/%D8%AE%D8%B1%DB%8C%D8%AF-%D8%AE%D9%88%D8%AF%D8%B1%D9%88?page=' + str(i) +'&kms=1000000')
    soup = BeautifulSoup(r.text, 'html.parser')

    price_list = []
    name_list = []
    model_list = []
    city_list = []
    mileage_list = []

    name = soup.find_all('div',attrs={'class': 'cars-title'})
    price = soup.find_all('div',attrs={'class': 'cars-price'})
    model_city = soup.find_all('div',attrs={'class': 'cars-title cars-year'})
    mileage = soup.find_all('div',attrs={'class': 'cars-kms'})


    #-----------------------------------
    for i in price:
        x = i.text.split()
        y = x[0].replace(',', '')
        price_list.append(persian.convert_fa_numbers(y))

        #print(persian.convert_fa_numbers(x[0]))
    #print(price_list)

    #--------------------------------------------
    for i in range(0, 30, 2):
        name_list.append(name[i].text)
    #print(name_list)

    #----------------------------------------------
    for i in model_city:
        x = i.text.split()
        model_list.append(persian.convert_fa_numbers(x[0]))
        city_list.append(x[2])

    #print(model_list)
    #print(city_list)

    for i in mileage:
        x = i.text.split()
        y = x[0].replace(',', '')
        mileage_list.append(persian.convert_fa_numbers(y))
    #print(mileage_list)

    sql = "INSERT INTO cars (name_car, model , Mileage , city , Price ) VALUES (%s, %s, %s, %s, %s)"

    for i in range(15):
        val_sql = (name_list[i], model_list[i], mileage_list[i], city_list[i], price_list[i])
        mycursor.execute(sql, val_sql)
        #print(val_sql)
        mydb.commit()

    mycursor.execute("SELECT * FROM cars")

    myresult = mycursor.fetchall()
    average = 0
    count = 0
    for line in myresult:
        if line[4] != 'توافقی':
            count += 1
            average = average + float(line[4])
    average = str(int(average/count))

    word = 'توافقی'
    for line in myresult:
        sql = "UPDATE cars SET price = %s WHERE price = %s"
        val = (average, 'توافقی')
        mycursor.execute(sql, val)
        mydb.commit()

mydb.close()

