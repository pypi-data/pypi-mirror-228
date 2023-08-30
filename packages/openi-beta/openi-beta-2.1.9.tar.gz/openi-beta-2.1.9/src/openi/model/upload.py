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
    can_upload = (
        openi_model.model_creator == openi_repo.current_user
        or openi_repo.is_admin
        or openi_repo.is_onwer
    )
    if can_upload is False:
        msg = f"❌ 本机登录用户无此模型上传权限，模型名称 `{openi_model.model_name}`, 仓库名称 `{openi_model.repo_id}`"
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


def upload_model_file(
    file: str,
    repo_id: str,
    model_name: str,
):
    # OpeniRepo, check repo_id, access
    openi_repo = OpeniRepo(repo_id=repo_id)
    # if openi_repo.access != "write" or openi_repo.is_collaborator is False:
    #     msg = f"`{openi_repo.username}` 无上传权限，无法操作此仓库`{openi_repo.full_display_name}`"
    #     log.error(msg)
    #     raise ValueError(msg)

    # OpeniModel
    openi_model = OpeniModel(
        model_name=model_name,
        repo_id=openi_repo.repo_id,
    )

    # OpeniFileUpload
    local_file = os.path.expanduser(file)
    if not os.path.exists(local_file):
        msg = f"❌ {local_file} 未找到本地文件"
        log.error(msg)
        raise ValueError(msg)

    # openifiles
    tiltle_pbar = tqdm(
        # total=local_file,
        leave=True,
        bar_format="{desc}",
        desc=f"Calculating file md5, this might take a while for large file… ",
        position=0,
    )

    openi_file = OpeniFileUpload(
        local_file=local_file,
        repo_id=openi_repo.repo_id,
        upload_type=constants.FILE.DEFAULT_UPLOAD_TYPE,
        dataset_or_model_id=openi_model.model_id,
        dataset_or_model_name=openi_model.model_name,
        target_type="model",
    )

    # # Display pbar
    display_progress_bar([openi_file])

    # # Upload
    openi_file.upload_with_tqdm()
