import os

from ..utils import logger, constants
from ..services import *

log = logger.setup_logger()


def download_file(
    file: str,
    repo_id: str,
    cluster: str = "npu",
    save_path: str = constants.PATH.DATASET_SAVE_PATH,
):
    upload_type = get_upload_type(cluster)

    openi_repo = OpeniRepo(repo_id=repo_id)
    if openi_repo.access not in ["read", "write"]:
        msg = f"`{repo_id}` 无权限操作此仓库"
        log.error(msg)
        raise ValueError(msg)

    openi_dataset = OpeniDataset(repo_id=openi_repo.repo_id)
    openi_dataset.get_dataset_file(upload_type=upload_type)
    targe_file = None
    for f in openi_dataset.dataset_files:
        if f["name"] == file and f["type"] == upload_type:
            targe_file = f
    if targe_file is None:
        msg = (
            f"❌ `{openi_repo.repo_id}`-`{openi_dataset.dataset_name}` "
            f"数据集内未找到名为{file}({cluster})的压缩文件"
        )
        log.error(msg)
        raise ValueError(msg)

    local_dir = os.path.expanduser(save_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)

    openi_file = OpeniFileDownload(
        filename=targe_file["name"],
        size=targe_file["size"],
        local_dir=local_dir,
        repo_id=openi_repo.repo_id,
        dataset_or_model_id=openi_dataset.dataset_id,
        dataset_or_model_name=openi_dataset.dataset_name,
        target_type="dataset",
        upload_type=upload_type,
        uuid=targe_file["uuid"],
    )

    display_progress_bar([openi_file])
    openi_file.download_with_tqdm()


def download_all(
    repo_id: str,
    cluster: str = "npu",
    save_path: str = constants.PATH.DATASET_SAVE_PATH,
):
    upload_type = get_upload_type(cluster)

    openi_repo = OpeniRepo(repo_id=repo_id)
    if openi_repo.access not in ["read", "write"]:
        msg = f"`{repo_id}` 无权限操作此仓库"
        log.error(msg)
        raise ValueError(msg)

    openi_dataset = OpeniDataset(repo_id=openi_repo.repo_id)
    openi_dataset.get_dataset_file()

    local_dir = os.path.expanduser(save_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)

    openifiles = list()
    for targe_file in openi_dataset.dataset_files:
        if targe_file["type"] == upload_type:
            openi_file = OpeniFileDownload(
                filename=targe_file["name"],
                size=targe_file["size"],
                local_dir=local_dir,
                repo_id=openi_repo.repo_id,
                dataset_or_model_id=openi_dataset.dataset_id,
                dataset_or_model_name=openi_dataset.dataset_name,
                target_type="dataset",
                upload_type=upload_type,
                uuid=targe_file["uuid"],
            )
            openifiles.append(openi_file)

    display_progress_bar(openifiles)
    for openi_file in openifiles:
        openi_file.download_with_tqdm()
