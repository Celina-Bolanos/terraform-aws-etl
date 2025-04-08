### ETL pipeline with terraform, AWS and Airflow

#### Description

In this repository you may find an example of building an <br>
ETL (extract, transform, load) pipeline on weather information <br>
for 10 belgian cities, using these technologies: <br><br>

AWS: for cloud services<br>
Airflow: to run the pipeline on a schedule <br>
Terraform: to manage the necessary infraestructure on aws<br>


#### Requirements

If you would like to try this pipeline out, please note you need the following prior to start:

- AWS account and credentials (aws_secret_key and aws_secrect_access_key)
- AWS key-pair on your local machine (to avoid downloading the private key each time you want to try this.)
- Free API from openweathermap.org

Software:
- AWS CLI 
- Airflow 2.10.5
- Terraform 1.11.1


#### Installation

- Building the infraestructure:

1. Clone this repository: ``` git clone https://github.com/Celina-Bolanos/terraform-aws-etl.git ``` 
2. On main.tf, look for  "resource "aws_instance" "weather_api" and replace the "key_name" parameter value with the name of your own key-pair's name.
3. On python_utils/etl_dag.py, enter your API from openweathermap.org.
4. On your terminal, cd to the cloned repository directory.
5. Sign in to aws ```aws configure``` 
6. Run ``` terraform init ``` to iniciate terraform on that directory.
7. Run ``` terraform apply ``` to start building the infraestructure.
8. Confirm the build of resouces with `yes` when prompted.

This will create the necessary resources on your aws account: ec2, dynamodb, vpc, security groups, roles, etc.

- Running the pipeline:

1. From your aws management console, copy the ec2 instance's public ip address.<br><br>

2. On your terminal, copy the etl_dag.py file from your local machine to the ec2 instance via scp (secure copy):<br>
    ```scp -i /home/user/path/to/your/key_pair.pem /home/user/path/to/repository/terraform-aws-etl/python_utils/etl_dag.py ec2-user@your.ec2.ip.address:/home/ec2-user/```<br><br>
3. Now, copy the requirements.txt to your ec2 instance:<br>
    ```scp -i /home/user/path/to/your/key_pair.pem /home/user/path/to/repository/terraform-aws-etl/python_utils/requirements.txt ec2-user@your.ec2.ip.address:/home/ec2-user/```<br><br>

2. Sign into the EC2 instance from your terminal: <br>
     ``` ssh -i /home/user/path/to/your/key_pair.pem ec2-user@your.ec2.ip.address```<br><br>


5. Once logged into the EC2 instance, create a new virtual environment and activate it: <br>
```python3 -m venv airflow-env ``` <br>
```source airflow-env/bin/activate ``` <br>

6. Run ```python3 install -r requirements.txt```

7. Run ``` python3 install apache-airflow ``` 

8. Move to the 'airflow' folder ```cd airflow ```
9. Create the dags directory ``` mkdir dags ```
10. Go back and move etl_dag to the dags folder: <br>
    ``` cd ..``` <br>
    ```mv etl_dag.py airflow/dags ``` <br>
11. Start airflow and the airflow scheduler: <br>
    ```airflow db migrate ``` <br>
    ```airflow scheduler ``` <br>

12. Finally, unpause the dag to start runing the pipeline: <br>
    ```airflow dags  unpause weather_pipeline ```

This second part will start collecting weather data, perform some small transformations and load it to the aws dynamodb table every five minutes. <br>
You may confirm the data is being loaded via the aws console management. <br>
Alternativelly, you may run all cells of db_test.ipynb on your local machine to see some records and even see <br>
see some EDA like the warmest city, or average temperature per city.<br>

#### Colaborators
Celina Bolanos