FROM python:latest
ENV LOCAL_HOSTNAME "192.168.10.3"
ENV POSTGRES_HOST "192.168.10.15"
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD python app.py
