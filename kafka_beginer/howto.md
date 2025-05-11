
download a GUI tool
https://kafkatool.com/download.html

`docker ps` to list the kafka containers id

create a topic
`docker exec -it <kafka-container-id> kafka-topics --create --bootstrap-server kafka-1:9092,kafka-2:9092 --replication-factor 1 --partitions 1 --topic my-topic`

check topic 
`docker exec -it <kafka-container-id> kafka-topics --bootstrap-server kafka-1:9092,kafka-2:9092 --list`

start the consumer
`docker exec -it <kafka-container-id> kafka-topics --bootstrap-server kafka-1:9092,kafka-2:9092 --describe --topic my-topic`

send a message
`docker exec -it <kafka-container-id> kafka-console-producer --broker-list kafka-1:9092,kafka-2:9092 --topic my-topic`


### 为特定主题设置保留策略
```
kafka-configs --bootstrap-server localhost:9092 \
 --entity-type topics --entity-name aio-topic \
 --alter --add-config retention.ms=3600000
```
















