import os

from ..utils import logger, constants
from ..utils.logger import *
from ..services import *

log = logger.setup_logger()


def download_model(
    repo_id: str,
    model_name: str,
    save_path: str = constants.PATH.MODEL_SAVE_PATH,
):
    openi_repo = OpeniRepo(repo_id=repo_id)
    if openi_repo.access not in ["read", "write"]:
        msg = f"`{repo_id}` 无权限操作此仓库"
        log.error(msg)
        raise ValueError(msg)

    openi_model = OpeniModel(
        model_name=model_name,
        repo_id=openi_repo.repo_id,
    )
    if openi_model.model_files == []:
        msg = f"❌ `{model_name}` 未找到文件"
        log.error(msg)
        raise ValueError(msg)
    if openi_model.can_download is False:
        msg = f"❌ 本机登录用户无此模型下载权限，模型名称 `{openi_model.model_name}`, 仓库名称 `{openi_model.repo_id}`"
        log.error(msg)
        raise ValueError(msg)

    save_path = os.path.expanduser(save_path)
    local_dir = os.path.join(save_path, f"{model_name}")
    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)

    openifiles = list()
    for targe_file in openi_model.model_files:
        openi_file = OpeniFileDownload(
            filename=targe_file["fileName"],
            size=targe_file["size"],
            local_dir=local_dir,
            repo_id=openi_repo.repo_id,
            dataset_or_model_id=openi_model.model_id,
            dataset_or_model_name=openi_model.model_name,
            target_type="model",
        )
        openifiles.append(openi_file)

    display_progress_bar(openifiles)
    for openi_file in openifiles:
        openi_file.download_with_tqdm()
