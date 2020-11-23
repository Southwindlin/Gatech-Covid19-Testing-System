import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import numpy as np
import hashlib

#when cannot instal flask_mysqldb:
#export PATH=$PATH:/usr/local/mysql/bin
#pip3 install flask-mysqldb


app = Flask(__name__)

# Random login values for mySQL, this will need to be changed for your own machine
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chy190354890'
app.config['MYSQL_DB'] = 'covidtest_fall2020'
# This code assumes you've already instantiated the DB

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('form.html')


#change this name to registForm for better understanding
@app.route('/registForm')
def registForm():
    return render_template('regform.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.form['Username']
        password = request.form['Password']
        try:
            fname = request.form['FName']
            # cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
            # mysql.connection.commit()
            cursor.close()
            return f"Done!!"
        except:
            select_statement = "SELECT * FROM USER WHERE username = %s AND MD5(%s) = user_password"
            result = cursor.execute(select_statement, (username, password))
            if result:
                return "Login Successful"
            return "Login Failed"


@app.route('/registuser',methods=['GET','POST'])
def getRegistRequest():
    if request.method == 'GET':
        return "Please register through the register form"
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        #SQL command


        userType = request.form.get('Type')
        userName = request.form.get('Username')
        email = request.form.get('Email')
        fName = request.form.get('FName')
        lName = request.form.get('LName')
        passWord = request.form.get('Password')
        confirmPass = request.form.get('ConfirmPwd')



        #see if the password match
        if confirmPass != passWord:
            return "Sorry, your passwords don't match"

        #no need to change the password to hashcode here since it's done in the mysql procedure

        #treatment according to the usertype
        if userType == 'admin':
            return 'erro: Sorry, Admin cannot register through here'
        elif userType == 'student':
            houseType = request.form.get('HouseType')
            location = request.form.get('Location')

            try:
                cursor.callproc("register_student",[userName,email,fName,lName,location,houseType,passWord])
            except pymysql.IntegrityError or KeyError as e:
                return "unable to register"+str(e)
            else:
                mysql.connection.commit()
                return "You have successfully registered"
        elif userType == 'employee':
            employee = request.form.getlist('employType')
            phone = request.form.get('Phone')
            if len(employee) == 2:
                lab = True
                tester = True
                try:
                    cursor.callproc("register_employee",[userName,email,fName,lName,phone,lab,tester,passWord])
                except pymysql.IntegrityError or KeyError as e:
                    return "unable to register" + str(e)
                else:
                    mysql.connection.commit()
                    return "You have successfully registered"
            elif len(employee) == 1:
                job = employee[0]
                if job == "labTech":
                    try:
                        cursor.callproc("register_employee",
                                        [userName, email, fName, lName, phone, True, False, passWord])
                    except pymysql.IntegrityError or KeyError as e:
                        return "unable to register" + str(e)
                    else:
                        mysql.connection.commit()
                        return "You have successfully registered"
                elif job == "siteTester":
                    try:
                        cursor.callproc("register_employee",
                                        [userName, email, fName, lName, phone, False, True, passWord])
                    except pymysql.IntegrityError or KeyError as e:
                        return "unable to register" + str(e)
                    else:
                        mysql.connection.commit()
                        return "You have successfully registered"


@app.route('/studentView',methods=['GET','POST'])
def studentView():
    if request.method == 'GET':
        return render_template('studentView.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()

        #Will change the way of getting username after the front end is done
        userName = request.form.get('Username')
        status = request.form.get('Status')
        startDate = request.form.get('TimeStart')
        endDate = request.form.get('TimeEnd')

        try:
            result = cursor.callproc("student_view_results",[userName, status, startDate,endDate])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            #print the view to the html

            # select from the student_view_results_result
            sql = "select * from student_view_results_result"
            cursor.execute(sql)
            mysql.connection.commit()
            content = cursor.fetchall()

            # get the field name
            sql = "SHOW FIELDS FROM student_view_results_result"
            cursor.execute(sql)
            labels = cursor.fetchall()
            mysql.connection.commit()
            labels = [l[0] for l in labels]

            #visualization template source:
            #https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('studentView.html', labels=labels, content=content)





    





















if __name__ == '__main__':
    app.run()