# FamPay-Hiring-Assignment
Backend Assignment (Intern)

<h4> TechStack Used</h4>
1. Python (Programming Language)<br>
2. Django (Web Framework)<br>
3. SQLite (Database)<br>

<h5> API's Postman ScreenShots</h5>
<h6> 1. Get Videos (GET Request)</h6>
Returns all the videos order by lates published date. When you get an error <b>All APIKey's Quota is over, Add a new APIKey</b> use Add Key API (2nd point) for adding a new Youtube Data API Key in the database.
<img src="https://user-images.githubusercontent.com/34139754/100717392-f9680700-33df-11eb-9062-5483774bac58.png">

| Status  |   Time  |    Size     |
| ------- | ------- | ------------|
| 200 OK  |   66 ms |   21.85 KB  |


<h6> 2. Add Key (POST Request)</h6>
When you get an error <b>All APIKey's Quota is over, Add a new APIKey</b>, then use this api, for adding a new Youtube Data API Key in the database, so the service will start again, fetch and store videos in the database.
<img src="https://user-images.githubusercontent.com/34139754/100717219-c887d200-33df-11eb-99af-035eb1eb967d.png">

| Status  |   Time  |    Size     |
| ------- | ------- | ------------|
| 201 OK  |   450ms |    294 B    |


<h5><a href="https://documenter.getpostman.com/view/6434629/TVmLBy5k"> Postman API's Documentation</a></h5>
<h5><a href="https://www.getpostman.com/collections/f87742cda0f1b51b494d"> Postman Collection</a></h5>


<h5> How to setup and run locally </h5>
<p>
  1. Clone the Repository <br>
  2. <a href="https://www.geeksforgeeks.org/python-virtual-environment/"> Create a Activate Python Virtual Environment </a></h5><br>
  3. After activating the virtual enviornment, redirect to project base directory. <br>
  4. Run the following command for installing dependencies.
</p>

    $ pip3 install -r requirements.txt

<br>
  5. Now direct to Fampay folder for starting the django server.

    $ cd Fampay

<br>
  6. Now before running the server, we have to setup database, so run.
 
    $ python3 manage.py migrate

<br>
  7. Now create superuser for accessing the dashboard to view the stored videos

    $ python3 manage.py createsuperuser
<br>
  8. After completeing of all the entries while creating superuser, we are ready to test the whole project. 
<br>
  9. Now run the following command for starting the server

    $ python3 manage.py runserver

<br>
  10. To access the dashboard checkout http://127.0.0.1:8000/admin
<br>

Now run the following apis described in the Postman collection for testing the project.
<br>

<b>Note : </b> While testing API's if you found an error of database is locked, then retry the api (don't restart the server). It occurs because SQLite is meant to be a lightweight database, and thus can't support a high level of concurrency.
<br>
