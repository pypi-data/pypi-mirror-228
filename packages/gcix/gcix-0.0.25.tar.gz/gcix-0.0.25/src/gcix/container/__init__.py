import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

from .. import Image as _Image_e46ac833


@jsii.data_type(
    jsii_type="@gcix/gcix.container.AWSRegistryProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "region": "region"},
)
class AWSRegistryProps:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: AWS account id. Default: AWSAccount.awsAccountId()
        :param region: AWS region where the ECR repository lives in. Default: AWSAccount.awsRegion()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70690165055af01ed6463f1d83e17300344a1a45d59ec7b9f16882e9308da882)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account id.

        :default: AWSAccount.awsAccountId()
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''AWS region where the ECR repository lives in.

        :default: AWSAccount.awsRegion()
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AWSRegistryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PredefinedImages(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.PredefinedImages",
):
    '''The PredefinedImages collection supplies commonly utilized container image objects within the gcix framework.'''

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALPINE_GIT")
    def ALPINE_GIT(cls) -> _Image_e46ac833:
        '''A predefined Alpine Git container image object.

        This image is useful for Git operations within containers.
        '''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "ALPINE_GIT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BUSYBOX")
    def BUSYBOX(cls) -> _Image_e46ac833:
        '''A predefined Busybox container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "BUSYBOX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRANE")
    def CRANE(cls) -> _Image_e46ac833:
        '''A predefined Crane container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "CRANE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DIVE")
    def DIVE(cls) -> _Image_e46ac833:
        '''A predefined Dive container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "DIVE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GCIP")
    def GCIP(cls) -> _Image_e46ac833:
        '''A predefined GCIP container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "GCIP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GCIX")
    def GCIX(cls) -> _Image_e46ac833:
        '''A predefined GCIX container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "GCIX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="KANIKO")
    def KANIKO(cls) -> _Image_e46ac833:
        '''A predefined Kaniko container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "KANIKO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRIVY")
    def TRIVY(cls) -> _Image_e46ac833:
        '''A predefined Trivy container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "TRIVY"))


class Registry(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.container.Registry"):
    '''Container registry urls constants.'''

    @jsii.member(jsii_name="aws")
    @builtins.classmethod
    def aws(
        cls,
        *,
        account_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Amazon Elastic Container Registry (ECR).

        If neither ``accountId`` nor ``region`` is given, the method attempts to
        evaluate ``accountId`` and ``region`` using helper functions from ``aws.AWSAccount``.
        If either of the helper functions does provide a valid value, a ``ValueError`` or ``KeyError`` exception will be raised.

        :param account_id: AWS account id. Default: AWSAccount.awsAccountId()
        :param region: AWS region where the ECR repository lives in. Default: AWSAccount.awsRegion()

        :return:

        Elastic Container Registry URL in the format of
        **${awsAccountId}.dkr.ecr.${region}.amazonaws.com**.

        :throws: {Error} If no region was found in ``aws.AWSAccount.awsRegion()``.
        '''
        props = AWSRegistryProps(account_id=account_id, region=region)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "aws", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOCKER")
    def DOCKER(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "DOCKER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GCR")
    def GCR(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "GCR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="QUAY")
    def QUAY(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "QUAY"))


__all__ = [
    "AWSRegistryProps",
    "PredefinedImages",
    "Registry",
]

publication.publish()

def _typecheckingstub__70690165055af01ed6463f1d83e17300344a1a45d59ec7b9f16882e9308da882(
    *,
    account_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
