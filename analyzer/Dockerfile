FROM python:3.9

ADD analyzer.py . 

RUN pip install paho-mqtt

CMD [ "python", "./analyzer.py" ]