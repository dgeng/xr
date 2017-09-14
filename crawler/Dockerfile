FROM python:2.7

ADD requirements.txt /
RUN pip install -r /requirements.txt

VOLUME /data

WORKDIR /app
COPY app /app

CMD ["python", "crawler.py"]
# CMD ["/bin/bash"]
