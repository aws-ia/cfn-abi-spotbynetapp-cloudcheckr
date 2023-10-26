---
weight: 1
title: CloudCheckr ABI Automation
description: Automate the process of configuring and credentialing CloudCheckr from the AWS marketplace
---

# CloudCheckr ABI Automation

The purpose of this document is to walk you through the process of automating the configuration and credentialing of CloudCheckr from the AWS marketplace. This document is intended for Customers who are using the CloudCheckr ABI and in the process of building an ABI project.

The AWS Built-in program is a differentiation program that validates Partner solutions which have automated their solution integrations with relevant AWS foundational services like identity, management, security and operations. This program helps customers find and deploy a validated Partner solution that addresses specific customer use cases while providing deep visibility and control of AWS native service integration.

## Prerequisites

Before you start, make sure you have completed the following steps:

1. Ensure you have an IAM role in your AWS account to run the ABI, and that you have the necessary permissions to create and manage CloudFormation stacks, as well as access to the required services such as S3 and Lambda.
2. Purchase CloudCheckr on AWS Marketplace at AWS Marketplace. For private pricing options reach to CloudCheckr at Contact Sales
3. Upon purchasing CloudCheckr, a CloudCheckr account is created, a user is automatically generated, and an email is sent to you with login instructions.
4. Using the activation link, login into CloudCheckr.
5. Create an API key and Secret within CloudCheckr:
   - Click the three vertical dots in the top right corner.
   - Select Access Management > API Management.
   - Choose Clients and click +NEW.
   - Name your API client and set the client Role to "Full administrator".
   - Save the new client.
   - Click +new to generate an access key, provide a name, and select Create.
   - Copy the API secret

Choose [Overview](/overview/index.html) to get started.


