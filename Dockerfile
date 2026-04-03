# Use official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies including tmux
RUN apt-get update && apt-get install -y \
    tmux \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies (FAISS needs libomp for cpu optimization sometimes, but slim works mostly)
# We also upgrade pip and install CPU-only PyTorch first to save space
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code

# Set permissions for the directory to run safely on HuggingFace Free Tier (which doesn't run as root)
RUN chmod -R 777 /code

# Expose port 7860 which is required by HuggingFace Spaces
EXPOSE 7860

# Command to run the FastApi application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
