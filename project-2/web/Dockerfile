FROM ubuntu:20.04
MAINTAINER Karma Woeser "karmawoeser1@gmail.com"
RUN apt-get update -y
RUN apt-get install python3.8 python3-pip -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
