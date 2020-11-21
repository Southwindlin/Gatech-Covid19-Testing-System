import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

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


@app.route('/regform')
def regform():
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






if __name__ == '__main__':
    app.run()