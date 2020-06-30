# Cs50-final-proyect - FastLearning

## You can see this project on:
### https://cs50-learningfast.herokuapp.com/
#### If you want to test the upload of images or files, please do not upload large files, as space in Azure Storages is limited

#### For administrations, go to /admin and credentials are admin-admin

## Structure
This project contains the main directory (called LearningFast) and two Django projects: Users and Courses

## LearningFast
My web application for the final CS50 project is an application to help people create their own learning courses or register for any course in a topic and learn about it. It is based on platforms like edX or Udemy, but with different and simpler features than these.

### My project requirements:

Search for courses: Users can search for courses by name or author, or they can select a topic to output courses related to that topic.

Login, Registration and Logout: That users can log in, register and log out from the website.
Create/Edit courses: Users must be able to create courses so that everyone can view and register for them.  These courses must have a name and an end date. Once that end date has passed, no one will be able to register for them.

Create/Edit units and sections: Within courses, the teacher (author) can create new units and/or sections and edit them whenever he wants, as long as the course is not finished

Create/Edit tasks:  The teacher can create tasks that the students will have to do and then upload the files needed to complete that task.  It should have a completion date, and when it is finished no one should be able to upload more files. When the assignment is created, an email should be sent to all students in the course advising that an assignment has been opened.

Rate tasks: The teacher must be able to rate the assignment once the completion time is over.When an assignment is graded, an email should be sent to the student concerned showing their grade.

Edit your profile: Users should be able to edit their profile at any time, and add a profile picture.

### setting.py
I added some configuration to run CKeditor, authentication via Gmail, send email, Azure Storage and for deploying on Heroku.

### urls.py
Lines have been added to allow routes for courses and users applications

## Users
This application manages the login, registration and logout of the project.

### views.py
Contains the register, sign-in and fun_logout functions that are used to register, log in and log out respectively.

### Models
I created the UserProfile model to represent the profile images of each user.

### forms.py
I have created forms for registration and login to make their validation easier (RegisterForm and UserLoginForm)

### static
Here all the static files of the users application are stored. I have the structure divided into different folders so that it is easier to find the different necessary files

## Courses 
This application contains all the logic of the application to subscribe to courses, create them, create units, sections and tasks and correct them.

### Models
I have decided to create the following models:
#### Category
Contains the categories of courses.
#### Course
Represents the courses to which users can enroll.
#### Unit
Represents the units into which a course is divided.
#### Section and Task
They represent the tasks and sections into which a course is divided.
#### Homework
Represents when a task has been delivered by a user and its grade
#### Attachment
They represent the files uploaded by users in a task

### forms.py
I have added forms to create and edit the necessary models.

## Templates
I create all templates with Bootstrap and Bootswatch(Lumen). I used css, JavaScript and Jquery to improve the user interface.

I also have used Ajax for the removal of files uploaded by users in tasks. 
I hope you like it!