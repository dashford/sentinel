FROM arm32v7/python:3.6.5-jessie

COPY requirements.txt ./

RUN pip install -r requirements.txt

ADD . ./

CMD ["python", "sentinel.py"]
