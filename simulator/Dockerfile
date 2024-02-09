FROM python:3.9

ADD simulator.py . 

RUN pip install paho-mqtt python-dateutil

CMD [ "python", "./simulator.py" ]