import json
from aiokafka import AIOKafkaProducer
import asyncio
import time
import random
import product_ids
from data import *
import uuid

async def enviar_mensaje():
    # Configurar el productor de Kafka
    p = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await p.start()
    text_file = open("ids.txt", "w")

    # Tema al que se enviarán los mensajes
    topic = 'Topic3'

    try:
        while True:
            # Crear el mensaje en formato JSON
            mensaje = {
                "ID": str(uuid.uuid4()),
                "productId": random.choice([product_ids.LIFE_ZURICH_PRODUCT_ID, product_ids.ONCOLOGICAL_PRODUCT_ID]),
                "estado": "pendiente",
                "link": None

            }

            if mensaje["productId"] == product_ids.LIFE_ZURICH_PRODUCT_ID:
                mensaje["data"] = life_zurich
            elif mensaje["productId"] == product_ids.ONCOLOGICAL_PRODUCT_ID:
                mensaje["data"] = oncological

            text_file.write(mensaje["ID"] + "\n")
            text_file.flush()

            # Convertir el mensaje a formato JSON
            mensaje_json = json.dumps(mensaje)

            # Enviar el mensaje al tema
            try:
                await p.send_and_wait(topic, mensaje_json.encode('utf-8'))
            except Exception as e:
                print(e)
            finally:
                await p.stop()

            print("Mensaje enviado:", mensaje_json)
            time.sleep(1)  # Esperar 10 segundos

    except KeyboardInterrupt:
        pass

    p.flush()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(enviar_mensaje())
