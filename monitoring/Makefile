IMAGE_NAME := movie-sentiment-app

build:
	@echo "Building Docker image $(IMAGE_NAME)"
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running Docker container"
	docker run --rm -p 8501:8501 $(IMAGE_NAME)

clean:
	@echo "Removing Docker image"
	docker rmi $(IMAGE_NAME) || true