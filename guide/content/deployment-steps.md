---
weight: 10
title: Deployment steps
description: Deployment steps
---

## Launch the CloudFormation Template in the Management Account

1. Download the CloudFormation template from the source: `https://<abi-template-location>`
2. Launch the CloudFormation template in your AWS Control Tower home region.
    * Stack name: `template-cfn-abi-spotbynetapp-cloudcheckr-enable-integrations`
    * List Parameters:
        * **pAPIKey**: The API ID created in the CloudCheckr environment.
        * **pAPISecret**: The secret associated with the APIKey.
        * **pCustomerNumber**: Found in the URL when logged into CloudCheckr. Example: https://app-us.cloudcheckr.com/customers/1234567 (The number after /customers/  in this case the customer number would be 1234567).
        * **pCurBucketName**: Name of the S3 bucket for CUR data (If master payer account).
        * **pCloudTrailBucketName**: Name of the S3 bucket of the organizational CloudTrail. For AWS Control Tower environments this follows the pattern (aws-controltower-logs-[AWS-LOG-ACCOUNT-ID]-[AWS-CONTROL-TOWER-HOME-REGION]) and can also be found in the AWS Control Tower console under Shared Accounts - Log archive - Log location in S3
        * **pABIStagingS3Key**: The staging S3 key for ABI.
        * **pABISourceS3BucketName**: The source S3 bucket name for ABI.
        * **pABIS3BucketRegion**: The region of the S3 bucket for ABI.
   
3. Choose both the **Capabilities** and select **Submit** to launch the stack.
   - [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.
   - [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND   

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.

## Launch using Customizations for Control Tower (CfCT)

Customizations for AWS Control Tower (CfCT) combines AWS Control Tower and other AWS services to help you set up an AWS environment. You can deploy the templates provided with the ABI solution using CfCT.

To deploy this sample partner integration page using CfCT, add the following blurb to the manifest.yaml file from your CfCT solution and update the account names as needed.

#### Pre-requisites

1. Create an IAM role with the required permissions in the AWS management account to allow the CfCT solution to launch resources.

#### How it works

To deploy the sample partner integration page, add the following blurb to the manifest.yaml file from your CfCT solution and update the account and organizational unit (OU) names as needed..

```yaml
resources:
resources:
  - name: deploy-cloudcheckr-init-stack
    resource_file: https://aws-abi.s3.us-east-1.amazonaws.com/cfn-abi-spotbynetapp-cloudcheckr/templates/CCBuiltIn.yaml
    deploy_method: stack_set
    parameters:
      - parameter_key: pAPIKey #The API ID created in the CloudCheckr environment.
        parameter_value: $[cloudcheckr/api_key] 
      - parameter_key: pAPISecret #The API Secret created in the CloudCheckr environment.
        parameter_value: $[cloudcheckr/api_secret]
      - parameter_key: pABISourceS3BucketName #The source S3 bucket name for ABI.
        parameter_value: aws-abi
      - parameter_key: pABIStagingS3Key #The staging S3 key for ABI.
        parameter_value: cfn-abi-spotbynetapp-cloudcheckr
      - parameter_key: pCloudTrailBucketName #Name of the S3 bucket of the organizational CloudTrail.
        parameter_value: [aws-controltower-logs-[AWS-LOG-ACCOUNT-ID]-[AWS-CONTROL-TOWER-HOME-REGION]
      - parameter_key: pCurBucketName #Name of the S3 bucket for CUR data (If master payer account).
        parameter_value: [[CUR-S3-BUCKET-NAME]]
      - parameter_key: pCustomerNumber #Found in the URL when logged into CloudCheckr. Example: https://app-us.cloudcheckr.com/customers/1234567 (The number after /customers/  in this case the customer number would be 1234567).
        parameter_value: [[CLOUDCHECKR-CUSTOMER-NUMBER]]
    regions:
      - us-east-1 # Update as needed
    deployment_targets:
      organizational_units: #Update as needed
        - OUName1
        - OUName2 
