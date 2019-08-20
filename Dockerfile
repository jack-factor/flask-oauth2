FROM python:3.7-slim

LABEL mainteiner="Jack Moreno"

WORKDIR /usr/src/

COPY . /usr/src/

EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]