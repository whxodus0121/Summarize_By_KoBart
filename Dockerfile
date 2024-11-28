# Step 1: Use Python 3.9 Slim as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy project files into the container
COPY . /app

# Step 4: Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libffi-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Step 5: Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-deps git+https://github.com/SKT-AI/KoBART#egg=kobart && \
    rm -rf ~/.cache/huggingface

# Step 6: Expose port 8000 for FastAPI
EXPOSE 8000

# Step 7: Command to run the FastAPI application
CMD ["uvicorn", "Summarize_By_KoBart:app", "--host", "0.0.0.0", "--port", "8000"]

