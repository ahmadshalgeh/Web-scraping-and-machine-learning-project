from sklearn import tree,preprocessing
import mysql.connector

x = []   #input
y = []   #output

mydb = mysql.connector.connect(user='root',
                              password='your_password',
                              host='127.0.0.1',
                              database='database_name')


mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM cars")

myresult = mycursor.fetchall()
name = input('Please enter the name of the car in Persian : ')


for line in myresult:
    if name in line[0]:

        x.append(line[1:3])
        y.append(line[4])


clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

model = int(input('Please enter the car model :'))
mileage = int(input('Please enter the mileage of the car :'))
new_data = [[model, mileage]]
answer = clf.predict(new_data)
print(answer[0] + ' toman')
