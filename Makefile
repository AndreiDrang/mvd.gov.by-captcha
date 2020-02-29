build:
	docker build -t andreidrang/mvd.gov.by-captcha-back -f Dockerfile .

pull:
	docker pull andreidrang/mvd.gov.by-captcha-back

push:
	docker push andreidrang/mvd.gov.by-captcha-back

start:
	docker-compose -f docker-compose.yml up -d

local:
	docker-compose -f docker-compose-local.yml up

stop:
	docker-compose -f docker-compose.yml down
