
#aa#
docker build -t cmc .
docker run -itd --name cmc1 -v /home/bot/cmc/config.json:/app/config.json cmc