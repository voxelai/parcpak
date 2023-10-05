
from __future__ import annotations

import os
import urllib.request
from pathlib import Path

PARCPAK_DIR = os.path.expanduser("~/parcpak_data")
REPO_URL = "https://github.com/voxelai/parcpak/raw/main/data/"


def _download_file(
    url: str, download_dir: 
    str | Path | None = None, 
    overwrite: bool = False
):

    if download_dir is None:
        download_dir = PARCPAK_DIR
    os.makedirs(download_dir, exist_ok=True)

    target_file = Path(download_dir, os.path.basename(url)).resolve()

    if overwrite or (not os.path.exists(target_file)):
        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, target_file)
    else:
        pass
    return str(target_file)


def fetch_schaefer(version: int, resolution: int = 2):

    name = f"Schaefer{version}_7Networks"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations", 
            f"Schaefer2018_{version}Parcels_7Networks_order_FSLMNI152_{resolution}mm.nii.gz"
        )
    )

    table = _download_file(
        os.path.join(
            REPO_URL,
            "tables", 
            f"Schaefer2018_{version}Parcels_7Networks.csv"
        )
    )

    return name, parc, table


def fetch_diedrichsen(resolution: int = 2):

    name = "Diedrichsen"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations", 
            f"Diedrichsen_space-MNI_dseg_{resolution}mm.nii.gz"
        )
    )

    table = _download_file(os.path.join(REPO_URL, "tables", "Diedrichsen.csv"))

    return name, parc, table


def fetch_buckner(resolution: int = 2):

    name = "Buckner7"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations", 
            f"Buckner7_space-MNI_dseg_{resolution}mm.nii.gz"
        )
    )

    table = _download_file(os.path.join(REPO_URL, "tables", "Buckner7.csv"))

    return name, parc, table


def fetch_tian(version: int, resolution: int = 2):

    name = f"Tian_Subcortex_S{version}"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations", 
            f"Tian_Subcortex_S{version}_3T_{resolution}mm.nii.gz"
        )
    )

    table = _download_file(
        os.path.join(
            REPO_URL,
            "tables", 
            f"Tian_Subcortex_S{version}_3T_label.csv"
        )
    )

    return name, parc, table


def fetch_parcellations(resolution: int = 2):

    parcs = []

    for i in range(100, 1100, 100):
        parcs.append(fetch_schaefer(i, resolution))

    for i in range(1, 4):
        parcs.append(fetch_tian(i, resolution))

    parcs.append(fetch_diedrichsen(resolution))
    parcs.append(fetch_buckner(resolution))
    return parcs
