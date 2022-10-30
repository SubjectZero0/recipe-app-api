# A Recipes API with Django

## Welcome to my Recipes API project.

This project is built with the Django Rest Framework,
to deliver a browsable API that is intuitive and easy to use.

The entirety of this app is containerized using Docker and docker-compose.
Additionally, there is a debugger configuration that gets attached to the containers.
That means the application gets debugged while the container is running.

For this repository, everything is set up to be ran in development mode. At this stage,
no changes have taken place to accomodate deployment.

In order to run the application you need docker installed. Then simply type in your terminal:

```
docker-compose build
```

and then,

```
docker-compose up
```
The development process was dependant on testing. There are 50 unit tests to
make sure all components are working as intended. To run the tests type:

```
docker-compose run --rm app sh -c "python manage.py test"
```

### Features of the Recipes API are:

- Complete user/superuser registration and authentication. Admin site provides a lot of flexibility.

- Users endpoint supports **GET** and **POST(create)** method for unauthorised users. Token is generated for users that login.

- Recipes endpoint supports **GET** method for ALL recipes for unauthorised users, but in order to Create, Update, Delete, a token is required.
A token authenticated user can ***only*** update and delete recipes ***they*** have created.They can also upload an image to a recipe they have created,
***after*** they have created it. Image upload is kept ***separate*** from recipe creation.

- My_Recipes endpoint requires a Token in order to CRUD. The difference to the Recipes endpoint is that on a **GET** request, my_recipes will ***only*** retireve the recipes created by ***that authenticated user***.

- Tags and ingredients endpoints require a Token to CRUD. Tags and ingredients that are created on recipe creation, are available to be manipulated here. Alternatively, tags and ingredients can be created by these endpoints, and used on recipe creation.

- Search functionality that filters recipes by tags, ingridients, name, and description.

- Automated API documentation using **drf-spectacular** and **Swagger**.

- Landing page that gives a sense of direction to users.

Feel free to reach me if you encounter any problems getting it to work. I will try to resolve the issue.

***Note: This project is for self education purposes.***