# Gardening Application with simple API

Application backend : Python/Django

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=python,django,djangorestframework"
    />
  </a>
</p>

Application Frontend: Html, Bootsrap css, Custom css, and Javascripts

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=html,bootstrap,css,javascript"
    />
  </a>
</p>

Description:

Gardening application  with fair html/boostrap frontend design, and Python - Django backend.

Application can store and show plants, diseases and pesticides data. Contain search functions,
signed in users can make protections schedules, and sowing diaries. Users can make comments, and replies.
Admin user have several site fuctions, API also included for the most of site functions.


Authentication/User:

- Sign up ( email confirmed, with google reCAPTCHA )
- Sign in ( email confirmed, with goole reCAPTCHA )
- Password change 
- Update user profile


General functions for anybody:

- View plants by category
- View all plants 
- View Diseases
- View Pesticides
- Read comments and replies
- Can read about page content, and send contact messages to site owners


Authenticated user functions:

- Create comment posts, and send replies to comments
- Create, update, delete, list own protection schedules
- Create, update, delete, list own sowing diaries


Admin functions:

- Create, update, delete plants
- Create, update, delete diseases
- Create, update, delete pesticides
- Update about page content
- List contact messages
- List Users
- Enable/Disable users
- Hide/Unhide comments, and replies


API DETAIL:


| Description                         | URLS                                                        | METHODS                                |  PERMISSIONS                                    |
| ----------------------------------- | ----------------------------------------------------------- | -------------------------------------- | ----------------------------------------------- |
| api summary                         | http://127.0.0.1:8000/api/                                  | GET, OPTIONS                           | for anybody                                     |
| api login page                      | http://127.0.0.1:8000/api/api-auth/login/                   | GET, POST, PUT, HEAD, OPTIONS          | for anybody, user and password will require     |
| obtain jwt auth token               | http://127.0.0.1:8000/api/token/                            | POST, OPTIONS                          | for anybody, user and password will require     |
| refresh jwt tokens                  | http://127.0.0.1:8000/api/token/refresh/                    | POST, OPTIONS                          | for anybody, refress token will require         |
| list plants                         | http://127.0.0.1:8000/api/plants/                           | GET, HEAD, OPTIONS                     | for anybody                                     |
| list diseases                       | http://127.0.0.1:8000/api/diseases/                         | GET, HEAD, OPTIONS                     | for anybody                                     |
| list pesticides                     | http://127.0.0.1:8000/api/pesticides/                       | GET, HEAD, OPTIONS                     | for anybody                                     |
| create plant                        | http://127.0.0.1:8000/api/plant/create/                     | POST, OPTIONS                          | admin only, token or session required           |
| create disease                      | http://127.0.0.1:8000/api/disease/create/                   | POST, OPTIONS                          | admin only, token or session required           |
| create pesticide                    | http://127.0.0.1:8000/api/pesticide/create/                 | POST, OPTIONS                          | admin only, token or session required           |
| plant detail                        | http://127.0.0.1:8000/api/plant/{int:pk}/                   | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | admin only, token or session required           |
| disease detail                      | http://127.0.0.1:8000/api/disease/{int:pk}/                 | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | admin only, token or session required           |
| pesticide detail                    | http://127.0.0.1:8000/api/pesticide/{int:pk}/               | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | admin only, token or session required           |
| schedule protection                 | http://127.0.0.1:8000/api/protections/                      | GET, POST, HEAD, OPTIONS               | authenticated users, token or session required  |
| protection detail                   | http://127.0.0.1:8000/api/protection/{int:pk}/              | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | authenticated users, token or session required  |
| schedule diary                      | http://127.0.0.1:8000/api/diaries/                          | GET, POST, HEAD, OPTIONS               | authenticated users, token or session required  |
| diary detail                        | http://127.0.0.1:8000/api/diary/{int:pk}/                   | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | authenticated users, token or session required  |
| create forum message                | http://127.0.0.1:8000/api/post/create/                      | GET, POST, HEAD, OPTIONS               | authenticated users, token or session required  |
| list forum messages                 | http://127.0.0.1:8000/api/posts/all/                        | GET, HEAD, OPTIONS                     | for anybody                                     |
| forum message detail                | http://127.0.0.1:8000/api/post/{int:pk}/                    | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | authenticated users, token or session required  |
| reply to forum message              | http://127.0.0.1:8000/api/post/{int:pk}/reply/              | GET, POST, HEAD, OPTIONS               | authenticated users, token or session required  |
| list forum message relies           | http://127.0.0.1:8000/api/post/{int:pk}/replies/            | GET, HEAD, OPTIONS                     | for anybody                                     |
| reply detail                        | http://127.0.0.1:8000/api/reply/{int:pk}/                   | GET, PUT, PATCH, DELETE, HEAD, OPTIONS | authenticated users, token or session required  |



INSTALLED PACKAGES:

- aiosmtpd==1.4.6
- annotated-types==0.7.0
- asgiref==3.8.1
- atpublic==6.0.1
- attrs==25.3.0
- beautifulsoup4==4.13.4
- crispy-bootstrap5==2025.4
- Django==4.2.20
- django-bootstrap-datepicker-plus==5.0.5
- django-bootstrap-v5==1.0.11
- django-bootstrap5==25.1
- django-crispy-forms==2.4
- django-recaptcha==4.1.0
- django-resized==1.0.3
- django-tinymce==4.1.0
- djangorestframework==3.16.0
- djangorestframework_simplejwt==5.5.0
- drf-redesign==0.5.1
- fontawesomefree==6.6.0
- pillow==11.2.1
- pydantic==2.11.5
- pydantic_core==2.33.2
- PyJWT==2.9.0
- PyYAML==6.0.2
- six==1.17.0
- soupsieve==2.7
- sqlparse==0.5.3
- typing-inspection==0.4.1
- typing_extensions==4.13.2


NOTES:

SENDING MAILS:

This site use email validated registration.
For the usage need some kind of mail server at least for the testing, or need modify the settings.py to real email providers port, and credentials

very simple pre-installed method for tesing with fake mail server on localhost port 1025:

aiosmtpd version 1.4.6 installed within the virtual environment with the requirements.txt, so just run in a different terminal (in the same virtual environment) the following command to run fake mailserver:

python -m aiosmtpd -n -l localhost:1025

emails will appear in the terminal


INSTALL:

- clone the repository ( git clone https://github.com/immonhotep/garden_app.git )
- Create python virtual environment and activate it ( depends on op system, example on linux: virtualenv venv  and source venv/bin/activate )
- Install the necessary packages and django  ( pip3 install -r requirements.txt ) into the virtual environment
- Create the database:( python3 manage.py makemigrations and then python3 manage.py migrate )
- Create a superuser ( python3 manage.py createsuperuser )
- Run the application ( python3 manage.py runserver )



  Example sample picture from home page


  ![sample home](https://github.com/user-attachments/assets/15ea9310-1966-4214-a914-b464a6c4ec4e)





