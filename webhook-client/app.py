from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Union # Union is more modern than Optional for type hinting

# --- FastAPI Instance Creation ---
app = FastAPI(
    title="Example POST API",
    description="A simple example of a POST endpoint with FastAPI",
    version="1.0.0",
)

# --- POST Endpoint Definition ---
@app.post("/test/", status_code=201)
async def create_item(request: Request):
    """
    Endpoint that accepts arbitrary JSON payload without Pydantic validation.
    
    Receives any JSON data in the request body and returns it.
    """
    try:
        # Parse the raw request body to ensure we get all fields
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8')
        
        # Use Python's built-in json module for more control
        import json
        json_body = json.loads(body_str)
        print("test")
        print(f"Data received: {json_body}")  # Print received data to the server console
        
        # Verify explicitly that userSshKey is present
        if 'userSshKey' in json_body:
            print(f"userSshKey found: {json_body['userSshKey'][:10]}...")  # Print only first 10 chars for security
        else:
            print("Warning: userSshKey field is missing in the payload")
        
        # Return the received data as confirmation
        return {"message": "Got it", "request_payload": json_body}
    except Exception as e:
        # Handle errors in parsing JSON
        return JSONResponse(
            status_code=400,
            content={"message": f"Invalid JSON: {str(e)}"},
        )

# --- (Optional) Basic GET endpoint to test if the server is running ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Example API!"}

# Note: You don't need to include server startup code here.
# Uvicorn will handle importing and running the 'app' object.