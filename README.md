# document_test
bosquejo para servicio de documentos

## Requisitos
- Apache Kafka
- Librerías python: AIOKafka, FastApi, pybars, pychromepdf

## Funcionamiento
Antes de ejecutar la aplicación, ejecutar el zookeeper y el server de Kafka
- `bin/zookeeper-server-start.sh config/zookeeper.properties`
- `bin/kafka-server-start.sh config/server.properties`

Para ejecutar la aplicación, se corre el comando:
- `uvicorn main:app --reload`

La aplicación recibe datos para dos tipos de producto: seguro oncológico y seguro de vida Zurich. Estos tienen sus templates y funciones propias, adaptadas desde el servicio original de documentos. 

Tiene una estructura productor-consumidor, y guarda los registros en un diccionario. 

Los pdfs se descargan en la carpeta /pdfs, se generan utilizando la librería pychromepdf. 

Una vez esté ejecutandose la aplicación, empezará a enviar y recibir mensajes. Para facilitar la lectura, se imprimen en consola los ids de los objetos.

Para consultar el estado del documento creado, se utiliza la ruta /consultar_datos/{id}, la cual a través de un json indica si el documento ya está listo y su link de descarga.

Se agregó también un temporizador y contador de mensajes enviados/recibidos, para revisar el rendimiento. 




