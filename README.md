Document-Management-System

This is a document management web application built using Flask framework and SQLAlchemy ORM. The application allows users to create, view, edit, delete and compare documents. The application also keeps track of version history for each document.
Installation

    Clone this repository to your local machine.

    Install the required dependencies using the following command:

pip install -r requirements.txt

    Create .env file in the root directory of the project and add the following configurations:


FLASK_APP=app.py
FLASK_ENV=development

    Run the following commands to create and upgrade the database:



flask db init

flask db migrate -m "initial migration"

flask db upgrade

Usage

To start the application, run the following command:

python app.py

Then, open your browser and go to http://localhost:8080/ to access the home page.

From there, you can create, view, edit, delete and compare documents.
