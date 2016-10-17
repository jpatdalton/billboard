# Billboard Metrics

This codebase was used to populate the following spreadsheet automatically:

https://docs.google.com/spreadsheets/d/1OKuFjBX0zcmsVKWZTyGJed1PfNoNg_q7H-ipa4JS6U8/edit?usp=sharing

Billboard releases it's top 100 list every week, so a new sheet gets made every week.  All other information is then populated based on what artists and songs are in the top 100.  This codebase backed up all the data to a MySQL database to create a caching mechanism.  Instead of hitting APIs an excessive number of times, all artist and song information is stored in the database and updated only on demand.


## Usage

This codebase is not meant to be run.  This is because there are many api keys and IDs along with database and server setups you need to perform to make it work.
