FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Set up a non-root user
RUN useradd -m -u 1000 user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy the rest of the application
COPY --chown=user . .
USER user

# Expose the port
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
