FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
EXPOSE 8000
COPY . /web_django/
WORKDIR /web_django
RUN pip install -r requirements.txt
RUN adduser --disabled-password admin-user


USER admin-user
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]