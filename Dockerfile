# pull official base image
FROM python:3.7

# set environment varibles
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /api_demo_app

# install dependencies
COPY requirments.txt /api_demo_app/requirments.txt
RUN pip install -r requirments.txt

# copy project
COPY . /api_demo_app

# copy entrypoint.sh
COPY ./entrypoint.sh /api_demo_app/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]