# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import (Any, ClassVar, Dict, Tuple, Union)

from . import errors
from .api_types import APIType, convert_str_to_api_type
from .auth import build_auth_provider
from .response import EBResponse
from .types import (HeadersType)
from .utils import add_query_params

__all__ = ['build_backend']


def build_backend(config_dict: Dict[str, Any],
                  api_type: Union[str, APIType]) -> 'EBBackend':
    if isinstance(api_type, str):
        api_type = convert_str_to_api_type(api_type)
    if api_type == APIType.QIANFAN:
        return QianFanBackend(config_dict)
    elif api_type == APIType.YINIAN:
        return YiNianBackend(config_dict)
    else:
        raise ValueError(f"Unrecoginzed API type: {api_type.name}")


class EBBackend(object):
    API_TYPE: ClassVar[APIType]
    BASE_URL: ClassVar[str]

    def __init__(self, config_dict: Dict[str, Any]) -> None:
        super().__init__()
        self.api_type = self.API_TYPE
        self.base_url = config_dict.get('api_base_url', None) or self.BASE_URL
        auth_cfg = self._extract_auth_config(config_dict)
        self.auth = build_auth_provider(auth_cfg, self.api_type)

    def prepare_request(self, url: str, headers: HeadersType,
                        access_token: str) -> Tuple[str, HeadersType]:
        raise NotImplementedError

    def handle_response(self, resp: EBResponse) -> EBResponse:
        raise NotImplementedError

    def get_access_token(self) -> str:
        return self.auth.get_access_token()

    def update_access_token(self) -> str:
        return self.auth.update_access_token()

    def _extract_auth_config(self,
                             config_dict: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class QianFanBackend(EBBackend):
    API_TYPE: ClassVar[APIType] = APIType.QIANFAN
    BASE_URL: ClassVar[
        str] = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop"

    def prepare_request(self, url: str, headers: HeadersType,
                        access_token: str) -> Tuple[str, HeadersType]:
        return _prepare_request_bce(url, headers, access_token)

    def handle_response(self, resp: EBResponse) -> EBResponse:
        if 'error_code' in resp and 'error_msg' in resp:
            ecode = resp['error_code']
            emsg = resp['error_msg']
            if ecode == 2:
                raise errors.ServiceUnavailableError(emsg)
            elif ecode == 6:
                raise errors.PermissionError(emsg)
            elif ecode in (17, 18, 19):
                raise errors.RequestLimitError(emsg)
            elif ecode == 110:
                raise errors.InvalidTokenError(emsg)
            elif ecode == 111:
                raise errors.TokenExpiredError(emsg)
            elif ecode == 336003:
                raise errors.InvalidParameterError(emsg)
            elif ecode == 336100:
                raise errors.TryAgain(emsg)
            else:
                raise errors.APIError(emsg)
        else:
            return resp

    def _extract_auth_config(self,
                             config_dict: Dict[str, Any]) -> Dict[str, Any]:
        return _extract_bce_auth_config(config_dict)


class YiNianBackend(EBBackend):
    API_TYPE: ClassVar[APIType] = APIType.YINIAN
    BASE_URL: ClassVar[str] = "https://aip.baidubce.com/rpc/2.0/ernievilg/v1"

    def prepare_request(self, url: str, headers: HeadersType,
                        access_token: str) -> Tuple[str, HeadersType]:
        return _prepare_request_bce(url, headers, access_token)

    def handle_response(self, resp: EBResponse) -> EBResponse:
        if 'error_code' in resp and 'error_msg' in resp:
            ecode = resp['error_code']
            emsg = resp['error_msg']
            if ecode in (4, 13, 15, 17, 18):
                raise errors.RequestLimitError(emsg)
            elif ecode == 6:
                raise errors.PermissionError(emsg)
            elif ecode == 110:
                raise errors.InvalidTokenError(emsg)
            elif ecode == 111:
                raise errors.TokenExpiredError(emsg)
            elif ecode == 216100:
                raise errors.InvalidParameterError(emsg)
            else:
                raise errors.APIError(emsg)
        else:
            return resp

    def _extract_auth_config(self,
                             config_dict: Dict[str, Any]) -> Dict[str, Any]:
        return _extract_bce_auth_config(config_dict)


def _prepare_request_bce(url: str, headers: Dict[str, Any],
                         access_token: str) -> Tuple[str, HeadersType]:
    url = add_query_params(url, [('access_token', access_token)])
    return url, headers


def _extract_bce_auth_config(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    return dict(
        access_token=config_dict['access_token'],
        access_token_path=config_dict['access_token_path'],
        ak=config_dict['ak'],
        sk=config_dict['sk'])
