# Claude Starter Kit Devcontainer

FROM mcr.microsoft.com/devcontainers/typescript-node:22

# Install system dependencies (cached layer)
RUN apt-get update && apt-get install -y \
    xvfb \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Install global npm packages (pinned versions for reproducibility)
RUN npm install -g \
    pm2@6.0.14 \
    @anthropic-ai/claude-code@2.1.116

# Kør som node-bruger (samme som GitHub Codespaces)
USER node

# Set up workspace directory
WORKDIR /workspaces/claude-starter-kit

# Labels for tracking
LABEL org.opencontainers.image.source="https://github.com/Simple-Bookings/claude-starter-kit"
LABEL org.opencontainers.image.description="Claude Starter Kit devcontainer with optimized caching"
LABEL org.opencontainers.image.version="phase1"
