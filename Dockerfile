FROM python:3.10.1-slim-buster

COPY demo_app /home/demo_app

RUN ["/bin/bash", "-c", "pip install -r /home/demo_app/requirements.txt"]

#Set working directory
WORKDIR /home/demo_app

CMD ["/bin/bash", "-c", "python", "main.py"]