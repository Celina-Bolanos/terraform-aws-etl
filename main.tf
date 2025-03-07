provider "aws" {
  region = "us-west-2"
}

provider "random" {}

resource "random_pet" "name" {}

resource "aws_instance" "weather_api" {
  ami                    = "ami-027951e78de46a00e" #"ami-a0cfeed8"
  instance_type          = "t2.micro"
  user_data              = file("init-script.sh")
  vpc_security_group_ids = [aws_security_group.web-sg.id]
  iam_instance_profile = "${aws_iam_instance_profile.dynamo_profile.name}"
  key_name = "ec2_pair"

  tags = {
    Name = random_pet.name.id
  }
}

resource "aws_security_group" "web-sg" {
  name = "${random_pet.name.id}.sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Not recommended. You may change to your own IP
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_dynamodb_table" "raw-weather-table" {
  name           = "raw_weather_data"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "name"
  range_key      = "dt"

  attribute {
    name = "name"
    type = "S"
  }

  attribute {
    name = "dt"
    type = "N"
  }
}