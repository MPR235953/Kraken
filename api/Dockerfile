FROM python:3.10-slim
WORKDIR /api
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN apt-get update && apt-get -y install cron
RUN echo "15 00 * * * /usr/local/bin/python /api/data_loader.py" > /etc/cron.d/daily-data-loader
RUN chmod 0644 /etc/cron.d/daily-data-loader
RUN crontab /etc/cron.d/daily-data-loader
ENTRYPOINT ["./start_service.sh"]