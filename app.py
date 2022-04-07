from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text  # textual queries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    i_s = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Users('{self.id}','{self.username}','{self.password}','{self.i_s}')"


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    assignment = db.Column(db.Integer, nullable=False)
    midterm = db.Column(db.Integer, nullable=False)
    final = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Student('{self.username}','{self.assignment}','{self.midterm}','{self.final}', ,'{self.lab}')"


class Remark(db.Model):
    __tablename__ = 'remark'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    request_type = db.Column(db.String(20), nullable=False)
    request_detail = db.Column(db.String(1000), nullable=False)
    closed_tf = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Remark('{self.username}','{self.request_question}')"


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    instructor_teaching = db.Column(db.String(1000), nullable=False)
    improve_teaching = db.Column(db.String(1000), nullable=False)
    like_labs = db.Column(db.String(1000), nullable=False)
    improve_lab = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"Feedback('{self.username}','{self.feedback}')"


@app.route('/')
@app.route('/index')
def index():
    pagename = 'index'
    return render_template('index.html', pagename=pagename)


@app.route('/assignments')
def assignments():
    return render_template('assignments.html')


@app.route('/labs')
def labs():
    return render_template('labs.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/student_grades', methods=['GET', 'POST'])
def student_grades():
    if request.method == 'GET':
        query_grades_result = query_student_grades()
        return render_template('student_grades.html', query_grades_result=query_grades_result)


@app.route('/all_anon_feedback', methods=['GET', 'POST'])
def all_anon_feedback():
    if request.method == 'GET':
        query_feedback_result = query_feedback()
        return render_template('all_anon_feedback.html', query_feedback_result=query_feedback_result)


@app.route('/all_regrade_requests', methods=['GET', 'POST'])
def all_regrade_requests():
    if request.method == 'GET':
        query_regrades_result = query_requests()
        return render_template('all_regrade_requests.html', query_regrades_result=query_regrades_result)
    else:
        ru = request.form['remark_username']
        rrt = request.form['remark_request_type']
        rrd = request.form['remark_request_detail']
        request_details = (
            ru,
            rrt,
            rrd
        )
        update_request(request_details)
        return redirect(url_for('all_regrade_requests'))


@app.route('/student_check_grade', methods=['GET', 'POST'])
def student_check_grade():
    if request.method == 'GET':
        query_grade_result = query_student_grade()
        return render_template('student_check_grade.html', query_grade_result=query_grade_result)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['Username']
        user_type = request.form['Type']
        hashed_password = bcrypt.generate_password_hash(
            request.form['Password']).decode('utf-8')

        reg_details = (
            username,
            user_type,
            hashed_password
        )
        add_users(reg_details)
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('already logged in!!')
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        user = Users.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            flash('Please check your login details and try again')
            return render_template('login.html')
        else:
            session['name'] = username
            session['type'] = user.i_s
            session.permanent = True
            return redirect(url_for('index'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        instructor_names = query_instructor_usernames()
        return render_template('feedback.html', instructor_options=instructor_names)
    else:
        instructor = request.form['instructor']
        instructor_teaching = request.form['instructor_teaching']
        improve_teaching = request.form['improve_teaching']
        like_labs = request.form['like_labs']
        improve_lab = request.form['improve_lab']
        feedback_details = (
            instructor,
            instructor_teaching,
            improve_teaching,
            like_labs,
            improve_lab
        )
        add_feedback(feedback_details)
        return redirect(url_for('feedback'))


@app.route('/remark_request', methods=['GET', 'POST'])
def remark_request():
    if request.method == 'GET':
        query_remarks = query_student_requests()
        return render_template('remark_request.html', query_remarks=query_remarks)
    else:
        username = session['name']
        request_type = request.form['request_type']
        closed_tf = "Open"
        request_detail = request.form['request_detail']
        request_details = (
            username,
            request_type,
            closed_tf,
            request_detail,
        
        )
        add_request(request_details)
        return redirect(url_for('remark_request'))


@app.route('/add_student_grade', methods=['GET', 'POST'])
def add_student_grade():
    if request.method == 'GET':
        return render_template('add_student_grade.html')
    else:

        username = request.form['username']
        assignment = request.form['assignment']
        midterm = request.form['midterm']
        final = request.form['final']
        lab = request.form['lab']

        grade_details = (
            username,
            assignment,
            midterm,
            final,
            lab
        )

        student_in = db.session.query(Student).filter(Student.username == username).first() is not None

        if(student_in):
            update_grade(grade_details)
        else:
            add_grade(grade_details)
        return redirect(url_for('add_student_grade'))


def update_grade(grade_details):
    db.session.query(Student).filter(Student.username == grade_details[0]).update({
        'assignment': grade_details[1],
        'midterm': grade_details[2],
        'final': grade_details[3],
        'lab': grade_details[4]
    })
    db.session.commit()

def update_request(request_details):
    db.session.query(Remark).filter(Remark.username == request_details[0]).filter(Remark.request_type == request_details[1]).filter(Remark.request_detail == request_details[2]).update({
        'closed_tf': "Closed"
    })
    db.session.commit()


def add_grade(grade_details):
    student = Student(  username=grade_details[0],
                        assignment=grade_details[1],
                        midterm=grade_details[2],
                        final=grade_details[3],
                        lab=grade_details[4])
    db.session.add(student)
    db.session.commit()


def add_request(request_details):
    remark = Remark(
        username=request_details[0],
        request_type=request_details[1],
        closed_tf =request_details[2],
        request_detail=request_details[3]
        )
    db.session.add(remark)
    db.session.commit()


def add_feedback(feedback_details):
    feedback = Feedback(
        username = feedback_details[0],
        instructor_teaching=feedback_details[1],
        improve_teaching=feedback_details[2],
        like_labs=feedback_details[3],
        improve_lab=feedback_details[4]
        )
    db.session.add(feedback)
    db.session.commit()


@app.route('/logout')
def logout():
    session.pop('name', default=None)
    session.pop('type', default=None)
    return redirect(url_for('index'))


def add_users(reg_details):
    user = Users(username=reg_details[0], i_s=0 if reg_details[1]
                 == "s" else 1, password=reg_details[2])
    db.session.add(user)
    db.session.commit()


def query_student_grades():
    query_grades = Student.query.all()
    return query_grades


def query_student_grade():
    query_gradess = Student.query.filter(
        Student.username == session['name'])
    return query_gradess


def query_feedback():
    query_feedback = Feedback.query.filter(
        Feedback.username == session['name'])
    return query_feedback


def query_requests():
    query_requests = Remark.query.all()
    return query_requests

def query_student_requests():
    query_requests = Remark.query.filter(Remark.username == session['name'])
    return query_requests

def query_instructor_usernames():
    query_instructors = Users.query.filter(Users.i_s == 1)
    return query_instructors


if __name__ == "__main__":
    app.run()
