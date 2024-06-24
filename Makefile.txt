# Build Docker image
build:
	docker-compose build

# Run Docker containers
run:
	docker-compose up -d

# Stop Docker containers
stop:
	docker-compose down

# Remove Docker containers and network
clean:
	docker-compose down --volumes --remove-orphans
