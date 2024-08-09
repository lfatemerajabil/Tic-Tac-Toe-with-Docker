FROM python:3.9

WORKDIR /Users/fatemerajabi/Dockers

COPY . .

RUN pip install -r requirements.txt

CMD python main.py