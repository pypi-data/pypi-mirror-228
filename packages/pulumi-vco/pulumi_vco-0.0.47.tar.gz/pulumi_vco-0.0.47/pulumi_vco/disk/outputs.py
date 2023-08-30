# coding=utf-8
# *** WARNING: this file was generated by pulumi. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'Endpoint',
]

@pulumi.output_type
class Endpoint(dict):
    def __init__(__self__, *,
                 address: str,
                 name: str,
                 port: int,
                 private_address: str,
                 private_port: int,
                 psk: str,
                 user: str):
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "private_address", private_address)
        pulumi.set(__self__, "private_port", private_port)
        pulumi.set(__self__, "psk", psk)
        pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter
    def address(self) -> str:
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> int:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def private_address(self) -> str:
        return pulumi.get(self, "private_address")

    @property
    @pulumi.getter
    def private_port(self) -> int:
        return pulumi.get(self, "private_port")

    @property
    @pulumi.getter
    def psk(self) -> str:
        return pulumi.get(self, "psk")

    @property
    @pulumi.getter
    def user(self) -> str:
        return pulumi.get(self, "user")


