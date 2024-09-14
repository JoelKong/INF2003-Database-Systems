<!-- @format -->

Installation and Hosting Guide
Front-end (ReactJS)
• Make sure node.js is downloaded and updated to install dependencies
• From the root folder, “cd client”, “npm install” to install dependencies
• “npm run dev” to run the website locally and visit localhost:5173 to view the GUI
Back-end (Flask)
• Make sure python is installed and updated
• From the root folder, “cd server”
• Run “pip install -r requirements.txt” or make a virtual environment before installing to install the required dependencies
• Run “flask --app webserver run” to run the flask server locally
• fking important - make sure u have python-dotenv installed, then create a .env file in your server directory. inside that .env put this inside
DB_HOST=localhost
DB_NAME="<ur local db name>"
DB_USER="<ur local db user>"
DB_PASSWORD="<ur local db password>"
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_general_ci

this is because since we might be using locally hosted db first, you will need this for webserver.py to read the connection.

then run this query in ur terminal to create the adopters table.

CREATE TABLE adopters ( id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, name VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL);
