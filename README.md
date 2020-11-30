# to-do-app
A simple web application for managing personal to do tasks.

## Usage
### Register
The application requires a new user to create an account. This is possible via the navigation bar or the link on the log in page. On the register page, the user needs to choose a username and password to register. Changing these credentials is not possible for now.

Register page also provides the conditions that the username and password have to satisfy. The username can contain only letters, numbers and full stop. The password needs to be at least 8 characters and can contain letters, numbers and symbols. 

The application checks the inputs against these conditions and provide a feedback as you type. Valid inputs will appear as green and invalid inputs will appear as red as shown below:

![register-feedback](static/register-invalid-input.png?raw=true "Invalid input")

If the user tries to submit invalid credentials, an error message will be prompted as shown below:

### Log in / Log out
After the user creates his account, he can log in at a later time with his credentials. If the user types in a wrong username or password, log in page will prompt an error. An example is below: 

After the user registers or logs in, he will be directed to the index page. The user can always log out by using the button on the navigation bar:

After logging out, the user needs to log in again to access the application.

### Create
Once the user is logged in, he can create to do items on the create page. A to do item has a title, a description (optional) and a status. The default status is, unsurprisingly, "to do". However, as the user might want to create a to do item which he is already working on or he already completed, it is possible to create to do items with status "in progress" and "done". After creating a to do item, it will appear on the index page or board page of the user.

### Board
The main UI of this web application is the board page. There, user can view his to do items in a structured format. There are three columns: TO DO, IN PROGRESS and DONE. Each will list to do items belonging to that category.

This page also permits the user to change the status of a to do item and to delete a to do item. After any update, the page will reload with the new information. On the delete action, a confirmation is required.

## Further work
- To do items can also have a label. This label can be used to group to do items that are somewhat related. The board can be filtered with a specific label to present only a certain type of items.
- The board would be more user friendly if to do items are draggable between the columns.
