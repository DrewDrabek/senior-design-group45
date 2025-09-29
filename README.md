# senior-design-group45
Repo used to store senior design dlp project


## Tech Stack Documentation

THIS IS TO BE FILLED OUT MORE AS TEAM MEETS AND STARTS TO DESIGN

### Frontend

React with JS?

Is this reasonable for the team?

How are we going to run this?

If we need to put it somewhere we can do so in AWS using Amplify for free. We can have the frontend hit whatever endpoint we specify. There are AWS services that we can use in order to do this as well. Or we could have it hit a locally hosted option as well. The hosting is the easy part as it could also be a Docker container. The hard part is making the frontend look good enough for the POC and to interact with the API services that are provided by the backend.

#### Authentication

This can be done with Auth0. This is a free service that we can use for authentication and it will also provide a frontend for that authentication that we can use. There are other fancy things that we can use as well but not something that is required.

### Backend

This will be run using Docker and then this can be run on any machine that has the Docker daemon running. This can be Windows with WSL installed or Linux or on any Linux distro that can run Docker on it. This includes Macs and other machines by default. Most often I see this run on things like Ubuntu but this does not really matter.

#### API Framework

This will be FastAPI. This is very popular and has plenty of examples and documentation. This will be written in Python that makes it easy to read and there are plenty of libraries that will and can be used to support the project. The only thing that will need to be researched and decided on will be the library that will support the DAC (data access connection service). This will be how the backend interacts with the database. The business logic should be pretty easy to manage and should not need anything crazy but if there are other libraries then these will be added as we go.

## Database

The initial database engine that was talked about was PostgreSQL but this can change as we go. This was originally chosen since there are no license costs so we can spin this up in something like AWS very cheaply. We can do most engines as they have a free dev/learning tier but they are all SQL just a little different here and there. 
