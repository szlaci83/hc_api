FROM python:3
RUN mkdir /app
WORKDIR /app
COPY *.py /app/
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt
EXPOSE 4567
CMD ["python3", "/app/app.py"]