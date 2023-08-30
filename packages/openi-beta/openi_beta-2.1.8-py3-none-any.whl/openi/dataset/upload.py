import os
from tqdm.auto import tqdm

from ..utils import logger
from ..services import *

log = logger.setup_logger()


def upload_file(
    file: str,
    repo_id: str,
    cluster: str = "npu",
):
    upload_type = get_upload_type(cluster)

    # OpeniFileUpload
    local_file = os.path.expanduser(file)
    if not os.path.exists(local_file):
        msg = f"❌ {local_file} 未找到本地文件"
        log.error(msg)
        raise ValueError(msg)

    openi_repo = OpeniRepo(repo_id=repo_id)
    can_operate = (
        openi_repo.access == "write"
        or openi_repo.is_collaborator
        or openi_repo.is_admin
    )
    if can_operate is False:
        msg = (
            f"`{openi_repo.username}` 无上传数据集权限，无法操作此仓库`{openi_repo.full_display_name}`"
        )
        log.error(msg)
        raise ValueError(msg)

    openi_dataset = OpeniDataset(repo_id=openi_repo.repo_id)

    # openifiles
    tiltle_pbar = tqdm(
        # total=os.path.getsize(local_file),
        leave=True,
        # unit="B",
        # unit_scale=True,
        # unit_divisor=1024,
        bar_format="{desc}",
        desc=f"Calculating file md5, this might take a while for large file… ",
        position=0,
    )

    openi_file = OpeniFileUpload(
        local_file=local_file,
        repo_id=openi_repo.repo_id,
        upload_type=upload_type,
        dataset_or_model_id=openi_dataset.dataset_id,
        dataset_or_model_name=openi_dataset.dataset_name,
        target_type="dataset",
        # md5_pbar=tiltle_pbar,
    )
    tiltle_pbar.close()

    # # Display pbar
    display_progress_bar([openi_file])

    # # Upload
    openi_file.upload_with_tqdm()


def upload_all(
    folder: str,
    repo_id: str,
    cluster: str = "npu",
):
    upload_type = get_upload_type(cluster)

    openi_repo = OpeniRepo(repo_id=repo_id)
    if openi_repo.access not in ["read", "write"]:
        msg = f"`{repo_id}` 无权限操作此仓库"
        log.error(msg)
        raise ValueError(msg)

    openi_dataset = OpeniDataset(repo_id=openi_repo.repo_id)

    # OpeniFileUpload
    local_dir, targe_files = get_upload_folder_files(folder)
    if targe_files == []:
        msg = f"❌ {local_dir} 未找到任何本地文件"
        log.error(msg)
        raise ValueError(msg)

    # openifiles
    tiltle_pbar = tqdm(
        total=len(targe_files),
        leave=True,
        bar_format="{desc}({n_fmt}/{total_fmt}) |{bar}| [{elapsed}]",
        desc=f"Calculating file md5… ",
        position=0,
    )
    openifiles = list()
    for file in targe_files:
        openi_file = OpeniFileUpload(
            local_file=file,
            repo_id=openi_repo.repo_id,
            upload_type=upload_type,
            dataset_or_model_id=openi_dataset.dataset_id,
            dataset_or_model_name=openi_dataset.dataset_name,
            target_type="dataset",
            # md5_pbar=tiltle_pbar,
        )
        tiltle_pbar.update(1)
        openifiles.append(openi_file)

    # Display pbar
    display_progress_bar(openifiles)

    # # Upload
    for openi_file in openifiles:
        openi_file.upload_with_tqdm()
