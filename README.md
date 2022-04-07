# Course Website Re-designed

This is the final project built for my class Introduction to Databases and Web Applications at UofT where we re-create a course website with amore appealing design. This project was built in groups of three.

Built with Flask, HTML, CSS, SQLAlchemy, SQLite

Make sure you have flask installed along with python3

Some required software to install:

```
$ pip install flask-bcrypt
$ pip install Flask-Session
$ pip install -U Flask-SQLAlchemy
```

Input these commands into the terminal when in the project file to set required software versions the same.

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

Test dummy accounts:
For student, username: student1
             password: student1
             
For instructor, username: instructor1
                password: instructor1
                
Some perks of using this website:
1. Hashed password when signing up in database
2. Session is stored temporarily so the user can continue where they left off without re-logging in again
3. Student's grades are private to individual student accounts, so no other students see each other's grades
4. Instructors can recieve feedback from students and the directed feedbacks towards different instructors are hidden from each other for privacy
5. Students can view marks and create a request for remark which then an instructor account will be able to view
