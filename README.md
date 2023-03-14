# SEEDING THE DATABASE
When seding the database for this app,
start the flask server and request localhost in the web browser.
Then seed the file in a separate shell, in python.
After, the database will have the data from the seed file. This process is because my app drops all databasaes then creates all databases
when it starts. This may be changed by deleteing the drop_all() function in
apps_methods.py.

# DATABSE AND THE STORAGE OF DATA FOR VARIOUS SERVER RUNS...
Note, when running the appp and adding data to the database,
the data will be gone if one stops the server then starts it up again; unless,
the drop_all() function in apps_methods.py is deleted. I kept the drop_all() function in
apps_methods.py when I was creating the logic and didn't want data in my database everytime I started my sevrer.

# STARTING APP
Make sure a PostrgreSQL database called, auth, is created, and make sure PostgreSQL and the Flask server is running.