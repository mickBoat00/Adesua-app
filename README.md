# Adesua
#### Summary of the project
Adesua is a backend developed with django. It is a plaform to provide private school courses or vacation class for pupil from Year 1 to Year 12.
Courses are based on the current curriculums available across the different education systems in Ghana. <br>

Please read the Why Adesua Section below to get more background detail. 
<br>

## Read more on details about Adesua

<details>
<summary><b>What is Adesua</b></summary>
<br>
Adesua is a ghanaian language word for education. 
Adesua is a platform where parents can get access to lessons for their wards based on their current school year and school curriculum.
The target market for this pupil from year 1 to year 12 or pupil who are not yet in High School.
<br>
<br>

</details>

<details>
<summary><b>Why Adesua </b></summary>
<br>
Growing up as a student in Ghana, we had private after school lessons from teachers who were not necessarily our school teacher at home, but the lessons were based on our school curriculum.

Also it was normal to go for vacation or summer break classes at cousins', friends' or the best schools in our vicinity.
This happens because students sometimes neeeds a different point of view or explanation. <br>

So why not create a platform where you students can get access to courses based on their curriculum from some of the best teachers from prestigious schools in their country

Hence `Adesua` app is the backend for a platform where parents will have access to courses for their wards based on their current curriculum, school year and subject from vetted course instructor. <br>
Course Instructors are currrently good teachers in other school.

Every Course created by a teacher for the platform passes through verfication checks before the the course is published on the platform.
<br>

<br>


</details>

<details>
<summary><b>Workflow of Adesua </b></summary>
<h4>User</h4>
    
<li>Any user can view courses listed on the platform and filter courses based on a school year or curriculum</li>
<li>Any user can view details of a courses but cannot view course lessons if they are not enrolled in that course</li>
<li>To enroll in a course, a user must sign up as a student</li>
<li>Students have access to course lessons of courses, they enrolled in.</li>
<li>Students will be able to rate courses, they are enrolled in.</li>
<li>Students are allowed to enroll in courses that are on trial for a few days. Once the trial period is over, they lose access to the course lessons.</li>
<br>

<h4>Course Instructor</h4>
    
<li>To upload a course on the platform, you have to sign up as an instructor</li>
<li>Courses created on the platform will be reviewed by reviewers before they are listed on the main page.</li>
<li>Course instructors will recieve an email, for their approved courses.</li>
<li>Course instructors can update, delete their course.</li>
<li>Course instructors can create,retrieve, update,and delete lessons for their courses.</li>
<br>

<h4>Reviewers</h4>
    
<li>Reviewers will have to perform backgorund checks on the course instructor.</li>
<li>Reviewers can see a list of pending courses to be approved.</li>
<li>Reviewers will approve or deny courses based on the results of their background check.</li>
<br>

<h4>Admin</h4>
    
<li>Admin can create promotions for a bunch of courses.</li>
<li>Admin creates reviewers.</li>
<li>Admin can delete any type of user on the platform.</li>
<br>

<br><br>


</details>


<details>
<summary><b>Database Schema</b></summary>
You can view the database schema for the web api from the link below
<br>
<br>
Link to Database Design https://youtu.be/APhI43fyRHI

</details>

<details>
<summary><b>Technologies used</b></summary>
<li>Django</li>
<li>Django Rest Framework</li>
<li>PostgreSQL</li>
<li>ElasticSearch</li>
<li>Celery</li>
<li>Redis</li>

</details>



## Instructions on setting the application up.
1.Clone the repository on your local machine
  ```
  git clone <repository address>
  ```
  
2. From your termical, navigate to the application folder
  
3. Open your terminal and stop any running docker containers you might have running.
  ```
   docker-compose down
  ```
   
4. Build a docker image for the application
  ```
   docker-compose build
  ```
5. Run the docker image
  ```
   docker-compose up
  ```
  
   <b>OPTIONAL</b> To load some dummy data into the database
   - Open a new terminal and navigate to the the adesua container
  ```
  docker exec -it adesua_container /bin/bash
  ```
  - Run this command
  ```
  python manage.py populate_db
  ```
  <br>
  
  <b>To run test</b>
   - Navigate to the the adesua container
  ```
  docker exec -it adesua_container /bin/bash
  ```
  - Run this command
  ```
  coverage run -m pytest
  ```
  


