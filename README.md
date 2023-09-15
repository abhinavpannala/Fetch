# FetchJob at Fetch
 **Data Engineering ETL task**

## Environment Setup:
- **Install python** (Version used during the assessment:`Python 3.11.5`)
- **Install docker** (https://docs.docker.com/get-docker/)
- **Install Psql** (https://www.postgresql.org/download/)
- **Install awscli** (`pip3 install awscli-local`)

## Packages Required:
- **boto3**
- **psycopg2**

## Installation Steps:
1. **Pull the repository with command** `git clone https://github.com/abhinavpannala/Fetch.git`

2. **Use the command** `docker compose up` **to start and run multiple instances present in docker-compose.yml** <br>
Alternatively, `docker compose up -d` can be used to continue with other tasks from the same terminal <br>
Use command `docker ps` to check whether the docker immages are up and running.

3. **Import the necessary packages by running** `pip3 install -r requirements.txt`
4. **Run the python script using the command** `python3 main.py`


## Validate Data in the database:
1. **Access the dataabse using the commaand** `psql -d postgres -U postgres -p 5432 -h localhost -W` <br>
Password is provided in the documentation provided or in this case, it can be found in `credentials.json`

2. **Query the database using the command** `select * from user_logins;` <br>
The messages required from SQS must be displayed here.

## Next Steps:
**Cosidering the time-constraint the assessment(2-3hours), few more steps can be performed.**
- Secret Managemenet Design Patterns can be practiced to abstract the credentials information.
- Functions can be refactoreed into classes if the code complexity increases further.
- Code can be further seggregated to make it more modular.
- Logging can be implemented to gain insights of the background processes.
- Perform transformation to identify inconsistencies in the data and inlude exceptions to understand errors if any.

## Design Decisions:
- **How will you read messages from the queue?**<br>
I've implemented a generator function which runs indefinitely waiting 20 seconds between each checks. <br>
Alternatively, the function can be run manually using batch processing if continous message check is not the criteria

- **What type of data structures should be used?**<br>
I've oprted Dictionaries as they are flexible providing key-value pair and are efficient.

- **How will you mask the PII data so that duplicate values can be identified?**<br>
Opted-out Salting/Randomness/Nonce encryption techniques to implement a standard SHA512 encryption technique. This encryption mathod results in same hash value for duplicate entries helping maintain the data unique

- **What will be your strategy for connecting and writing to Postgres?**<br>
Imported a python package called psycop2 to create, execute, commit, close connections with the PSQL database

- **Where and how will your application run?**<br>
The python script is run locally which fetches the data from local stack docker image and writes the messages onto Presgres docker images. <br>
Alternatively, the script can be into the docker images, so docker images can communicate directly to run the application.

## Assessment Questions:
- **How would you deploy this application in production?** <br>
    1. Instances such as EC2 can be used to deploy the application but I'd prefer docker for portability and consistency.
    2. Create a dockerhub build.
    3. Implement a ochestration tool such as Kubernetes to manage and scale application.
    4. Deploy accross multiple availablity zones for better reliability and robustness.
    
- **What other components would you want to add to make this production ready?**<br>
    1. Introduce load balancing and auto-scaling techniques.
    2. Implement Logging and Monitoring services to analyze the performance of the nodes.
    3. Move the python script to the local stack docker image.
- **How can this application scale with a growing dataset?**<br>
    1. From the insights from monitoring services, horizontal and vertical scaling can be done manually.
    2. The data in the database can be sharded for better query performance.
    3. Decrease the wait-time in the fetch code to perform write operations more frequently on different nodes.
    4. I would use more efficient queue managers such as Kafka or Kinesis Datasteams to help process the messages faster.
    5. Caching can be performed on the database to reduce the load and improve the query performance.
- **How can PII be recovered later on?**<br>
    1. The encryption algorithm used (SHA512) is irreversible.
    2. Alternative would be to create a secondary table with restricted roles to copy the PII data.
    3. The concept of private key can be implemented to encrypt and decrypt the data using algorithms such as RSA.
- **What are the assumptions you made?**<br>
    1. The messages fetched has consistent data.
    2. The stack and database connections are successfully created using dummy credentials. 
    3. No duplicate or null messages in the SQS queue.