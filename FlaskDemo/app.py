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

app.config['MYSQL_HOST'] = 'localhost'

#Hongyu's configs, comment these back in lol
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'chy190354890'

#zilong's configs, comment these out
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = '123123123'
app.config['MYSQL_DB'] = 'covidtest_fall2020'
# This code assumes you've already instantiated the DB

mysql = MySQL(app)

# -------------------------- Platform Functions -------------------------

@app.route('/dashboard')
def dashboard():
    #First checks to see if there's someone logged in
    if 'user' in session:
        #Depending on their permissions, they get a different screen
        if session['userPerms'] == 'Admin':
            return render_template('adminDashboard.html')
        elif session['userPerms'] == 'Student':
            #Not sure if this should be homeScreenStudent, left this here as a default
            return render_template('basicDashboard.html')
        elif session['userPerms'] == 'Tester':
            return "You are a tester"
        return None
    #If not logged in, pushes the user to the index page
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    #All this does is clear the session information, meaning that the app no longer knows user or user-perms
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

#This is poorly named, but this is the login form
@app.route('/form')
def form():
    return render_template('form.html')

#change this name to registForm for better understanding
@app.route('/registForm')
def registForm():
    return render_template('regform.html')

#a very basic screen collection for test
@app.route('/EachScreen')
def eachScreen():
    return render_template('EachScreen.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect(url_for('form'))

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.form['Username']
        password = request.form['Password']
        select_statement = "SELECT * FROM USER WHERE username = %s AND MD5(%s) = user_password"
        result = cursor.execute(select_statement, (username, password))
        #If it finds the user credentials in the DB, it then seeks to update the session accordingly
        if result:
            session['user'] = username
            checkForPermissions()
            cursor.close()
            return redirect(url_for('dashboard'))
        cursor.close()
        return "Login Failed"

def checkForPermissions():
    #These SQL statements check to see which class of user is logged in, and updates the session information accordingly
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

# -------------------------- All Users Experience -----------------------

@app.route('/dailyresults')
def dailyresults():
    cursor = mysql.connection.cursor()
    try:
        result = cursor.callproc("daily_results")
    except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
    else:
        sql = "select * from daily_results_result"
        cursor.execute(sql)
        mysql.connection.commit()
        content = cursor.fetchall()

        # get the field name
        sql = "SHOW FIELDS FROM daily_results_result"
        cursor.execute(sql)
        labels = cursor.fetchall()
        mysql.connection.commit()
        labels = [l[0] for l in labels]

        return render_template('dailyresults.html', labels=labels, content=content)


# -------------------------- Student Specific Experience ----------------

@app.route('/studentView',methods=['GET','POST'])
def studentView():
    if request.method == 'GET':
        return render_template('studentView.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()

        #Will change the way of getting username after the front end is done
        userName = request.form.get('Username')
        status = request.form.get('Status')
        startDate = None if request.form.get('TimeStart')  == '' else request.form.get('TimeStart')
        endDate = None if request.form.get('TimeEnd') == '' else request.form.get('TimeEnd')


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
            labels = ['Test ID#','Timeslot Date','Date Processed','Pool Status','Status']

            #visualization template source:
            #https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('studentView.html', labels=labels, content=content)

# -------------------------- Tester Experience -------------------------- 

# -------------------------- LabTech Experience -------------------------

# -------------------------- Admin User Experience ----------------------

@app.route('/resassigntester')
def reassigntester():
    if 'user' not in session or session['userPerms'] != 'Admin':
        redirect(url_for('index'))
    

@app.route('/createAppointment',methods=['GET','POST'])
def createAppointment():
    if request.method == 'GET':
        return render_template('createAppointment.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        siteName = request.form.get('siteName')
        date = request.form.get('date')
        time = request.form.get('time')


        try:
            cursor.callproc("create_appointment",[siteName,date,time])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to create appointment beacuse "+str(e)
        else:
            mysql.connection.commit()
            return "create appointment succesfully"


@app.route('/viewAppointment',methods=['GET','POST'])
def viewAppointment():
    if request.method =='GET':
        return render_template('viewAppointment.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        siteName = request.form.get('siteName')
        startDate = None if request.form.get('DateStart') == '' else request.form.get('DateStart')
        endDate = None if request.form.get('DateEnd') == '' else request.form.get('DateStart')
        startTime = None if request.form.get('TimeStart') == '' else request.form.get('TimeStart')
        endTime = None if request.form.get('TimeEnd') == '' else request.form.get('TimeEnd')
        avail = request.form.get('Availability')

        if avail == 'booked':
            avail = 0
        elif avail == 'available':
            avail = 1
        elif avail == 'all':
            avail = None

        try:
            cursor.callproc("view_appointments",[siteName,startDate,endDate,startTime,endTime,avail])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            #print the view to the html

            # select from the student_view_results_result
            sql = "select * from view_appointments_result"
            cursor.execute(sql)
            mysql.connection.commit()
            content = cursor.fetchall()

            # get the field name
            sql = "SHOW FIELDS FROM view_appointments_result"
            cursor.execute(sql)
            mysql.connection.commit()
            labels = ['Date','Time','test Site','Location','User']

            #visualization template source:
            #https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('viewAppointment.html', labels=labels, content=content)




@app.route('/viewTester',methods=['GET'])
def viewTester():

    cursor = mysql.connection.cursor()

    try:
        cursor.callproc("view_testers")
    except pymysql.IntegrityError or KeyError as e:
        return "unable to view because " + str(e)
    else:
        #print the view to the html


        # select from the student_view_results_result
        sql = "select * from view_testers_result"
        cursor.execute(sql)
        mysql.connection.commit()
        content = cursor.fetchall()

        # get the field name
        sql = "SHOW FIELDS FROM view_testers_result"
        cursor.execute(sql)
        mysql.connection.commit()
        labels = ['UserName','Name','Phone Number','Assigned Site']

        #visualization template source:
        #https://blog.csdn.net/a19990412/article/details/84955802

        return render_template('viewTester.html', labels=labels, content=content)


@app.route('/createTestSite',methods=['GET','POST'])
def createTestSite():
    if request.method =='GET':
        return render_template('createTestSite.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()

        site = request.form.get("Site")
        address = request.form.get("Address")
        city = request.form.get("City")
        state = request.form.get("State")
        zipCode = request.form.get("Zip")
        location = request.form.get("Location")
        tester = request.form.get("Tester")
        try:
            cursor.callproc("create_testing_site",[site,address,city,state,zipCode,location,tester])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to create because " + str(e)
        else:
            mysql.connection.commit()
            return "create_testing_site alreay"


@app.route('/viewPools',methods=['GET','POST'])
def viewPools():
    if request.method =='GET':
        return render_template('viewPools.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        startDate = None if request.form.get('DateStart') == '' else request.form.get('DateStart')
        endDate = None if request.form.get('DateEnd') == '' else request.form.get('DateStart')
        status = request.form.get("Status")
        labtech = request.form.get('LabTech')


        try:
            cursor.callproc("view_pools",[startDate,endDate,labtech,status])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            #print the view to the html

            # select from the student_view_results_result
            sql = "select * from view_pools_result"
            cursor.execute(sql)
            mysql.connection.commit()
            content = cursor.fetchall()

            # get the field name
            sql = "SHOW FIELDS FROM view_pools_result"
            cursor.execute(sql)
            mysql.connection.commit()
            labels = ['Pool ID','Test Ids','Date Processed','Processed By','Pool Status']

            #visualization template source:
            #https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('viewPools.html', labels=labels, content=content)



@app.route('/poolResult',methods=['GET'])
def poolMetaDate():
    cursor = mysql.connection.cursor()

    try:
        cursor.callproc("pool_metadata")
    except pymysql.IntegrityError or KeyError as e:
        return "unable to view because " + str(e)
    else:
        #print the view to the html

        # select from the student_view_results_result
        sql = "select * from pool_metadata_result"
        cursor.execute(sql)
        mysql.connection.commit()
        content = cursor.fetchall()

        # get the field name
        sql = "SHOW FIELDS FROM pool_metadata_result"
        cursor.execute(sql)
        mysql.connection.commit()
        labels = ['Pool ID','Date Processed','Pooled Result','ProcessedBy']

        #visualization template source:
        #https://blog.csdn.net/a19990412/article/details/84955802

        return render_template('poolResult.html', labels=labels, content=content)





















if __name__ == '__main__':
    app.run()