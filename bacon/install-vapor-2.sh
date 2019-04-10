# Install CURL
apt-get update && \
    apt-get -y install curl && \
    rm -rf /var/lib/apt/lists/*;

# Get Vapor repo including Swift
curl -sL https://apt.vapor.sh | bash;

# Installing Swift & Vapor
apt-get update && \
    apt-get -y install swift vapor && \
    rm -rf /var/lib/apt/lists/*;
