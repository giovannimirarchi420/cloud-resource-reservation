---
sidebar_position: 2
---

# Webhooks Integration Guide

Learn how to integrate external resources with the Cloud Resource Reservation System using custom webhooks.

## User Story: Alice's Resource Integration

Meet **Alice**, a cloud infrastructure engineer who needs to integrate a new type of computing resource (a specialized GPU cluster) with the reservation system. Alice wants users to be able to reserve these GPU resources through the web interface, and she wants the system to automatically configure the resources when a reservation is made.

### Alice's Requirements

1. **Web UI Configuration**: Alice should be able to configure the webhook endpoint from the reservation system's web interface
2. **Automatic Resource Setup**: When a user makes a reservation, the system should automatically provision the GPU cluster
3. **Status Updates**: The webhook should provide real-time status updates about the resource provisioning
4. **Security**: The integration should be secure and authenticated

## Configuring a Webhook from the UI

### Step 1: Access the Webhook Configuration

1. Log into the Cloud Resource Reservation System
2. Navigate to **Settings** → **Webhook Integrations**
3. Click **"Add New Webhook"**

### Step 2: Configure Webhook Details

Fill in the webhook configuration form:

- **Webhook Name**: `GPU Cluster Manager`
- **Endpoint URL**: `https://your-service.com/api/webhook`
- **Resource Type**: `gpu-cluster`
- **Authentication Method**: `API Key` or `OAuth 2.0`
- **Event Triggers**: 
  - ✅ Reservation Created
  - ✅ Reservation Modified
  - ✅ Reservation Cancelled

### Step 3: Test the Integration

Use the built-in test feature to verify your webhook:

1. Click **"Test Webhook"**
2. The system sends a test payload to your endpoint
3. Verify the response and troubleshoot if needed

## Python Webhook Example

Here's a complete Python example that Alice can use as a starting point for her GPU cluster webhook:

### FastAPI Webhook Server

```python
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import hashlib
import hmac
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GPU Cluster Webhook",
    description="Webhook service for managing GPU cluster reservations",
    version="1.0.0",
)

# Configuration
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")
GPU_CLUSTER_API_BASE = os.getenv("GPU_CLUSTER_API", "https://gpu-cluster-api.example.com")

class ReservationPayload(BaseModel):
    reservation_id: str
    user_id: str
    resource_type: str
    start_time: datetime
    end_time: datetime
    user_ssh_key: str
    additional_config: Dict[str, Any] = {}

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify the webhook signature for security"""
    if not signature.startswith("sha256="):
        return False
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    received_signature = signature[7:]  # Remove 'sha256=' prefix
    return hmac.compare_digest(expected_signature, received_signature)

@app.post("/api/webhook/reservation")
async def handle_reservation_webhook(
    request: Request,
    x_webhook_signature: Optional[str] = Header(None, alias="X-Webhook-Signature")
):
    """
    Handle reservation webhook events from the Cloud Resource Reservation System
    """
    try:
        # Get raw request body for signature verification
        body_bytes = await request.body()
        
        # Verify webhook signature for security
        if x_webhook_signature:
            if not verify_webhook_signature(body_bytes, x_webhook_signature):
                raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Parse the JSON payload
        import json
        payload_data = json.loads(body_bytes.decode('utf-8'))
        
        # Extract reservation details
        reservation = ReservationPayload(**payload_data)
        
        logger.info(f"Processing reservation: {reservation.reservation_id}")
        
        # Handle different resource types
        if reservation.resource_type == "gpu-cluster":
            result = await provision_gpu_cluster(reservation)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported resource type: {reservation.resource_type}"
            )
        
        return {
            "status": "success",
            "reservation_id": reservation.reservation_id,
            "message": "Resource provisioned successfully",
            "details": result
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def provision_gpu_cluster(reservation: ReservationPayload) -> Dict[str, Any]:
    """
    Provision a GPU cluster for the reservation
    This is where Alice implements her specific GPU cluster logic
    """
    logger.info(f"Provisioning GPU cluster for reservation {reservation.reservation_id}")
    
    # Example GPU cluster provisioning logic
    cluster_config = {
        "cluster_id": f"gpu-cluster-{reservation.reservation_id}",
        "user_id": reservation.user_id,
        "ssh_key": reservation.user_ssh_key,
        "start_time": reservation.start_time.isoformat(),
        "end_time": reservation.end_time.isoformat(),
        "gpu_type": reservation.additional_config.get("gpu_type", "nvidia-a100"),
        "gpu_count": reservation.additional_config.get("gpu_count", 4),
        "memory_gb": reservation.additional_config.get("memory_gb", 512),
    }
    
    # Here Alice would integrate with her actual GPU cluster management system
    # For example:
    # - Call GPU cluster API to create cluster
    # - Configure networking and security groups
    # - Set up user access and SSH keys
    # - Schedule automatic cleanup at end_time
    
    # Simulate cluster creation
    cluster_ip = "192.168.100.10"  # This would come from actual provisioning
    cluster_port = 22
    
    # Return cluster details that will be sent back to the reservation system
    return {
        "cluster_id": cluster_config["cluster_id"],
        "access_info": {
            "ip_address": cluster_ip,
            "port": cluster_port,
            "username": f"user-{reservation.user_id}",
            "connection_command": f"ssh user-{reservation.user_id}@{cluster_ip}"
        },
        "cluster_config": cluster_config,
        "estimated_ready_time": "5 minutes"
    }

@app.post("/api/webhook/reservation/cancel")
async def handle_reservation_cancellation(
    request: Request,
    x_webhook_signature: Optional[str] = Header(None, alias="X-Webhook-Signature")
):
    """
    Handle reservation cancellation events
    """
    try:
        body_bytes = await request.body()
        
        if x_webhook_signature:
            if not verify_webhook_signature(body_bytes, x_webhook_signature):
                raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        import json
        payload_data = json.loads(body_bytes.decode('utf-8'))
        
        reservation_id = payload_data.get("reservation_id")
        cluster_id = f"gpu-cluster-{reservation_id}"
        
        logger.info(f"Cancelling reservation: {reservation_id}")
        
        # Here Alice would implement cluster cleanup logic
        # - Stop GPU cluster instances
        # - Release allocated resources
        # - Clean up networking configuration
        # - Remove user access
        
        return {
            "status": "success",
            "reservation_id": reservation_id,
            "message": "GPU cluster successfully destroyed",
            "cluster_id": cluster_id
        }
        
    except Exception as e:
        logger.error(f"Error cancelling reservation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "gpu-cluster-webhook"}

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "GPU Cluster Webhook Service",
        "version": "1.0.0",
        "description": "Webhook service for managing GPU cluster reservations",
        "endpoints": {
            "reservation": "/api/webhook/reservation",
            "cancellation": "/api/webhook/reservation/cancel",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Requirements File

Create a `requirements.txt` file for the webhook service:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
requests==2.31.0
```

### Docker Configuration

Create a `Dockerfile` for easy deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Advanced Webhook Features

### Event Types

The webhook system supports various event types:

- `reservation.created` - New reservation created
- `reservation.updated` - Reservation modified
- `reservation.cancelled` - Reservation cancelled
- `reservation.expired` - Reservation time expired
- `user.access_requested` - User requesting access to resource

### Webhook Retry Logic

The system automatically retries failed webhook calls:

- **Retry attempts**: 3 times
- **Backoff strategy**: Exponential (1s, 2s, 4s)
- **Timeout**: 30 seconds per request

### Webhook Security

Best practices for secure webhook implementation:

1. **Signature Verification**: Always verify webhook signatures
2. **HTTPS Only**: Use HTTPS endpoints for production
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Input Validation**: Validate all incoming data
5. **Secret Management**: Store webhook secrets securely

## Testing Your Webhook

### Manual Testing with curl

```bash
# Test webhook endpoint
curl -X POST https://your-webhook.com/api/webhook/reservation \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=your-signature" \
  -d '{
    "reservation_id": "test-123",
    "user_id": "alice",
    "resource_type": "gpu-cluster",
    "start_time": "2024-01-01T10:00:00Z",
    "end_time": "2024-01-01T18:00:00Z",
    "user_ssh_key": "ssh-rsa AAAAB3NzaC1yc2E...",
    "additional_config": {
      "gpu_type": "nvidia-a100",
      "gpu_count": 4
    }
  }'
```

### Integration Testing

Use the built-in webhook testing feature in the reservation system:

1. Go to **Settings** → **Webhook Integrations**
2. Select your configured webhook
3. Click **"Send Test Event"**
4. Review the response and logs

## Troubleshooting

### Common Issues

1. **Signature Verification Failures**: Check webhook secret configuration
2. **Timeout Errors**: Ensure webhook responds within 30 seconds
3. **SSL Certificate Issues**: Verify HTTPS certificate is valid
4. **Rate Limiting**: Check if your webhook is being rate limited

### Debugging Tips

- Enable detailed logging in your webhook service
- Use webhook testing tools like ngrok for local development
- Monitor webhook delivery status in the reservation system dashboard
- Check webhook response codes and error messages

## Next Steps

After implementing your webhook:

1. **Monitor Performance**: Track webhook response times and error rates
2. **Scale if Needed**: Use load balancers for high-traffic scenarios
3. **Add Monitoring**: Implement health checks and alerting
4. **Documentation**: Document your webhook API for team members
5. **Security Review**: Regular security audits of webhook implementations

For more advanced webhook patterns and examples, check out our [GitHub repository](https://github.com/giovannimirarchi420/cloud-resource-reservation).