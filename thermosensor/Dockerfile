FROM arm32v7/python:latest

RUN apt-get update

RUN apt-get -y install gcc

RUN pip install prometheus_client Adafruit_GPIO Adafruit_MCP3008

COPY . /root/

CMD ["python", "/root/client.py"]