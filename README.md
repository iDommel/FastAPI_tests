# FastAPI_tests
## Installing dependecies
To install dependencies for this project, run:

`pip install -r ./requirements.txt`

Then run the project with:

`python3 ./main.py`
## Environment
You can provide the following environment variables inside a .env file:

```
SERVICE_HOST=           # The url where the server should run. 127.0.0.1 by default

SERVICE_PORT=           # The Port where the server should listen. 8000 by default
```

## Testing

Test using

`coverage run -m pytest`

and get coverage with:

`coverage report`
