TAG:=$(shell git log -1 --pretty='%h')
IMAGE:=demo1

build_app:
	docker build --tag $(IMAGE):$(TAG) .

run_app:
	docker run -p 8001:8001 --rm $(IMAGE):$(TAG)
