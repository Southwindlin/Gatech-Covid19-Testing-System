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
        if confirmPass == passWord:
            return "Sorry, your passwords don't match"


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
        elif userType == 'employee':
            pass


















if __name__ == '__main__':
    app.run()