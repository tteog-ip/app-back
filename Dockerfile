FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/tteog-ip/app-back
WORKDIR /app-back
RUN pip3 install virtualenv
RUN virtualenv venv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
