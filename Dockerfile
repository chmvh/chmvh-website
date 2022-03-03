FROM python:3.9 AS dev

WORKDIR /opt/chmvh-website

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./chmvh_website ./chmvh_website

WORKDIR ./chmvh_website

ENTRYPOINT ["./manage.py"]
# We have to explicitly bind to 0.0.0.0 so the dev server is available outside
# the docker container.
CMD ["runserver", "0.0.0.0:8000"]

# Production development environment runs Gunicorn instead of the Django dev
# server.
FROM dev

COPY ./entrypoint.sh .

# The combination of this environment variable and the
# "--enable-stdio-inheritance" switch allow for messages sent by Django to
# stdout to propagate properly.
ENV PYTHONUNBUFFERED=true

ENTRYPOINT ["./entrypoint.sh"]
CMD []
