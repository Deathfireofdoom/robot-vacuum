# Overview
The robot-vacuum-slim is a rest-api written in python 3.11 with the framework Flask. Since the "api" part is minimal, one main endpoint with one method, I did not put that much thought into choosing flask over other frameworks. 

I provided a post-man collection to easily send job to the robot.

# How to get started
This project is deployed with docker-compose, so need docker-compose and docker.

Get into project root, so `/tibber-robot-vacuum-slim`
```
cd <project-root>
```

Run docker compose
```
docker compose up
```
Check that everything started as it should 
```
curl http://localhost:5000/health 
```
_or open that url in your browser_

Migrate the database - creating the table for job-results
```
curl http://localhost:5000/migrate/1/up
```
_to migrate up just change to down_ 

Everything should not be up and running, ready to accept jobs.


# Design and thought process
### Repository and service pattern
Even though Python is a OOP language I decided to not go with inherientance/mixins, instead I went for the repository and service pattern. I personally find this pattern more enjoyable, and easier to understand.

A shortcut I made is to initialise the repository in the service, and the service in the user. Like this
```
class Service:
    def __init__(self):
        self.repo = Repo()
```
Non of the services or repos had any complex initialising logic, so I thought it was an ok shortcut. But more often than not I would gone for depency injection.
```
class Service:
    def __init__(self, repo: Repo):
        self.repo = repo
```

### Database interaction with context-manager
I went for a context-manager approach for the postgres interaction, this is driven by:
* Only need to handle the connection in one place, not accidently not closing the connection, or forgetting to handle OperationalError.
* Very smooth to use once it's been implemented 
```
from src.db.db import transaction_scope
with transaction_scope() as cursor:
    cursor.execute(sql, params)
```
* Easily handling transaction without thinking about commiting

Could argue it is a bit overkill since the only interaction with postgres is a insert statement and migration, but could be good for the future.

### Data-validation and models
Implemented a model system for the different objects `ex. Job, Command, Direction`. This allows for factory methods on each model, making the code DRY. Another upside with models instead of just raw dictionaries is the auto-completion you get if you type-hint and documentation inside the code.

In this project I went with the standard module `dataclasses`, but in bigger project I would consider using something like `pydantic` to get free data-validation etc. As you can see I needed to implement my own data-validation for the dataclasses, which get tedious.

### Robots Memory
To remember which coordinates that has been visited I decided to implement a `Memory` class. In hindsight, it may not be needed to have it in it's own class, since the logic became very simple, but could be good if we need to implement a more probalistic approach in the future.

The memory is storing each coordinate in form as a `Location` object in a set, making sure each coordinate is unique. To make this work we need to make `Location` unmutable, which can be done to set `Frozen=True` in the dataclass decorator.

This implementation has a space-complexity of O(n) and speed-complexity of O(n), did not manange to think of any better solution. In a rabot vacuum I dont think this would be this biggest bottleneck anyway.

### Testing
Unit testing is hard, what to test and what to mock. I believe, and try, to only test behaviour and not implementation, with some exceptions of complex business logic.

Did I pull it off 100%? Probably not, but I am overall happy with the outcome of my tests, with a little note that I may have tested some functionallity several times. e.x. in `test_handlers.py` and `test_robot.py` I test how the flow from getting a job to returning result.

A different approach to the above problem could be to more extensive mocking, so in `test_handlers.py` I could have mocked `Robot`, making the test only test if the endpoint calls the correct functions and returns what I expected it to return. I was torned if I should done that or not, in the end I decided not to do it since I dont think it aligns with "test behaviours not implementation". One downside of extensive mocking is that we need to updates all mocks in case the underlying class is changed making it more of a tech-debt thing, a upside is that it could be easier to identify what broke and did not broke.

Things like interaction with databases, or other external systems, should of course be mocked. Therefore I implemented the `mock_transaction_scope`. 

I am running the test in a dockerfile so you dont have too, but if you want to run them yourself make sure to install the `test-requirements.txt` since I do pytest.