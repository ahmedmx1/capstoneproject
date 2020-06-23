# Casting Agency

Casting Agency is a service that is responsible for creating movies and managing and assigning actors to those movies.

The application performs the following functions:
- Showing existing actors and movies, creating actors and movies, editing actors and movies data, delete actors and movies.
- **Casting Assistant** can view actors and movies.
- **Casting Director** has all permissions of Casting Assistant, add or delete an actor from the database and modify actors or movies.
- **Executive Producer** has all permissions of Casting Director and add or delete a movie from the database.

# Getting started

- Casting Agency API is hosted on heroku
- **Base URL**: [localhost:5000/](http://localhost:5000/)

- API has an Authentication managed by Auth0

# Error Handling

**Errors** are returned as JSON object like th following:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
#### API will handle these errors:
- **400** bad request
- **404** resources not found
- **422** unprocessable
- **500** Internal Server error

# Endpoints

### GET /actors

- returns list of actors and success value
- sample `curl -X GET http://localhost:5000/actors`

```
{
    "actors": [
        {
            "name": "actor name",
            "age": "15",
            "gender": "male"
        }, 
        {
            "name": "actor name 2",
            "age": "15",
            "gender": "male"
        }
    ], 
    "success": True
}
```


### GET /movies


### POST /actors


### POST /movies


### DELETE /actors


### DELETE /movies


### PATCH /actors


### PATCH /movies
