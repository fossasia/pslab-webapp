FROM python:3
MAINTAINER Mario Behling <mb@mariobehling.de>
RUN app-get update -y && apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "views.py" ]
