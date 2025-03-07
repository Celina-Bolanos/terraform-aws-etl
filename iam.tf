resource "aws_iam_role" "dynamo_role" {
  name = "dynamo_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_instance_profile" "dynamo_profile" {
  name = "dynamo_profile"
  role = "${aws_iam_role.dynamo_role.name}"
}


resource "aws_iam_role_policy" "pipeline_policy" {
  name = "pipeline_policy"
  role = "${aws_iam_role.dynamo_role.id}"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudwatch:DeleteAlarms",
                "cloudwatch:DescribeAlarmHistory",
                "cloudwatch:DescribeAlarms",
                "cloudwatch:DescribeAlarmsForMetric",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics",
                "cloudwatch:PutMetricAlarm",
                "dynamodb:*",
                "sns:CreateTopic",
                "sns:DeleteTopic",
                "sns:ListSubscriptions",
                "sns:ListSubscriptionsByTopic",
                "sns:ListTopics",
                "sns:Subscribe",
                "sns:Unsubscribe",
                "sns:SetTopicAttributes"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Sid": "DDBConsole"
        },
        {
            "Action": [
                "lambda:*",
                "iam:ListRoles"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Sid": "DDBConsoleTriggers"
        },
        {
            "Action": [
                "datapipeline:*",
                "iam:ListRoles"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Sid": "DDBConsoleImportExport"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRolePolicy",
                "iam:PassRole"
            ],
            "Resource": [
                "*"
            ],
            "Sid": "IAMEDPRoles"
        },
        {
            "Action": [
                "ec2:CreateTags",
                "ec2:DescribeInstances",
                "ec2:RunInstances",
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:TerminateInstances",
                "elasticmapreduce:*",
                "datapipeline:*"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Sid": "EMR"
        },
        {
            "Action": [
                "s3:DeleteObject",
                "s3:Get*",
                "s3:List*",
                "s3:Put*"
            ],
            "Effect": "Allow",
            "Resource": [
                "*"
            ],
            "Sid": "S3"
        }
    ]
})

}