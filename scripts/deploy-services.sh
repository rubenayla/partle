#!/bin/bash

# Partle systemd services deployment script
# This script installs and enables Partle services on the Hetzner server

set -e

echo "🚀 Deploying Partle systemd services..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   exit 1
fi

# Create log directory
echo -e "${YELLOW}Creating log directory...${NC}"
mkdir -p /var/log/partle
chown root:root /var/log/partle
chmod 755 /var/log/partle

# Copy service files to systemd directory
echo -e "${YELLOW}Installing systemd service files...${NC}"
cp systemd/partle-backend.service /etc/systemd/system/
cp systemd/partle-frontend.service /etc/systemd/system/
cp systemd/partle-mcp.service /etc/systemd/system/

# Set proper permissions
chmod 644 /etc/systemd/system/partle-*.service

# Reload systemd daemon
echo -e "${YELLOW}Reloading systemd daemon...${NC}"
systemctl daemon-reload

# Enable services (but don't start them yet)
echo -e "${YELLOW}Enabling services...${NC}"
systemctl enable partle-backend.service
systemctl enable partle-frontend.service
systemctl enable partle-mcp.service

# Check service status
echo -e "${YELLOW}Service status:${NC}"
for service in partle-backend partle-frontend partle-mcp; do
    status=$(systemctl is-enabled $service)
    echo -e "  $service: ${GREEN}$status${NC}"
done

echo -e "${GREEN}✅ Services deployed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  • Start backend: sudo systemctl start partle-backend"
echo "  • Start frontend: sudo systemctl start partle-frontend"
echo "  • Start MCP server: sudo systemctl start partle-mcp"
echo ""
echo "  • View logs: sudo journalctl -u partle-backend -f"
echo "  • Check status: sudo systemctl status partle-backend"
echo ""
echo -e "${YELLOW}Or start all services at once:${NC}"
echo "  sudo systemctl start partle-backend partle-frontend partle-mcp"