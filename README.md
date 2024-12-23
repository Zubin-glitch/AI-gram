# AI-Gram - Stable Diffusion Experiment

## Objective

This project sets up a backend API using [Modal](https://modal.com/) that generates images from input text prompts using the `stabilityai/sdxl-turbo` model from [HuggingFace](https://huggingface.co/). The API is optimized for low latency and high-quality image generation leveraging serverless Nvidia A10G GPUs.

## Features

- **Text-to-Image Generation:** Convert textual prompts into high-quality images.
- **Low Latency:** Optimized for quick response times.
- **Secure API:** Protect endpoints with API keys.
- **Health Monitoring:** Health check endpoint to monitor service status.
- **Automatic Keep-Alive:** Prevents cold starts with scheduled warm-up requests.

## Getting Started

### Prerequisites

- **Python 3.9** or higher
- **Modal Account:** [Sign up](https://modal.com/) if you don’t have one.
- **HuggingFace API Token:** [Get your token](https://huggingface.co/settings/tokens)
- **Git:** Installed on your machine

### Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/https://github.com/Zubin-glitch/AI-gram.git
    cd backend
    ```

2. **Set Up Virtual Environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Secrets:**

    - **Modal Secrets:** Add your HuggingFace API token and your custom API key in Modal’s secret management.
    - **Environment Variables:** Ensure that secrets are managed securely and are not hard-coded.

### Backend Usage

1. **Deploy the Application:**

    ```bash
    python3 -m modal setup
    modal deploy main.py
    ```

2. **Access the API Endpoints:**

    - **Generate Image:** `POST https://your-modal-app-url/generate`
    - **Health Check:** `GET https://your-modal-app-url/health`

### Frontend Usage:

- Specified in frontend readme file.

## Contributing

Contributions are welcome! Please open issues and submit pull requests for any improvements or bug fixes.

