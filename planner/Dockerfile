FROM python:3.9

ADD planner.py . 

RUN pip install paho-mqtt python-dateutil

CMD [ "python", "./planner.py" ]