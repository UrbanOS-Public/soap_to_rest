# SOAP To Rest
This is a project to abstract SOAP calls as REST calls.

- Environment: Python 3.8

## Limitations
If one of the parameters sent is meant to be an instance of a subclassed object, the underlying SUDS library won't be able to form a valid SOAP request. This can be addressed when time permits.

## Local development
### Environment Setup
#### Install Python dependencies
```bash
pip3 install poetry
poetry install
```

### Running the application locally
```bash
poetry run uvicorn soap_to_rest:app --host 127.0.0.1 --port 5000
```

### Calling the application
The app takes a json body as a POST request. In addition to this example, the app provides Swagger documentation if you navigate to `localhost:5000/docs` in your browser.

```bash
curl --location --request POST 'localhost:5000/api/v1/wsdl' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://www.dneonline.com/calculator.asmx?WSDL",
    "action": "Add",
    "params": {
        "intA": 5,
        "intB": 6
    }
}'
```

#### Required params

+ `url`
    + The url to a wsdl file. This is used to dynamically build the client.
+ `action`
    + The action (or "operation") that should be called on the service.

#### Optional params

+ `params`
    + Params that should be passed to the service. If no params are required for the action, an empty map is used as the default.
+ `auth`
    + A map with two keys, `username` and `password`. Both keys are required if auth is passed.
    + The credentials provided here will be sent as a wsse header to the service. This is the only type of auth explicitly supported at the moment. If credentials are sent as part of the request body, they should be sent as part of `params`.

### Running tests
```bash
poetry run pytest
```

## Contributing

### Formatting and Linting
Please lint the code before submitting pull requests, fixing errors as appropriate. Pylint may complain about things that are not worth fixing. Use your best judgement.

#### Linting
```pylint soap_to_rest```

Most pylint problems can be solved by running the formatter and input sorter.

#### Formatting
```black --config ./pyproject.toml soap_to_rest tests```

#### Sorting Imports
```isort --settings-path ./pyproject.toml --recursive .```
