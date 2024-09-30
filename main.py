from flask import Flask, render_template, request, redirect,session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import waitress


app = Flask(__name__)
app.secret_key="your_secret_key"

#configure SQL
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

#Database

class User(db.Model):
    #class variable
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(25),nullable=False)
    registration_number = db.Column(db.String(25), unique=True,nullable=False)
    passwordhash = db.Column(db.String(20),nullable=False)

    def set_name(self,name):
        self.fullname=name
    def set_email(self,email):
        self.email=email
    def set_registration_number(self,registration_number):
        self.registration_number=registration_number
    def set_password(self,password):
        self.passwordhash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.passwordhash,password)



#routes

@app.route("/")
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        registration_number = request.form['registration_number']
        password = request.form['password']
        user = User.query.filter_by(registration_number=registration_number).first()
        print(user)
        if user and user.check_password(password):
            print("yes")
            session['registration_number'] = registration_number 
            session['fullname']=user.fullname
            print("yes1")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Credentials !",'error')
    return render_template('login.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=="POST":
        fullname=request.form['fullname']
        #print(fullname)
        email=request.form['email']
        #print(email)
        registration_number=request.form['registration_number']
        #print(registration_number)
        password=request.form['password']
        #print(password)
        cnf=request.form['confirm_password']
        #print(cnf)
        if password !=cnf:
            flash("Password and Confirm Password not matched !",'error')
        user = User.query.filter_by(registration_number=registration_number).first()
        print(user)
        if user:
            flash("User Already Exists !",'error')
        else:
            new_user = User()
            new_user.set_name(fullname)
            new_user.set_email(email)
            new_user.set_registration_number(registration_number)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("User Registered successfully !","success")
            
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if "registration_number" in session:
        print("yes2")
        return render_template('dashboard.html',fullname=session['fullname'])
    return redirect(url_for('login'))

@app.route("/forgot")
def forgotpass():
    return render_template('forgot.html')
@app.route("/logout")
def logout():
    session.clear() 
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))



if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    #app.run(debug=True)
    waitress.serve(app, host="0.0.0.0", port=8080)