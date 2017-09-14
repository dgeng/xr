FROM busybox

WORKDIR /app
COPY app /app
VOLUME /data

CMD ["./filebeat", "-e", "-c", "filebeat.yml", "-d", "public"]
