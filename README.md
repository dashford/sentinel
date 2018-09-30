# sentinel

*This project is under early development, breaking changes may occur at any time*

Sentinel is an open source project for collecting sensor and publishing sensor data to an MQTT
broker. See the list of currently supported sensors.

Currently this project was developed to run on a Raspberry Pi Zero with sensors connected via
GPIO pins. Depending on the sensor choice, multiple sensors can be run off the one Pi.

## Prerequisites

This project depends on an already configured MQTT broker where it can push sensor information
to. Any broker should do and connection details are defined in the `.env` file.

## Supported Sensors

- BME280
- BME680
- CCS811
- DS18B20

## Installation

The recommended way of running Sentinel is through `virtualenv`. Docker support is on the roadmap.

- Create a virtual environment for the project

```
$ virtualenv ~/virtualenv/sentinel
```

- Clone the project to a directory of your choice

```
$ mkdir -p ~/projects/github/dashford
$ cd ~/projects/github/dashford
$ git clone git@github.com:dashford/sentinel.git
```

- Create a `.env` and `config.yaml` file making the necessary changes

```
$ cp .env.example .env
$ cp config.example.yaml
```

- Activate the virtual environment and run the application

```
$ source ~/virtualenv/sentinel/bin/activate
(sentinel) $ python sentinel.py
```

## Configuration

Sensors can be configured through a `config.yaml` file. At the moment both sensors and LEDs can
be configured this way.

See `config.example.yaml` for more examples.

Other configuration details are defined in the `.env` file.

## TODO

- Validate and update dockerfile
- Refactor scheduler add job in `__main__`
- Convert into executable script?
- Implement event observers
- Tests
- Clean up `Sensors` folder
- Logging
- Type-hint methods
- Add MQTT message definitions/objects
- Subscribers and MQTT client needs to have some error handling