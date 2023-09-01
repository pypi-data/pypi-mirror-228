import os
import importlib.util
from typing import Tuple, List


def extract_points(
    base_folder_path: str,
) -> Tuple[List[List[Tuple[int, int]]], List[List[Tuple[int, int]]]]:
    version_path = (
        base_folder_path
        + "/"
        + next(
            filter(
                lambda folder: folder.startswith("version"),
                os.listdir(base_folder_path),
            )
        )
    )
    folders = list(
        filter(lambda folder: folder.startswith("A"), os.listdir(version_path))
    )
    point_dicts = []
    for folder in folders:
        point_dicts.append(extract_site_points(f"{version_path}/{folder}/"))
    config_module_path = version_path + "/global_config.py"
    spec = importlib.util.spec_from_file_location("global_config", config_module_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    global_points = config_module.global_points
    from_points, to_points = [], []
    for points in point_dicts:
        keys = points.keys()
        from_points.append(list(points.values()))
        to_points.append([global_points[key] for key in keys])
    return (from_points, to_points)


def extract_site_points(folder_path: str):
    config_module_path = folder_path + "/station_config.py"
    spec = importlib.util.spec_from_file_location("station_config", config_module_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    return config_module.points
