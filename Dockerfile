FROM openjdk:slim
COPY --from=python:3.9 / /

#FROM python:3.9.2

#RUN mkdir /TopicModelerWebApp/src
#WORKDIR /TopicModelerWebApp
ADD . /TopicModelerWebApp
WORKDIR /TopicModelerWebApp
#WORKDIR /src

COPY venv venv

RUN python3 -m venv /opt/venv

COPY src/requirements.txt .
 
#COPY . TopicModelerWebApp
RUN pip install -r requirements.txt

#COPY /src/ .  
#COPY . /src
COPY src src

ENV MALLET_HOME = "src/mallet-2.0.8" 
#COPY src/ .

#CMD ["ls"]
#CMD ["python", "src/index.py"]
#EXPOSE 5000
#ENV FLASK_APP="src/index.py"
#ENTRYPOINT  python index.py

#ENTRYPOINT ["flask"]
#CMD ["run", "--host", "0.0.0.0"]
#CMD ["python", "src/index.py"]
