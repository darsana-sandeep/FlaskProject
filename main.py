from flask import Flask,render_template,request,redirect,session,flash,url_for
from functools import wraps
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST']='localhost';
app.config['MYSQL_USER']='root';
app.config['MYSQL_PASSWORD']='';
app.config['MYSQL_DB']='samp';
app.config['MYSQL_CURSORCLASS']='DictCursor';
mysql=MySQL(app)

@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    if request.method=='POST':
        name=request.form['uname']
        email=request.form['email']
        pwd=request.form['upass']
        cur=mysql.connection.cursor()
        cur.execute('insert into users(username,email,password) values(%s,%s,%s)',(name,email,pwd))
        mysql.connection.commit()
        cur.close()
        flash('Registration Successfully. Login Here...','success')
        return redirect('login')
    return render_template('reg.html',status=status)


@app.route('/')
@app.route('/login',methods=['POST','GET'])
def login():

    if request.method=='POST':
        email=request.form['email']
        pwd=request.form['upass']
        cur=mysql.connection.cursor()
        cur.execute('select * from users where email=%s and password=%s',(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data['username']
            flash('Login Successfully','success')

            return redirect('home')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template('login.html')


#Home page
@app.route('/home')
def home():
    return render_template('home.html')
#logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

if __name__=='__main__':
    app.secret_key='secret';
    app.run(debug=True)


##haiiiii