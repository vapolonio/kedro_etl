ARG BASE_IMAGE=python:3.6-buster
FROM $BASE_IMAGE

# install system libraries
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN apt install libreoffice -y
# install project requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -d /home/kedro -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro

# copy the whole project except what is in .dockerignore
WORKDIR /home/kedro
COPY . .
RUN chown -R kedro:${KEDRO_GID} /home/kedro
USER kedro
RUN chmod -R a+w /home/kedro
RUN pip install "kedro[pandas]"
EXPOSE 8888 4141

CMD ["kedro", "run"]
