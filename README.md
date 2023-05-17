# `speedtest` to MySQL

This application will perform a network speed test (using the `speedtest` CLI provided by Ookla (speedtest.net)) and
store the results in a MySQL DB.

## Prerequisites

1. `docker-compose`
2. A MySQL DB

## Setup

1. Create a new MySQL DB to use
2. Copy `config.example.yaml` to `config.yaml`
3. Edit the `config.yaml` file with the desired settings.
4. `docker-compose -f docker-compose.yml build`
5. `docker-compose up speedtest_to_mysql -d`

## Maintainer Notes

### Developing Quick Start

The below commands to get the basic setup for developing on this repository.

```shell 
python3 -m venv venv
ln -s venv/bin/activate activate
source activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Building the `Dockerfile`

```shell
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```

### Publish the Docker image to Docker Hub

```shell
docker login --username chriscarini

VERSION=0.0.1
IMAGE="chriscarini/speedtest-to-mysql"

# Give the image two tags; one version, and one `latest`.
docker build -t "$IMAGE:latest" -t "$IMAGE:$VERSION" .

docker push "$IMAGE:latest" && docker push "$IMAGE:$VERSION"
```

## References

The `speedtest` CLI is as provided by Ookla (speedtest.net).

You can find [installation instructions for your platform here](https://www.speedtest.net/apps/cli).

This project pulls in this CLI into a docker container for easier use.
