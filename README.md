OAUTH2 SERVER WITH FLASK
========================

DESCRIPTION:
------------
We will learn to protect resources with access token, For this example we will use [oauth2 server with flask](https://flask-oauthlib.readthedocs.io/en/latest/oauth2.html)

Prerequisites / Requirements
----------------------------
install these requirements

1. Download and Install [Docker](https://docs.docker.com/v17.09/engine/installation/)

Getting Started
---------------

1. clone this repository:
  `git@github.com:jack-factor/flask-oauth2.git`

2. pull image:
  `docker pull python:3.7-slim`

3. create a image (into repository):
  `docker build . -t api-oauth`

4. create a container:
  `docker run --rm -d -it -p 5000:5000 --name api-oauth api-oauth`

5. In your shell:

  `curl -X POST http://localhost:5000/oauth/token` 

  This return the next respose: {"error": "unsupported_grant_type"}

6. For a success test (create an access token):

  `curl -X POST http://localhost:5000/oauth/token \
   --data "grant_type=password" \
   --data "client_id=3DdJGJccboo576fsd3op986ddszx" \
   --data "client_secret=MN435DSFS7ugsd219ojkhujuwdg43P21df3" \
   --data "username=jack12972@gmail.com" \
   --data "password=123456"` 

  The response will be like this: {"access_token": "jpOnJgCUI8tII1uqoPX35zxS9IfV5e", "expires_in": 3600, "token_type": "Bearer", "scope": "", "refresh_token": "6gwxOBba6OPGXWeZv4Rc9vQbQzjANp"}%

 7. Testing our access token:

   `curl -X POST http://localhost:5000/oauth/me \
    --header 'Authorization: Bearer <access_token>'`

   This access token protect the resource "me":

   `{
  		"celphone": "999999999",
 	    "document": "44444444",
  	    "email": "jack12972@gmail.com",
  		"lastname": "Moreno",
  		"name": "Jack",
  		"telephone": null
  	}`
