# Variables
HOST_PORT=8080
CNTR_PORT=8000
TAG=v1.1
NAME=opp-app
REPO_HOST=352194481459.dkr.ecr.us-east-1.amazonaws.com
TAGGED_IMAGE=$(REPO_HOST):$(TAG)
REGION=us-east-1

image: Dockerfile
	docker build --platform linux/amd64 -t opp-app .
	@echo "DONE"

run-app-local:
	uvicorn backend.main:app --reload

run-app-docker-container:
	docker run --name $(NAME) -p $(HOST_PORT):$(CNTR_PORT) opp-api:v1

exec-app:
	docker exec -it $(NAME) bash

stop-app:
	docker stop $(NAME)

rm-app:
	docker rm $(NAME)

ecr-login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(REPO_HOST)

ecr-logout:
	docker logout $(REPO_HOST)

prod-image: ecr-login image
	docker tag opp-app:$(TAG) $(TAGGED_IMAGE)
	docker push $(TAGGED_IMAGE)
	$(MAKE) ecr-logout

all:
	@echo ${USER}