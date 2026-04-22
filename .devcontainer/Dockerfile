# Claude Starter Kit Devcontainer

FROM mcr.microsoft.com/devcontainers/typescript-node:22

# Install system dependencies (cached layer)
RUN apt-get update && apt-get install -y \
    xvfb \
    tmux \
    psmisc \
    && rm -rf /var/lib/apt/lists/*

# Install global npm packages (pinned versions for reproducibility)
RUN npm install -g \
    pm2@6.0.14 \
    @anthropic-ai/claude-code@2.1.116 \
    @github/copilot@1.0.34

# Ensure claude config mount point is owned by node user so the named
# volume initializes with correct permissions on first use
RUN mkdir -p /home/node/.claude && chown -R node:node /home/node/.claude

# Kør som node-bruger
USER node

# Set up workspace directory
WORKDIR /workspaces/claude-starter-kit

# Labels for tracking
LABEL org.opencontainers.image.source="https://github.com/Simple-Bookings/claude-starter-kit"
LABEL org.opencontainers.image.description="Claude Starter Kit devcontainer with optimized caching"
LABEL org.opencontainers.image.version="0.1.3"
