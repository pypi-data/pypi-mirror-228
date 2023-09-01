import json
import logging
import math
import os
import sys
from datetime import datetime
from typing import List, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.optim as optim
import yaml
from scipy.io import savemat
from torch.utils.data import DataLoader

from lidar_camera_calibration import general as gn
from lidar_camera_calibration import model as camLiDARMI
from lidar_camera_calibration import rotations as rot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)


def convert_numpy_to_list(data):
    if isinstance(data, dict):
        return {key: convert_numpy_to_list(value) for key, value in data.items()}
    elif isinstance(data, (list, tuple)):
        return [convert_numpy_to_list(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data


class LiDARCameraCalibrationResults:
    def __init__(
        self,
        Tlc: torch.Tensor,
        camera_matrix: torch.Tensor,
        distortion_coefficients: torch.Tensor,
        is_camera_learned: bool,
        is_using_Lie_group: bool,
        num_epochs: int,
        learning_rate: float,
        generator_file: str = sys._getframe(1).f_code.co_name,
        git_id: str = gn.get_git_revision_short_hash(),
    ):
        # Set attributes
        self.Tlc = Tlc
        self.camera_matrix = camera_matrix
        self.distortion_coefficients = distortion_coefficients
        self.is_camera_learned = is_camera_learned
        self.is_using_Lie_group = is_using_Lie_group
        self.num_epochs = num_epochs
        self.learning_rate = learning_rate

        # Optionally set attributes
        self.generator_file = generator_file
        self.git_id = git_id

        # Internally set attributes
        self.date_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    def toNumpyDict(self) -> dict:
        toSave = dict()
        # Set attributes
        toSave["Tlc"] = self.Tlc.numpy()
        toSave["camera_matrix"] = self.camera_matrix.numpy()
        toSave["distortion_coefficients"] = self.distortion_coefficients.numpy()
        toSave["is_camera_learned"] = self.is_camera_learned
        toSave["is_using_Lie_group"] = self.is_using_Lie_group
        toSave["num_epochs"] = self.num_epochs
        toSave["learning_rate"] = self.learning_rate

        # Optionally set attributes
        toSave["git_id"] = self.git_id
        toSave["generator_file"] = self.generator_file

        # Internally set attributes
        toSave["date_time"] = self.date_time
        return toSave

    def toYAML(self, filepath: str):
        data = self.toNumpyDict()
        data = convert_numpy_to_list(data)
        with open(filepath, "w") as file:
            yaml.dump(data, file)

    def toJSON(self, filepath: str):
        data = self.toNumpyDict()
        data = convert_numpy_to_list(data)
        with open(filepath, "w") as file:
            json.dump(data, file)

    def toMATLAB(self, filepath: str):
        savemat(filepath, self.toNumpyDict())


def get_factors(x: int) -> List[int]:
    factors_ = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors_.append(i)
    return factors_


def showLiDARCameraCorrelation(fig_num: int, train_loader, model, title: str):
    I_lidar = []
    I_image = []
    for batch_idx, data in enumerate(train_loader):
        Il, Ii = model.forward(data)
        I_lidar.append(Il.flatten())
        I_image.append(Ii.flatten())
    I_lidar, I_image = (
        torch.hstack(I_lidar).detach().cpu(),
        torch.hstack(I_image).detach().cpu(),
    )

    hist_lidar = torch.histogram(I_lidar, density=True)
    hist_image = torch.histogram(I_image, density=True)

    plt.figure(fig_num)
    plt.subplot(1, 4, 1)
    x = (hist_lidar[1][0:-1] + hist_lidar[1][1:]) / 2
    plt.plot(x, hist_lidar[0])
    plt.xlabel("Intensity")
    plt.title("LiDAR")
    plt.ylim([0, hist_lidar[0].max() * 1.25])

    plt.subplot(1, 4, 2)
    x = (hist_image[1][0:-1] + hist_image[1][1:]) / 2
    plt.plot(x, hist_image[0])
    plt.xlabel("Intensity")
    plt.title("Camera")
    plt.ylim([0, hist_image[0].max() * 1.25])

    plt.subplot(1, 4, (3, 4))

    plt.hist2d(
        I_image.numpy(),
        I_lidar.numpy(),
        density=True,
        bins=100,
        cmap=mpl.colormaps["plasma"],
    )
    plt.ylabel("LiDAR Intensities")
    plt.xlabel("Camera Intensities")

    plt.suptitle(title, fontsize=14)


def calibrate(
    calibration_data_dir: str,
    eta0: torch.Tensor,
    max_samples: int = 5000,
    num_epochs: int = 300,
    plot_iter: bool = False,
    plot_correlation: bool = True,
    learn_camera: bool = True,
    learning_rate: float = 1e-3,
    max_lidar_range: float = 15,
    device: str = "cpu",
    dtype=torch.float64,
) -> Tuple[
    LiDARCameraCalibrationResults, camLiDARMI.CameraLiDARMutualInformation, DataLoader
]:
    """_summary_

    Args:
        calibration_data_dir (str): Directory that contains calibration data folders:
            calibration_data_dir/raw directory with
            calibration_data_dir/compressed
            calibration_data_dir/results
        eta0 (torch.Tensor): Initial pose [rCLl; Thetalc], where rCLl ∈ ℝ^3 is the translational vector and Thetalc ∈ ℝ^3
                             is the Euler angles that define the relative rotation
        max_samples (int, optional): _description_. Defaults to 5000.
        num_epochs (int, optional): _description_. Defaults to 300.
        plot_iter (bool, optional): _description_. Defaults to False.
        plot_correlation (bool, optional): _description_. Defaults to True.
        learn_camera (bool, optional): _description_. Defaults to True.
        learning_rate (float, optional): _description_. Defaults to 1e-3.
        max_lidar_range (float, optional): _description_. Defaults to 15.
        device (str, optional): _description_. Defaults to "cpu".
        dtype (_type_, optional): _description_. Defaults to torch.float64.

    Returns:
        Tuple[ LiDARCameraCalibrationResults, camLiDARMI.CameraLiDARMutualInformation, DataLoader ]: _description_
    """

    assert os.path.isdir(calibration_data_dir), "Expected {} to be a directory.".format(
        calibration_data_dir
    )
    raw_data_dir = os.path.join(calibration_data_dir, "raw")
    matlab_compressed_data_dir = os.path.join(calibration_data_dir, "compressed")
    calibration_results_dir = os.path.join(calibration_data_dir, "results")

    if not os.path.isdir(calibration_results_dir):
        os.mkdir(calibration_results_dir)

    mat_files = [
        f
        for f in os.listdir(matlab_compressed_data_dir)
        if os.path.isfile(os.path.join(matlab_compressed_data_dir, f))
        and f.startswith("frame-")
    ]

    mat_files.sort()
    log.info(
        "%d frame data files found in %s", len(mat_files), matlab_compressed_data_dir
    )

    assert len(mat_files) > 0, "Expected there to be frame data"

    train_data = gn.CalibrationDataset(
        matlab_compressed_data_dir, mat_files, max_samples=max_samples
    )

    factors = get_factors(len(train_data))
    if len(factors) > 2:
        batch_size_train = factors[-2]
    else:
        batch_size_train = round(min(10, len(train_data) * 0.25))

    train_loader = DataLoader(
        train_data, batch_size=batch_size_train, shuffle=True, collate_fn=gn.my_collate
    )

    camera_params_name = "camera_params.yaml"

    camera_params_file = os.path.join(raw_data_dir, camera_params_name)
    assert os.path.isfile(camera_params_file), "Expected {} to be a file in {}".format(
        camera_params_name, raw_data_dir
    )

    Tlc0 = rot.getTransformationMatrixFromVector(eta0)
    Rlc0 = Tlc0[0:3, 0:3]
    rCLl0 = Tlc0[0:3, [3]]

    model = camLiDARMI.CameraLiDARMutualInformation(
        rCLl0,
        Rlc0,
        camera_params_file,
        use_Lie_group=False,
        learn_camera=learn_camera,
        max_range=max_lidar_range,
        device=device,
        dtype=dtype,
    )
    if plot_correlation:
        showLiDARCameraCorrelation(1, train_loader, model, "pre-calibration")

    Kc, dist_theta = model.getCamera()

    train_iter_loss = []
    train_iter_counter = []
    train_epoch_loss = []
    train_epoch_counter = []

    # Calibration
    def train(epoch):
        ndisp = 10
        nmod = math.ceil(len(train_loader) / float(ndisp))

        epoch_cost = 0
        npoints = 0
        npoints_batch = 0
        for batch_idx, data in enumerate(train_loader):
            optimizer.zero_grad()
            Il, Ii = model.forward(data)
            loss = model.cost(Il, Ii)
            loss.backward()
            loss_eval = loss.item()

            optimizer.step()
            npoints_batch = len(Il)
            npoints = npoints + npoints_batch

            assert (
                not model.getRelativePose().detach().cpu().isnan().any()
            ), "Relative pose is nan after optimisation step"

            if batch_idx % nmod == 0:
                log.info(
                    "Train Epoch: {} [{}/{:3d} ({:3.0f}%)]\tLoss: {:.6f}".format(
                        epoch,
                        batch_idx * train_loader.batch_size,
                        len(train_loader.dataset),
                        100.0 * batch_idx / len(train_loader),
                        loss_eval,
                    )
                )

            train_iter_loss.append(loss_eval)
            epoch_cost += npoints_batch * loss_eval
            epoch_val = (
                1.0 * (batch_idx * batch_size_train)
                + ((epoch - 1) * len(train_loader.dataset))
            ) / len(train_loader.dataset)
            train_iter_counter.append(epoch_val)

        epoch_cost = epoch_cost / npoints
        train_epoch_loss.append(epoch_cost)
        train_epoch_counter.append(epoch)

    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)

    if plot_iter:
        fig, ax = plt.subplots()  # Create figure and axes

        (line_iter,) = ax.plot(
            train_iter_counter, -np.array(train_iter_loss), "r-", label="Train iter MI"
        )
        (line_epoch,) = ax.plot(
            train_epoch_counter, -np.array(train_epoch_loss), "b-x", label="Train MI"
        )
        ax.set_ylabel("Mutual Information")
        ax.set_xlabel("No. of epochs")
        ax.legend()

    for epoch in range(1, 1 + num_epochs):
        train(epoch)
        if plot_iter:
            line_iter.set_data(train_iter_counter, -np.array(train_iter_loss))

            line_epoch.set_data(train_epoch_counter, -np.array(train_epoch_loss))
            ax.relim()  # Recalculate the data limits
            ax.autoscale_view()  # Auto-scale the axes
            fig.canvas.draw()  # Redraw the figure

            plt.pause(0.01)

    # Post Calibration
    Tlc_final = model.getRelativePose().detach().cpu()

    Kc, dist_theta = model.getCamera()

    res = LiDARCameraCalibrationResults(
        Tlc_final,
        Kc,
        dist_theta,
        learning_rate=learning_rate,
        is_camera_learned=model.learn_camera,
        is_using_Lie_group=model.use_Lie_group,
        nepochs=epoch,
        generator_file=__file__,
    )

    parameterisation = "Lie" if model.use_Lie_group else "Euler"
    output_file = os.path.join(
        calibration_results_dir, "calibration_{}_{}".format(parameterisation, epoch)
    )
    res.toMATLAB(output_file)
    res.toYAML(output_file)

    if plot_correlation:
        showLiDARCameraCorrelation(2, train_loader, model, "post-calibration")

    return res, model, train_loader
