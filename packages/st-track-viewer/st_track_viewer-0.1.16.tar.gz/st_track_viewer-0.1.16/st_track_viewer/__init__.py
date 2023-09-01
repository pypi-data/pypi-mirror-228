import os
from typing import List
from extract_installation import FolderData, Image, Ground, Camera, extract_data
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from helper import HeaderDictType, process_img_string, process_tracks

_RELEASE = True

track_viewer = False


if not _RELEASE:
    _component_func = components.declare_component(
        "st_track_viewer",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_track_viewer", path=build_dir)


def st_track_viewer(
    data: HeaderDictType,
    tracks=[],
    grounds=[],
    images=[],
    shapes=[],
    names=[],
    key=None,
):
    if not (
        len(tracks) == len(grounds)
        and len(tracks) == len(images)
        and len(tracks) == len(shapes)
    ):
        raise ValueError(
            f"""Length of tracks, grounds, images, shapes and names must be equal:
                         Tracks length: {len(tracks)}
                         Grounds length: {len(grounds)}
                         Images length: {len(images)}
                         Shapes length: {len(shapes)}
                         Names length: {len(names)}"""
        )
    ims = []
    # Convert images into url strings
    for im in images:
        url_string = process_img_string(im)
        ims.append(url_string)
    component_value = _component_func(
        tracks=tracks,
        data=data,
        images=ims,
        grounds=grounds,
        shapes=shapes,
        names=names,
        tool="trackviewer",
        key=key,
        default=0,
    )
    return component_value


def st_line_placement_tool(
    data: HeaderDictType,
    tracks,
    img_gnd: Image,
    ground: Ground,
    cameras: List[Image],
    grounds: List[Image],
    cam_data: List[Camera],
    ground_data: List[Ground],
    to_globals,
    to_locals,
    key=None,
):
    ground_image = process_img_string(img_gnd["frame"])
    images_cams = []
    images_grounds = []
    for img in cameras:
        images_cams.append(process_img_string(img["frame"]))
    for img in grounds:
        images_grounds.append(process_img_string(img["frame"]))
    component_value = _component_func(
        tracks=tracks,
        data=data,
        ground_image=ground_image,
        ground_shape=[img_gnd["height"], img_gnd["width"]],
        ground=ground,
        images_cams=images_cams,
        images_grounds=images_grounds,
        cameras=cam_data,
        grounds=ground_data,
        cam_shapes=[[value["width"], value["height"]] for value in cameras],
        ground_shapes=[[value["width"], value["height"]] for value in grounds],
        to_globals=to_globals,
        to_locals=to_locals,
        tool="lineplacementtool",
        key=key,
        default=0,
    )
    return component_value


# Test code
if not _RELEASE:
    import streamlit as st

    st.set_page_config(layout="wide")
    if track_viewer:
        # TODO - type the same and use the same as lineplacementtool
        groundGlobal = plt.imread("./assets/ground.png")
        folder_path = "./CSV2"
        folder_path2 = "./CSV"
        csv_files = os.listdir(folder_path)
        csv_files2 = os.listdir(folder_path2)
        keys = list(map(lambda string: string.split("_")[0], csv_files))
        keys2 = list(map(lambda string: string.split("_")[0], csv_files2))
        if "data" not in st.session_state:
            st.session_state["data"]: HeaderDictType = {
                "date": "2023-05-04T10:10:00",
                "min": 10,
                "sec": 0,
                "versions": ["A1"],
                "types": [
                    "Unknown",
                    "Bicycle",
                    "Pedestrian",
                    "Light vehicle",
                    "Heavy vehicle",
                ],
                "filter": {"filter": False, "minLength": 0, "maxLength": 100},
            }
        if "track_data" not in st.session_state:
            track_data = {}

            for file_name in csv_files:
                if file_name.endswith(".csv"):
                    date_str = file_name.split("_")[0]
                    date_key = pd.to_datetime(date_str).date().isoformat()
                    file_path = os.path.join(folder_path, file_name)
                    tracks = pd.read_csv(
                        file_path, sep=";", parse_dates=["Time"]
                    ).set_index("Time")
                    track_data[date_key] = tracks
            st.session_state["track_data"] = track_data
        _tracks = (
            process_tracks(
                st.session_state.track_data[st.session_state.data["date"].split("T")[0]]
            )
            if st.session_state.data["date"].split("T")[0] in keys
            else []
        )

        ground = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 30.0, 27.0]
        ground1 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 90.35000000000001, 82.55000000000001]

        shape1 = [600, 540]
        shape2 = [1807, 1651]
        tracks = [
            _tracks,
        ]

        grounds = [
            ground,
        ]
        cam_shapes = [
            shape1,
        ]
        images = [
            groundGlobal,
        ]
        names = [
            "A1",
        ]
        key = st_track_viewer(
            tracks=tracks,
            data=st.session_state.data,
            images=images,
            grounds=grounds,
            shapes=cam_shapes,
            names=names,
        )
        if (
            key != 0
            and "data" in st.session_state
            and not st.session_state.data["date"] == key["date"]
        ):
            st.session_state.data = key
            st.experimental_rerun()
        else:
            pass
    else:
        file_path = "../../../../Repositories/_V2.6_/"
        image_path = "version.5239d62ced86/"
        img_gnd: Image = {
            "frame": plt.imread(file_path + image_path + "OsloSPG_Viscando.png"),
            "width": 1651,
            "height": 1807,
        }
        ground: Ground = {
            "Pos": [0.0, 0.0, 0.0, 0, 0.0, 0.0],
            "width": 82.55000000000001,
            "height": 90.35000000000001,
        }
        folder_path = file_path + "CSV2/"
        csv_files = os.listdir(folder_path)
        keys = list(map(lambda string: string.split("_")[0], csv_files))
        if "data" not in st.session_state:
            st.session_state["data"]: HeaderDictType = {
                "date": "2023-05-22T22:10:00",
                "min": 1,
                "sec": 0,
                "versions": ["A1"],
                "types": [
                    "Unknown",
                    "Bicycle",
                    "Pedestrian",
                    "Light vehicle",
                    "Heavy vehicle",
                ],
                "filter": {"filter": False, "minLength": 0, "maxLength": 100},
            }
        if "track_data" not in st.session_state:
            track_data = {}

            for file_name in csv_files:
                if file_name.endswith(".csv"):
                    date_str = file_name.split("_")[0]
                    date_key = pd.to_datetime(date_str).date().isoformat()
                    path = os.path.join(folder_path, file_name)
                    tracks = pd.read_csv(path, sep=";", parse_dates=["Time"]).set_index(
                        "Time"
                    )
                    track_data[date_key] = tracks
            st.session_state["track_data"] = track_data
        _tracks = (
            process_tracks(
                st.session_state.track_data[st.session_state.data["date"].split("T")[0]]
            )
            if st.session_state.data["date"].split("T")[0] in keys
            else []
        )
        data: List[FolderData] = extract_data(
            "/Users/elliotglas/Programming/Viscando/Repositories/2023-05-22_Oslo_Lovenskiold"
        )

        # TODO - rename, restructure everything
        # TODO - check what is common and separate

        cameras = [value["cam"] for value in data]
        grounds = [value["ground"] for value in data]
        cam_data = [value["cam_data"] for value in data]
        ground_data = [value["ground_data"] for value in data]
        to_globals = [
            [
                [-0.7996342947738874, -0.8769677783932325, 1651.916464797217],
                [0.4312543563662252, -0.7767425867073505, 310.0446351241412],
                [-0.00020043863826757166, -0.00020792247664442307, 1.0],
            ],
            [
                [-0.7533756708857366, -0.6236930307373453, 1022.5735295242847],
                [0.5883237915580407, -0.7185988786048618, 525.6706133728866],
                [-0.00010220702930661576, 5.760901306676068e-05, 1.0],
            ],
        ]
        to_locals = [
            [
                [-0.7142406277457849, 0.5387831100350821, 1012.7411564760955],
                [-0.49546956285460614, -0.46961928284526505, 963.8125363144507],
                [-0.0002453463794479733, 1.3825273362550616e-5, 1.0],
            ],
            [
                [-0.8330190324794313, 0.7626289305675337, 451.43540600874707],
                [-0.7129342269436779, -0.7209177707109871, 1108.475078762635],
                [-3.204230845353476e-05, 0.00012694219795996383, 1.0],
            ],
        ]
        val = st_line_placement_tool(
            st.session_state.data,
            _tracks,
            img_gnd,
            ground,
            cameras,
            grounds,
            cam_data,
            ground_data,
            to_globals,
            to_locals,
        )
