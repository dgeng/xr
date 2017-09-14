FROM busybox

VOLUME /data

WORKDIR /app
COPY app /app

CMD ["./filebeat", "-e", "-c", "filebeat.yml", "-d", "public"]
