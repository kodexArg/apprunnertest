# AWS App Runner Test Project

This Django web application serves as a testing ground for exploring AWS App Runner's capabilities and its integration with various AWS services. It provides a platform for experimenting with different deployment scenarios, particularly focusing on automated deployments and service integrations. **Note:** This is a testing project and is not intended for production use without significant modifications.


## AWS App Runner Deployment

This project is automatically deployed to AWS App Runner (us-east-1) with each push to the `main` branch of the GitHub repository: [github.com/kodexArg/apprunnertest](github.com/kodexArg/apprunnertest).

**Key Features:**

*   **Automatic Deployment:** Commits to the `main` branch trigger automatic deployments via AWS App Runner.
*   **RDS PostgreSQL Integration:** The application is configured to use an RDS PostgreSQL database.
*   **Environment Variables:** App Runner environment variables are defined in `apprunner.yaml` to manage the application's settings and secrets.
*   **Secrets management:** Secrets are managed in AWS Secrets Manager, and are retrieved through environment variables.
*   **Health Check:** The `/healthz/` endpoint provides a simple health check, returning HTTP 200.
*   **Database Check:** The `/db/` endpoint tests the database connection and reports its status.
*   **Database Info:** The `/db-info/` endpoint provides information about the current database, including its version.

## To-Do List

*   **S3 Bucket Integration:** Complete the setup for using an S3 bucket for storing static and media files. The settings are in place, but further testing is necessary.
*   **django-vite:** Implement `django-vite` to handle frontend asset bundling. This will involve testing `npm run build` within the App Runner environment.
*   **django-signals:** Add tests for `django-signals` to handle asynchronous events within the application.
*   **Async Operations:** Explore non-blocking I/O practices in Django. (Note: "Async" is not the conventional term in Django; it refers to asynchronous tasks, potentially managed by Celery or similar).


## AI Guidance

This README.md serves as the primary context for AI interactions with this project. When modifying or adding code, please adhere to the following:

*   **Purpose:** This project's purpose is to test AWS App Runner.
*   **Conventions:** Follow modern Django 5.2 and Python conventions (PEP 8).
*   **Comments:** Avoid overly verbose code and inline comments.
*   **Selected Content:** When using `selected_content`, add any necessary imports at the beginning of the file, following PEP 8. Extending the selection is allowed if needed.
*   **Keep it simple:** Keep the code as simple as possible.
*   **Secure:** Do not write any key nor secret, never. Ask for environment variables creation instead.

## Environment Variables

*   `PORT`: The port on which the application will listen for requests.
*   `DJANGO_SETTINGS_MODULE`: Specifies the Django settings module (e.g., `project.settings`).
*   `APP_RUNNER_SUBDOMAIN`: Subdomain assigned by App Runner.
*   `APP_RUNNER_REGION`: Region of App Runner.
*   `APP_RUNNER_DOMAIN`: Base domain of App Runner.
*   `S3_BUCKET_NAME`: The name of the S3 bucket used for static file storage (e.g., `alvs-virginia-s3`).
*   `S3_REGION`: The AWS region where the S3 bucket is located (e.g., `us-east-1`).

## Secrets
*   `DJANGO_SECRET_KEY`: The Django secret key for cryptographic signing. Stored in AWS Secrets Manager.
*   `PING`: Secret used for healtchecks. Stored in AWS Secrets Manager.
*   `MS_GRAPH_CLIENT_SECRET`: Secret used to connect to Microsoft Graph. Stored in AWS Secrets Manager.
*   `WELPDESK_DB_CONNECTOR`: Secret used to connect to the database. Stored in AWS Secrets Manager.

This project uses an App Runner instance role for S3 access and therefore does not require explicit S3 credentials.