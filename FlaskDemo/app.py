import pymysql

pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import numpy as np


# when cannot instal flask_mysqldb:
# export PATH=$PATH:/usr/local/mysql/bin
# pip3 install flask-mysqldb


app = Flask(__name__)

# Random login values for mySQL, this will need to be changed for your own machine
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'covidtest_fall2020'
# This code assumes you've already instantiated the DB

mysql = MySQL(app)
current_user = None

# Screen 4
# 1. only student can do it and he/she doesn't need to upload the form, the system should know who he/she is
# 2. there is no "all" selection
@app.route('/studentViewTestResults', methods=['GET', 'POST'])
def studentView():
    if request.method == 'GET':
        return render_template('studentViewTestResults.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()

        # Will change the way of getting username after the front end is done

        userName = request.form.get('Username')
        status = None if request.form.get('Status') == '' else request.form.get('Status')
        startDate = None if request.form.get('TimeStart') == '' else request.form.get('TimeStart')
        endDate = None if request.form.get('TimeEnd') == '' else request.form.get('TimeEnd')

        try:
            result = cursor.callproc("student_view_results", [userName, status, startDate, endDate])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            # print the view to the html

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
            labels = ['Test ID#', 'Timeslot Date', 'Date Processed', 'Pool Status', 'Status']

            # visualization template source:
            # https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('studentViewTestResults.html', labels=labels, content=content)

#Screen 5: Explore test result
@app.route('/exploreTestResult', methods=['GET', 'POST'])
def exploreTestResult():
    if request.method == 'GET':
        return render_template('exploreTestResult.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        testid = request.form.get('Testid')

        try:
            result = cursor.callproc("explore_results", [testid])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            # print the view to the html

            # select from the student_view_results_result
            sql = "select * from explore_results_result"
            cursor.execute(sql)
            #one row code below may be not neccessary
            mysql.connection.commit()
            content = cursor.fetchall()

            # get the field name
            sql = "SHOW FIELDS FROM explore_results_result"
            cursor.execute(sql)
            labels = cursor.fetchall()
            mysql.connection.commit()
            labels = ['Test ID#','Date Tested', 'Timeslot', 'Testing Location', 'Date Processed', 'Pooled Result', 'Individual Result','Processed By']

            # visualization template source:
            # https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('studentViewTestResults.html', labels=labels, content=content)

#Screen 6: Aggregate Results
@app.route('/aggregateResult', methods=['GET', 'POST'])
def aggregateResult():
    if request.method == 'GET':
        return render_template('aggregateResult.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()

        Location = None if request.form.get('Location') == '' else request.form.get('Location')
        Housing = None if request.form.get('Housing') == '' else request.form.get('Housing')
        Testing_site = None if request.form.get('testingSite') == '' else request.form.get('testingSite')
        startDate = None if request.form.get('TimeStart') == '' else request.form.get('TimeStart')
        endDate = None if request.form.get('TimeEnd') == '' else request.form.get('TimeEnd')
        try:
            result = cursor.callproc("aggregate_results", [Location,Housing,Testing_site,startDate,endDate])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            # print the view to the html

            # select from the student_view_results_result
            sql = "select * from aggregate_results_result"
            cursor.execute(sql)
            #one row code below may be not neccessary
            mysql.connection.commit()
            content = cursor.fetchall()

            # get the field name
            sql = "SHOW FIELDS FROM aggregate_results_result"
            cursor.execute(sql)
            labels = cursor.fetchall()
            mysql.connection.commit()
            labels = ['Total','Number of Testing','Percentage']

            # visualization template source:
            # https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('aggregateResult.html', labels=labels, content=content)

#Screen 7a:
@app.route('/testSignUpFilter', methods=['GET', 'POST'])
def testSignUpFilter():
    if request.method == 'GET':
        return render_template('testSignUpFilter.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.form.get('Username')

        Testing_site = None if request.form.get('testingSite') == '' else request.form.get('testingSite')
        startDate = None if request.form.get('DateStart') == '' else request.form.get('DateStart')
        endDate = None if request.form.get('DateEnd') == '' else request.form.get('DateEnd')
        startTime = None if request.form.get('startTime') == '' else request.form.get('startTime')
        endTime = None if request.form.get('endTime') == '' else request.form.get('endTime')
        try:
            result = cursor.callproc("test_sign_up_filter", [username,Testing_site,startDate,endDate,startTime,endTime])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            # print the view to the html

            # select from the student_view_results_result
            sql = "select * from test_sign_up_filter_result"
            cursor.execute(sql)
            #one row code below may be not neccessary
            mysql.connection.commit()
            content = cursor.fetchall()
            print(content)
            # get the field name
            sql = "SHOW FIELDS FROM test_sign_up_filter_result"
            cursor.execute(sql)
            labels = cursor.fetchall()
            print(labels)
            mysql.connection.commit()
            labels = ['appt_date','appt_time','street','city','state','zip','site_name']

            # visualization template source:
            # https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('testSignUpFilter.html', labels=labels, content=content)

#Screen 7b:
@app.route('/testSignUp', methods=['GET', 'POST'])
def testSignUp():
    if request.method == 'GET':
        return render_template('testSignUp.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.form.get('Username')
        Testid = request.form.get('Testid')
        Testing_site = None if request.form.get('testingSite') == '' else request.form.get('testingSite')
        Date = None if request.form.get('Date') == '' else request.form.get('Date')
        Time = None if request.form.get('Time') == '' else request.form.get('Time')
        print([username, Testing_site, Date, Time, Testid])
        try:
            cursor.callproc("test_sign_up", [username,Testing_site,Date,Time,Testid])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to sign up" + str(e)
        else:
            mysql.connection.commit()
            return "You have successfully Signed up the Test"



#Screen 8a:
@app.route('/tests_processed', methods=['GET', 'POST'])
def tests_processed():
    if request.method == 'GET':
        return render_template('tests_processed.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.form.get('labtechUsername')

        testStatus = None if request.form.get('testStatus') == '' else request.form.get('testStatus')
        startDate = None if request.form.get('DateStart') == '' else request.form.get('DateStart')
        endDate = None if request.form.get('DateEnd') == '' else request.form.get('DateEnd')
        try:
            result = cursor.callproc("tests_processed", [startDate,endDate,testStatus,username])
        except pymysql.IntegrityError or KeyError as e:
            return "unable to view because " + str(e)
        else:
            # print the view to the html

            # select from the student_view_results_result
            sql = "select * from tests_processed_result"
            cursor.execute(sql)
            #one row code below may be not neccessary
            mysql.connection.commit()
            content = cursor.fetchall()
            print(content)
            # get the field name
            sql = "SHOW FIELDS FROM tests_processed_result"
            cursor.execute(sql)
            labels = cursor.fetchall()
            print(labels)
            mysql.connection.commit()
            labels = ['test_id','pool_id','test_date','process_date','test_status']

            # visualization template source:
            # https://blog.csdn.net/a19990412/article/details/84955802

            return render_template('tests_processed.html', labels=labels, content=content)







if __name__ == '__main__':
    app.run()
