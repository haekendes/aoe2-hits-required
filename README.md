# aoe2-unit-breakpoints
uses Flask, Bootstrap, Google Charts, SlickGrid & Select2

Full web application for a one-page website displaying unit-breakpoints in Age of Empires II DE.
More specifically, it displays the hits a unit needs to defeat another unit. All possibilities are displayed in a grid since all upgrade combinations are taken into account.

The website is hosted on a RaspberryPi with Python Flask, an nginx reverse proxy and no database. Unit-breakpoints are calculated on system startup. Upon request, the data is sent to the client as compressed JSON to save bandwidth. JSON data is parsed to the table data by the client and stored in local storage, again, to save bandwidth.

Specific units can be chosen, which results in their data being displayed in dynamic charts. A snapshot of each chart can be downloaded as png file.

![preview image](https://i.imgur.com/ybU83Qn.jpeg)
