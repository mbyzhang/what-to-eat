# what-to-eat

Get bi-daily menu for canteens near [Computer Laboratory, Cambridge](https://www.cst.cam.ac.uk/).

[⚡️ Subscribe now!](https://t.me/s/what_to_eat_near_CL_Cambridge)

## Supported canteens

* [Garden Restaurant, Robinson College](https://www.robinson.cam.ac.uk/college-life/garden-restaurant-menu)
* [Churchill College Dining](https://www.chu.cam.ac.uk/campus-facilities/college-dining/menus/)
* [West Hub Canteen](https://www.westcambridgehub.uk/canteen)

## Developing

### Installation

```
$ pip3 install -r requirements.txt
$ telegram-send --configure
```

### Setting up cron job

Run `crontab -e` and add the following lines.

Adjust `/path/to/what-to-eat` based on your setup.

```
30 11 * * * /path/to/what-to-eat/main.py lunch
0 17 * * * /path/to/what-to-eat/main.py dinner
```
