# Finds rectangle intersections

## pip install intersectioncalc

### Tested against Windows 10 / Python 3.10 / Anaconda - should work on MacOS / Linux


```python
Finds rectangle intersections in a DataFrame and populates a new column with results.
The function utilizes NumExpr for calculations, which can significantly improve
performance when dealing with large datasets of rectangles

Args:
    df (pd.DataFrame): Input DataFrame containing rectangle coordinates.
    columns (tuple or list, optional): Names of columns containing rectangle coordinates
        (start_x, start_y, end_x, end_y). Defaults to ("start_x", "start_y", "end_x", "end_y").
    new_column (str, int, float, optional): Name of the new column to store intersection results.
        Defaults to "aa_intersecting".
    dtype (np.float32 | np.float64 | np.int32 | np.int64, optional): Data type for calculations. Defaults to np.int32.
    convert_to_tuples (bool, optional): If True, converts intersection results to tuples.
        Defaults to False.

Returns:
    pd.DataFrame: Input DataFrame with the new_column populated with intersection results.

from intersectioncalc import find_rectangle_intersections
import time
import pandas as pd
import numpy as np
min_x = 1
max_x = 100
min_y = 1
max_y = 100
size = 50000
min_width = 1
max_width = 1000
min_height = 1
max_height = 1000
df = pd.DataFrame(
    [
        (startx := np.random.randint(min_x, max_x, size=size)),
        (starty := np.random.randint(min_y, max_y, size=size)),
        startx + np.random.randint(min_width, max_width, size=size),
        starty + np.random.randint(min_height, max_height, size=size),
    ]
).T.rename(columns={0: "start_x", 1: "start_y", 2: "end_x", 3: "end_y"})
start = time.perf_counter()
df = find_rectangle_intersections(
    df,
    columns=("start_x", "start_y", "end_x", "end_y"),
    new_column="aa_intersecting",
    dtype=np.int32,
    convert_to_tuples=False,
)
print(time.perf_counter() - start) 
```
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                