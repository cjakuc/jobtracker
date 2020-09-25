This is a job tracker web app made using Python (Flask, SQL-Alchemy, plotly) and PostgreSQL. The PGSQL database is hosted on ElephantSQL and the app itself on Heroku [here](https://the-best-job-tracker.herokuapp.com/).

Built in collaboration with [Adriann Lefebvere](https://github.com/aklefebvere)

Local Setup:
* Host your own PGSQL database on a platform like ElephantSQL
* Clone this repository
* Add a `.env` file that include the following vairables corresponding to your database and what you choose as a secret key: `AUSER`, `DBNAME`, `DBPASSWORD`, `HOST`, `DBURL`, `SECRET_KEY`
* CD into the directory of the cloned repository
* `pipenv install` to create the pipenv enviornment
* `pipenv shell` to enter the environment
* `flask run` to run the site locally and connec to your live database

Feel free to reach out at chris.jakuc@gmail.com if you have any questions or you encounter any bugs!