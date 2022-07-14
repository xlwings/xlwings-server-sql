# xlwings: Connect Google Sheets to SQL databases

This is a demo repo that shows how you can connect Google Sheets to the following SQL databases:

* SQLite
* PostgreSQL
* MySQL
* MariaDB
* Microsoft SQL Server
* Oracle

The easiest way to try things out is by clicking the Deploy to Render button below and filling in the required environment variables in the Render dashboard:

* `GOOGLE_ALLOWED_DOMAINS` (make sure to format like a Python list): `["your_workspace_domain.com"]`
* `XLWINGS_LICENSE_KEY` (get a [trial key](https://www.xlwings.org/trial)): `your_xlwings_pro_license_key`
* `DB_CONNECTION_STRING` (other databases see below): `sqlite:///sqlite-data/xlwings.db`

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Google Sheets Template

* https://docs.google.com/spreadsheets/d/1FAILMOCpzRHjWS_7ud9lmnkVWtWntaalLjJtrnhoVmg/template/preview
* Go to `Extensions` > `Apps Script` and adjust the `URL` to the match your backend (e.g., the URL of the Render service from above)
* Click the `Run` button to query the included SQLite database (see `app/api/employees.py` for the relevant SQL query)

## Database connection strings

* SQLite: `sqlite:///rel/path/to/xlwings.db`
* PostgreSQL: `postgresql://user:password@host:port/database`
* MySQL: `mysql://user:password@host:port/database`
* MariaDB: `mariadb://user:password@host:port/database`
* Microsoft SQL Server: `mssql://user:password@host:port/database`
* Oracle: `oracle://user:password@host:port/service_name`

Note: if you want to use an absolute file path for SQLite, it will have a total of 4 slashes: `sqlite:////abs/path/to/xlwings.db`

## Sample Data

If you aren't using the included SQLite database, you'll need to create and populate the `employees` table.
You can do this by running the `scripts/create_table.py` module:

* Run locally: requires the database connection string to be pasted in the script before running it
* Run via docker compose: Set up your `.env` file according to the `.env.template`, then run `docker-compose up`, followed by `docker-compose exec app python /scripts/create_table.py`.

Alternatively, you could change the query under `app/api/employees.py` to match an existing table in your database.

## Local development with docker compose

Local development is easiest via docker compose:

* Copy `.env.template` to `.env` and fill in the values as outlined above
* Uncomment the service that corresponds to the database you want to use (make sure the indentation is correct after uncommenting). This step is not required fro SQLite.
* Run `docker-compose up`
* Expose your local port via a service like ngrok, or use an online IDE like GitPod (click button below), see the [docs](https://docs.xlwings.org/en/stable/remote_interpreter.html#local-development-with-google-sheets-or-excel-on-the-web).

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/xlwings/xlwings-googlesheets-sql)

Here are the connection strings when you run everything via docker compose:

```
DB_CONNECTION_STRING=sqlite:///sqlite-data/xlwings.db
DB_CONNECTION_STRING=postgresql://postgres:MyPassw0rd@postgres:5432/xlwings
DB_CONNECTION_STRING=mysql://root:MyPassw0rd@mysql:3306/xlwings
DB_CONNECTION_STRING=mariadb://root:MyPassw0rd@mariadb:3306/xlwings
DB_CONNECTION_STRING=mssql://SA:MyPassw0rd@mssql:1433/master
DB_CONNECTION_STRING=oracle://system:MyPassw0rd@oracle:1521/XE
```

### Oracle

Oracle requires to build the docker image locally:

```
git clone https://github.com/oracle/docker-images oracle
cd oracle/OracleDatabase/SingleInstance/dockerfiles
./buildContainerImage.sh -v 18.4.0 -x
```

Note that the Oracle database takes a very long time (>15 minutes) when you first use it!