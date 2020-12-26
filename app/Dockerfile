FROM python:3.7.2-slim

# Install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

WORKDIR /usr/src/app

RUN export FLASK_APP=app.py
RUN export PYTHONPATH=$PYTHONPATH:/usr/src/app
ENV PYTHONPATH /usr/src/app

RUN pip install --upgrade pip

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install flask_script
RUN pip install sqlalchemy --upgrade

# needed for vscode
RUN pip install pylint

COPY . /usr/src/app

EXPOSE 5000
EXPOSE 3000

CMD ["python","manage.py", "runserver" ,"--host=0.0.0.0"]