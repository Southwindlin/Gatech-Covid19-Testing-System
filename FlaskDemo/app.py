import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import numpy as np
import hashlib

#when cannot instal flask_mysqldb:
#export PATH=$PATH:/usr/local/mysql/bin
#pip3 install flask-mysqldb


app = Flask(__name__)
app.secret_key = 'team 84 is the best team'

# Random login values for mySQL, this will need to be changed for your own machine
app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'chy190354890'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = '123123123'
app.config['MYSQL_DB'] = 'covidtest_fall2020'
# This code assumes you've already instantiated the DB

mysql = MySQL(app)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        if session['userPerms'] == 'Admin':
            return render_template('adminDashboard.html')
        elif session['userPerms'] == 'Student':
            #This is what I was kinda thinking, since the overall screen seemed a bit different from homeScreenStudent. 
            #We can talk about this later
            #return render_template('studentdashboard.html')
            return render_template('basicDashboard.html')
        elif session['userPerms'] == 'Tester':
            return "You are a tester"
        return None
    else:
        return render_template('loginprompt.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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
        select_statement = "SELECT * FROM USER WHERE username = %s AND MD5(%s) = user_password"
        result = cursor.execute(select_statement, (username, password))
        if result:
            session['user'] = username
            checkForPermissions()
            cursor.close()
            return redirect(url_for('dashboard'))
        cursor.close()
        return "Login Failed"

def checkForPermissions():
    cursor = mysql.connection.cursor()
    select_statement = "SELECT * FROM ADMINISTRATOR WHERE admin_username = %s"
    result = cursor.execute(select_statement, (session['user']))
    if result:
        session['userPerms'] = 'Admin'
        cursor.close()
        return
    select_statement = "SELECT * FROM STUDENT WHERE student_username = %s"
    result = cursor.execute(select_statement, (session['user']))
    if result:
        session['userPerms'] = 'Student'
        cursor.close()
        return
    select_statement = "SELECT * FROM LABTECH WHERE labtech_username = %s"
    result = cursor.execute(select_statement, (session['user']))
    if result:
        session['userPerms'] = 'LabTech'
        cursor.close()
        return
    select_statement = "SELECT * FROM SITETESTER WHERE sitetester_username = %s"
    result = cursor.execute(select_statement, (session['user']))
    if result:
        session['userPerms'] = 'Tester'
        cursor.close()
        return
    return

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

            return render_template('studentView.html', labels=labels, content=content)





    





















if __name__ == '__main__':
    app.run()