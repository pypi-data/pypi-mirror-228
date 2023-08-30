import os
from pathlib import Path, PosixPath
from typing import Optional

import pydantic

# support pydantic v1 (since as of 21/08/2023 thats what Chariot supports)
using_pydantic_v1 = pydantic.__version__[0] == "1"
if using_pydantic_v1:
    from pydantic import BaseSettings, ConfigDict, SecretStr
    from pydantic import validator as field_validator
else:
    from pydantic import ConfigDict, SecretStr, field_validator
    from pydantic_settings import BaseSettings


GENERATED_UIDS_PREFIX = ".generated_uids"


def storage_path_from_base_path(path: PosixPath) -> PosixPath:
    return path / "storage"


def generated_uids_path_from_base_path(path: PosixPath) -> PosixPath:
    return storage_path_from_base_path(path) / GENERATED_UIDS_PREFIX


base_path = Path(os.path.expanduser("~/.radops/"))


class Settings(BaseSettings):
    email: Optional[str] = None
    base_path: PosixPath = Path(base_path)
    mlflow_url: Optional[str] = None
    mlflow_username: Optional[str] = None
    mlflow_password: Optional[SecretStr] = None
    s3_endpoint_url: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[SecretStr] = None
    bucket_name: str = "radops"
    verbose: bool = True

    model_config = ConfigDict(env_file=base_path / ".env")

    @property
    def local_mode(self):
        return not bool(self.s3_endpoint_url)

    @field_validator("base_path")
    def validate_base_path(cls, v):
        # this is so we can accept strings
        v = Path(v)
        os.makedirs(storage_path_from_base_path(v), exist_ok=True)
        os.makedirs(generated_uids_path_from_base_path(v), exist_ok=True)
        return v

    @property
    def local_storage(self):
        return storage_path_from_base_path(self.base_path)

    @property
    def generated_uids_path(self):
        return generated_uids_path_from_base_path(self.base_path)

    @property
    def local_file_info(self) -> PosixPath:
        # used for storing file info and lineage locally in case there's
        # an issue syncing with s3
        return self.base_path / ".file_infos"

    if using_pydantic_v1:

        class Config:
            env_file: str = base_path / ".env"

        # in pydantic v2, dict got renamed to model_dump
        def model_dump(self):
            return self.dict()


settings = Settings()
