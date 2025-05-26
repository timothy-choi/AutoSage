from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from StreamIngestorHelper import start_stream_ingestor, stop_stream_ingestor
import logging

app = FastAPI()

@app.post("/stream/ingest/start")
def api_start_stream(
    name: str = Query(...),
    topic: str = Query(...),
    bootstrap_servers: str = Query("localhost:9092"),
    group_id: str = Query("stream-ingestor"),
    auto_offset_reset: str = Query("latest")
):
    try:
        def print_callback(msg):
            logging.info(f"Received message: {msg}")

        started = start_stream_ingestor(
            name=name,
            topic=topic,
            callback=print_callback,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset
        )
        return {"status": "started" if started else "already running"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/stream/ingest/stop")
def api_stop_stream(name: str = Query(...)):
    try:
        stopped = stop_stream_ingestor(name)
        return {"status": "stopped" if stopped else "not found or already stopped"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})