""" """

from vaapi.client import Vaapi
import os
import numpy as np
import matplotlib.pyplot as plt


def candidates_distribution(logs):
    x_list = list()
    y_list = list()
    for data in logs:
        response = client.cognition_repr.list(
            log_id=data.id,
            representation_name="BallCandidates",
        )
        print(len(response))

        for candidates in response:
            patch_list = candidates.representation_data["patches"]
            for patch in patch_list:
                mid_x = (patch["max"]["x"] + patch["min"]["x"]) / 2
                mid_y = (patch["max"]["y"] + patch["min"]["y"]) / 2
                x_list.append(mid_x)
                y_list.append(mid_y)
        break

    fig, ax = plt.subplots()
    plt.title("Frequency of Ball Canditates found in Image")
    h = ax.hist2d(x_list, y_list, bins=[np.arange(0, 640, 20), np.arange(0, 480, 20)])
    fig.colorbar(h[3], ax=ax)
    plt.savefig("candidates_distribution.png")


def candidates_top_distribution(logs):
    x_list = list()
    y_list = list()
    for data in logs:
        response = client.cognition_repr.list(
            log_id=data.id,
            representation_name="BallCandidatesTop",
        )
        print(len(response))

        for candidates in response:
            patch_list = candidates.representation_data["patches"]
            for patch in patch_list:
                mid_x = (patch["max"]["x"] + patch["min"]["x"]) / 2
                mid_y = (patch["max"]["y"] + patch["min"]["y"]) / 2
                x_list.append(mid_x)
                y_list.append(mid_y)
        break

    fig, ax = plt.subplots()
    plt.title("Frequency of Ball Canditates found in Image Top")
    h = ax.hist2d(x_list, y_list, bins=[np.arange(0, 640, 20), np.arange(0, 480, 20)])
    fig.colorbar(h[3], ax=ax)
    plt.savefig("candidates_top_distribution.png")


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    logs = client.logs.list()
    # candidates_top_distribution(logs)
    # candidates_distribution(logs)

    x_list_top = list()
    y_list_top = list()
    x_list_bottom = list()
    y_list_bottom = list()
    for data in logs:
        print(data.log_path)
        response = client.cognition_repr.list(
            log_id=168,
            representation_name="MultiBallPercept",
        )

        for multipercept in response:
            if "percepts" in multipercept.representation_data:
                for percept in multipercept.representation_data["percepts"]:
                    cx = percept["centerInImage"]["x"]
                    cy = percept["centerInImage"]["y"]
                    cam = percept["cameraId"]
                    if cam == "top":
                        x_list_top.append(cx)
                        y_list_top.append(cy)
                    else:
                        x_list_bottom.append(cx)
                        y_list_bottom.append(cy)

    fig, ax = plt.subplots()
    plt.title("Frequency of Ball Percepts found in Image Top")
    h = ax.hist2d(
        x_list_top, y_list_top, bins=[np.arange(0, 640, 20), np.arange(0, 480, 20)]
    )
    fig.colorbar(h[3], ax=ax)
    plt.savefig("ball_percepts_top_distribution.png")

    fig, ax = plt.subplots()
    plt.title("Frequency of Ball Percepts found in Image")
    h = ax.hist2d(
        x_list_bottom,
        y_list_bottom,
        bins=[np.arange(0, 640, 20), np.arange(0, 480, 20)],
    )
    fig.colorbar(h[3], ax=ax)
    plt.savefig("ball_percepts_distribution.png")
