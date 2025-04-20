# Stage 1: Builder stage for compiling Python dependencies
FROM python:3.11-slim AS builder


# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.11-slim


ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

# Install PostgreSQL 16 client and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    git \
    nano &&\
    # Add PostgreSQL repository
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/postgresql.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client-16 && \
    # Clean up
    apt-get purge -y --auto-remove curl gnupg2 lsb-release && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local


WORKDIR /django

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000","-w","8", "core.wsgi"]