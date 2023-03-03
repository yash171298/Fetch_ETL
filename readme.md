# Data Engineering Take Home: ETL off a SQS Queue

# Steps to follow to execute this project
- Install docker desktop and postgres(pgadmin) to run this project
- run command pip install -r requirements.txt in cli
- run docker-compose up
- The run aws configure in your cli. 
- Add any random secret key and access key and region accordingly
- You can run awslocal sqs create-queue --queue-name sample-queue and awslocal sqs send-message --queue-url http://localhost:4566/00000000000/sample-queue --message-body test or you can use http://localhost:4566/000000000000/login-queue.
- Connection to the postgres should be simple using the credentials and table name provided in the exercise.Please set password in main.py accordingly.
- run python main.py which should start executing SQS messages and push them to DB accordingly.
- You can monitor DB in pgadmin to see new messages and details added having masked device_id and ip.

The project has been thoroughly tested and compiles flawlessly. Please let me know if you encounter any issues during the compilation process.

# Questions in exercise

- How will you read messages from the queue?
To read messages from an AWS SQS queue, we can use the boto3 library, which is a Python SDK for AWS. 

- What type of data structures should be used?
In the solution for reading JSON data from the SQS queue and writing it to the Postgres database, we can use a few different data structures:
1) JSON
2) Dictionary
3) Tuple

- How will you mask the PII data so that duplicate values can be identified?
To mask the PII data in the device_id and ip fields, we can use a hash function that produces a fixed-length, deterministic output for each input value. This way, we can mask the original values in a way that preserves their uniqueness, so that we can still identify duplicate values.

- What will be your strategy for connecting and writing to Postgres?
To connect to and write data to Postgres, I have used the psycopg2 library, which is a popular Python library for working with Postgres databases.

- Where and how will your application run?
he application can be run on a local machine or on a server, depending on the requirements of the use case. 

- How would you deploy this application in production?
Deploying an application in production involves a number of steps, and the specific approach will depend on the requirements of the use case. 
1) Set up infrastructure
2) Configure environment variables
3) Create deployment package
4) Deploy application
5) Set up monitoring and logging
6) Test and verify
I would create a docker image and have it deployed in a container scheduled everyday. I would create an infrasturcture using terraform and used AWS ECS and deploy my image in a ECS container.

- What other components would you want to add to make this production ready?
1) Load balancer
2) CI/CD
3) Auto-scaling
4) Encryption and security
5) Backup and disaster recovery

- How can this application scale with a growing dataset.
1) Database optimization
2) Caching
3) Asynchronous processing
4) Performance Monitoring
- How can PII be recovered later on?
If PII is masked or encrypted during processing, it can be recovered later using a decryption key or other means of unmasking the data. However, it is important to ensure that access to the decryption key is restricted to authorized personnel and that proper security protocols are in place to protect against unauthorized access or data breaches.

- What are the assumptions you made?
1) Development environment 
2) Infrastructure: Docker
3) Data format: AWS SQS queue and assumed fields: user_id, device_id, ip, device_type, locale, app_version, and create_date.