# Internationanl Space Station tracker

The goal of this project was to work on an introductory data engineering challenge.  

In this project, I want to build a data pipeline that retrieves real-time data from a public API, processes and formats the data, and stores it for easy access and querying.  
I will use Python and tools such as pandas, SQLAlchemy, and GitHub to build and run the pipeline.  

Steps:  
- Find a public API that provides real-time data without the need for registration.  
    [Open-Notify-API](!http://open-notify.org/Open-Notify-API/) is an API put together by Nathan Bergey to provide services which include showing the [current position of the ISS in space](!http://api.open-notify.org/iss-now.json) and the [current number of people in space](!http://api.open-notify.org/astros.json). 
- Use Python and requests to retrieve the data from the API, and transform it into a format that is suitable for storage and analysis. This can involve cleaning the data, normalizing the data, or converting the data to a different format.  
- Store the processed data in a database table for easy querying and analysis. You can use a lightweight database such as SQLite or MySQL, or a cloud-based database such as AWS RDS.  
- Use pandas to perform exploratory data analysis of the data, and use visualizations to identify trends and patterns in the data.  
- Use SQL and pandas to perform more advanced analysis of the data, such as calculating summary statistics or identifying correlations between features.  
- Use prettymaps to customize and display the map.  
- Upload project and use github actions to run the script.  


![ISS Tracker Output Figure](https://raw.githubusercontent.com/lagom-QB/ISS-Tracker/master/output.png)
