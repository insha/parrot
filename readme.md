# Parrot

### An API Mocking Server

The server is geared towards mocking up APIs for general development, unit tests, UI testing and automation tests.

[![Build Status](https://travis-ci.org/insha/parrot.svg?branch=master)](https://travis-ci.org/insha/parrot) [![codecov](https://codecov.io/gh/insha/parrot/branch/master/graph/badge.svg)](https://codecov.io/gh/insha/parrot) [![codebeat badge](https://codebeat.co/badges/7e56faf8-fe3e-4471-8ead-56753fa59c57)](https://codebeat.co/projects/github-com-insha-parrot-master)

### Supported Features

- Easy configuration
- Dynamic responses - Responses can use request data (e.g. to simulate different login scenarios based on username): - Request path - GET/POST parameters - Respond with different status code for specific requests.
- HTTP Methods support includes GET, POST, PUT, DELETE, PATCH, TRACE, HEAD, and OPTIONS.
- Cross Origin Resource Sharing (CORS).
- Delayed responses at service and endpoint level.

### Wish List

- Random data generators.
- Required parameter validation.

## Development Environment

At the bare minimum you'll need the following for your development environment:

- [Python 3.6.x or later](http://www.python.org/)

It is strongly recommended to also install and use the following tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)
2. [virtualenvwrapper](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenvwrapper)

### Local Setup

The best way to setup the local environment for the development server is to use Python 3.6.x and the dynamic duo of virutalenv and virtualenvwrapper.

For macOS the best way to install Python 3.6.x (or later) is using [Homebrew](https://brew.sh); if you already have Homebrew, you can install it simply by:

    $ brew install python3

The dynamic duo of virtualenv and virtualenvwrapper can also be easily installed by using [Virtual Burrito](https://github.com/brainsik/virtualenv-burrito).

The following assumes you have all of the recommended tools listed above installed.

#### 1. Create and initialize virtualenv for the project

    $ mkvirtualenv parrot
    $ cd parrot
    $ pip install -r requirements/dev.txt

#### 2. Run the development server:

Running the server:

    $ export FLASK_APP=parrot._cli_app
    $ export FLASK_ENV=development
    $ export PARROT_CONFIG=/path/to/your/parrot.cfg
    $ export PARROT_LOGGING_CONFIG=/path/to/your/logging.yaml
    $ flask run

When using `virtualenvwrapper`, you can add the environment variables to the `postactivate` script
and then unset them in the `postdeactivate` script.

Add the following to the `postactivate` script in your virtual environment's `bin` folder (generally it is `~/.virtualenvs/parrot/bin/postactivate`):

    export FLASK_APP=parrot._cli_app
    export FLASK_ENV=development

Add the following to the `postdeactivate` script in your virtual environment's `bin` folder (generally it is `~/.virtualenvs/parrot/bin/postdeactivate`):

    unset FLASK_APP
    unset FLASK_ENV

Doing this will configure everything once the environment is activated and then you would only have to
do the following to run the server:

    $ flask run

#### 3. Open [http://localhost:5000](http://localhost:5000)

## Bundles

If you are the kind of person that like to have config files for your API endpoints, you can peek inside the `bundles` folder to see the conventions that are used for providing payloads for the mock server. There is a sample bundle there with some endpoints and responses define that can be loaded. The bundles have the following structure:

```
/bundles
    /bundle_name
        config.json
        /responses
            ...
```

In the `bundles` directory, there is a sub-directory called `movies`. The `movies` directory has a `config.json` and a directory called `responses`. Responses are in JSON format for all endpoints and they are stored in the `responses` directory. The `config.json` references files from this directory. Please take a look at the structure of the `config.json` as it is simple and should be easy to understand. In any case more detailed documentation for this topic will be added as time permits.

## Dynamic Responses

By default the server launches in dynamic mode. A default service is created and you can use the following endpoints to build out your API endpoints:

| Method | Endpoint                | Description                                                                              |
| ------ | ----------------------- | ---------------------------------------------------------------------------------------- |
| GET    | /1/manage               | This will return a response with a map of all currently configured API endpoints.        |
| POST   | /1/manage               | Add a new API endpoint with a response.                                                  |
| PUT    | /1/manage               | Update an existing endpoint/response.                                                    |
| DELETE | /1/manage               | This will reset the service and remove all endpoints and responses. No body is required. |
| PUT    | /1/manage/bundle/<name> | The service will load the bundle with the provided name, if it exists.                   |

The schema that is used for interacting with Parrot is:

```
{
	"endpoint": String,
	"method": String,
	"status_code": Integer,
	"parameters": Object (Used only with 'GET' method),
	"content": Object (can be null)
	"lag": Float (defaults to `0`),
	"fuzz": Boolean (defaults to `false`),
}
```

| Key           | Description                                                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `endpoint`    | This is the _relative_ URL without the domain name. The endpoint should not start with a `/`.                                    |
| `method`      | The HTTP method for the endpoint.                                                                                                |
| `status_code` | HTTP status code that will be returned for the response.                                                                         |
| `parameters`  | Query string that will be used for matching the endpoint. NOTE both keys and values must be strings.                             |
| `content`     | Content (dictionary, array, etc.) that will be in body of the response for the endpoint.                                         |
| `lag`         | The response will be delayed by the provided value, which is in seconds, defaults to 0 (no delay).                               |
| `fuzz`        | When set to `true`, the content of the response will be randomly generate gibberish. When `true` the `content` value is ignored. |

Outside of the managing endpoints, all endpoints that need to be mimicked are invoked with the `/api` prefix, followed by the endpoint, e.g given the endpoint `login`, it will be invoked like this using the `GET` method:

```
curl -X GET https://parrot.themacronaut.com/api/login
```

## Code of Conduct

Our contributor code of conduct can be found in the `code-of-conduct.md` file.

## License

The full license text can be found in the `LICENSE` file.
