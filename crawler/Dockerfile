FROM python:2.7

RUN pip install schedule

VOLUME /data

WORKDIR /app
COPY app /app

CMD ["python", "crawler.py"]
# CMD ["/bin/bash"]
