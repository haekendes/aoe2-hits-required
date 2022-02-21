# aoe2-unit-breakpoints
uses Flask, Bootstrap, Google Charts, SlickGrid & Select2

Full web application for a one-page website displaying unit-breakpoints in Age of Empires II DE.
More specifically, it shows the hits unit needs to defeat another unit. All possibilities are displayed in a grid since all upgrades are also taken into account.

Is made to run on a RaspberryPi with Python Flask, an nginx reverse proxy and no database. Unit-breakpoints are calculated on startup and sent to the client as compressed JSON to save bandwidth. JSON data is parsed to table data by the client and stored in local storage, again, to save bandwidth.

Specific units can be chosen, which results in their data being displayed in dynamic charts. A snapshot of each chart can be downloaded as png file.
