# Use UV python for the base image
FROM python:3.12-slim
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Receive the version from GitHub Actions
ARG WHISPER_SUBTITLES_VERSION

# Set it as an ENV so it's available at runtime
ENV WHISPER_SUBTITLES_VERSION=$WHISPER_SUBTITLES_VERSION

# Install curl and clean up apt cache to keep the image slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Run uv to build the application dependencies
WORKDIR /app
COPY . .
RUN uv sync --frozen

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Run
CMD ["uv", "run", "python", "main.py"]