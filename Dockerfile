FROM python:3.9-buster

# RUN command #1 to get the CLI
RUN curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash && \
    apt-get install speedtest

ADD requirements.txt /

# RUN command #2 to install requirements; we have two
# to add an extra layer so we don't need to fetch the
# CLI every time.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ADD config.py /
ADD db_models.py /
ADD engine.py /
ADD log.py /
ADD speedtest_to_db.py /

CMD [ "python3", "./speedtest_to_db.py" ]
