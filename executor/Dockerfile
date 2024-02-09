FROM python:3.9

ADD app.py .
ADD ./static ./static 
Add ./templates ./templates 

RUN pip install paho-mqtt Flask python-dateutil

EXPOSE 5000

ENV FLASK_APP=app

#CMD [ "python", "./webappp.py"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]