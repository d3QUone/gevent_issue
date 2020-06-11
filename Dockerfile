FROM python:3.8.3

RUN pip install pipenv==2020.6.2

WORKDIR /www/demo

COPY Pipfile Pipfile.lock /www/demo/
RUN pipenv install --dev

COPY ./ /www/demo

CMD ["pipenv", "run", "uwsgi", "--ini", "/www/demo/src/uwsgi.ini", "--pythonpath", "/www/demo/"]

EXPOSE 8001
