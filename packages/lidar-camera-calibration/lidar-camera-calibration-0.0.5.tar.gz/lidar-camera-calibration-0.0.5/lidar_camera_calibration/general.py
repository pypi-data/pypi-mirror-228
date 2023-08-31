import logging as log
import os
import subprocess
from typing import List, Tuple

import numpy as np
import torch
import yaml
from scipy.io import loadmat
from torch.utils.data import Dataset


def get_git_revision_hash() -> str:
    out = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8")
    out = out.strip()
    return out


def get_git_revision_short_hash() -> str:
    out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode(
        "utf-8"
    )
    out = out.strip()
    return out


def GaussianInterpolant(
    image: torch.Tensor, sigma: float, rQOi: torch.Tensor
) -> torch.Tensor:
    assert len(image.shape) == 2, "Expected image to be a 2d tensor."
    assert sigma > 0, "Expected sigma to be greater than 0."
    assert len(rQOi.shape) == 2, "Expected rQOi to be a 2d tensor."
    assert rQOi.shape[0] == 2, "Expected rQOi to have two rows."

    dtype = rQOi.dtype
    device = rQOi.device

    nW = int(max(1, round(2 * sigma)))

    xx = torch.arange(-nW, nW + 1, device=device)
    U, V = torch.meshgrid((xx, xx))
    pad = torch.vstack((U.flatten(), V.flatten()))

    rQOi_exp = rQOi.unsqueeze(2)
    rr = rQOi_exp.floor() + pad.unsqueeze(2).permute([0, 2, 1])

    z = (rr - rQOi_exp) / sigma
    z2 = (z * z).sum(0)
    sigTens = torch.tensor(sigma, dtype=dtype, device=device)
    logdetS = sigTens.log() * 2
    logw = (
        -0.5 * z2 - logdetS - torch.tensor(torch.pi, dtype=dtype, device=device).log()
    )
    logw = logw - torch.logsumexp(logw, dim=1, keepdim=True)
    nw = logw.exp()

    # This is returning a nans
    u0 = torch.clamp(rr[0, :, :], 0, image.shape[1] - 1)
    v0 = torch.clamp(rr[1, :, :], 0, image.shape[0] - 1)
    idxd = u0 + v0 * image.shape[1]
    idx = idxd.to(dtype=torch.long)

    image_flat = image.flatten()
    idx_flat = idx.flatten()
    I_flat = image_flat[idx_flat]
    I = I_flat.reshape(idx.size())

    Ii = (I * nw).sum(1)
    return Ii


def logGaussianMixtureAtXSingleCov(
    x: torch.Tensor, mu: torch.Tensor, S: torch.Tensor, logW: torch.Tensor
) -> torch.Tensor:
    assert len(x.shape) == 2
    assert len(mu.shape) == 2
    m = x.shape[-1]
    [n, N] = mu.shape
    assert N == logW.shape[1]

    logdetS = S.diag().abs().log().sum()
    # [N x n x m]
    e = x.reshape((1, n, m)) - mu.T.reshape((N, n, 1))
    SinvT = S.inverse().unsqueeze(2).permute(2, 0, 1)
    z = torch.matmul(SinvT, e)
    z2norm = (z * z).sum(1)
    lm = (
        -0.5 * z2norm
        - logdetS
        - 0.5 * n * torch.tensor(2 * torch.pi, dtype=x.dtype, device=x.device).log()
        + logW.reshape((N, 1))
    )
    l = torch.logsumexp(lm, dim=0).reshape(1, m)
    return l


def entropyUpperBoundGaussianMixtureSingleCov(
    mu: torch.Tensor, S: torch.Tensor, logW: torch.Tensor
) -> torch.Tensor:
    assert len(mu.shape) == 2
    [n, N] = mu.shape
    assert N == logW.shape[1]

    w = logW.exp()
    logdetS = S.diag().abs().log().sum()
    Z = (
        -logW
        + 0.5
        * n
        * (1 + torch.tensor(2 * torch.pi, dtype=mu.dtype, device=mu.device).log())
        + 0.5 * logdetS
    )
    H = w.inner(Z)
    return H


def getQuartiles(
    A: torch.Tensor, qvl=0.05, qvu=0.95
) -> Tuple[torch.Tensor, torch.Tensor]:
    assert A.shape[0] > 1, "Expected A to have data"
    Avec = A.flatten()

    A_torch, idx = torch.sort(Avec)

    nd = A_torch.shape[0]

    idxU = round((nd - 1) * qvu)
    idxL = round((nd - 1) * qvl)

    vU = A_torch[idxU]
    vL = A_torch[idxL]
    return vL, vU


def interQuartileRange(x: torch.Tensor) -> torch.Tensor:
    vL, vU = getQuartiles(x, qvl=0.25, qvu=0.75)
    return vU - vL


# Datasets
class CalibrationDataset(Dataset):
    def __init__(
        self,
        mat_dir: str,
        files: List[str],
        max_samples: int = -1,
        dtype=torch.float32,
        device: str = "cpu",
    ):
        self.data_dir = mat_dir
        self.files = files
        self.dtype = dtype
        self.device = device
        self.max_samples = max_samples
        if max_samples > 0:
            log.info(
                "Building training dataset where each frame has a maximum "
                + "of {} random samples from each image frame.".format(max_samples)
            )
        else:
            log.info("Building training dataset using all in each frame samples.")

    def __len__(self) -> int:
        return len(self.files)

    def getItemFromFile(self, idx) -> dict:
        mat_path = os.path.join(self.data_dir, self.files[idx])
        data = loadmat(mat_path)
        idxValid = (0 <= data["intensities"]) & (data["intensities"] <= 100)

        rPLl_np = data["rPLl"][:, idxValid.flatten()]
        intensities_np = data["intensities"][:, idxValid.flatten()] * 2.55

        if self.max_samples > 0:
            nValid = intensities_np.shape[1]
            idx_choose = np.random.choice(nValid, self.max_samples)
            intensities_np = intensities_np[:, idx_choose]
            rPLl_np = rPLl_np[:, idx_choose]

        rPLl = torch.from_numpy(rPLl_np).to(device=self.device, dtype=self.dtype)
        lidar_i = torch.from_numpy(intensities_np).to(
            device=self.device, dtype=self.dtype
        )
        img = torch.from_numpy(data["img"]).to(device=self.device, dtype=self.dtype)

        format_data = dict()
        format_data["img"] = img
        format_data["rPLl"] = rPLl
        format_data["intensities"] = lidar_i
        return format_data

    def getItemFromCache(self, idx):
        return self.cache_t[idx], self.cache_z[idx]

    def __getitem__(self, idx):
        return self.getItemFromFile(idx)


def my_collate(batch) -> List:
    data = []
    for packet in batch:
        data.append(packet)
    return data


# Camera
def readCameraIntrinsicsFromYaml(camera_params_file: str) -> dict:
    assert os.path.isfile(camera_params_file), (
        "Expected " + camera_params_file + " to be a file."
    )

    with open(camera_params_file, "r") as stream:
        try:
            camera_params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    names = [
        "camera_matrix",
        "distortion_coefficients",
        "rectification_matrix",
        "projection_matrix",
    ]
    param = camera_params
    for name in names:
        data = camera_params[name]
        nrows = data["rows"]
        ncols = data["cols"]
        datastr = data["data"]
        param[name] = np.array(datastr).reshape((nrows, ncols))
    return param


def vec2pix(
    rPCc: torch.Tensor, Kc: torch.Tensor, dist_theta: torch.Tensor
) -> torch.Tensor:
    assert rPCc.shape[0] == 3, (
        "Expected rPCc to have three rows, but its shape is " + str(rPCc.shape) + "."
    )
    assert Kc.shape[0] == 3 & Kc.shape[1] == 3, (
        "Expected Kc to have three rows and three columns, but its shape is "
        + str(Kc.shape)
        + "."
    )

    device = rPCc.device
    dtype = rPCc.dtype
    ntp = dist_theta.shape[1]
    nt = 12
    theta = torch.hstack(
        (dist_theta, torch.zeros(1, nt - ntp, device=device, dtype=dtype))
    )

    k1 = theta[0, 0]
    k2 = theta[0, 1]

    p1 = theta[0, 2]
    p2 = theta[0, 3]

    k3 = theta[0, 4]
    k4 = theta[0, 5]
    k5 = theta[0, 6]
    k6 = theta[0, 7]

    s1 = theta[0, 8]
    s2 = theta[0, 9]
    s3 = theta[0, 10]
    s4 = theta[0, 11]

    x = rPCc[[0], :]
    y = rPCc[[1], :]
    z = rPCc[[2], :]

    u = x / z
    v = y / z

    r2 = (u**2 + v**2).sum(dim=0, keepdim=True)
    r4 = r2 * r2
    r6 = r4 * r2

    alpha = k1 * r2 + k2 * r4 + k3 * r6
    beta = k4 * r2 + k5 * r4 + k6 * r6
    c = (1 + alpha) / (1 + beta)

    up = c * u + 2 * p1 * u * v + p2 * (r2 + 2 * u**2) + s1 * r2 + s2 * r4
    vp = c * v + 2 * p2 * u * v + p1 * (r2 + 2 * v**2) + s3 * r2 + s4 * r4

    fx = Kc[0, 0]
    fy = Kc[1, 1]
    cx = Kc[0, 2]
    cy = Kc[1, 2]

    rQOi = torch.vstack([fx * up + cx, fy * vp + cy])

    return rQOi


def lidar2pix(
    Tlc: torch.Tensor, rPLl: torch.Tensor, Kc: torch.Tensor, dist_theta: torch.Tensor
) -> torch.Tensor:
    assert (Tlc.shape[0] == 4) & (Tlc.shape[1] == 4), "Expected Tlc to be a 4x4"
    Rlc = Tlc[0:3, 0:3]
    rCLl = Tlc[0:3, [3]]
    rPCc = Rlc.T @ (rPLl - rCLl)
    return vec2pix(rPCc, Kc, dist_theta)
