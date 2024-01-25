# goes-notify-ntfy.sh

This is a small modification to [Drewster727's excellent goes-notify](https://github.com/Drewster727). It largely does the same thing, however instead of email/txtmsg it sends notifications with [ntfy.sh](https://www.ntfy.sh). This lets you install an app on your phone and get push notifications when an appointment becomes available.  It was also run through python 2to3 to move to python3.

This app will simply parse json output from the interview scheduler for many of CBP's Trusted Traveler Programs, including Global Entry, NEXUS, SENTRI, US/Mexico FAST, and US/Canada FAST. You don't need to provide a login, it will simply check the available dates against your current interview date, then notify you if a better date can be locked in.

Based on the [ge-cancellation-checker](https://github.com/davidofwatkins/ge-cancellation-checker) that originally utilized phantomjs to login as the user

## Getting started

- Clone the repo
- Enter required fields into `config.json`:
  - Look up your enrollment center in the list below
  - Enter your current interview date in Month name-Day-Year format. E.g., "December 10, 2017"
  - Change the CHANGEME in the ntfy.sh to a unique id you subscribe to on your phone/webapp, etc. This runs it every 15 minutes from 6AM to 8AM.

```
*/15 6-20 * * * /usr/bin/python3 /home/jquagga/goes-notify/goes-notify.py --config /home/jquagga/goes-notify/config.json >/dev/null 2>&1
```

## Usage

Run the script with python:

```bash
python goes-notify.py --config config.json
```

If you would like to check multiple nearby locations at once you need to make copies the config.json you just edited and change the location code on each config file. Then in seperate windows run each copy of the diffrent locations. If you set `enrollment_location_name` in the config file, the alert message will display this name, otherwise the `enrollment_location_id` will be displayed.

You also may want to have cron run this every X minutes to send you a notification.

## GOES center codes

Visit [this link](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry) for a current complete list, find your desired location; and use the 'id' field as the location code in your config file.

### Location codes for other Trusted Traveler programs

Appointments for other programs, including NEXUS, SENTRI, US/Mexico FAST, and US/Canada FAST are available using the same scheduler API as Global Entry. Many sites use the same location id for multiple types of appointments, but some do not (e.g., Blaine, WA is 5020 for Nexus Appointments and 13321 for Global Entry; Ft. Erie is 5228 for US/Canada FAST and 5022) so it is best to consult the lists below to make sure you are requesting the correct type of appointment.

Retrieve the location list for each type of appointment using the URLs below. Find your desired location, and then use the 'id' field as the 'locationId' in your config file.

- [NEXUS location list](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=NEXUS)

- [SENTRI location list](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=SENTRI)

- [US/Mexico FAST location list](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=U.S.%20%2F%20Mexico%20FAST)

- [US/Canada FAST location list](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=U.S.%20%2F%20Canada%20FAST)
