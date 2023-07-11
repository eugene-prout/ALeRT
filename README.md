# ALeRT

The webapp version of ALeRT.

## Running the application

There are two ways to serve the application: using the Flask development server locally or use the container image.

Note: gunicorn is not compatible with Microsoft Windows, to test application on Windows either use the Flask dev server, or run the container.

### Flask Development Server

1. Create virtual environment, activate it and install dependencies from `requirements.txt`

2. Install the project with `pip install -e .`

3. From the root folder, run `flask --app alert.app run --debug`

4. Server is accessible at `http://127.0.0.1:5000/`

The `--debug` flag enables live reloading so if you modify then save a file the server will restart automatically.

### Container

1. Install Docker and ensure it is running

2. Create a copy of `.env.example` rename it `.env`. Remove Azure variables and Key Vault name if not needed.

3. To build and start the container, `docker-compose up --build`

4. Server is accessible at `http://127.0.0.1:8000/`

There is no live reloading so you must rebuild the image to see your changes.

## Testing

Pytest is used to run the tests. Run `pytest` at the root directory to execute the tests.

Test code coverage is available with `coverage run -m pytest` and then `coverage report` to view the report.

100% coverage in handlers is the goal.

## Contributing

There are pipelines set up for CI. All changes must be brought in `main` through a pull request. When a PR is created, a code quality check pipeline is executed. This will check that `black` would not change the format, and that `pytest` reports no errors. Then the code can be merged into `main`. On a merge, a release pipeline is executed, this will build and push a Docker image to a container registry for deployment.

In short, before committing make sure `black` and `pytest` report no errors.

## Configuration

### Loading from Azure Key Vault

To load from an Azure Key Vault (AKV) set `$KEY_VAULT_NAME` to the name of the vault and it will be automatically loaded. 