import base64
import io
import matplotlib.pyplot as plt
from typing import TypedDict, List
import pandas as pd


class HeaderDictType(TypedDict):
    date: str
    min: int
    sec: int
    versions: List[str]
    types: List[str]
    filter: dict[str, int]


def process_img_string(img) -> str:
    buffer = io.BytesIO()
    plt.imsave(buffer, img, cmap="gray", format="png")
    base64_string = base64.b64encode(buffer.getvalue()).decode()
    mime_type = "image/png"
    return f"data:{mime_type};base64,{base64_string}"


def process_tracks(tracks: pd.DataFrame):
    grouped = None
    if "Id" in tracks.columns:
        grouped = tracks.groupby("Id")
    elif "ID" in tracks.columns:
        grouped = tracks.groupby("ID")
    else:
        raise ValueError("No ID column in datafram")

    result_tuples = []

    for group_id, group_data in grouped:
        timestamps = group_data.index.strftime("%Y-%m-%dT%H:%M:%S.%f").tolist()
        x_list = group_data["X"].tolist()
        y_list = group_data["Y"].tolist()
        speed_key = None
        for column in group_data.columns:
            if column.startswith("Speed"):
                speed_key = column
                break
        speed = group_data[speed_key].tolist()
        estimated_list = group_data["Estimated"].tolist()
        type_key = None
        if "Type" in group_data.columns:
            type_key = "Type"
        elif "Class_id" in group_data.columns:
            type_key = "Class_id"
        else:
            raise ValueError("No typekey recognized")
        track_type = group_data[type_key].tolist()

        result_tuple = (
            group_id,
            timestamps,
            [x_list, y_list],
            speed,
            estimated_list,
            track_type,
        )
        result_tuples.append(result_tuple)
    return result_tuples
