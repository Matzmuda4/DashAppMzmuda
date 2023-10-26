import influxdb_client, os, time
from sqlalchemy import create_engine
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "Mat"
url = "http://localhost:8086"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "Designing Databases"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

query = """
    select f.film_id, f.title, sum(p.amount), count(*) as total_revenue
    FROM film f 
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    JOIN payment p on r.rental_id = p.rental_id
    group by f.title, f.film_id
    limit 5; 
    """
engine = create_engine('mysql://root:@localhost/sakila')

# Connect to the MySQL database using SQLAlchemy
with engine.connect() as connection:
    result = connection.execute(query)

    for row in result:
        title = row['title']  # Extracting the customer_id
        total_revenue = row['total_revenue']  # Extracting the num_rentals

        # Create a point and write it to InfluxDB
        point = (
            Point("Top grossing movies")
            .tag("title", (title))
            .field("total_revenue", total_revenue)
        )
        write_api.write(bucket=bucket, org=org, record=point)

