IMAGE_NAME := movie-sentiment-api
LOGS_DIR := $(PWD)/../logs

build:
	@echo "Building Docker image $(IMAGE_NAME)"
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running Docker container with logs mounted"
	docker run --rm -p 8000:8000 -v $(LOGS_DIR):/app/logs --name move-sentiment-api $(IMAGE_NAME)

clean:
	@echo "Removing Docker image"
	docker rmi $(IMAGE_NAME) || true
