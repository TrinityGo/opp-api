# Deployment Pipeline
- **Title:** Deployment Pipeline
- **Date:** Nov 2, 2023
- **Author:** Xinyi Gao
- **Version:** 1.0

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 2, 2023|1.0|Initial release| Xinyi Gao|
-------------


## Deployment Pipeline:
1.	Frontend: On every push to GitHub, a GitHub Action builds the React app and syncs it to your S3 bucket.
2.	Backend: On push, a GitHub Action zips your Flask app and deploys to Elastic Beanstalk.
3.	Lambdas: On push, GitHub Actions zips the Lambda function codes and update them on AWS.

## Implementation of this pipeline:
1.	Set up Elastic Beanstalk, S3, and Lambda via the AWS Management Console.
2.	Use the AWS Management Console to perform manual deployments initially.
3.	Set up a basic GitHub Actions workflow for the frontend, backend, and Lambdas.
