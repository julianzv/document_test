# document_test
bosquejo para servicio de documentos

## Requisitos
- Apache Kafka
- Librerías python: AIOKafka, FastApi, pybars

## Funcionamiento
Antes de ejecutar la aplicación, ejecutar el zookeeper y el server de Kafka
- `bin/zookeeper-server-start.sh config/zookeeper.properties`
- `bin/kafka-server-start.sh config/server.properties`

Para ejecutar la aplicación, se corre el comando:
`uvicorn main:app --reload`
