Development Start-up
--------------------------------------------------------
To start the application:
Run 'docker-compose up -d --build'

then within the flask container, the one named 'app'

Run 'python manage.py db init'
Run 'python manage.py db migrate'
Run 'python manage.py db upgrade'
Run 'python manage.py recreate_db'
Run 'python manage.py seed_db'


For test coverage report documentation
Run 'coverage run -m pytest'
Run 'coverage report'
Run 'coverage html'

Now the front end application will be served at localhost:8080/
and the back end application will be served at localhost:8080/app



Production Start-up
--------------------------------------------------------
NOT YET IMPLEMENTED.