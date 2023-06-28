FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/tteog-ip/app-back
WORKDIR /app-back
ENV VIRTUAL_ENV=/venv
RUN python3.9 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD sleep 5 && python manage.py makemigrations && python manage.py migrate && gunicorn dr_tart.wsgi --bind 0.0.0.0:8000
