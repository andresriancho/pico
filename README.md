# Pico

Tool to identify and exploit timing attacks.

## Install

```
virtualenv pico-venv
source pico-venv/bin/activate

git clone git@github.com:andresriancho/pico.git
cd pico
pip install -r requirements.txt
```

## Getting Timing Samples

Please note that this tool is Linux-specific and requires root privileges
to run due to the OS tricks implemented in the `os_utils.py` module.

Edit the constants in `timing-collector.py` and then:

```
sudo -s -H
source pico-venv/bin/activate

cd pico
python timing-collector.py sample-name
```

## Analyzing Samples

Edit the token values in `graph-results.py` and then:

```
python graph-results.py sample-name
```
