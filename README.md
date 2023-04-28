# Delish Express Data Visualization

Delish Express, it's tech company which designed an app connecting restaurants, delivery person, and customers. The app allows customers to place orders in restaurants and receive them at their doorstep. It's a simple and easy to use platform which has helped many restaurants to grow and become popular.

The company has a lot of data being processed like orders, deliveries, traffic, ratings, and even weather conditions. With this much data, the CEO requested a solution to visualize the KPIs, the main one, the growth of orders.

As a data scientist, the main objective is to deliver a data product to help the CEO and the sales team make better and faster decisions. For this project it was decided to build a dashboard with graphics and tables that can be accessed online.

# Premises for analysis:
1. The analysis was formed with data ranging from 11/02/2022 to 06/04/2022.
2. Marketplace is the assumption business model.
3. The 3 main business views were: Orders, Delivery Person and Restaurants.

# Solution strategy
Develop a strategic dashboard using metrics that correspond to the 3 main views of the company's business model. Each view is represented by the following sets of metrics:

### 1. Orders
  - a. Orders by Day
  - b. Orders distribution by Traffic Type
  - c. Comparison of the orders by city and Traffic Type
  - d. Orders by Week
  - e. Weekly Orders by Delivery Person
  - f. Orders Central Region

### 2. Delivery Person
  - a. Delivery Person Maximum and Minimum Age
  - b. Vechiles Best and Worst Condition
  - c. Average Ratings by Delivery Person
  - d. Average Ratings by Traffic
  - e. Average Ratings by Weather
  - f. Top 10 Fastest and Slowest Deliveries by City

### 3. Restaurants
  - a. Unique Deliverers
  - b. Average and Standard Deviation Time Delivery During Festivals
  - c. Average and Standard Deviation Time Delivery
  - d. Average Delivery Time by City
  - e. Average Delivery Time by City & Order Types
  - f. Average Delivery Distance by City
  - g. Average Delivery Time by City and Traffic

# Top 4 data insights
1. The seasonality of the number of orders is daily, with an approximate variation of 10% in the number of orders on sequential days
2. Semi-Urban type cities do not have low traffic conditions
3. The biggest variations in delivery time happen during sunny days
4. The smallest variations in ratings are found when traffic is Medium or when weather conditions indicate Fog. 

# Project Final Product
Online dashboard hosted on a Cloud service and available for access from any device connected to the internet. 
This dashboard can be accessed through the link https://food-delivery-data-visualization.streamlit.app

https://user-images.githubusercontent.com/88066683/235245521-18e184eb-747b-4727-9426-e34b1a51603a.mp4

# Conclusion
The objective of this project is to create a set of graphs and/or tables that display these metrics in an easy and quick way for the CEO of the company. We can see that the number of orders grew between week 6 and week 13 of the year 2022.

# Next Steps
1. Develop new filters
2. Build new charts
3. Add new business views
4. Reviews the quantity of metrics
