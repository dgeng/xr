FROM vekerdyb/rpi-python3

ADD requirements.txt /
RUN pip install -r /requirements.txt

VOLUME /data

WORKDIR /app
COPY app /app

CMD ["python3", "crawler.py"]
# CMD ["/bin/bash"]
