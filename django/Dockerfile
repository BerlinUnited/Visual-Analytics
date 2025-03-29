# Stage 1: Builder stage for compiling Python dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONUNBUFFERED=1
# Install build dependencies and PostgreSQL development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    gcc \
    python3-dev \
    libpq-dev && \
    # Add PostgreSQL repository
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/postgresql.list && \
    apt-get update && \
    # Clean up apt
    apt-get purge -y --auto-remove curl gnupg2 lsb-release && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Stage 2: Final runtime image
FROM python:3.11-slim

# Install runtime dependencies (PostgreSQL client 16 and libpq5)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    git \
    nano \
    lsb-release && \
    # Add PostgreSQL repository
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/postgresql.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client-16 \
    libpq5 && \
    # Remove pip and Python package management tools
    apt-get purge -y python3-pip python3-setuptools && \
    # Clean up apt
    apt-get purge -y --auto-remove curl gnupg2 lsb-release && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local

RUN mkdir /django
WORKDIR /django
# Copy application code
COPY . .

# Add user-installed Python packages to PATH
ENV PATH=/root/.local/bin:$PATH
    

# Verify installations
RUN python --version && \
    psql --version
EXPOSE 8000    
CMD ["gunicorn", "--bind", "0.0.0.0:8000","-w","8", "core.wsgi"]