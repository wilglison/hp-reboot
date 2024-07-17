FROM python:3.8-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY crontab /etc/cron.d/hp-reboot
RUN chmod 0644 /etc/cron.d/hp-reboot
RUN crontab /etc/cron.d/hp-reboot
RUN touch /var/log/cron.log

CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
