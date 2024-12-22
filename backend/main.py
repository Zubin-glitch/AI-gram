"""
    Objective: This python code sets up the backend API using Modal
    that generates images from an input text prompt.
"""
# Import necessary libraries.
import io
import modal
from fastapi import Response, HTTPException, Query, Request
from datetime import datetime, timezone
import requests
import os

def download_model():
    from diffusers import AutoPipelineForText2Image
    import torch

    AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        torch_dtype=torch.float16,
        variant="fp16"
    )

image = (modal.Image.debian_slim()
         .pip_install("fastapi[standard]", "transformers", "accelerate", "diffusers[torch]",
                      "requests")
         .run_function(download_model))
app = modal.App("stable-diffusion-experiment", image=image)

@app.cls(
    image=image,
    gpu="A10G",
    container_idle_timeout=300,
    secrets=[modal.Secret.from_name("dev-secret"), modal.Secret.from_name("HF_API_KEY")]
)

class Model:

    # @app.function(secrets=[modal.Secret.from_name("dev-secret")])
    # def f():
    #     print(os.environ["MODAL_API_KEY_1"])
    
    @modal.build()
    @modal.enter()
    def load_model_weights(self):
        from diffusers import AutoPipelineForText2Image
        import torch

        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16,
            variant="fp16"
        )
        # ensure that the container is leveraging GPU memory
        self.pipe.to("cuda")
        self.API_KEY=os.environ["MODAL_API_KEY_1"]

    @modal.web_endpoint()
    def generate(self, request: Request, prompt: str=Query(..., \
        description="The prompt for image generation")):
        api_key = request.headers.get("X-API-Key")
        if api_key != self.API_KEY:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized Access"
            )
        
        image = self.pipe(prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        
        # TODO:Add validation result type.
        return Response(content=buffer.getvalue(), media_type="image/jpeg")
    
    @modal.web_endpoint()
    def health(self):
        """Lightweight endpoint for keeping container warm
            during phases of inactivity.
        """
        return {"status": "health-check", "timestamp": datetime.now(timezone.utc).isoformat()}
    

# Warm-up function that runs a CRON expresion every minutes to prevent cold-starting
# of the application due to inactivity.

@app.function(
    schedule=modal.Cron("*/5 * * * *"),
    secrets=[modal.Secret.from_name("dev-secret"), modal.Secret.from_name("HF_API_KEY")]
)
def keep_warm():
    health_url = "https://zubin-glitch--stable-diffusion-experiment-model-health.modal.run"
    generate_url = "https://zubin-glitch--stable-diffusion-experiment-model-generate.modal.run"
    
    # Check the health endpoint (No API Key required)
    health_response = requests.get(health_url)
    print(f"Health check at: {health_response.json()['timestamp']}")

    # Make a test request to the generate-endpoint with API key
    headers = {"X-API-Key": os.environ["MODAL_API_KEY_1"]}
    generate_response = requests.get(generate_url, headers=headers)
    print(f"Generate endpoint is running successfully at: {datetime.now(timezone.utc).isoformat()}")
    
