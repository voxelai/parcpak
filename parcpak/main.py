from __future__ import annotations

import os
import urllib.request
from pathlib import Path

import nibabel as nib
import pandas as pd
from nilearn.maskers import NiftiLabelsMasker

PARCPAK_DIR = os.path.expanduser("~/parcpak_data")
REPO_URL = "https://github.com/voxelai/parcpak/raw/main/data/"


def _download_file(
    url: str,
    download_dir: str | Path | None = None,
    overwrite: bool = False,
):
    """Download file from URL

    Args:
        url (str): File URL
        download_dir (str | Path | None, optional): Directory to save file in.
        If None, default directory ($HOME/parcpak) is used. Defaults to None.
        overwrite (bool, optional): If False, download is skipped if file
        exists; if True, then overwrite existing file. Defaults to False.

    Returns:
        str: Path to downloaded file
    """
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


def fetch_schaefer(
    version: int,
    resolution: int = 2,
    download_dir: str | Path | None = None,
    overwrite: bool = False,
) -> tuple:
    """Get specific Schaefer parcellation

    Args:
        version (int): Number of regions in Schaefer parcellation (100-1000)
        resolution (int, optional): 1 or 2 mm version of parcellation. Defaults to 2.
        download_dir (str | Path | None, optional): Directory to save file in.
        If None, default directory ($HOME/parcpak) is used. Defaults to None.
        overwrite (bool, optional): If False, download is skipped if file
        exists; if True, then overwrite existing file. Defaults to False.

    Returns:
        tuple: (Parcellation name, path to file, path to associated label table)
    """
    name = f"Schaefer{version}_7Networks"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations",
            f"Schaefer2018_{version}Parcels_7Networks_order_FSLMNI152_{resolution}mm.nii.gz",
        ),
        download_dir,
        overwrite,
    )

    table = _download_file(
        os.path.join(
            REPO_URL,
            "tables",
            f"Schaefer2018_{version}Parcels_7Networks.csv",
        ),
        download_dir,
        overwrite,
    )

    return name, parc, table


def fetch_diedrichsen(
    resolution: int = 2,
    download_dir: str | Path | None = None,
    overwrite: bool = False,
) -> tuple:
    """Download Diedrichsen cerebellar parcellation

    Args:
        resolution (int, optional): 1 or 2 mm version of parcellation. Defaults to 2.
        download_dir (str | Path | None, optional): Directory to save file in.
        If None, default directory ($HOME/parcpak) is used. Defaults to None.
        overwrite (bool, optional): If False, download is skipped if file
        exists; if True, then overwrite existing file. Defaults to False.

    Returns:
        tuple: (Parcellation name, path to file, path to associated label table)
    """
    name = "Diedrichsen"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations",
            f"Diedrichsen_space-MNI_dseg_{resolution}mm.nii.gz",
        ),
        download_dir,
        overwrite,
    )

    table = _download_file(os.path.join(REPO_URL, "tables", "Diedrichsen.csv"))

    return name, parc, table


def fetch_buckner(
    resolution: int = 2,
    download_dir: str | Path | None = None,
    overwrite: bool = False,
) -> tuple:
    """Download Buckner cerebellar parcellation

    Args:
        resolution (int, optional): 1 or 2 mm version of parcellation. Defaults to 2.
        download_dir (str | Path | None, optional): Directory to save file in.
        If None, default directory ($HOME/parcpak) is used. Defaults to None.
        overwrite (bool, optional): If False, download is skipped if file
        exists; if True, then overwrite existing file. Defaults to False.

    Returns:
        tuple: (Parcellation name, path to file, path to associated label table)
    """
    name = "Buckner7"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations",
            f"Buckner7_space-MNI_dseg_{resolution}mm.nii.gz",
        ),
        download_dir,
        overwrite,
    )

    table = _download_file(os.path.join(REPO_URL, "tables", "Buckner7.csv"))

    return name, parc, table


def fetch_tian(
    version: int,
    resolution: int = 2,
    download_dir: str | Path | None = None,
    overwrite: bool = False,
) -> tuple:
    """Download Tian subcortical parcellation

    Args:
        version (int): Parcellation version (1-4)
        resolution (int, optional): 1 or 2 mm version of parcellation. Defaults to 2.
        download_dir (str | Path | None, optional): Directory to save file in.
        If None, default directory ($HOME/parcpak) is used. Defaults to None.
        overwrite (bool, optional): If False, download is skipped if file
        exists; if True, then overwrite existing file. Defaults to False.

    Returns:
        tuple: (Parcellation name, path to file, path to associated label table)
    """
    name = f"Tian_Subcortex_S{version}"
    parc = _download_file(
        os.path.join(
            REPO_URL,
            "parcellations",
            f"Tian_Subcortex_S{version}_3T_{resolution}mm.nii.gz",
        ),
        download_dir,
        overwrite,
    )

    table = _download_file(
        os.path.join(REPO_URL, "tables", f"Tian_Subcortex_S{version}_3T_label.csv"),
        download_dir,
        overwrite,
    )

    return name, parc, table


def get_parcellations(resolution: int = 2, overwrite: bool = False) -> list:
    """Get all standard parcellations and their respective label tables

    Args:
        resolution (int, optional): 1 or 2 mm version of parcellation. Defaults to 2.
        overwrite (bool, optional): If False, download is skipped if file
        exists; if True, then overwrite existing file. Defaults to False.

    Returns:
        list: List of parcellation tuples. For each parcellation:
        (Parcellation name, path to file, path to associated label table)
    """

    parc_list = []
    for i in range(100, 1100, 100):
        parc_list.append(fetch_schaefer(i, resolution, overwrite))

    for i in range(1, 4):
        parc_list.append(fetch_tian(i, resolution, overwrite))

    parc_list.append(fetch_diedrichsen(resolution, overwrite))
    parc_list.append(fetch_buckner(resolution, overwrite))
    return parc_list


def img2table(img: str | Path | nib.Nifti1Image, metric: str = "mean"):
    """Convert NIFTI image into data table of regional values for each
    standard parcellation

    Computes regional values (e.g., mean, standard deviation) for each
    parcellation and outputs data in a long data frame

    Args:
        img (str | Path | nib.Nifti1Image): File path or loaded NIFTI image
        metric (str, optional): Regional metric to use. Must be one of: sum,
        mean, median, minimum, maximum, variance, standard_deviation. Defaults
        to "mean".

    Returns:
        pandas.DataFrame: Single dataframe with columns "Parcellation",
        "Region", and "Value"; contains regional values for each
        parcellation
    """
    parcs = get_parcellations()

    list_ = []
    for p in parcs:
        name, parc_file, table = p
        masker = NiftiLabelsMasker(labels_img=parc_file, strategy=metric)
        data = masker.fit_transform(img).ravel()

        table = pd.read_csv(table)
        df = pd.DataFrame(
            {"Parcellation": name, "Region": table["Label"], "Value": data},
        )
        list_.append(df)

    return pd.concat(list_)
