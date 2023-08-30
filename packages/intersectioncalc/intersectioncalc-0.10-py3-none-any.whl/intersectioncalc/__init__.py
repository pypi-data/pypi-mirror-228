import pandas as pd
import numpy as np
import numexpr


def find_rectangle_intersections(
    df: pd.DataFrame,
    columns: tuple | list = ("start_x", "start_y", "end_x", "end_y"),
    new_column: str | int | float = "aa_intersecting",
    dtype: np.float32 | np.float64 | np.int32 | np.int64 = np.int32,
    convert_to_tuples: bool = False,
) -> pd.DataFrame:
    """
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

    Example:
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


    """

    def find_overlaps(rect):
        numexpr.evaluate(
            "y1 | y2 | y3 | y4",
            global_dict={},
            local_dict={
                "y1": data2smaller[rect[0]],
                "y2": data0bigger[rect[2]],
                "y3": data1bigger[rect[3]],
                "y4": data3smaller[rect[1]],
            },
            out=tmparray,
            casting="no",
        )
        subresult = datatuples[np.where(tmparray)]
        if convert_to_tuples:
            return tuple(subresult)
        else:
            return subresult

    datadf = df[[*columns]].astype(dtype)
    data = datadf.__array__()
    if convert_to_tuples:
        datatuples = np.fromiter(map(tuple, data), dtype="object")
    else:
        datatuples = data

    box2_0 = datadf[columns[0]].unique().__array__()
    box2_1 = datadf[columns[1]].unique().__array__()
    box2_2 = datadf[columns[2]].unique().__array__()
    box2_3 = datadf[columns[3]].unique().__array__()

    box1_0 = datadf[columns[0]].__array__()
    box1_1 = datadf[columns[1]].__array__()
    box1_2 = datadf[columns[2]].__array__()
    box1_3 = datadf[columns[3]].__array__()
    tmparray = np.zeros_like(box1_0).astype(bool)

    data2smaller = {
        k: numexpr.evaluate(
            f"(box1_2 < {k})",
            global_dict={},
            local_dict={"box1_2": box1_2},
        )
        for k in box2_0
    }
    data0bigger = {
        k: numexpr.evaluate(
            f"(box1_0 > {k})",
            global_dict={},
            local_dict={"box1_0": box1_0},
        )
        for k in box2_2
    }
    data1bigger = {
        k: numexpr.evaluate(
            f"(box1_1 > {k})",
            global_dict={},
            local_dict={"box1_1": box1_1},
        )
        for k in box2_3
    }
    data3smaller = {
        k: numexpr.evaluate(
            f"(box1_3 < {k})",
            global_dict={},
            local_dict={"box1_3": box1_3},
        )
        for k in box2_1
    }
    df.loc[:, new_column] = df.apply(
        lambda x: find_overlaps(
            (x[columns[0]], x[columns[1]], x[columns[2]], x[columns[3]]),
        ),
        axis=1,
    )
    return df
