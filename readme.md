# Wallet API

Submission for the Wallet API take-home assignment -
Below you'll find information for running the project on
your machine, API routes, code structure, and tests.

## Running the API locally

There's a `docker-compose.yml` file that defines the
container stack needed to run the project locally.

You can `cd` into the project directory and from there
spin up all the services:

````commandline
cd /Users/phil/PycharmProjects/pjauvincamlin
docker compose up
````

This will create two containers, one with the Python app
and another that runs DynamoDB locally.

Once the containers are created and running, you'll
be able to access the API at `localhost:5500` (you can use
the `/docs` endpoint to get a Swagger UI like in other FastAPI apps).

Please note that the intent behind using `docker-compose`
in this project is to ease the process of running
the API locally rather than as a deployment mechanism.
The `Dockerfile` in the repository is written in
a way to be deployed to a cloud service, with some elements 
overriden in the `docker-compose` configuration.


## API Operations

You can authenticate into the API using the following
credentials:
- username: `pjauvin`
- password: `supermariobros`

Please note that the API expects to receive the username
and password as multipart form data.

Our API offers 4 different routes that can be used:

- `GET /wallet/original` retrieves the original wallet without conversions
- `GET /wallet` retrieves the wallet converted to PLN as well as the PLN total
- `POST /wallet/add/{currency}/{amount}` adds a given quantity of a currency to the user's wallet
- `POST /wallet/subtract/{currency}/{amount}` removes a given quantity of a currency from the user's wallet

## Project structure

The API endpoints are defined in the `main.py` file, from
there we import elements from `services` that are used
to perform wallet-related operations (`WalletService`)
as well as user authentication (`AuthService`).

In the `clients` directory you'll find clients that are used
to interact with AWS services as well as the client
used to fetch data from the NBP API.

Lastly, Pydantic models are defined in the `models` directory
and used throughout the application.

There are some other miscellaneous items such as environment configs
in the `env` directory as well as the `requirements` files used
to install the dependencies.

Perhaps the following items could be of most interest when first looking
at the code:

- API call to NBP API can be found in `clients/exchange_rates/nbp_client.py`
- Wallet retrieval and updates can be found in `services/wallet_service.py`

## Tests

In the `test` directory you'll find all test-related functionality.
The `test_api.py` file contains some basic test cases
which make use of the `pytest` framework.

The dependencies needed to run these tests are mocked (where reasonable),
the fixtures and configurations can be found in the
same directory.

We use the same fixtures to create default data
for the API when we run it locally.

If you wish to run the tests you can do so by
starting the docker services as explained previously
and then run the following command:

````commandline
 docker compose exec -it fastapi python -m pytest test/
````

Here `fastapi` refers to the name of the service defined
in the `docker-compose.yml` configuration.
