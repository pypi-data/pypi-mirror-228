# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import json
import yaml

from threading import Lock

from nacos import NacosClient, DEFAULT_GROUP_NAME

from ...extend.base import Utils
from ...extend.config import ConfigureBase


class Configure(ConfigureBase):
    """配置类
    """

    __slots__ = [r'_lock', r'_format', r'_client', r'_listener_callback', r'_listener_params']

    def __init__(
            self, server_addresses, *,
            endpoint=None, namespace=None,
            ak=None, sk=None, username=None, password=None
    ):

        super().__init__()

        self._lock = Lock()
        self._format = None

        self._client = NacosClient(
            server_addresses,
            endpoint=endpoint, namespace=namespace,
            ak=ak, sk=sk, username=username, password=password
        )

        self._listener_params = {}

    def _update_config(self, data=None):

        with self._lock:

            if data is None:
                raw_content = self._client.get_config(**self._listener_params)
            else:
                raw_content = data[r'raw_content']

            self._parser.clear()

            if self._format == r'text':
                self._parser.read_string(raw_content)
            elif self._format == r'json':
                self._parser.read_dict(json.loads(raw_content))
            elif self._format == r'yaml':
                self._parser.read_dict(yaml.load(raw_content, yaml.Loader))

            self._load_options()

        Utils.log.info(f'nacos config update {Utils.md5(raw_content)}')

    def _add_config_watcher(self, data_id, group, timeout, no_snapshot):

        self._listener_params[r'data_id'] = data_id
        self._listener_params[r'group'] = group
        self._listener_params[r'timeout'] = timeout
        self._listener_params[r'no_snapshot'] = no_snapshot

        self._client.add_config_watcher(
            self._listener_params[r'data_id'], self._listener_params[r'group'],
            self._update_config
        )

    def release(self):

        self._client.remove_config_watcher(
            self._listener_params[r'data_id'], self._listener_params[r'group'],
            self._update_config
        )

    def read(self, data_id, group=DEFAULT_GROUP_NAME, timeout=None, no_snapshot=None):

        self._format = r'text'
        self._add_config_watcher(data_id, group, timeout, no_snapshot)
        self._update_config()

    def read_json(self, data_id, group=DEFAULT_GROUP_NAME, timeout=None, no_snapshot=None):

        self._format = r'json'
        self._add_config_watcher(data_id, group, timeout, no_snapshot)
        self._update_config()

    def read_yaml(self, data_id, group=DEFAULT_GROUP_NAME, timeout=None, no_snapshot=None):

        self._format = r'yaml'
        self._add_config_watcher(data_id, group, timeout, no_snapshot)
        self._update_config()
