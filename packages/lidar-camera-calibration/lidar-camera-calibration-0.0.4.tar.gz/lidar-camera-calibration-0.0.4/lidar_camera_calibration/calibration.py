import logging
import math
import os
from typing import Any, List, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.optim as optim
from scipy.io import savemat
from torch.utils.data import DataLoader

from lidar_camera_calibration import general as gn
from lidar_camera_calibration import model as camLiDARMI
from lidar_camera_calibration import rotations as rot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)


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
    maxSamples: int = 5000,
    numEpochs: int = 300,
    plot_iter: bool = False,
    plot_correlation: bool = True,
    device: str = "cpu",
    dtype=torch.float64,
) -> Tuple[dict, Any, Any]:
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
        matlab_compressed_data_dir, mat_files, maxSamples=maxSamples
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
        useLieGroup=False,
        learnCamera=True,
        device=device,
        dtype=dtype,
    )
    if plot_correlation:
        showLiDARCameraCorrelation(1, train_loader, model, "pre-calibration")
    # plt.show(block=True)

    Kc, dist_theta = model.getCamera()
    Kc_init = Kc.detach().cpu().numpy()

    train_iter_loss = []
    train_iter_counter = []
    train_epoch_loss = []
    train_epoch_counter = []
    learning_rate = 1e-4

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
    for epoch in range(1, 1 + numEpochs):
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
    Kc_final, dist_theta_final = (
        Kc.detach().cpu().numpy(),
        dist_theta.detach().cpu().numpy(),
    )

    toSave = dict()
    toSave["Tlc"] = Tlc_final.numpy()
    toSave["camera_matrix"] = Kc_final
    toSave["distortion_coefficients"] = dist_theta_final
    toSave["train_counter"] = train_epoch_counter
    toSave["mutual_information"] = -np.array(train_epoch_loss)
    toSave["generatorFile"] = __file__
    toSave["git_id"] = gn.get_git_revision_short_hash()

    filename = "calibration"
    if model.learnCamera:
        filename += "_joint"
    else:
        filename += "_pose"

    if model.useLieGroup:
        filename += "_lie"
    else:
        filename += "_euler"
    filename += "_{}.mat".format(epoch)
    filepath = os.path.join(calibration_results_dir, filename)
    savemat(filepath, toSave)

    print("Initial Tlc")
    print(Tlc0.numpy())

    print("Final Tlc")
    print(Tlc_final.numpy())

    print("Initial Kc")
    print(Kc_init)

    print("Final Kc")
    print(Kc_final)
    if plot_correlation:
        showLiDARCameraCorrelation(2, train_loader, model, "post-calibration")

    return toSave, model, train_loader
