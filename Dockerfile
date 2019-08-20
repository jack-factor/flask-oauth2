FROM python:3.7-slim

LABEL mainteiner="Jack Moreno"

RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS && apt-get purge -y --auto-remove

WORKDIR /usr/src/

COPY . /usr/src/

EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./start.sh

CMD ["./start.sh"]