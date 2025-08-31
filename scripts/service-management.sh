#!/bin/bash

# Partle service management script
# Provides easy commands to manage all Partle services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SERVICES=("partle-backend" "partle-frontend" "partle-mcp")

print_usage() {
    echo -e "${BLUE}Partle Service Management${NC}"
    echo ""
    echo "Usage: $0 {start|stop|restart|status|logs|enable|disable|deploy}"
    echo ""
    echo "Commands:"
    echo "  start    - Start all Partle services"
    echo "  stop     - Stop all Partle services"
    echo "  restart  - Restart all Partle services"
    echo "  status   - Show status of all services"
    echo "  logs     - Show logs from all services (use -f to follow)"
    echo "  enable   - Enable all services to start on boot"
    echo "  disable  - Disable all services from starting on boot"
    echo "  deploy   - Deploy/update systemd service files"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs -f"
    echo "  $0 status"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}This script must be run as root${NC}"
        exit 1
    fi
}

service_action() {
    local action=$1
    echo -e "${YELLOW}${action^}ing Partle services...${NC}"
    
    for service in "${SERVICES[@]}"; do
        echo -e "  ${action^}ing $service..."
        systemctl $action $service
    done
    
    echo -e "${GREEN}✅ All services ${action}ed successfully${NC}"
}

show_status() {
    echo -e "${BLUE}📊 Partle Services Status:${NC}"
    echo ""
    
    for service in "${SERVICES[@]}"; do
        status=$(systemctl is-active $service)
        enabled=$(systemctl is-enabled $service)
        
        if [[ $status == "active" ]]; then
            status_color=$GREEN
            status_icon="🟢"
        elif [[ $status == "inactive" ]]; then
            status_color=$YELLOW
            status_icon="🟡"
        else
            status_color=$RED
            status_icon="🔴"
        fi
        
        echo -e "  $status_icon $service: ${status_color}$status${NC} ($enabled)"
    done
    
    echo ""
    echo -e "${BLUE}Recent logs (last 5 lines):${NC}"
    for service in "${SERVICES[@]}"; do
        echo -e "${YELLOW}--- $service ---${NC}"
        journalctl -u $service -n 5 --no-pager -q || echo "  No logs available"
        echo ""
    done
}

show_logs() {
    local follow_flag=""
    if [[ "$2" == "-f" ]]; then
        follow_flag="-f"
        echo -e "${BLUE}Following logs from all Partle services (Ctrl+C to exit)...${NC}"
    else
        echo -e "${BLUE}Recent logs from all Partle services:${NC}"
    fi
    
    # Combine logs from all services
    journalctl -u partle-backend -u partle-frontend -u partle-mcp $follow_flag --no-pager
}

deploy_services() {
    echo -e "${YELLOW}Deploying Partle systemd services...${NC}"
    
    # Check if deploy script exists
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DEPLOY_SCRIPT="$SCRIPT_DIR/deploy-services.sh"
    
    if [[ -f "$DEPLOY_SCRIPT" ]]; then
        bash "$DEPLOY_SCRIPT"
    else
        echo -e "${RED}❌ Deploy script not found at $DEPLOY_SCRIPT${NC}"
        exit 1
    fi
}

# Main script logic
case "${1:-}" in
    start)
        check_root
        service_action start
        ;;
    stop)
        check_root
        service_action stop
        ;;
    restart)
        check_root
        service_action restart
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$@"
        ;;
    enable)
        check_root
        service_action enable
        ;;
    disable)
        check_root
        service_action disable
        ;;
    deploy)
        check_root
        deploy_services
        ;;
    *)
        print_usage
        exit 1
        ;;
esac