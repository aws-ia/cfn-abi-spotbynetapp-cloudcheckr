---
weight: 99
title: Cleanup Instructions
description: Instructions to clean up the resources created by the ABI package
---

## Cleanup Instructions

To ensure that all resources created by the ABI package are removed and you do not incur any unexpected costs, follow the instructions below. The cleanup process involves deleting the CloudFormation stack and all associated resources.

![Under Construction](/images/under_construction.jpeg)

### Deleting the CloudFormation Stack:

1. **Navigate to the AWS CloudFormation Console:**
   Open the [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/).
2. **Find the Stack:**
   Locate the stack created by the ABI package in the list of stacks.
3. **Delete the Stack:**
   Select the stack and choose “Delete”. Confirm the deletion to proceed. AWS CloudFormation will automatically delete all related resources.

### Deleting Additional Resources:

If any additional resources were created outside of the CloudFormation stack, be sure to delete them manually. These may include:

- S3 Buckets
- IAM Roles
- Lambda Functions

#### For S3 Buckets:

1. **Navigate to the S3 Console:**
   Open the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. **Locate and Delete the Buckets:**
   Find the buckets created by the ABI and delete them.

#### For IAM Roles:

1. **Navigate to the IAM Console:**
   Open the [AWS IAM Console](https://console.aws.amazon.com/iam/).
2. **Locate and Delete the Roles:**
   Find the roles created by the ABI and delete them.

#### For Lambda Functions:

1. **Navigate to the Lambda Console:**
   Open the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. **Locate and Delete the Functions:**
   Find the Lambda functions created by the ABI and delete them.

### Verification:

After deleting the resources, ensure that no additional resources are left undeleted. Verify in each service console that all related resources have been removed. If any resources are left, they may continue to incur costs.

**Note:** Be cautious and ensure that you are only deleting resources related to the ABI, to avoid accidentally deleting important resources.
