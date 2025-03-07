### ETL pipeline with terraform and AWS

#### Description

In this repository you may find an example of building an <br>
ETL pipeline with terraform and aws to collect, transform and load <br>
weather information for 10 belgian cities. <br><br>

Terraform has been used to manage the required infraestructure on aws cloud services.<br>

#### Requirements

If you would like to try this pipeline out, please note you need the following prior to start:

- AWS account and credentials (aws_secret_key and aws_secrect_access_key)
- AWS key-pair on your local machine (to avoid downloading the private key each time you want to try this out.)
- Free API from openweathermap.org

Software:
- aws CLI
- Terraform 1.11.1


#### Installation

- Building the infraestructure:

1. Clone this repository: ``` git clone https://github.com/Celina-Bolanos/terraform-aws-etl.git ``` 
2. On main.tf, look for  "resource "aws_instance" "weather_api" and replace the "key-pair" parameter value with the name of your own key-pair's name.
3. On python_utils/etl.py, enter your API from openweathermap.org.
4. On your termnal, cd to the cloned repository directory.
5. Sign in to aws ```aws configure``` 
6. Run ``` terraform init ``` to iniciate terraform on that directory.
7. Run ``` terraform apply ``` to start building the infraestructure.
8. Confirm the build resouces with `yes` when prompted.

This will create the necessary resources on your aws account: ec2, dynamodb, vpc, security groups, roles, etc.

- Running the pipeline:

1. From your aws management console, copy the ec2 instance's public ip address.<br><br>
2. On your terminal, sign into the EC2 instance: <br>
     ``` ssh -i /home/user/path/to/your/key_pair.pem ec2-user@your.ec2.ip.address```<br><br>
3. From another terminal, copy the etl.py file on your local machine to the ec2 instance via sco (secure copy):<br>
    ```scp -i /home/user/path/to/your/key_pair.pem /home/user/path/to/repository/terraform-aws-etl/python_utils/etl.py ec2-user@your.ec2.ip.address:/home/ec2-user/home```<br><br>
4. Copy the requirements.txt to your ec2 instance:<br>
    ```scp -i /home/user/path/to/your/key_pair.pem /home/user/path/to/repository/terraform-aws-etl/python_utils/requirements.txt ec2-user@your.ec2.ip.address:/home/ec2-user/home```<br><br>
5. On the terminal where you logged in to ec2 run ```python3 install -r requirements.txt```<br><br>
6. Then run ```python3 etl.py```<br><br>

This second part will start collecting weather data, perform some small transformations and load it to the aws dynamodb. <br>
You may confirm the data is being loaded via the aws console management, DynamoDB. <br>
Alternativelly, you may check db_test.ipynb on your local machine to see some records and even see <br>
see some EDA like the warmest city, or average temperature per city.<br># terraform-elt


#### Colaborators
Celina Bolanos