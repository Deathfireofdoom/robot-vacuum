# Overview
The robot-vacuum-slim is a rest-api written in python 3.11 with the framework Flask. Since the "api" part is minimal, one main endpoint with one method, I did not put that much thought into choosing flask over other frameworks. 

I provided a post-man collection to easily send job to the robot.

# How to get started
This project is deployed with docker-compose, so need docker-compose and docker.

Get into project root
```
cd <project-root>
```

Run docker compose
```
docker compose up
```
Check that everything started as it should, if you have trouble pulling from GHCR I may need to ask you uncomment the block in compose.yml and build it locally. 
```
curl http://localhost:5000/health 
```
_or open that url in your browser_

Migrate the database - creating the table for job-results
```
curl http://localhost:5000/migrate/1/up
```
_to migrate up just change to down_ 

Everything should now be up and running, ready to accept jobs.

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


# GitHub workflow
Added a simple ci/cd pipeline to test, build and push the image to a ghcr.io. 

A new "deployment" is done by making a new tag.



# EDIT: Performance optimization
The original code has to little focus on performance. In hindsight this does not really make sense since the requirements of the code was specified clearly in the instructions, so that one is on me. But luckily I got a second chance. 


The requirements we need to follow:
* 200 001 x 200 001 grid
* 10 000 commands
* 100 000 steps per command 
* up 10 000 000 000 unique locations will be visited per run


The current approach, using a set that stores locations as a tuple of two INTs are not feasible. Potentially storing 10 000 000 000 locations in a set we would not only have memory issues, but also most likely speed issues on inserting etc. 


So we need are a more memory optimized approach, since we have a fixed grid a bitarray could potentially solve our issues. Other solutions I looked at was QuadTree and SparseMatrix, but both of them seemed to use a lot of memory when we started visiting many unique locations, never got it to finish the full job.


We can use a bitarray because the grid is fixed, making it possible to initialize the underlying bitarray. We only care about if a coordinate has been visited or not, making it a boolean operation. 


Implementing a performant bitarray could be challenging, even more challenging if it need to be able to handle a grid-size of 200 001 x 200 001, especially in python.


Since I cant get it to work with sets or come up with any other method that work, I do need to go with the bitarray method. However, I need to take some shortcuts. As mentioned, to do this correctly in a performant fashion, we would most likely need to use cython or something. Since I am not that comfortable with c or super comfortable with bitarrays, this would be very time consuming, would love to do it some day, but you probably dont want to wait to long on this.


So I thought I would do following:
* Implement a bitarray memory for the robot with the python package bitarray, a performant bitarray written in c by some smart people with more time on their hands than me right now.
* To show that I dont just randomly use a package without understanding the underlying concepts I will implement a not so performant "bitarray" in python, that can handle small grids. 


The downside of using a bit array is that we will occupy memory even though we dont visit the location, making it use same memory for small and large jobs. Its around 4GB, so not optimal probably.



### Other performance optimizations
Since I went heavy on code design, and not optimization in the initial code I thought I would do some changes to make it more performant, here I will document the changes and benchmarks. Normally the benchmark tests would be saved somewhere, but for now I will just paste them here using pytest-benchmark.


I will limit commands to 300, dont want to wait all day, and since I am running on my local machine there may be some fluctuations.

##### New memory
This will be the start point since the set-memory approach does not really finish with 300 commands. So the new bit-array-memory is implemented, the rest is as before.
|min    | avg    | max    | std   |
|-------|--------|--------|-------|
|43.7460|47.2832 |45.6277 |1.4347 |

time in seconds


##### Changing logic of handling command
Looking at `_act_on_command` there is a bit of a flaw in the logic. It considers each step as a separate command, so for each step, we check at what direction we are going. A more efficient way would be to handle each step as a repetition of a command. 

```
def _act_on_command(self, command: Command):
    action = self._get_action(command.direction)
    for _ in range(command.steps):
        new_location = action()
        self._update_location(new_location)

def _move_north(self) -> Location:
    return Location(self.location.x + 1, self.location.y)

def _move_east(self) -> Location:
    return Location(self.location.x, self.location.y + 1)

def _move_south(self) -> Location:
    return Location(self.location.x - 1, self.location.y)

def _move_west(self) -> Location:
    return Location(self.location.x, self.location.y - 1)

def _get_action(
    self, direction: Direction
):
    match Direction(direction):
        case Direction.NORTH:
            return self._move_north
        case Direction.EAST:
            return self._move_east
        case Direction.SOUTH:
            return self._move_south
        case Direction.WEST:
            return self._move_west
        case _:
            log.warning(f"{direction} is not a real direction, ignoring...")

```

This was kind of successful

|min   | avg    | max    | std   |
|------|--------|--------|-------|
|23.6331|24.1466|23.8824|0.2012|



##### Making location mutable
To get performance increases we need to focus on parts that either is slow or parts that are repeated many times. One of these is updating the location, it is done every step, so potentially 10 000 000 000 times in a run.


In the inital code I put location as a immuatable object, two reasons, a location is normally static and it needed to be static for the set approach to work. Since we no longer uses that approach I think I will unfreeze the location, and start updating the location instead of making a new one.

```
def _act_on_command(self, command: Command):
    action = self._get_action(command.direction)
    for _ in range(command.steps):
        action()
        self._update_location(self.location)

def _update_location(self, location: Location):
    self.location = location
    self.memory.add_location(self.location)

def _move_north(self):
    self.location.x += 1

def _move_east(self):
    self.location.y += 1

def _move_south(self):
    self.location.x -= 1

def _move_west(self):
    self.location.y -= 1
```

This was ok successful
|min    | avg    | max    | std   |
|-------|--------|--------|-------|
|14.0960|14.5114 |14.2348 |0.1614 |



##### Removing the use of the location object
This is a gamble, could work and could not, but for my own curiosity I decide that we try. So remove the overhead of the location object, and add x, y directly on the robot.

```
def _move_north(self):
    self.x += 1

def _move_east(self):
    self.y += 1

def _move_south(self):
    self.x -= 1

def _move_west(self):
    self.y -= 1
```
It seems like we got a small improvement, I have not done the math but I dont think it would be statistical different. 

|min    | avg    | max    | std   |
|-------|--------|--------|-------|
|12.8782|13.5043 |13.1699 |0.3071 |


#### Final version
With the bitarray-memory in place and the above performance optimizations, it is finally time to run the whole job. I know for a fact it wont be any speed-demon, but better than crashing from memory-issues.


| Time    |
|---------|
| 314.8761 |



The code has been improved a lot from the start, from dnf til 5 min, memory footprint (fetch via top) seems to be around 4000M, which is not bad for this job. But keep in mind it is the same memory print regardless of the size of the job. 


Since majority of the time is spent in the memory part(checked this by disabling memory) I believe there is little to gain from making other improvements outside the memory class. Solving(trying to solve) the memory part has been a fun and educating challenge for me, but I have this feeling I am missing something, either that SparseMatrix or QuadTree was the way to go, but it was my implementation that failed it, or that there is a better method. I dont see how we could store 10 000 000 000 locations in a dynamic way without getting memory issues.


### Performance improvements round two
After submitting the above version yesterday, I had a hard time letting go the fact that we were using 4GB of memory, even if we just wanted to traverse 2 points. This was a side effect of the bitmap-memory, where I rendered the whole 200 001 by 200 001 grid as the first step. Ealier in my performance optimization journey, when I tried to implement a similar idea but with list and bools in pure python, I had the idea of subgridding. 


Instead of rendering everything from the start my plan was to render a chunk in the proximity of the robot, and if it stepped out of the chunk, a new one would be rendered. This did not work with list + bools, due to the reasons stated above, but this should work with my new bitmap array memory.


The concept is that I will take the 200 001 x 200 001 grid, divide it into smaller grids (I started with 10 000 x 10 000, just a random number), and only render the bitarray for each subgrid if we ever stepped into it. The first version looked liked:

```
class DynamicGridBitMapMemory:
    total_grid_height = 200_001
    total_grid_width = 200_001
    sub_grid_size = 10_000  # each subgrid is sub_grid_size x sub_grid_size

    def __init__(self):
        self.unique_visited = 0
        self.grids = {}

    def add_location(self, x: int, y: int):
        # Adjust coordinates
        x_adjusted = x + self.total_grid_width // 2
        y_adjusted = y + self.total_grid_height // 2

        # Get the grid-index of the sub-grid
        grid_pos = self._get_grid_index(x_adjusted, y_adjusted)

        # Check if grid exists
        if grid_pos not in self.grids:
            self.grids[grid_pos] = bitarray(self.sub_grid_size * self.sub_grid_size)
            self.grids[grid_pos].setall(0)

        # Get location index in the sub-grid
        location_index = self._get_location_index_in_grid(x_adjusted, y_adjusted)

        # Check if we already visited it
        if not self.grids[grid_pos][location_index]:
            self.grids[grid_pos][location_index] = 1
            self.unique_visited += 1

    def get_unique_n_visited(self):
        return self.unique_visited

    def _get_grid_index(self, x: int, y: int):
        grid_x = x // self.sub_grid_size
        grid_y = y // self.sub_grid_size
        return (grid_x, grid_y)

    def _get_location_index_in_grid(self, x: int, y: int):
        local_x = x % self.sub_grid_size
        local_y = y % self.sub_grid_size
        return local_x * self.sub_grid_size + local_y
```

Run time for the big job got slightly worse, but according to top, it was now using 700MB, compared to 4000MB. This was great, since this was the job I expected to use the most memory. Runtime wise, it took 8min instead of 5min, which was expected since we added more checks. I think this is a good tradeoff, since small jobs runs much faster + uses a lot less memory.

|min    | avg    | max    | std   |
|-------|--------|--------|-------|
|498.2151 | 498.2151 | 498.2151 | 0.0000


#### Further improvements - attempt 1

One thing with this implementation that I did not like, was that I re-calcuated which subgrid the robot was in at every step. This is not super efficient since the chance of the robot being the same sub-grid as before is high, since the movement is continous. To address this problem I decided to "cache" the bounds of the subgrid, and the subgrind index, and instead of checking which grid the robot was in, I checked if the robot has stepped out of the bounderies and only then checked which subgrid I should use. I did not really get any great speed performance here, and the code became more complex, not a good tradeoff.


```
if self._is_within_current_grid(x_adjusted, y_adjusted):
    grid_pos = self._current_grid
else:
    grid_pos = self._get_grid_index(x_adjusted, y_adjusted)
    self._update_current_grid(grid_pos)
```

|min    | avg    | max    | std   |
|-------|--------|--------|-------|
| 488.1164 | 488.1164 | 488.1164 | 0.0000

#### Further improvements - attempt 2

Then I decided to check which size of the subgrid that made most sense, I tested `100`, `500`, `1 000`, `2 000`, `10 000`. As you can see in the table `500` had the best run time. This is not a super scientific test, in the real world we would most likely do more iterations and control for other factors, like not running on my localmachine.  


| SUB_GRID_SIZE | Time (ms) |
|---------------|-----------|
| 500           | 399.5204  |
| 1000          | 401.6915  |
| 2000          | 411.0268  |
| 100           | 428.1878  |
| 10000         | 465.0370  |


#### Further improvements - attempt 3 - Most successful

As a last improvement I came up with a new concept of checking if the robot was within a new subgrid or not. The new method is using `_steps_from_potential_edge`, which is a numbrt that keeps tracks of how many steps the robot are from a potential edge.


It works like this:
* Robot enters a new subgrid, `_steps_from_potential_edge` is now `1`. 
* Next movement we will decrease `_steps_from_potential_edge` by `1`, when it hits zero it will re-trigger a calucation, we first checks if the robot has leaved the subgrid, if not we re-calculate `_steps_from_potential_edge`. E.x. If the robot went towards the middle of the subgrid then the `_steps_from_potential_edge` will be 2. This time we take 2 steps without checking. 

This way, we will peform less checks if the robot are operating in the middle of a subgrid. Comparing if a int is bigger than zero should be faster than comparing if the current location are within the boundaries.

With this new improvement I got a significant performance boost in the heavy job.

| Time |
|------|
| 355.70 |

 
Since we managed to decrease the memory foot print of the robot, without loosing that much of runtime I would say my performance improvements are successful. 