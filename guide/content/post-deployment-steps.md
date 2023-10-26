---
weight: 9
title: PostDeployment Options
description: Post deployment options
---

## Verifying the solution functionality

After deploying the ABI package, you can verify its functionality by checking the following:

1. **AWS Management Console**: Wait for the CloudFormation stack to finish deploying, and then check the status of the deployment by running the following command:

aws cloudformation describe-stacks --stack-name <YOUR_STACK_NAME>
The stack status is returned in the output. Wait until the status is CREATE_COMPLETE before proceeding to the next step. When the stack finishes deploying, you can check the AWS resources created via the AWS Management Console or AWS CLI.

2. **CloudCheckr Dashboard**: Log in to your CloudCheckr account and check if the AWS account has been credentialed and if the expected data is being pulled in .


**Next:** Choose [Test the Deployment](/test-deployment/index.html) to get started.