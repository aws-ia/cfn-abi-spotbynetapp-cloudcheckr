---
weight: 8
title: Deployment steps
description: Deployment steps
---

## Launch the CloudFormation template in the AWS Organizations management account {#launch-cfn}

1. Download the CloudFormation template: `https://github.com/aws-ia/cfn-abi-spotbynetapp-cloudcheckr/blob/main/templates/CCBuiltIn.yaml`
2. Launch the CloudFormation template in your AWS Control Tower home Region.
    * Stack name: `template-cfn-abi-spotbynetapp-cloudcheckr-enable-integrations`
    * List parameters:
        * **pAPIKey**: The API ID created in the CloudCheckr environment.
        * **pAPISecret**: The secret associated with the APIKey.
        * **pEnvironment**: The environment associated with your CloudCheckr Instance (US, EU, AU, GOV)
        * **pCustomerNumber**: Found in the URL when logged into CloudCheckr, for example https://app-us.cloudcheckr.com/customers/1234567. In this example, the customer number is 1234567.
        * **pCurBucketName**: Name of the S3 bucket for CUR data (if master payer account).
        * **pCloudTrailBucketName**: Name of the S3 bucket for CloudTrail logs.
        * **pABIStagingS3Key**: The staging S3 key for AWS Built-in.
        * **pABISourceS3BucketName**: The source S3 bucket name for AWS Built-in.
        * **pABIS3BucketRegion**: The Region of the S3 bucket for AWS Built-in.

3. Choose both **Capabilities** and then **Submit** to launch the stack.
   - [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.
   - [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND.

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.

## Launch using Customizations for Control Tower {#launch-cfct}

You can use CfCT to deploy the templates provided with the AWS Built-in package.

### Prerequisites

The CfCT solution does not launch resources on the management account. Therefore, you must create the role with required permissions in the management account.

### How it works

To deploy this sample partner integration page using CfCT, add the following blurb to the `manifest.yaml` file from your CfCT solution and update the account/ou names as needed.

```yaml
resources:
  - name: deploy-cloudcheckr-init-stack
    resource_file: https://aws-abi.s3.us-east-1.amazonaws.com/cfn-abi-spotbynetapp-cloudcheckr/templates/CCBuiltIn.yaml
    deploy_method: stack_set
    parameters:
      - parameter_key: pAPIKey #The API ID created in the CloudCheckr environment.
        parameter_value: $[cloudcheckr/api_key]
      - parameter_key: pAPISecret #The API Secret created in the CloudCheckr environment.
        parameter_value: $[cloudcheckr/api_secret]
      - parameter_key: pEnvironment #The environment associated with your CloudCheckr Instance (US, EU, AU, GOV)
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
```

**Next**: [Postdeployment options](/post-deployment-steps/index.html)
