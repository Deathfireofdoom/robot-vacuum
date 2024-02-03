use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::HashMap;
use std::cmp::{min, max};
use pyo3::conversion::FromPyObject;

#[pyfunction]
fn handle_job(commands: Vec<Command>, start_location: Location) -> PyResult<i32> {
    let mut memory = Memory {
        rows: HashMap::new(),
        columns: HashMap::new(),
    };

    memory.handle_commands(commands, &start_location);
    return Ok(memory.get_unique_visited()); 
}

#[pymodule]
fn rust_memory(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(handle_job, m)?)?;
    return Ok(());
}

struct Memory {
    rows: HashMap<i32, Vec<Interval>>,
    columns: HashMap<i32, Vec<Interval>>,
}

#[pyclass]
struct Command {
    direction: String,
    steps: i32,
}

#[pymethods]
impl Command {
    #[new]
    fn new(direction: String, steps: i32) -> Self {
        Command { direction, steps }
    }
}

impl<'source> FromPyObject<'source> for Command {
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let direction: String = obj.getattr("direction")?.extract()?;
        let steps: i32 = obj.getattr("steps")?.extract()?;

        Ok(Command {
            direction,
            steps,
        })
    }
}


#[pyclass]
struct Location {
    x: i32,
    y: i32,
}

#[pymethods]
impl Location {
    #[new]
    fn new(x: i32, y: i32) -> Self {
        Location { x, y }
    }
}

impl<'source> FromPyObject<'source> for Location {
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let x: i32 = obj.getattr("x")?.extract()?;
        let y: i32 = obj.getattr("y")?.extract()?;

        Ok(Location {
            x,
            y,
        })
    }
}

struct Interval {
    start: i32,
    end: i32,
}

impl Memory {
    fn get_unique_visited(&self) -> i32 {
        let unique_visited = self._calculate_unique_visited();
        unique_visited
    }

    fn handle_commands(&mut self, commands: Vec<Command>, start_location: &Location) {
        let mut current_location = Location {x: start_location.x, y: start_location.y};
        for command in commands {
            current_location = self.handle_command(command, &current_location);
        }
    }

    fn handle_command(&mut self, command: Command, current_location: &Location) -> Location {
        let end_location = self._calculate_end_location(command, current_location);
        self.add_interval(&current_location, &end_location);
        end_location
    }

    fn _calculate_end_location(&self, command: Command, current_location: &Location) -> Location {
        match command.direction.as_str() {
            "north" => return Location {x: current_location.x, y: current_location.y + command.steps},
            "east" => return Location {x: current_location.x + command.steps, y: current_location.y},
            "south" => return Location {x: current_location.x, y: current_location.y - command.steps},
            "west" => return Location {x: current_location.x - command.steps, y: current_location.y},
            _ => return Location {x: current_location.x, y: current_location.y},
        }
    }

    fn add_interval(&mut self, start_location: &Location, end_location: &Location) {
        let mut start = start_location;
        let mut end = end_location;

        if start.x == end.x {
            // Vertical movement
            // swap if we do downwards movement
            if start.y > end.y {
                std::mem::swap(&mut start, &mut end);
            }
            self._insert_and_merge_interval(start.x, start.y, end.y, true);

        } else {
            // Horizontal movement
            // swap if we do left movement
            if start.x > end.x {
                std::mem::swap(&mut start, &mut end);
            }
            self._insert_and_merge_interval(start.y, start.x, end.x, false);
        }
    }

    fn _insert_and_merge_interval(&mut self, index: i32, start: i32, end: i32, is_vertical: bool) {
        let intervals = if is_vertical {
            self.columns.entry(index).or_insert_with(Vec::new)
        } else {
            self.rows.entry(index).or_insert_with(Vec::new)
        };

        let mut new_interval = Interval {
            start: start,
            end: end,
        };
        let mut n = intervals.len();
        let mut i = 0;
        while i < n {
            if new_interval.start <= intervals[i].end {
                
                // new non overlapping interval
                if new_interval.end < intervals[i].start - 1 {
                    intervals.insert(i, new_interval);
                    return;
                }
                
                new_interval.start = min(intervals[i].start, new_interval.start);
                new_interval.end = max(intervals[i].end, new_interval.end);
                intervals.remove(i);
                n -= 1;
            } else {
               i += 1;
            }
        }

        // the interval was in the end
        intervals.push(new_interval);
    }

    fn _calculate_unique_visited(&self) -> i32 {
        let row_count = self.rows.values()
            .flat_map(|intervals| intervals.iter())
            .map(|interval| interval.end - interval.start + 1)
            .sum::<i32>();

        let col_count = self.columns.values()
            .flat_map(|intervals| intervals.iter())
            .map(|interval| interval.end - interval.start + 1)
            .sum::<i32>();

        row_count + col_count - self._calculate_overlaps()
    }

    fn _calculate_overlaps(&self) -> i32 {
        let mut overlap_count = 0;

        for (&col_index, col_intervals) in &self.columns {
            for col_interval in col_intervals {
                for row_index in col_interval.start..=col_interval.end {
                    if let Some(row_intervals) = self.rows.get(&row_index) {
                        for row_interval in row_intervals {
                            if row_interval.start <= col_index && row_interval.end >= col_index {
                                overlap_count += 1;
                            }
                        }
                    }
                }
            }
        }

        overlap_count
    }
}