#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Main Script
main() {
    print_header "Test Suite Runner - API Backend Tests"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_warning ".env not found!"
        print_info "Creating .env from .env.example..."
        cp .env.example .env
        print_success ".env created. Please edit it with your credentials."
    fi
    
    # Check if requirements are installed
    print_info "Checking dependencies..."
    python -c "import requests, pytest, dotenv" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_warning "Dependencies not installed!"
        print_info "Installing requirements..."
        pip install -r requirements.txt
    else
        print_success "Dependencies OK"
    fi
    
    # Check API connectivity
    print_info "Checking API connectivity..."
    curl -s http://localhost:7999/swagger/index.html > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "API is running at http://localhost:7999"
    else
        print_error "Cannot connect to API at http://localhost:7999"
        print_info "Make sure the API server is running!"
        exit 1
    fi
    
    # Display menu
    echo ""
    print_header "Select Test Mode"
    echo "1) Quick Test (Single endpoint) - Fast ⚡"
    echo "2) Smoke Tests (All resources) - Medium ⏱️"
    echo "3) Full Test Suite (All endpoints) - Complete ✅"
    echo "4) Specific Resource"
    echo "5) Test with Coverage"
    echo "6) View Test Summary"
    echo "7) Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            print_info "Running quick test..."
            pytest tests/api/test_teacher.py::TestTeacherAPI::test_teacher_login_success -v
            ;;
        2)
            print_info "Running smoke tests..."
            pytest tests/api/ -m smoke -v
            ;;
        3)
            print_info "Running full test suite (176 tests)..."
            pytest tests/api/ -v
            ;;
        4)
            echo ""
            echo "Available resources:"
            ls tests/api/test_*.py | sed 's|tests/api/test_||g' | sed 's|.py||g' | nl
            read -p "Enter resource number: " resource_num
            resource=$(ls tests/api/test_*.py | sed -n "${resource_num}p")
            if [ -z "$resource" ]; then
                print_error "Invalid selection"
                exit 1
            fi
            print_info "Running tests for $(basename $resource)..."
            pytest "$resource" -v
            ;;
        5)
            print_info "Running tests with coverage..."
            pytest tests/api/ --cov=tests --cov-report=html --cov-report=term-missing
            print_success "Coverage report generated in htmlcov/index.html"
            ;;
        6)
            print_info "Test Summary:"
            echo ""
            find tests/api -name "test_*.py" -type f | sort | while read file; do
                count=$(grep -c "def test_" "$file" 2>/dev/null || echo "0")
                echo "  $(basename $file): $count tests"
            done
            echo ""
            total=$(find tests/api -name "test_*.py" -type f | xargs grep -c "def test_" 2>/dev/null | awk -F: '{sum+=$NF} END {print sum}')
            print_success "Total: $total tests"
            ;;
        7)
            print_info "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    echo ""
    print_success "Done!"
}

# Run main function
main
