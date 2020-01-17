Create a python web app(Use web framework of your choice, however flask is preferred) to save and list learning topics list from https://www.tutorialspoint.com/<technology>/index.htm for a given technology
1. Add GET API to fetch latest content list from the above URL  - GET topics/<technology>
                If technology details are present in local DB, serve the technology topics list
                If not, in the backend asynchronously call the tutorialspoint html page to get the content
                                API should be async, it should call the https://www.tutorialspoint.com/python/index.htm in the backend asynchronously
                                                - parse the html page content 
                                                - Persist all the topics list 
                NOTE: In this case a task/job id should be returned which client can poll to check if content parsing is done.
2. Listing API GET topics/ to list all available technology and topic names from local DB.
3. Update API PUT topics/<technology> to update the topics list in the local db
                In the backend asynchronously call the tutorialspoint html page to get the content
4. Delete API topics/<technology> to delete the technology and topics from the local db.

- Design the DB schema to persist the data.
- Use SQLite(or of your choice) as database to persist the data.
- Use swagger and openAPI specs to validate API request and response schemas
- Write unit test for functions/methods
- Automate the deployment using docker to deploy application as a container
- All unit tests should get run as a part of application deployment

GET: topics/<technology>
POST
PUT: PUT topics/<technology> to update the topics list 
DELETE: Delete API topics/<technology>  