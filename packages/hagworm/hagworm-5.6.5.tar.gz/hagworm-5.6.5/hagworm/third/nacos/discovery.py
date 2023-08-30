# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from threading import Lock, Timer

from nacos import NacosClient, DEFAULT_GROUP_NAME
from nacos.listener import SubscribeListener

from ...extend.base import Utils
from ...extend.error import catch_error


class ServiceRegister:
    """服务发现注册
    """

    def __init__(
            self, server_addresses, *,
            endpoint=None, namespace=None,
            ak=None, sk=None, username=None, password=None,
            heartbeat_interval=5
    ):

        super().__init__()

        self._lock = Lock()

        self._client = NacosClient(
            server_addresses,
            endpoint=endpoint, namespace=namespace,
            ak=ak, sk=sk, username=username, password=password
        )

        self._heartbeat_timer = Timer(heartbeat_interval, self._send_heartbeat)
        self._heartbeat_params = {}

    def _send_heartbeat(self):

        with self._lock:
            if self._heartbeat_params:
                self._client.send_heartbeat(**self._heartbeat_params)

    def register(
            self, service_name, ip, port, *,
            cluster_name=None, weight=1.0, metadata=None,
            enable=True, healthy=True, ephemeral=True, group_name=DEFAULT_GROUP_NAME
    ):

        with self._lock:

            self._client.add_naming_instance(
                service_name, ip, port,
                cluster_name=cluster_name, weight=weight, metadata=metadata,
                enable=enable, healthy=healthy, ephemeral=ephemeral, group_name=group_name
            )

            self._heartbeat_params[r'service_name'] = service_name
            self._heartbeat_params[r'ip'] = ip
            self._heartbeat_params[r'port'] = port
            self._heartbeat_params[r'cluster_name'] = cluster_name
            self._heartbeat_params[r'weight'] = weight
            self._heartbeat_params[r'metadata'] = metadata
            self._heartbeat_params[r'ephemeral'] = ephemeral
            self._heartbeat_params[r'group_name'] = group_name

            self._heartbeat_timer.start()

    def deregister(self):

        with self._lock:

            params = {
                r'service_name': self._heartbeat_params[r'service_name'],
                r'ip': self._heartbeat_params[r'ip'],
                r'port': self._heartbeat_params[r'port'],
                r'cluster_name': self._heartbeat_params[r'cluster_name'],
                r'ephemeral': self._heartbeat_params[r'ephemeral'],
                r'group_name': self._heartbeat_params[r'group_name'],
            }

            self._client.remove_naming_instance(**params)

            self._heartbeat_timer.cancel()
            self._heartbeat_params.clear()


class ServiceQuery:
    """服务发现查询
    """

    def __init__(
            self, server_addresses, *,
            endpoint=None, namespace=None,
            ak=None, sk=None, username=None, password=None,
            listener_interval=5
    ):

        super().__init__()

        self._lock = Lock()
        self._hosts = []

        self._client = NacosClient(
            server_addresses,
            endpoint=endpoint, namespace=namespace,
            ak=ak, sk=sk, username=username, password=password
        )

        self._listener_interval = listener_interval
        self._listener_callback = SubscribeListener(self._update_naming_instance, r'listener_callback')
        self._listener_params = {}

    def _update_naming_instance(self, *_):

        with catch_error(), self._lock:

            resp = self._client.list_naming_instance(**self._listener_params)

            if resp[r'hosts']:
                self._hosts = resp[r'hosts']

            Utils.log.info(f'nacos instance update {self._hosts}')

    def start(self, service_name, *, clusters=None, namespace_id=None, group_name=None, healthy_only=True):

        self._listener_params[r'service_name'] = service_name
        self._listener_params[r'clusters'] = clusters
        self._listener_params[r'namespace_id'] = namespace_id
        self._listener_params[r'group_name'] = group_name
        self._listener_params[r'healthy_only'] = healthy_only

        self._client.subscribe(
            self._listener_callback, self._listener_interval,
            **self._listener_params
        )

        self._update_naming_instance()

    def stop(self):

        self._client.unsubscribe(
            self._listener_params[r'service_name']
        )

    def get_host(self):

        return Utils.randhit(self._hosts, lambda x: x[r'weight'])
