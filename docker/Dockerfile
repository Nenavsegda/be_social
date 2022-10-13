FROM python:3.8-bullseye

RUN mkdir -p var/www/be-social
COPY . var/www/be-social/
RUN cd var/www/be-social && pip install --no-cache-dir -r requirements.txt

WORKDIR var/www/be-social
RUN chmod +x docker/docker-entrypoint.sh

ENTRYPOINT ["docker/docker-entrypoint.sh"]
