FROM python:3.12-alpine
WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5050
COPY . . 
CMD ["ls"]
