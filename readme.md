### Kanban Board SSR

Kanban is a task management application that can be used to track completed tasks, pending tasks, and tasks that are not completed. This application allows us to manage tasks and create lists for various projects. It is designed to handle multiple projects and track their respective tasks.

I have created a Kanban board, implementing it as an SSR (Server Side Rendering) application. I utilized the Flask framework to build the server, and this server dynamically generates HTML on the server-side. Therefore, for every client click or request within the application or web app, the server processes the request, renders the HTML using Jinja2, and subsequently sends the response to the client.

Note: I have created a Kanban application with two methods: **SSR** (Server Side Rendering) and **SPA** (Single Page Application).

1. In SSR (Server Side Rendering): The entire HTML content of web pages is generated on the backend (server) rather than relying on client-side rendering. Data is seamlessly integrated into the HTML structure using the Jinja2 templating engine, resulting in fully-formed HTML documents that are ready to be sent to the user's browser.

2. In SPA (Single Page Application): Here, I have separated the frontend and backend. For the frontend, I've utilized VueJS CDN to transform the app into an SPA. The backend is responsible for API handling, caching, and asynchronous tasks (powered by Celery). VueJS has been instrumental in making the app an SPA. 
You can check out the **SPA** version in a different repository named "kanban-ssr."


This Repo demonstrates the **SSR** version.


**Objective of the Application:**
A Kanban board that can efficiently manage tasks and provide a clear visualization of which tasks are completed, pending, and have passed their deadline.
1. The application is designed to be multi-user and secured with Flask-Login
2. Users have the ability to create lists or projects and add tasks to them.
3. Users can move tasks between sections such as completed, pending, or deadline passed.
4. Users can access a summary that provides insights into completed projects versus ongoing projects. Detailed task information is also available.
5. Users can download their tasks in CSV format at any time and share them with others.


**Technologies Used:**

<u>Languages Used:</u>
1. Python
2. Javascript
3. HTML/CSS


<u>Backend Technologies:</u>

1. Flask: Used for building the backend of the application.
2. Flask Login: used simple security to check the user is logged or not, while using the app.
3. Jinja2: Used to render dynamic data within HTML templates in Python web applications.
4. Pandas/Numpy: Utilized for data manipulation on the backend (server).
5. Matplotlib/Seaborn: Used for plotting the graphs. This is used on the summary page of the application, which is also rendered on the server side and embedded in the HTML before being sent as a response to the client.

<u>Database Technologies:</u>

1. SQLite3: This SQL database is used in this application.
2. SQLAlchemy: It serves as an Object Relational Mapper (ORM) for SQLite3.


<u>Tools Utilized:</u>

1. dbbrowser: Used for visualizing the SQLite database.






**How to run the application:** 

Step 1: Install all the required dependencies. Refer to the 'requirements.txt' file.
If you want to install all the requirements in one go, use the following command:
```
pip install -r requirements.txt
```
Ensure that you are in the correct directory, and pip should be installed on your machine.


Step 2: Run the applcation by using the command.
```
python3 app.py
```
If you have a different Python version, adjust the command accordingly. Makesure you are in correct directory.

This application uses SSR (Server Side Rendering), so you only need to run the server. When a client or user makes a request, the server dynamically renders the HTML page using Jinja2 and sends the response to the client. The server renders a response every time there is a request from a client.

Note: This application is not in the production phase, so it runs on the localhost after executing the provided commands. These commands must be executed in the terminal.

