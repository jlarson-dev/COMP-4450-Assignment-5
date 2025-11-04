IMAGE_NAME := monitoring-app
LOGS_DIR := $(PWD)/../logs

build:
	@echo "Building Docker image $(IMAGE_NAME)"
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running Docker container with logs mounted"
	docker run --rm -p 8501:8501 -v $(LOGS_DIR):/app/logs --name monitoring-app $(IMAGE_NAME)

clean:
	@echo "Removing Docker image"
	docker rmi $(IMAGE_NAME) || true