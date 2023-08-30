import json

from typing import List

import requests

import config as cfg

"""
USAGE:
First you have to init factory with base settings
factory = RequestFactory(stage=${STAGE}, version=${VERSION}, api_key=${API_KEY})

Then need to create request instance depend on the type of the request you want to send
metrics_request = factory.create_request("Metrics")

Pass the data to set_data function
metrics_request.set_data(
    agent_version,
    overview,
    plugins
)

Then send it to the BackEnd and receive the response
response = metrics_request.send()
"""

DEFAULT_BASE_URL = "https://api{}.cloudvisor.io"
ESTABLISH_CONN_TIMEOUT = 10
RECEIVE_RESPONSE_TIMEOUT = 30


class RequestFactory:
    requests = {}
    stage = None
    version = None
    api_key = None
    api_base = None

    def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
        self.stage = stage
        self.version = version
        self.api_key = api_key
        self.api_base = api_base

    def create_request(self, request_type):
        if request_type not in RequestFactory.requests:
            request_class = Request.subclasses.get(request_type)
            if request_class:
                RequestFactory.requests[request_type] = request_class.Factory(self.stage, self.version, self.api_key,
                                                                              self.api_base)
        return RequestFactory.requests[request_type].create()


class Request:
    stage = None
    version = None
    api_key = None
    prefix = None
    api_base = None
    api_is_private_endpoint = False
    subclasses = {}

    def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
        self.stage = stage
        self.version = version
        self.api_key = api_key
        self.prefix = ""
        if self.stage == 'staging':
            self.prefix = "-staging"
        if api_base != DEFAULT_BASE_URL:
            self.api_is_private_endpoint = True

        self.api_base = api_base.format(self.prefix)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls

    def send(self):
        res = requests.post(
            self.build_url(),
            data=json.dumps(self.message, separators=(',', ':')),
            headers={"Cache-Control": "no-cache", "Pragma": "no-cache", "x-api-key": self.api_key},
            timeout=(ESTABLISH_CONN_TIMEOUT, RECEIVE_RESPONSE_TIMEOUT)
        )
        return self.Response(res)


class Metrics(Request):
    message = {}

    def build_url(self):
        if self.api_is_private_endpoint:
            return '{}{}'.format(self.api_base, "/post-metrics")
        else:
            return '{}{}'.format(self.api_base, cfg.post_metrics_ep)

    def set_data(self, agent_version, overview, plugins, package_version=None, autoupdate_last_execution_time=None):
        self.message = {
            "agent": {
                "version": agent_version,
                "package_version": package_version,
                "autoupdate_last_execution_time": autoupdate_last_execution_time
            },
            "overview": overview,
            "plugins": plugins
        }

    class Response:
        raw_data: dict = None
        status_code = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            for k, v in self.raw_data.items():
                setattr(self, str(k), v)

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return Metrics(stage=self.stage, version=self.version, api_key=self.api_key,
                                         api_base=self.api_base)


class MetricsCollection(Request):
    message: List[dict] = []

    def build_url(self):
        if self.api_is_private_endpoint:
            return f'{self.api_base}/bulk-post-metrics'
        else:
            return f'{self.api_base}{cfg.bulk_post_metrics_ep}'

    def set_data(self, metrics: dict):
        self.message.append(metrics)

    def clear(self):
        self.message = []

    class Response:
        raw_data: dict = None
        status_code = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            for k, v in self.raw_data.items():
                setattr(self, str(k), v)

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return MetricsCollection(stage=self.stage, version=self.version, api_key=self.api_key,
                                                   api_base=self.api_base)


class NotifyException(Request):
    message = {}

    def build_url(self):
        if self.api_is_private_endpoint:
            return '{}{}'.format(self.api_base, "/post-notify-exception")
        else:
            return '{}{}'.format(self.api_base, cfg.notify_exception_ep)

    def set_data(self, account_id, instance_id, exception, msg):
        self.message = {
            "exception": exception,
            "message": msg,
            "instance_id": instance_id,
            "account_id": account_id
        }

    class Response:
        raw_data = None
        status_code = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            for k, v in self.raw_data.items():
                setattr(self, str(k), v)

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return NotifyException(stage=self.stage, version=self.version, api_key=self.api_key,
                                                 api_base=self.api_base)


class FsResizeCompleted(Request):
    message = {}

    def build_url(self):
        if self.api_is_private_endpoint:
            return '{}{}'.format(self.api_base, "/post-delete-resize-item")
        else:
            return '{}{}'.format(self.api_base, cfg.fs_resize_completed_ep)

    def set_data(self, dev_path, filesystems, action_id, exit_code, resize_output, account_id):
        self.message = {
            "dev_path": dev_path,
            "filesystems": filesystems,
            "action_id": action_id,
            "exit_code": exit_code,
            "resize_output": resize_output,
            "account_id": account_id
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return FsResizeCompleted(stage=self.stage, version=self.version, api_key=self.api_key,
                                                   api_base=self.api_base)


class HoldingRemoveAction(Request):
    message = {}

    def build_url(self):
        return '{}{}'.format(self.api_base, cfg.hold_remove_action_ep)

    def set_data(self, dev_path, filesystems, action_id, exit_code, index, account_id):
        self.message = {
            "dev_path": dev_path,
            "filesystems": filesystems,
            "action_id": action_id,
            "exit_code": exit_code,
            "index": index,
            "account_id": account_id
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return HoldingRemoveAction(stage=self.stage, version=self.version, api_key=self.api_key,
                                                     api_base=self.api_base)


class FsResizeFailed(Request):
    message = {}

    def build_url(self):
        if self.api_is_private_endpoint:
            return '{}{}'.format(self.api_base, "/post-fs-resize-failed")
        else:
            return '{}{}'.format(self.api_base, cfg.resize_failed_ep)

    def set_data(self, dev_path, filesystems, action_id, exit_code, resize_output, error, resize_steps, account_id):
        self.message = {
            "dev_path": dev_path,
            "filesystems": filesystems,
            "action_id": action_id,
            "exit_code": exit_code,
            "resize_output": resize_output,
            "error": error,
            "resize_steps": resize_steps,
            "account_id": account_id
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return FsResizeFailed(stage=self.stage, version=self.version, api_key=self.api_key,
                                                api_base=self.api_base)


class SyncMachineActions(Request):
    message = {}

    def build_url(self):
        if self.api_is_private_endpoint:
            return '{}{}'.format(self.api_base, "/post-sync-machine-actions")
        else:
            return '{}{}'.format(self.api_base, cfg.sync_machine_actions_ep)

    def set_data(self, action_id, account_id, status, fs_id):
        self.message = {
            'account_id': account_id,
            'actions': {
                action_id: {
                    'fs_id': fs_id,
                    'instruction_status': status
                }
            }
        }

    def add_data(self, action_id, status, fs_id):
        self.message['actions'][action_id] = {
            'fs_id': fs_id,
            'instruction_status': status
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return SyncMachineActions(stage=self.stage, version=self.version, api_key=self.api_key,
                                                    api_base=self.api_base)


class MigrationStartActionCompleted(Request):
    message = {}

    def build_url(self):
        if self.api_is_private_endpoint:
            return '{}{}'.format(self.api_base, "/post-migration-start-action-complete")
        else:
            return '{}{}'.format(self.api_base, cfg.migration_start_action_completed_ep)

    def set_data(self, account_id, fs_id, action_id, mount_path, volume_id, region, cloud_vendor, dev_path, exit_code,
                 error):
        self.message = {
            "account_id": account_id,
            "fs_id": fs_id,
            "action_id": action_id,
            "mount_path": mount_path,
            "volume_id": volume_id,
            "region": region,
            "cloud_vendor": cloud_vendor,
            "dev_path": dev_path,
            "exit_code": exit_code,
            "error": error
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None
        api_base = None

        def __init__(self, stage, version, api_key, api_base: str = DEFAULT_BASE_URL):
            self.stage = stage
            self.version = version
            self.api_key = api_key
            self.api_base = api_base

        def create(self): return MigrationStartActionCompleted(stage=self.stage, version=self.version,
                                                               api_key=self.api_key,
                                                               api_base=self.api_base)
