<br/>
<p align="center">
  <h1 align="center">Message Broker</h3>

  <p align="center">
    A message broker developed with Django framework inspired by <a href="https://kafka.apache.org">Apache Kafka</a>
    <br/>
    <br/>
  </p>
</p>

## About The Project

This is a message broker created with the Django framework. It was developed as a project for the "Systems Analysis and Design" course at Sharif University of Technology.
Here are some of the features of this app:
* pushing messages to a queue
* pulling messages from the queue
* subscribing to the queue
* handling multiple server nodes

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python 3.7 or higher
* docker-compose

### Installation

1. Clone the repo

```sh
https://github.com/mjmaher987/Message-Broker.git
```

2. Run the coordinator

```sh
cd message-broker-server\coordinator
python manage.py runserver 0.0.0.0:7000
```

3. Build the server docker image

```sh
cd message-broker-server\server
docker-compose build
```

4. Run the server

```sh
docker-compose up
```

## Tests
You can find and run the predefined tests in the `message-broker-server\tests` directory.
