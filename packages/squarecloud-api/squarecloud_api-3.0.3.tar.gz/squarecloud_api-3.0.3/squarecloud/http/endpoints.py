from __future__ import annotations

from typing import Dict, Any


class Endpoint:
    # ENDPOINTS_V1 = {
    #     'USER_ME': {'METHOD': 'GET', 'PATH': '/user'},
    #     'USER_INFO': {'METHOD': 'GET', 'PATH': '/user/{user_id}'},
    #     'APP_STATUS': {'METHOD': 'GET', 'PATH': '/status/{app_id}'},
    #     'LOGS': {'METHOD': 'GET', 'PATH': '/logs/{app_id}'},
    #     'FULL_LOGS': {'METHOD': 'GET', 'PATH': '/full-logs/{app_id}'},
    #     'START': {'METHOD': 'POST', 'PATH': '/start/{app_id}'},
    #     'STOP': {'METHOD': 'POST', 'PATH': '/stop/{app_id}'},
    #     'RESTART': {'METHOD': 'POST', 'PATH': '/restart/{app_id}'},
    #     'BACKUP': {'METHOD': 'GET', 'PATH': '/backup/{app_id}'},
    #     'COMMIT': {'METHOD': 'POST', 'PATH': '/commit/{app_id}'},
    #     'DELETE': {'METHOD': 'POST', 'PATH': '/delete/{app_id}'},
    #     'UPLOAD': {'METHOD': 'POST', 'PATH': '/upload'},
    # }

    ENDPOINTS_V2 = {
        'USER_ME': {'METHOD': 'GET', 'PATH': '/user'},
        'APP_DATA': {'METHOD': 'GET', 'PATH': '/apps/{app_id}'},
        'USER_INFO': {'METHOD': 'GET', 'PATH': '/user/{user_id}'},

        'APP_STATUS': {'METHOD': 'GET', 'PATH': '/apps/{app_id}/status'},
        'LOGS': {'METHOD': 'GET', 'PATH': '/apps/{app_id}/logs'},

        'START': {'METHOD': 'POST', 'PATH': '/apps/{app_id}/start'},
        'STOP': {'METHOD': 'POST', 'PATH': '/apps/{app_id}/stop'},
        'RESTART': {'METHOD': 'POST', 'PATH': '/apps/{app_id}/restart'},

        'BACKUP': {'METHOD': 'GET', 'PATH': '/apps/{app_id}/backup'},
        'COMMIT': {'METHOD': 'POST', 'PATH': '/apps/{app_id}/commit'},
        'DELETE_APP': {'METHOD': 'DELETE', 'PATH': '/apps/{app_id}/delete'},
        'UPLOAD_APP': {'METHOD': 'POST', 'PATH': '/apps/upload'},

        'STATISTICS': {'METHOD': 'GET', 'PATH': '/service/statistics'},
        'FILES_LIST': {'METHOD': 'GET',
                       'PATH': '/apps/{app_id}/files/list?path={path}'},
        'FILES_READ': {'METHOD': 'GET',
                       'PATH': '/apps/{app_id}/files/read?path={path}'},
        'FILES_CREATE': {'METHOD': 'POST',
                         'PATH': '/apps/{app_id}/files/create'},
        'FILES_DELETE': {'METHOD': 'DELETE',
                         'PATH': '/apps/{app_id}/files/delete?path={path}'}
    }

    def __init__(self, name: str):
        endpoint: Dict[str: Dict[str, Any]] = self.ENDPOINTS_V2[name]
        self.name: str = name
        self.method: str = endpoint['METHOD']
        self.path: str = endpoint['PATH']

    def __eq__(self, other: Endpoint):
        return isinstance(other, Endpoint) and self.name == other.name

    def __repr__(self):
        return f"{Endpoint.__name__}('{self.name}')"

    @classmethod
    def user_me(cls) -> Endpoint:
        return cls('USER_ME')

    @classmethod
    def app_data(cls) -> Endpoint:
        return cls('APP_DATA')

    @classmethod
    def user_info(cls) -> Endpoint:
        return cls('USER_INFO')

    @classmethod
    def app_status(cls) -> Endpoint:
        return cls('APP_STATUS')

    @classmethod
    def logs(cls) -> Endpoint:
        return cls('LOGS')

    @classmethod
    def start(cls) -> Endpoint:
        return cls('START')

    @classmethod
    def stop(cls) -> Endpoint:
        return cls('STOP')

    @classmethod
    def restart(cls) -> Endpoint:
        return cls('RESTART')

    @classmethod
    def backup(cls) -> Endpoint:
        return cls('BACKUP')

    @classmethod
    def commit(cls) -> Endpoint:
        return cls('COMMIT')

    @classmethod
    def delete_app(cls) -> Endpoint:
        return cls('DELETE_APP')

    @classmethod
    def upload(cls) -> Endpoint:
        return cls('UPLOAD_APP')

    @classmethod
    def files_list(cls) -> Endpoint:
        return cls('FILES_LIST')

    @classmethod
    def files_read(cls) -> Endpoint:
        return cls('FILES_READ')

    @classmethod
    def files_create(cls) -> Endpoint:
        return cls('FILES_CREATE')

    @classmethod
    def files_delete(cls) -> Endpoint:
        return cls('FILES_DELETE')

    @classmethod
    def statistics(cls) -> Endpoint:
        return cls('STATISTICS')


class Router:
    """Represents a route"""
    # BASE_V1: str = 'https://api.squarecloud.app/v1/public'
    BASE_V2: str = 'https://api.squarecloud.app/v2'

    # noinspection StrFormat
    def __init__(self, endpoint: Endpoint, **params) -> None:
        self.endpoint: Endpoint = endpoint
        self.method: str = endpoint.method
        self.path: str = endpoint.path
        url: str = self.BASE_V2 + self.path.format(**params)
        if params:
            url.format(params)
        self.url = url

    def __repr__(self):
        return f"{Router.__name__}(path='{self.path}', method='{self.method}')"
