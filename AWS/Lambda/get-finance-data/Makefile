-include variables.txt

.PHONY: build-tools deploy docker-image

.venv:
	virtualenv -p python3 .venv
	.venv/bin/pip install -r ./src/requirements.txt

node_modules/serverless:
	npm install serverless

node_modules/serverless-python-requirements:
	npm install serverless-python-requirements

node_modules/serverless-vpc-discovery:
	npm install serverless-vpc-discovery

docker-image:
	docker pull lambci/lambda:build-python3.8

build-tools: \
	.venv \
	node_modules/serverless \
	node_modules/serverless-python-requirements \
	node_modules/serverless-vpc-discovery

deploy: build-tools test clean
	cd src && AWS_PROFILE=$(AWS_PROFILE) ../node_modules/.bin/serverless deploy

src/test-requirements.txt: .venv
	.venv/bin/pip install -r src/test-requirements.txt

test: src/test-requirements.txt
	bash -c "source .venv/bin/activate && cd src && pytest tests"
	make clean

clean:
	rm -rf .venv/ && \
	rm -rf src/__pycache__/ && \
	rm -rf src/.pytest_cache && \
	rm -rf src/.serverless/ && \
	rm -rf src/tests/__pycache__ \


deploy-test:
	cd src && AWS_PROFILE=$(AWS_PROFILE) serverless invoke --function get-finance-data $(AWS_PROFILE) $(AWS_REGION) $(S3_BUCKET) $(S3_FOLDER)

