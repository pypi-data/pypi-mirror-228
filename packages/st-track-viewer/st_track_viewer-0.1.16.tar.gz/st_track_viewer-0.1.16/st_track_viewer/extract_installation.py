from datetime import timedelta
import json
import cv2
import numpy as np
import os
import re
from typing import Tuple, TypedDict, List

Pos = Tuple[float, float, float, float, float, float]


class Proj(TypedDict):
    Type: int
    Fov: Tuple[float, float]
    K: Tuple[float, float, float]
    C: Tuple[float, float]
    P: Tuple[float, float]


class Ground(TypedDict):
    Pos: Pos
    width: float
    height: float


class Camera(TypedDict):
    Pos: Pos
    Proj: Proj


class Image(TypedDict):
    frame: np.ndarray
    width: int
    height: int


class FolderData(TypedDict):
    cam: Image
    ground: Image
    cam_data: Camera
    ground_data: Ground


def extract_data(base_folder_path: str) -> List[FolderData]:
    folders = list(
        filter(lambda folder: folder.startswith("A"), os.listdir(base_folder_path))
    )
    data_list = []
    for folder in folders:
        data_list.append(extract_folder_information(f"{base_folder_path}/{folder}/"))
    return data_list


def extract_folder_information(folder_path: str) -> FolderData:
    data: FolderData = {}
    desired_pattern = "cap_[0-9]_0.avi"
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)) and re.match(
            desired_pattern, filename
        ):
            data["cam"] = extract_frame_from_video(folder_path + filename)
    data["ground"] = extract_image_data(folder_path + "ground.png")
    data["cam_data"] = extract_cam_data(folder_path + "cam0.cam")
    data["ground_data"] = extract_ground_data(folder_path + "ground.gnd")
    return data


def extract_frame_from_video(video_path: str) -> Image:
    video_cap = cv2.VideoCapture(video_path)
    ret, frame = video_cap.read()
    videoframe: Image = {}
    if ret:
        height, width, _ = frame.shape
        videoframe["frame"] = cv2.rotate(frame, cv2.ROTATE_180)
        videoframe["width"] = width
        videoframe["height"] = height
    else:
        print("Error reading frame")
    video_cap.release()
    return videoframe


def extract_image_data(image_path: str) -> Image:
    img = cv2.imread(image_path)
    img = cv2.rotate(img, cv2.ROTATE_180)
    height, width, _ = img.shape
    ground_image: Image = {}
    ground_image["frame"] = img
    ground_image["height"] = height
    ground_image["width"] = width
    return ground_image


def extract_cam_data(file_path: str) -> Camera:
    with open(file_path, "r") as file:
        cam_data_str = file.read()
    cam_data_dict: Camera = json.loads(cam_data_str)
    pos = cam_data_dict["Pos"]
    converted_pos = [
        pos[0],
        pos[1],
        pos[2],
        pos[3] * np.pi / 180.0,
        pos[4] * np.pi / 180.0,
        pos[5] * np.pi / 180.0,
    ]
    converted_fov = [value * np.pi / 180.0 for value in cam_data_dict["Proj"]["Fov"]]
    cam_data_dict["Pos"] = converted_pos
    cam_data_dict["Proj"]["Fov"] = converted_fov
    return cam_data_dict


def extract_ground_data(file_path: str) -> Ground:
    with open(file_path, "r") as file:
        lines = file.readlines()
    pos = list(map(float, lines[0].split()))
    angles = [value * np.pi / 180.0 for value in list(map(float, lines[1].split()))]
    h_w = list(map(float, lines[2].split()))
    return {"Pos": pos + angles, "width": h_w[0], "height": h_w[1]}
