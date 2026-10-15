# PulseCheck

A serverless website uptime monitor built on AWS. PulseCheck checks a list of websites on a schedule, records availability and response times, and sends email alerts when a site goes down.

> 🚧 Work in progress — built as a hands-on cloud engineering learning project.

## Planned architecture
- **AWS Lambda** (Python 3.14) — runs the website checks and the API
- **Amazon EventBridge Scheduler** — triggers checks every 5 minutes
- **Amazon DynamoDB** — stores monitored sites and check results
- **Amazon API Gateway** — HTTP API for managing sites
- **Amazon S3 + CloudFront** — hosts the dashboard over HTTPS
- **Amazon CloudWatch + SNS** — metrics, alarms, and email alerts
- **Terraform** — all infrastructure defined as code
- **GitHub Actions** — automated tests and deployment