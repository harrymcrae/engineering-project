# ExePlore

### the sexy engineers
___

The group members are:

1. Harry McRae
2. Ed Villiers
3. Dan Hole
4. Jacob Holleron-Silk
5. Vivan Arora
6. Jenifer Osifo

This project is **ExePlore**, our Sustainability Challenge app designed to encourage users to participate in sustainability-related challenges. The app allows users to register, complete challenges, track progress, and view rankings.

This is our final product submnission. There are three types of document that you will find the following places.

## PROCESS DOCUMENTS
Our process documents are managed in the trello platform. The link to our project page is below. We (harrymcrae2) have added solomonoyelere1 to the board so it is visible.

trello link: [https://trello.com/b/amM167CG/software-engineering-project]

We have also taken regular snapshots of the kanban board in trello to archive our progress. These are held in the repository below.

[./process-documents/kanban-snapshot/](./process-documents/kanban-snapshot/)

Within process documents we have also included the meeting notes, agenda and minutes. These will be found in the repository below.

[./process-documents/meeting-notes/](./process-documents/meeting-notes/)


## TECHNICAL DOCUMENTS
Our technical documents are primarily managed on the github system. The link to the project is below:

github link: [https://github.com/harrymcrae/engineering-project]

We have also include the versioned source code for archiving.

[./technical-documents/](./technical-documents/)

Technical documents are broken down into front end and back end etc.  

## PRODUCT DOCUMENTS
Our product documents contain most of the documentation of the whole project.

The documentation for the client have also been archived under the link below:

[./product-documents/documentation/](./product-documents/documentation/)

## DEPENDENCIES
You will need to have Python3 installed. From there, this project requires you to install some dependencies in order to run it locally:
    - Django (pip install Django)
    - Pillow (pip install Pillow)

## DEPLOYMENT
We deployed our application on Render. You can access the page using the link below:

https://engineering-project-snk7.onrender.com/home/

We have provided a pred-made Admin account for you to access the Admin panel through https://engineering-project-snk7.onrender.com/admin/

To access the **Admin Panel**, the credentials are provided in the internal documentation for review and marking purposes.




This will let you access the admin panel to approved any submissions, or manage users and challenges.

## LOCAL TESTING

To run the project locally, simply pull the repository from the GitHub. From there, you may need to migrate any database changes through the following commands:

python manage.py makemigrations
python manage.py migrate

Now you can launch the application locally:

python manage.py runserver

Tests for this application are located in the `tests.py` file in the following directories:
- **accounts**
- **challenges**
- **dashboard**
