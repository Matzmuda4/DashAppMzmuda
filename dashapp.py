import dash
from dash import html,dcc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Connect to the Sakila database
engine = create_engine('mysql://root:@localhost/sakila')

# Create the Dash app
app = dash.Dash(__name__)
def update_bar_chart():
    # SQL query to retrieve data for the selected category over time
    query = """
    select f.film_id, f.title, sum(p.amount), count(*) as total_revenue
    FROM film f 
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    JOIN payment p on r.rental_id = p.rental_id
    group by f.title, f.film_id
    limit 5;
    """
    film_data = pd.read_sql(query, engine)
    fig = px.bar(film_data, x="title", y="total_revenue")
    return fig

def update_bar_chart2():
    # SQL query to retrieve data for the selected category over time
    query = """
    SELECT category, film_id, title, rating
    FROM (SELECT c.name as category, f.film_id, f.title, f.rating, RANK() OVER (PARTITION BY c.name ORDER BY f.rating DESC) AS rating_rank
    FROM film AS f
    JOIN film_category AS fc ON f.film_id = fc.film_id
    JOIN category AS c ON fc.category_id = c.category_id
    ) AS film_ratings
    WHERE rating_rank = 1;
    """
    film_data = pd.read_sql(query, engine)
    fig = px.bar(film_data, x="title", y="rating")
    return fig

def update_bar_chart3():
    # SQL query to retrieve data for the selected category over time
    query = """
    SELECT actor.first_name, actor.last_name, COUNT(*) as film_count
    FROM actor
    JOIN film_actor ON actor.actor_id = film_actor.actor_id
    JOIN film ON film_actor.film_id = film.film_id
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE category.name = 'Horror'
    GROUP BY actor.actor_id
    ORDER BY film_count DESC
    LIMIT 3
    """
    film_data = pd.read_sql(query, engine)
    fig = px.bar(film_data, x="first_name", y="film_count")
    return fig

def update_bar_chart4():
    # SQL query to retrieve data for the selected category over time
    query = """
    select actor.first_name , actor.last_name, count(film_actor.film_id) as film_count
    from actor
    join film_actor on actor.actor_id = film_actor.actor_id
    group by actor.actor_id
    having film_count > 15
    order by film_count desc;
    """
    film_data = pd.read_sql(query, engine)
    fig = px.bar(film_data, x="first_name", y="film_count")
    return fig

def update_bar_chart5():
    # SQL query to retrieve data for the selected category over time
    query = """
    select c.customer_id, c.first_name, p.amount
    from customer as c
    join payment as p on c.customer_id = p.customer_id
    order by p.amount desc;
    """
    film_data = pd.read_sql(query, engine)
    fig = px.bar(film_data, x="first_name", y="amount")
    return fig

fig = update_bar_chart()
fig2 = update_bar_chart2()
fig3 = update_bar_chart3()
fig4 = update_bar_chart4()
fig5 = update_bar_chart5()
# Define the layout of the app
app.layout = html.Div([
    html.H1("top 5 highest grossing"),
    dcc.Graph(id='Top 5 highest Grossing', figure = fig),
    html.H1("highest rated"),
    dcc.Graph(id='highest rated in each category', figure=fig2),
    html.H1("3 Actors in horror"),
    dcc.Graph(id='3 Actors in horror', figure=fig3),
    html.H1("Actors in more than 15 movies"),
    dcc.Graph(id='3 Actors in horror', figure=fig4),
    html.H1("Highest paying Customers"),
    dcc.Graph(id='3 Actors in horror', figure=fig5),

])

if __name__ == '__main__':
    app.run_server(debug=True)





# Define callback to update the line chart based on the selected category
#@app.callback(
    #Output('line-chart', 'figure'),
    #[Input('category-dropdown', 'value')])