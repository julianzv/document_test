import asyncio
import concurrent.futures

from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import time
import random
import product_ids
from data import *
import uuid
import sys
import time

from fastapi.responses import HTMLResponse, FileResponse
from pychromepdf import ChromePDF

PATH_TO_CHROME_EXE = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
from product_ids import *
import functions_oncologico, functions_life_zurich
import tempfile
import os
import pybars
import inspect

# esto es para renderizar el html con handlebars
compiler = pybars.Compiler()


app = FastAPI()

# aqui dejar los templates y las funciones de cada producto
documentos = {
    LIFE_ZURICH_PRODUCT_ID: {
        "template": "templates/index_life_zurich.hbs",
        "functions": functions_life_zurich,
    },
    ONCOLOGICAL_PRODUCT_ID: {
        # para que carguen las imagenes, deben tener su ruta absoluta
        "template": "templates/index_onco_editado.hbs",
        "functions": functions_oncologico,
    },
}

################# CONSUMIDOR #################
datos_recibidos = {}
total_recibidos = 0
cola_mensajes = asyncio.Queue()


async def consume():
    consumer = AIOKafkaConsumer(
        "my_topic", "topic6", bootstrap_servers="localhost:9092", group_id="my-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print("-------------------------------------------------------")
            mensaje = json.loads(msg.value)
            datos_recibidos[mensaje["ID"]] = mensaje
            await cola_mensajes.put(mensaje)
            print("ID recibida:", mensaje["ID"])
            print("-------------------------------------------------------")
            global total_recibidos
            total_recibidos += 1

    finally:
        await consumer.stop()


# con esta ruta se puede consultar si el documento ya está listo para descargar
# ademas entrega los datos de la notificacion de poliza
@app.get("/consultar_datos/{id}")
def consultar_datos_id(id: str):
    if id in datos_recibidos:
        return datos_recibidos[id]
    else:
        return {"message": "ID no encontrado"}


# aqui se genera el PDF y se actualiza el estado y link de descarga
async def render(id: str):
    if id in datos_recibidos:
        product_id = datos_recibidos[id]["productId"]
        datos = datos_recibidos[id]["data"]
        if product_id not in documentos:
            return "Error"
        else:
            template_src = open(documentos[product_id]["template"]).read()
            template = compiler.compile(template_src)
            elements = inspect.getmembers(
                documentos[product_id]["functions"], inspect.isfunction
            )
            helpers = dict(elements)
            rendered_html = template(datos, helpers=helpers)
            cpdf = ChromePDF(PATH_TO_CHROME_EXE)

            pdf_folder = "pdfs"
            os.makedirs(pdf_folder, exist_ok=True)
            pdf_path = os.path.join(pdf_folder, f"insurance_{id}.pdf")

            with open(pdf_path, "wb") as output_file:
                if cpdf.html_to_pdf(rendered_html, output_file):
                    print("PDF generated successfully: {0}".format(pdf_path))
                    datos_recibidos[id]["estado"] = "listo"
                    datos_recibidos[id][
                        "link"
                    ] = f"http://localhost:8000/descargar_pdf/{id}"
                    try:
                        return FileResponse(
                            pdf_path,
                            media_type="application/pdf",
                            filename=f"insurance_{id}.pdf",
                        )
                    except Exception as e:
                        return str(e)
                else:
                    print("Error creating PDF")

            cola_mensajes.task_done()


# Ruta para descargar el PDF para cierto ID, se puede ver en /consultar_datos
@app.get("/descargar_pdf/{id}")
def descargar_pdf_id(id: str):
    if id in datos_recibidos:
        datos_mensaje = datos_recibidos[id]
        if datos_mensaje["estado"] == "listo":
            pdf_folder = "pdfs"
            pdf_path = os.path.join(pdf_folder, f"insurance_{id}.pdf")
            response = FileResponse(pdf_path, media_type="application/pdf")
            response.headers[
                "Content-Disposition"
            ] = f"attachment; filename=insurance_{id}.pdf"
            return response
        else:
            raise HTTPException(
                status_code=400, detail="El documento aún no está listo para descargar"
            )
    else:
        raise HTTPException(status_code=404, detail="ID no encontrado")


#################  PRODUCTOR #################
total_enviados = 0


async def enviar_mensaje():
    p = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await p.start()
    text_file = open("ids.txt", "w")
    topic = "topic6"

    try:
        while True:
            mensaje = {
                "ID": str(uuid.uuid4()),
                "productId": random.choice(
                    [
                        product_ids.LIFE_ZURICH_PRODUCT_ID,
                        product_ids.ONCOLOGICAL_PRODUCT_ID,
                    ]
                ),
                "estado": "pendiente",
                "link": None,
            }

            if mensaje["productId"] == product_ids.LIFE_ZURICH_PRODUCT_ID:
                mensaje["data"] = life_zurich
            elif mensaje["productId"] == product_ids.ONCOLOGICAL_PRODUCT_ID:
                mensaje["data"] = oncological

            text_file.write(mensaje["ID"] + "\n")
            text_file.flush()

            mensaje_json = json.dumps(mensaje)

            try:
                await p.send_and_wait(topic, mensaje_json.encode("utf-8"))
            except Exception as e:
                print(e)
            print("-------------------------------------------------------")
            print("ID enviada:", mensaje["ID"])
            print("-------------------------------------------------------")
            global total_enviados
            total_enviados += 1
            await asyncio.sleep(3)

    except KeyboardInterrupt:
        pass

    p.flush()
    await p.stop()


# temporizador y contador de mensajes, por fines estadisticos

async def temporizador():
    global total_enviados
    global total_recibidos
    start_time = time.time()
    try:
        while True:
            print("-------------------------------------------------------")
            print(f"Total enviados: {total_enviados}")
            print(f"Total recibidos: {total_recibidos}")
            print(f"Tiempo transcurrido: {time.time() - start_time}")
            print("-------------------------------------------------------")
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        pass


# procesadores para la generacion de pdfs, aun tengo que revisar esto
async def procesadores():
    num_processors = 2
    semaforo = asyncio.Semaphore(num_processors)

    async def procesar_mensaje():
        while True:
            async with semaforo:
                mensaje = await cola_mensajes.get()
                await render(mensaje["ID"])

    await asyncio.gather(*[procesar_mensaje() for _ in range(num_processors)])


@app.on_event("startup")
async def startup_event():
    # iniciar consumidor y productor como tareas en segundo plano
    consumer_task = asyncio.create_task(consume())
    productor_task = asyncio.create_task(enviar_mensaje())
    temporizador_task = asyncio.create_task(temporizador())
    procesadores_task = asyncio.create_task(procesadores())


@app.on_event("shutdown")
async def shutdown_event():
    # realizar limpieza o detener tareas en segundo plano si es necesario
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
