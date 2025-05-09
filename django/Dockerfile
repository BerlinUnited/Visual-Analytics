FROM python:3.11-slim-bookworm

# show the stdout and stderr streams right in the command line instead of getting buffered.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir /django
WORKDIR /django
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]