import socket
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, Response

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Generate a unique identifier based on hostname and a random string
server_id = f"{socket.gethostname()}-{str(uuid.uuid4())[:8]}"


@app.get("/home")
async def home():
    return {
        "message": f"Hello from Server: {server_id}",
        "status": "Successful"
    }


@app.get("/heartbeat")
async def heartbeat():
    return Response(status_code=200)
