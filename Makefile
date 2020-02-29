build:
	docker build -t mvd.gov.by-captcha-back -f Dockerfile .

start:
	docker-compose -f docker-compose.yml up -d

local:
	docker-compose -f docker-compose-local.yml up

stop:
	docker-compose -f docker-compose.yml down
