FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron python3-pip curl wget unzip xvfb libxi6 libgconf-2-4 gnupg && rm -rf /var/lib/apt/lists/*

#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
#    && apt-get update \
#    && apt-get install -y google-chrome-stable \
#    && rm -rf /var/lib/apt/lists/*

RUN apt install chromium-driver -y

COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY crontab /etc/cron.d/hp-reboot
RUN chmod 0644 /etc/cron.d/hp-reboot
RUN crontab /etc/cron.d/hp-reboot
RUN touch /var/log/cron.log

CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
