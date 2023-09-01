from tqdm.auto import tqdm

from ..utils import logger, constants
from ..services import *

log = logger.setup_logger()


def upload_model(
    folder: str,
    repo_id: str,
    model_name: str,
):
    # OpeniFileUpload
    local_dir, targe_files = get_upload_folder_files(folder)
    if targe_files == []:
        msg = f"❌ {local_dir} 未找到任何本地文件"
        log.error(msg)
        raise ValueError(msg)

    # OpeniRepo, check repo_id, access
    openi_repo = OpeniRepo(repo_id=repo_id)

    # OpeniModel
    openi_model = OpeniModel(
        model_name=model_name,
        repo_id=openi_repo.repo_id,
    )
    if openi_model.can_operate is False:
        msg = f"❌ `{openi_repo.current_user}` 无此模型上传权限，模型名称 `{openi_model.model_name}`, 仓库名称 `{openi_model.repo_id}`"
        log.error(msg)
        raise ValueError(msg)
    if openi_model.model_type == 0:
        msg = f"❌ `{openi_model.model_name}` 为线上模型，无法上传本地文件"
        log.error(msg)
        raise ValueError(msg)

    # openifiles
    tiltle_pbar = tqdm(
        total=len(targe_files),
        leave=True,
        bar_format="{desc}({n_fmt}/{total_fmt}) |{bar}| [{elapsed}]",
        desc=f"Calculating file md5… ",
        position=0,
        # dynamic_ncols=True,
    )
    openifiles = list()
    for file in targe_files:
        openi_file = OpeniFileUpload(
            local_file=file,
            repo_id=openi_repo.repo_id,
            upload_type=constants.FILE.DEFAULT_UPLOAD_TYPE,
            dataset_or_model_id=openi_model.model_id,
            dataset_or_model_name=openi_model.model_name,
            target_type="model",
        )
        tiltle_pbar.update(1)
        openifiles.append(openi_file)
    tiltle_pbar.close()

    # # Display pbar
    display_progress_bar(openifiles)

    # # Upload
    for openi_file in openifiles:
        openi_file.upload_with_tqdm()
