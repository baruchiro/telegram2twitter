FROM python:3

COPY src/*.py /
COPY requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./telegram-bot.py" ]
