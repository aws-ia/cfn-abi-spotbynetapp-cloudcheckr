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

## Launch on AWS Organizations member accounts using AWS CloudFormation Stacksets
If you're using this solution in an AWS organization that doesn't use AWS Control Tower, you need to create IAM roles to [Set up basic permissions for stack set operations](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html#stacksets-prereqs-accountsetup) so that this ABI solution can be deployed to all member accounts in the AWS Organizations or to specific accounts or OUs you select.

    1. You need to create an IAM role (AWSCloudFormationStackSetAdministrationRole) in your management account to establish a trusted relationship between the account you're administering the stack set from and the account you're deploying stack instances to. The CloudFormation template to create this role is [available here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html#stacksets-prereqs-accountsetup).
    
    2. You need to create an IAM execution role (AWSCloudFormationStackSetExecutionRole) for AWS CloudFormation to deploy the StackSets across all member accounts with in the organization. You can use [this CloudFormation template](https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/AWSCloudFormationStackSetExecutionRole.yml) and deploy the stack acoss the organization using instructions from [Create a stack set with service-managed permissions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html#stacksets-orgs-associate-stackset-with-org)
    
    3. From your Management Account create your AWS CloudFormation StackSets and chose `Self-service permissions` under Permission model and use `AWSCloudFormationStackSetAdministrationRole` for the IAM admin role name and  `AWSCloudFormationStackSetExecutionRole` for the IAM execution role name and then you can select the CloudFormation template from `https://github.com/aws-ia/cfn-abi-spotbynetapp-cloudcheckr/blob/main/templates/CCBuiltIn.yaml`.
    [AWS CloudFormation StackSets Self-service permissions](/images/stack-set-admin.png)


## Launch using Customizations for Control Tower (CfCT) {#launch-cfct}

Customizations for AWS Control Tower combines AWS Control Tower and other highly available, trusted AWS services to help customers set up a secure, multiaccount AWS environment according to AWS best practices. You can add customizations to your AWS Control Tower landing zone using an AWS CloudFormation template and service control policies (SCPs). You can deploy the custom template and policies to individual accounts and organizational units (OUs) within your organization.

CfCT also integrates with AWS Control Tower lifecycle events to hlep ensure that resource deployments stay in sync with your landing zone. For example, when you create a new account using AWS Control Tower account factory, CfCT deploys all of the resources that are attached to the account.

The templates provided by this ABI package are deployable through CfCT.

### Prerequisites

The CfCT solution can't launch resources in the management account by default. You need select pCreateAWSControlTowerExecutionRole : true to allow the stack to create the role or must manually create a role in that account that has necessary permissions.

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
