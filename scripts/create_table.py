"""
Run this script to create a table "employees". It uses data from Microsoft's
AdventureWorks sample database, which is released under the MIT license,
see: https://github.com/microsoft/sql-server-samples
"""
import os
import re
import sys
import urllib.parse

import pandas as pd
from sqlalchemy import create_engine

db_connection_string = ""  # TODO
source_table_url = "https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/oltp-install-script/Employee.csv"

# If no db_connection_string is provided, take it from the env vars
if not db_connection_string:
    db_connection_string = os.environ["DB_CONNECTION_STRING"]

# Driver tweaks
db_connection_string = (
    db_connection_string.replace("postgres://", "postgresql://")
    .replace("mysql://", "mysql+pymysql://")
    .replace("mariadb://", "mariadb+pymysql://")
)

if "mssql" in db_connection_string:
    db_connection_string += "?driver=ODBC+Driver+17+for+SQL+Server"
elif "oracle" in db_connection_string:
    # This is only required for SQLAlchemy < 2.0, see:
    import oracledb

    oracledb.version = "8.3.0"
    sys.modules["cx_Oracle"] = oracledb

# URL encoded password
pattern = re.compile(r"(.*)://[^:]*:(.*)@")
match = pattern.match(db_connection_string)
if match:
    password = match.group(2)
    connection_string_parts = db_connection_string.split(password)
    connection_string_parts.insert(1, urllib.parse.quote_plus(password))
    db_connection_string = "".join(connection_string_parts)


df = pd.read_csv(
    source_table_url,
    encoding="utf-16",
    delimiter="\t",
    names=[
        "business_entity_id",
        "national_id_number",
        "login_id",
        "organization_node",
        "organization_level",
        "job_title",
        "birth_date",
        "marital_status",
        "gender",
        "hire_date",
        "salaried_flag",
        "vacation_hours",
        "sick_leave_hours",
        "current_flag",
        "rowguid",
        "modified_date",
    ],
    dtype={"salaried_flag": bool, "current_flag": bool},
    parse_dates=["birth_date", "hire_date", "modified_date"],
)

engine = create_engine(db_connection_string)
df.to_sql("employees", con=engine, index=False)
