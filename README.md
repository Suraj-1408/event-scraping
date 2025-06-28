# WebScraping details of upcoming events in Sydney.

This is a simple web application that displays detailed information such as event title,event date,event description,URL and image by scraping from the Original Website -https://www.sydney.com/events .From orignal website I have scarped all upcoming events located inside section called "All events in Sydney". The data is collected and displayed with a clean, responsive interface.

## Features

- Scrapes upcoming events in Sydney
- Displays event details like title, location, description, date, and image
- Allows users to submit their email to get event tickets
- Stores submitted emails in a MySQL database

## Technologies Used

- Python (Flask)
- HTML, Tailwind CSS
- BeautifulSoup (for scraping)
- MySQL (for data storage)


## Preview of Application.




## Setup Instructions to run locally

##  1)Clone the Repository
```
git clone https://github.com/Suraj-1408/WebScraping-Sydney-Events.git

```

## 2) Install Dependencies
Install the required packages present inside requirement.txt using pip command

## 3) Set up MySQL Database

```
CREATE DATABASE events_db;
USE events_db;
```

## 4) create tables having following fields.

1) For Sydney
```
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| id          | int           | NO   | PRI | NULL    | auto_increment |
| title       | varchar(255)  | YES  |     | NULL    |                |
| location    | varchar(255)  | YES  |     | NULL    |                |
| description | text          | YES  |     | NULL    |                |
| start_date  | varchar(50)   | YES  |     | NULL    |                |
| end_date    | varchar(50)   | YES  |     | NULL    |                |
| url         | varchar(2048) | YES  | UNI | NULL    |                |
| img_url     | text          | YES  |     | NULL    |                |
| view_count  | int           | YES  |     | 0       |                |
+-------------+---------------+------+-----+---------+----------------+

```


2) For Pune
```
+------------+--------------+------+-----+-------------------+-------------------+
| Field      | Type         | Null | Key | Default           | Extra             |
+------------+--------------+------+-----+-------------------+-------------------+
| id         | int          | NO   | PRI | NULL              | auto_increment    |
| title      | varchar(255) | YES  |     | NULL              |                   |
| location   | varchar(255) | YES  |     | NULL              |                   |
| price      | varchar(100) | YES  |     | NULL              |                   |
| date       | varchar(100) | YES  |     | NULL              |                   |
| url        | text         | YES  |     | NULL              |                   |
| img_url    | text         | YES  |     | NULL              |                   |
| created_at | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| category   | varchar(100) | YES  |     | NULL              |                   |
| view_count | int          | YES  |     | 0                 |                   |
+------------+--------------+------+-----+-------------------+-------------------+
```

## 3) Update your db.py and app.py accordingly

```
mydb = mysql.connector.connect(
  host="localhost",
  user="your_mysql_username",
  password="your_mysql_password",
  database="events_db"
)
```

## 4) Run the Flask main app
```
  source venv/bin/activate 
```

## Run the app.py
```
python3 app.py
```


