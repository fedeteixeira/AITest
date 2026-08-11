# Build an image with the Python 3.12 image
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to `/app`
WORKDIR /app

# Install `uv`
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy uv package requirements
COPY pyproject.toml ./
COPY uv.lock ./

# Install the Python dependencies with uv
RUN uv sync --locked --no-install-project

# Copy the current directory `.` in the project to the workdir `.` in the image
COPY . .

# Install the Project
RUN uv sync --locked

# Set the default command for the container
CMD ["uv", "run", "aitest"]