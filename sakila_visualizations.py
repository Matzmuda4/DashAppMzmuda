from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# Replace 'username' and 'password' with your MySQL username and password
engine = create_engine('mysql://root:@localhost/sakila')
query = """
select f.film_id, f.title, sum(p.amount), count(*) as total_revenue
FROM film f 
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p on r.rental_id = p.rental_id
group by f.title, f.film_id
limit 5;
"""

# Execute the SQL query and load the results into a pandas DataFrame
film_data = pd.read_sql(query, engine)


# Set the figure size
plt.figure(figsize=(10, 6))

# Create a bar chart
plt.bar(film_data['title'], film_data['total_revenue'])

# Customize the chart
plt.title('5 Highest Grossing Films')
plt.xlabel('title')
plt.ylabel('total_revenue')
plt.xticks(rotation=45)  # Rotate category labels for readability
# Display the chart
plt.tight_layout()
plt.show()

query = """
select c.customer_id, c.first_name, p.amount
from customer as c
join payment as p on c.customer_id = p.customer_id
order by p.amount desc;
limit 10;
"""

# Execute the SQL query and load the results into a pandas DataFrame
Cust_data = pd.read_sql(query, engine)

# Set the figure size
plt.figure(figsize=(12, 6))

# Create a time-series line chart
plt.bar(Cust_data['first_name'], Cust_data['amount'])

# Customize the chart
plt.title('Customers with highest total payments ')
plt.xlabel('first_name')
plt.ylabel('amount')
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Display the chart
plt.tight_layout()
plt.show()