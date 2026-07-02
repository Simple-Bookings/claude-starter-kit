# CSK2 Workshop Devcontainer

FROM mcr.microsoft.com/devcontainers/typescript-node:22

# Install system dependencies (cached layer)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    xvfb \
    tmux \
    psmisc \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install global npm packages (pinned versions for reproducibility)
RUN npm install -g \
    @anthropic-ai/claude-code@2.1.197

# Install Python packages
RUN pip3 install --break-system-packages \
    click>=8.1.0 \
    rich>=13.0.0 \
    pyyaml>=6.0 \
    pytest>=8.0.0

# Ensure claude config mount point is owned by node user
RUN mkdir -p /home/node/.claude && chown -R node:node /home/node/.claude

# Run as node user
USER node

# Set up workspace directory
WORKDIR /workspaces

# Labels
LABEL org.opencontainers.image.description="CSK2 Workshop — Claude Code learning environment"
LABEL org.opencontainers.image.version="1.1.0"
