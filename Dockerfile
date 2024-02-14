FROM python:3.9
COPY . /opt
WORKDIR /opt

RUN mkdir -p data
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-c", "config.py", "api:app"]