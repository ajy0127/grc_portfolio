# Lab 2: Identity and Access Management - Step-by-Step Guide

This guide provides detailed instructions for implementing a comprehensive identity and access management solution on AWS. By following these steps, you will establish security best practices for IAM, implement role-based access control, set up permission boundaries, configure identity federation, and analyze access patterns.

## Module 1: IAM Foundations and Best Practices

### 1.1 Review Your Current IAM Configuration

1. Sign in to the AWS Management Console and navigate to the IAM dashboard.
2. Review the IAM security status section at the top of the dashboard.
3. Make note of any security recommendations that need to be addressed.

### 1.2 Configure Your IAM Password Policy

1. In the IAM dashboard, select **Account settings** from the left navigation pane.
2. Click **Change password policy**.
3. Configure the following settings:
   - Minimum password length: 14 characters
   - Require at least one uppercase letter
   - Require at least one lowercase letter
   - Require at least one number
   - Require at least one non-alphanumeric character
   - Enable password expiration after 90 days
   - Prevent password reuse (last 24 passwords)
   - Enable password expiration requires administrator reset
4. Click **Save changes**.

### 1.3 Create IAM Admin User with MFA

1. In the IAM dashboard, select **Users** from the left navigation pane.
2. Click **Add users**.
3. For User name, enter `iam-administrator`.
4. Select **Provide user access to the AWS Management Console**.
5. Select **I want to create an IAM user**.
6. For Console password, select **Autogenerated password**.
7. Deselect **Users must create a new password at next sign-in**.
8. Click **Next**.
9. Select **Attach policies directly**.
10. Search for and select the `IAMFullAccess` policy.
11. Click **Next**.
12. Review the user details and click **Create user**.
13. On the success page, download the CSV file with the user's credentials.
14. Sign out and log back in as the new `iam-administrator` user.
15. Set up MFA for the `iam-administrator` user:
    - In the IAM dashboard, select **Users** from the left navigation pane.
    - Select the `iam-administrator` user.
    - Select the **Security credentials** tab.
    - Under Multi-factor authentication (MFA), click **Assign MFA device**.
    - Choose your preferred MFA type (Virtual, Security Key, or Hardware TOTP).
    - Follow the prompts to complete MFA setup.

### 1.4 Implement IAM User Lifecycle Management

1. Create a script to automate IAM user management (we'll use AWS CLI):
   - Create or navigate to the `scripts` directory within Lab 2.
   - Create a file named `iam-user-lifecycle.sh`.
   - Add script content to create, audit, and deactivate IAM users.
   - Make the script executable with `chmod +x iam-user-lifecycle.sh`.

2. Test the script to create a test user:
   ```bash
   ./iam-user-lifecycle.sh create-user test-user
   ```

3. Verify the user was created in the IAM dashboard.

## Module 2: Role-Based Access Control

### 2.1 Design IAM Roles for Common Job Functions

1. In the IAM dashboard, select **Roles** from the left navigation pane.
2. Click **Create role**.
3. Select **AWS service** as the trusted entity type.
4. Under Common use cases, select **EC2**.
5. Click **Next**.
6. Search for and select the `AmazonS3ReadOnlyAccess` policy.
7. Click **Next**.
8. For Role name, enter `EC2-S3ReadOnly`.
9. For Description, enter `Allows EC2 instances to read from S3 buckets`.
10. Click **Create role**.

Repeat this process to create the following roles:

**DevOps Role**
- Name: `DevOps-Role`
- Trusted entity: AWS account (this account)
- Policies: `AmazonEC2FullAccess`, `AmazonS3FullAccess`, `AmazonRDSFullAccess`
- Description: `Role for DevOps engineers to manage EC2, S3, and RDS resources`

**Security Auditor Role**
- Name: `Security-Auditor`
- Trusted entity: AWS account (this account)
- Policies: `SecurityAudit`, `IAMReadOnlyAccess`
- Description: `Role for security team members to audit AWS resources`

**Finance Role**
- Name: `Finance-Billing`
- Trusted entity: AWS account (this account)
- Policies: `Billing`, `AWSBudgetsReadOnlyAccess`
- Description: `Role for finance team members to access billing information`

### 2.2 Implement Custom IAM Policies

1. In the IAM dashboard, select **Policies** from the left navigation pane.
2. Click **Create policy**.
3. Select the JSON tab.
4. Enter the following policy document:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-company-data",
                "arn:aws:s3:::my-company-data/*"
            ],
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "192.0.2.0/24"
                }
            }
        }
    ]
}
```

5. Click **Next**.
6. For Policy name, enter `RestrictedS3Access`.
7. For Description, enter `Allows read-only access to the company data bucket from corporate IP range`.
8. Click **Create policy**.

### 2.3 Create Policy Using the Visual Editor

1. In the IAM dashboard, select **Policies** from the left navigation pane.
2. Click **Create policy**.
3. Ensure you're on the Visual editor tab.
4. For Service, select **EC2**.
5. For Actions allowed, expand **List** and select **DescribeInstances**, **DescribeInstanceStatus**, and **DescribeInstanceTypes**.
6. Expand **Read** and select **GetConsoleOutput** and **GetConsoleScreenshot**.
7. For Resources, select **Specific**.
8. Click **Add ARN** and enter your AWS region and instance ID (or use '*' for all instances).
9. Under Request conditions, select **Add condition**.
10. For Condition Key, enter `aws:PrincipalTag/Department`.
11. For Operator, select **StringEquals**.
12. For Value, enter `IT`.
13. Click **Add**.
14. Click **Next**.
15. For Policy name, enter `IT-EC2Monitoring`.
16. For Description, enter `Allows IT department to monitor EC2 instances`.
17. Click **Create policy**.

### 2.4 Attach Policies to Roles

1. In the IAM dashboard, select **Roles** from the left navigation pane.
2. Select the `DevOps-Role`.
3. Click the **Add permissions** dropdown and select **Attach policies**.
4. Search for and select the `RestrictedS3Access` policy you created earlier.
5. Click **Add permissions**.

## Module 3: Permission Boundaries and SCPs

### 3.1 Create a Permission Boundary

1. In the IAM dashboard, select **Policies** from the left navigation pane.
2. Click **Create policy**.
3. Select the JSON tab.
4. Enter the following policy document:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:*",
                "s3:*",
                "rds:*",
                "cloudwatch:*",
                "logs:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "Action": [
                "iam:*",
                "organizations:*",
                "account:*"
            ],
            "Resource": "*"
        }
    ]
}
```

5. Click **Next**.
6. For Policy name, enter `DevOpsPermissionBoundary`.
7. For Description, enter `Permission boundary for DevOps roles limiting access to specific services`.
8. Click **Create policy**.

### 3.2 Apply the Permission Boundary to an IAM Role

1. In the IAM dashboard, select **Roles** from the left navigation pane.
2. Select the `DevOps-Role`.
3. In the **Permissions boundary** section, click **Set boundary**.
4. Search for and select the `DevOpsPermissionBoundary` policy you created earlier.
5. Click **Set boundary**.

### 3.3 Create a Service Control Policy (SCP)

**Note**: This step requires AWS Organizations. If you haven't set it up, you'll need to do so first.

1. Sign in to the AWS Management Console and navigate to the AWS Organizations dashboard.
2. In the left navigation pane, select **Policies**.
3. Click **Service control policies**.
4. Click **Create policy**.
5. For Policy name, enter `PreventIAMUserCreation`.
6. For Description, enter `Prevents the creation of IAM users`.
7. In the policy editor, enter the following:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "iam:CreateUser",
                "iam:CreateAccessKey"
            ],
            "Resource": "*"
        }
    ]
}
```

8. Click **Create policy**.

### 3.4 Attach the SCP to an Organizational Unit

1. In the AWS Organizations dashboard, select **AWS accounts** from the left navigation pane.
2. Navigate to the organizational unit where you want to apply the SCP.
3. Select the **Policies** tab.
4. Select the checkbox next to the `PreventIAMUserCreation` SCP.
5. Click **Attach**.

## Module 4: Identity Federation

### 4.1 Set Up IAM Identity Center (AWS SSO)

1. Sign in to the AWS Management Console and navigate to the IAM Identity Center dashboard.
2. If prompted, click **Enable IAM Identity Center**.
3. Choose your identity source:
   - **Option 1**: Use the default Identity Center directory
   - **Option 2**: Connect to an existing Active Directory
   - **Option 3**: Connect to an external identity provider

For this lab, we'll use the default Identity Center directory:

4. Under **Directory** in the left navigation pane, select **Users**.
5. Click **Add user**.
6. Enter the required details:
   - Username: `sso-admin`
   - Email address: your email
   - First name and Last name
   - Confirm email
7. Click **Next**.
8. Assign the user to a group (create one if needed).
9. Click **Add user**.

### 4.2 Configure AWS Access Portal

1. In the IAM Identity Center dashboard, select **AWS accounts** from the left navigation pane.
2. Select the checkboxes next to your AWS accounts in the organization.
3. Click **Assign users or groups**.
4. Select the **Groups** tab, then select your admin group.
5. Click **Next**.
6. Click **Create permission set**.
7. Select **Predefined permission set**.
8. Select **AdministratorAccess**.
9. Click **Next**.
10. Review the information and click **Create**.
11. Back on the permission sets screen, select the AdministratorAccess permission set.
12. Click **Finish**.

### 4.3 Set Up External Identity Provider (Optional)

This step is for organizations with an external identity provider. We'll outline the steps for setting up federation with Okta:

1. In the IAM Identity Center dashboard, select **Settings** from the left navigation pane.
2. Under Identity source, click **Change**.
3. Select **External identity provider**.
4. Download the IAM Identity Center SAML metadata file.
5. Log in to your Okta Admin dashboard.
6. Add a new application and search for "AWS IAM Identity Center".
7. Upload the SAML metadata file you downloaded from AWS.
8. Configure the appropriate user attributes and assignments.
9. Download the Okta SAML metadata file.
10. Return to the IAM Identity Center dashboard and upload the Okta metadata file.
11. Complete the configuration and test the connection.

## Module 5: Access Analysis and Monitoring

### 5.1 Enable IAM Access Analyzer

1. Sign in to the AWS Management Console and navigate to the IAM dashboard.
2. Select **Access analyzer** from the left navigation pane.
3. Click **Create analyzer**.
4. For Analyzer name, enter `AccountAccessAnalyzer`.
5. For Organization zone of trust, select **Current account**.
6. Click **Create analyzer**.

### 5.2 Review External Access Findings

1. In the IAM Access Analyzer dashboard, review any findings under the **Active findings** tab.
2. Select a finding to view details.
3. For each finding, decide whether to:
   - Archive the finding (if the access is intended)
   - Modify the resource to remove the external access (if unintended)

### 5.3 Set Up CloudTrail for IAM Activity Monitoring

1. Sign in to the AWS Management Console and navigate to the CloudTrail dashboard.
2. Click **Create trail**.
3. For Trail name, enter `IAMActivityTrail`.
4. For Storage location, choose **Create new S3 bucket**.
5. For S3 bucket, enter a globally unique name such as `iam-activity-trail-[your-account-id]`.
6. Under Trail log, select **Enable** for CloudWatch Logs.
7. For Log group, enter `IAMActivityLogGroup`.
8. For IAM role, select **New** to create a new role.
9. For Role name, enter `CloudTrailIAMActivityRole`.
10. Under Event types, ensure **Management events** is selected.
11. Ensure **Read** and **Write** are selected under Management events.
12. Click **Next**.
13. Under Data events, keep the default settings.
14. Click **Next**.
15. Review your selections and click **Create trail**.

### 5.4 Create IAM Activity Alerts

1. Sign in to the AWS Management Console and navigate to the CloudWatch dashboard.
2. Select **Rules** under **Events** from the left navigation pane.
3. Click **Create rule**.
4. Select **Event pattern**.
5. Select **Pre-defined pattern by service**.
6. For Service name, select **AWS IAM**.
7. For Event type, select **AWS API Call via CloudTrail**.
8. For Specific operations, enter `CreateUser`, `CreateAccessKey`, `AttachRolePolicy`, `AttachUserPolicy`.
9. Click **Add target**.
10. For Target type, select **SNS topic**.
11. For Topic, select **Create a new topic**.
12. Enter `IAMActivityAlerts` for the topic name.
13. Click **Create**.
14. Add your email address as a subscription to this topic.
15. Click **Configure details**.
16. For Name, enter `IAMHighRiskActivityRule`.
17. For Description, enter `Alerts for high-risk IAM activities`.
18. Click **Create rule**.

## Validation

Congratulations! You have successfully implemented a comprehensive identity and access management solution on AWS. To verify your implementation, proceed to the [Validation Checklist](validation-checklist.md).

## Troubleshooting

- **IAM Policy Simulator**: Use the IAM Policy Simulator to test the effects of IAM policies before applying them to users or resources.
- **CloudTrail**: Check CloudTrail logs for information about API calls if you encounter unexpected permission issues.
- **AWS Support**: AWS Support can provide guidance on best practices for identity and access management.

## Cleanup

To clean up resources created in this lab, you can:

1. Delete IAM users, roles, and policies created during the lab
2. Disable IAM Identity Center if you don't plan to use it
3. Delete the CloudTrail trail and associated S3 bucket if no longer needed

## Next Steps

For more advanced tasks and challenges, see [Challenges](challenges.md) and [Open Challenges](open-challenges.md). 