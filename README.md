# Advanced Data Storage and Retrieval Using SQLAlchemy and Flask App

<img src=other_images/sqlalchemy_logo.jpeg width="40%" alt="SQLAlchemy's logo"><img src=other_images/flask_logo.png width="40%" alt="Flask's logo">

Penn Data Boot Camp Assignment 10 - Advanced Data Storage and Retrieval with SQLAlchemy and Flask App.

In this exercise, I analyzed a given Hawaii climate database using SQLAlchemy, Pandas, and Matplotlib. I also created multiple Flask API routes based on queries to store data for customized ways to retrieval the information.

## Goal
* Practice using SQLAlchemy by performing complex queries and aggregations with functions such as filter(), group_by(), order_by(), func.avg(), etc.
* Practice using Python Flask to build an application which interacts with a databased and the localhost to store and return desired data.

## Analysis Highlights

**The tasks/analyses performed include but are not limited to:**
* Precipitation Analysis
  * Retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.
* Station Analysis
  * Design a query to calculate the total number of stations in the dataset.
  * Design a query to find the most active stations (Which station id has the highest number of observations?).
  * Design a query to retrieve the last 12 months of temperature observation data (TOBS) and show the distribution.
* Temperature Analysis
  * Identify the average temperature in June at all stations across all available years in the dataset.
  * Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?
  * You are looking to take a trip from August first to August seventh of this year, but are worried that the weather will be less than ideal. Using historical data in the dataset find out what the temperature has previously looked like (average, min, max) within a certain time period.
  * Calculate the daily historical temperature daily normals within a week's time period.

### Below are a few plots created within this exercise:

<img src=plots/precipitation_analysis.png width="90%" alt="Line Chart - Precipitation Over the Last 12 Months">

<img src=plots/station_analysis.png width="90%" alt="Temperature Distribution Over the Last 12 Months for the Station with the Most Observations">

<img src=plots/temperature_analysis_2.png width="30%" alt="Historical Average-Min-Max Temperature within a Specific Date Range">

<img src=plots/daily_rainfal_average.png width="90%" alt="Historical Temperature Daily Normals for a Specific Week">
