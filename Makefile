# Root Makefile

MONITORING_IMAGE := monitoring-app
API_IMAGE := movie-sentiment-api

MONITORING_DIR := ./monitoring
API_DIR := ./api
LOGS_DIR := $(CURDIR)/logs

.PHONY: all build run clean stop

all: build


build: build-monitoring build-api

build-monitoring:
	@echo "Building Monitoring Dashboard image..."
	docker build -t $(MONITORING_IMAGE) $(MONITORING_DIR)

build-api:
	@echo "Building API image..."
	docker build -t $(API_IMAGE) $(API_DIR)

run: run-monitoring run-api
	@echo "✅ Both containers are running."

run-monitoring:
	@echo "Running Monitoring Dashboard..."
	docker run -d --rm -p 8501:8501 --name $(MONITORING_IMAGE) $(MONITORING_IMAGE)

run-api:
	@echo "Running API container with logs mounted..."
	docker run -d --rm -p 8000:8000 -v "$(LOGS_DIR):/app/logs" --name $(API_IMAGE) $(API_IMAGE)

stop:
	@echo "Stopping containers if running..."
	-docker stop $(MONITORING_IMAGE) 2>nul || true
	-docker stop $(API_IMAGE) 2>nul || true

clean:
	@echo "Removing Docker images..."
	-docker rmi $(MONITORING_IMAGE) 2>nul || true
	-docker rmi $(API_IMAGE) 2>nul || true
