# Course Website Re-designed

This is the final project built for my class at UofT where we re-create a course website with amore appealing design. This project was built in groups of three.

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

# Some photos to show as example:

<img width="1276" alt="Screen Shot 2022-04-06 at 11 42 38 PM" src="https://user-images.githubusercontent.com/81793294/162117549-3fad74fc-ae58-45c9-a760-36fa8fdbef86.png">

This is the first page the user is introduced to where the actual content is blocked off until the user logins. The user can also choose to register an account if they don't have one already.

<img width="623" alt="Screen Shot 2022-04-06 at 11 43 29 PM" src="https://user-images.githubusercontent.com/81793294/162117823-c65dae97-d2f3-48c8-b7a0-48bacac90a61.png">

<img width="1105" alt="Screen Shot 2022-04-06 at 11 44 24 PM" src="https://user-images.githubusercontent.com/81793294/162117834-ee1601b1-1a48-4334-bc20-1a1c97119a36.png">

This is the home page of a student user where the student can access all the contents of the course. As well, access their specifc grades so far, provide feedback to instructors or request regrades. 

<img width="1069" alt="Screen Shot 2022-04-06 at 11 47 06 PM" src="https://user-images.githubusercontent.com/81793294/162117949-18a5dae8-c7fe-4686-bbaa-c46130b903cd.png">

This is an example that's restriced to an instructor account where the instructor can check to see student user's request for remarks


