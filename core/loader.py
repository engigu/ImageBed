from config import Config

from core.uploader.gitee import GiteeUploader
from core.uploader.github import GithubUploader
from core.uploader.coding import CodingUploader
from core.uploader.minio import MinioUploader

# 其他接口
from core.uploader_other import (
    G360Uploader, SouGouUploader, BaiDuUploader,
    AliUploader
)

__UPLODER_MAPS__ = {
    GithubUploader.name: GithubUploader(
        access_token=Config.GITHUB_ACCESS_TOKEN,
        owner=Config.GITHUB_OWNER,
        repo=Config.GITHUB_REPO,
        branch=Config.GITHUB_BRANCH,
        store_path=Config.GITHUB_STORE_PATH,
        use_cdn=Config.CDN_USE
    ),
    GiteeUploader.name: GiteeUploader(
        access_token=Config.GITEE_ACCESS_TOKEN,
        owner=Config.GITEE_OWNER,
        repo=Config.GITEE_REPO,
        branch=Config.GITEE_BRANCH,
        store_path=Config.GITEE_STORE_PATH
    ),
    CodingUploader.name: CodingUploader(
        token=Config.CODING_ACCESS_TOKEN,
        owner=Config.CODING_OWNER,
        repo=Config.CODING_REPO,
        branch=Config.CODING_BRANCH,
        store_path=Config.CODING_STORE_PATH
    ),
    MinioUploader.name: MinioUploader(
        token=Config.MINIO_ACCESS_TOKEN,
        secret=Config.MINIO_SECRET,
        bucket=Config.MINIO_BUCKET,
        server=Config.MINIO_SERVER,
        alias_server=Config.MINIO_ALIAS_SERVER,
    ),
    G360Uploader.name: G360Uploader(),
    SouGouUploader.name: SouGouUploader(),
    BaiDuUploader.name: BaiDuUploader(),
    AliUploader.name: AliUploader(),
}

SUPPORT_UPLOAD_WAYS = [name.lower() for name in __UPLODER_MAPS__.keys()]
