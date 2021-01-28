FROM python:latest
ENV LOCAL_HOSTNAME "192.168.10.3"
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD python app.py
