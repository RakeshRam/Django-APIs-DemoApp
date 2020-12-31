FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /api_demo_app
COPY requirments.txt /api_demo_app/requirments.txt
RUN pip install -r requirments.txt
COPY . /api_demo_app

CMD python manage.py runserver 0.0.0.0:8000