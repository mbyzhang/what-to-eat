# what-to-eat

## Installation

```
$ pip3 install -r requirements.txt
$ telegram-send --configure
```

## Setting up cron job

Run `crontab -e` and add the following lines.

Adjust `/path/to/what-to-eat` based on your setup.

```
30 11 * * * /path/to/what-to-eat/main.py lunch
0 17 * * * /path/to/what-to-eat/main.py dinner
```
