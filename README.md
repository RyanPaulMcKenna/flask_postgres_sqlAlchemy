Development Start-up
--------------------------------------------------------
To start the application:
Run 'docker-compose up -d --build'
then within the flask container, the one named 'app'
Run 'python manage.py db init'
Run 'python manage.py db migrate'
Run 'python manage.py db upgrade'

Now the front end application will be served at localhost:8080/
and the back end application will be served at localhost:8080/app



Production Start-up
--------------------------------------------------------
NOT YET IMPLEMENTED.