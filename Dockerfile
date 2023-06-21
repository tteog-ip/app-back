FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /appback
COPY requirements.txt /appback/requirements.txt
ENV VIRTUAL_ENV=/venv
RUN python3.9 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /appback
CMD sleep 5 && python manage.py makemigrations && python manage.py migrate && gunicorn config.wsgi --bind 0.0.0.0:8000
