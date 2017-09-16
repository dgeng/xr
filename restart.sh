docker stop $(docker ps -q)
docker rm filebeat crawler

docker build -t jgeng/crawler crawler
docker build -t jgeng/filebeat filebeat

docker run -d --restart unless-stopped --name crawler jgeng/crawler
docker run -d --restart unless-stopped --name filebeat --volumes-from crawler jgeng/filebeat
