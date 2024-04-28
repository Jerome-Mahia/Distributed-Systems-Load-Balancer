from fastapi import FastAPI, Response
import socket
import uuid

app = FastAPI()

server_name = f"{socket.gethostname()-{str(uuid.uuid4())[:8]}}"

@app.get("/home")
def home():
    return {"Hello": "World" , "server_name": server_name}

@app.get("/heartbeat")
def heartbeat():
    return Response (content="OK", status_code=200)