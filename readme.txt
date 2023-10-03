# README 

This ABI is designed to automate the process of configuring and credentialing CloudCheckr for customers/partners once purchased from the AWS marketplace. This automation includes building an IAM Role, generating and credentialing an AWS account in CloudCheckr, as well as setting up required resources such as S3 buckets, Lambda functions, and CloudFormation stacks etc.
Using this ABI, CloudCheckr customers can monitor their environment for CloudWatch events automatically and efficiently, as well as access other valuable cloud management features within CloudCheckr. 
#ABI for CloudCheckr Built-In Documentation

Prerequisites (Manual)

1. Ensure you have an IAM role in your AWS account to run the ABI, and that you have the necessary permissions to create and manage CloudFormation stacks, as well as access to the required services such as S3 and Lambda..
2. Purchase CloudCheckr on AWS Marketplace at 
https://aws.amazon.com/marketplace/pp/prodview-s3pimhbls2qpm. 
For private pricing options reach to CloudCheckr at https://cloudcheckr.com/contact-sales/
3. Upon purchasing CloudCheckr, a CloudCheckr account is created, a user is automatically generated, and an email is sent to you with login instructions.
3. Using the activation link, login into CloudCheckr.
3. Create an API key and Secret within CloudCheckr:
   - Click the three vertical dots in the top right corner.
   - Select Access Management > API Management.
   - Choose Clients and click +NEW.
   - Name your API client and set the client Role to "Full administrator".
   - Save the new client.
   - Click +new to generate an access key, provide a name, and select Create.
   - Copy the API secret and API ID number for later use in the CloudFormation stack.
For more details around creating an API key please refer to https://success.cloudcheckr.com/article/93urirlmng-cloudcheckr-cmx-api.


Running ABI


After completing the prerequisites, you can now run ABI to automatically provision your AWS account within the CloudCheckr environment. The template will require the following information:
- APIKey: The API ID created in the CloudCheckr environment.
- APISecret: The secret associated with the APIKey.
- BillingBucketName: Name of the S3 bucket for billing data. (if used in environment, or can be left blank) (***ensure versioning is enabled on S3 bucket***)
- CloudTrailBucketName: Name of the S3 bucket for CloudTrail logs. (if used in environment, or can be left blank) (ensure versioning is enabled on S3 bucket***)
- CurBucketName: Name of the S3 bucket for CUR data. (***For payer account only*** if used in environment, or can be left blank) - CloudCheckr requires a CUR bucket with a specific format, please refer to 
   https://success.cloudcheckr.com/article/v663i9wzaj-configure-the-cost-and-usage-report-in-aws for detail instructions to setup CloudCheckr specific CUR.  (***ensure versioning is enabled on S3 bucket***)
   Once the CUR is created in AWS please follow the instructions to configure CUR report in CloudCheckr https://success.cloudcheckr.com/article/emle9kpgbz-configure-the-cost-and-usage-report-in-cloud-checkr
- CustomerNumber: Found in the URL when logged into CloudCheckr. Example: https://app-us.cloudcheckr.com/customers/1234567 (The number after /customers/  in this case the customer number would be 1234567).

## Parameters

The template includes the following parameters:
- `pAPIKey`: The API key for CloudCheckr.
- `pAPISecret`: The API secret for CloudCheckr.
- `pCustomerNumber`: The customer number for CloudCheckr.
- `pCurBucketName`: The name of the S3 bucket for CUR (Cost and Usage Report) data. (Only needed for AWS Payer accounts)
- `pBillingBucketName`: The name of the S3 bucket for billing data.
- `pCloudTrailBucketName`: The name of the S3 bucket for CloudTrail logs.
- `pSRAStagingS3Key`: The S3 key for staging resources. Default value: `cfn-abi-spotbynetapp-cloudcheckr`. (we suggest leaving the default)
- `pSRASourceS3BucketName`: The name of the source S3 bucket for Lambda function packages. Default value: `aws-abi-pilot`. (we suggest leaving the default)

## Resources

The CloudFormation template creates the following resources:
- `rABIStagingS3Bucket`: An S3 bucket for staging resources.
- `rABIStagingS3BucketPolicy`: A bucket policy for the staging S3 bucket.
- `rLambdaExecutionRole`: An IAM role for Lambda execution.
- `rLambdaawsCreateAccountFunction`: A Lambda function for creating AWS accounts.
- `rCustomResourceAwsCreateAccountInvoke`: A custom resource that invokes the `rLambdaawsCreateAccountFunction` Lambda function.
- `rgetExternalIDFunction`: A Lambda function for getting the external ID.
- `rCustomResourceGetExternalIDInvoke`: A custom resource that invokes the `rgetExternalIDFunction` Lambda function.
- `rdeployIAMstack`: A CloudFormation stack that deploys an IAM stack using an external template.
- `rLambdaAwsCredentialAccountFunction`: A Lambda function for credentialing the AWS account.
- `rCustomResourceAwsCredentialAccountInvoke`: A custom resource that invokes the `rLambdaAwsCredentialAccountFunction` Lambda function.
- `rCopyZips`: A custom resource that copies Lambda function packages from the source S3 bucket to the staging S3 bucket.
- `rCopyZipsRole`: An IAM role for the `rCopyZips` custom resource.
- `rCopyZipsFunction`: A Lambda function for copying objects between S3 buckets.

Note: Remember to clean up the resources created by deleting the CloudFormation stack when you no longer need them to avoid incurring unnecessary costs.
