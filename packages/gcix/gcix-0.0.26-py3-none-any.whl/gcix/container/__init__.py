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


@jsii.data_type(
    jsii_type="@gcix/gcix.container.DockerClientConfigProps",
    jsii_struct_bases=[],
    name_mapping={"config_file_path": "configFilePath"},
)
class DockerClientConfigProps:
    def __init__(
        self,
        *,
        config_file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_file_path: Docker client config path. Default: $HOME/.docker/config.json
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206d2b583e918e93a1ff212d6af4cd76afeb3ac91bd0bf5e2193df801f76b70d)
            check_type(argname="argument config_file_path", value=config_file_path, expected_type=type_hints["config_file_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_file_path is not None:
            self._values["config_file_path"] = config_file_path

    @builtins.property
    def config_file_path(self) -> typing.Optional[builtins.str]:
        '''Docker client config path.

        :default: $HOME/.docker/config.json
        '''
        result = self._values.get("config_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerClientConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.container.IDockerClientConfig")
class IDockerClientConfig(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "IDockerClientConfigType":
        '''Docker client configuration.'''
        ...

    @config.setter
    def config(self, value: "IDockerClientConfigType") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        '''Docker client config path.

        :default: $HOME/.docker/config.json
        '''
        ...

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        ...


class _IDockerClientConfigProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDockerClientConfig"

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "IDockerClientConfigType":
        '''Docker client configuration.'''
        return typing.cast("IDockerClientConfigType", jsii.get(self, "config"))

    @config.setter
    def config(self, value: "IDockerClientConfigType") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e083816c6ae221d335e5ff8ce0e91aa7f1e31492a64baf65024fe45cd17037fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        '''Docker client config path.

        :default: $HOME/.docker/config.json
        '''
        return typing.cast(builtins.str, jsii.get(self, "configFilePath"))

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7a975cf87bb5d079e0e97120574ec688b6767aedfbaacb31d43ca74d1e4788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFilePath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerClientConfig).__jsii_proxy_class__ = lambda : _IDockerClientConfigProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IDockerClientConfigType")
class IDockerClientConfigType(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="auths")
    def auths(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        ...

    @auths.setter
    def auths(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="credHelpers")
    def cred_helpers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @cred_helpers.setter
    def cred_helpers(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="credsStore")
    def creds_store(self) -> typing.Optional[builtins.str]:
        ...

    @creds_store.setter
    def creds_store(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rawInput")
    def raw_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @raw_input.setter
    def raw_input(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _IDockerClientConfigTypeProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDockerClientConfigType"

    @builtins.property
    @jsii.member(jsii_name="auths")
    def auths(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "auths"))

    @auths.setter
    def auths(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c06e68bf27701f47e2c6385823c047b7c48641502ed2b70c2e6cb00bf4ff745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auths", value)

    @builtins.property
    @jsii.member(jsii_name="credHelpers")
    def cred_helpers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "credHelpers"))

    @cred_helpers.setter
    def cred_helpers(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbecbff16e0ecee4e2f306a4eaf894e4c91614f6ff695a7a129b9ea08b16ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credHelpers", value)

    @builtins.property
    @jsii.member(jsii_name="credsStore")
    def creds_store(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credsStore"))

    @creds_store.setter
    def creds_store(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82864bc1bc4d58efa2a54428508f6ebc1c52cfd22adf629cbd02e1c714987e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credsStore", value)

    @builtins.property
    @jsii.member(jsii_name="rawInput")
    def raw_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "rawInput"))

    @raw_input.setter
    def raw_input(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f757d69a2d460924dab774a4f874fe7a6bcc483a62e890ea65eaa6e060088dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawInput", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerClientConfigType).__jsii_proxy_class__ = lambda : _IDockerClientConfigTypeProxy


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


@jsii.implements(IDockerClientConfig)
class DockerClientConfig(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.DockerClientConfig",
):
    '''Class which represents a docker client configuration.

    After creating an instance of this class you can add new credential helper,
    basic authentication settings or default credential store.
    '''

    def __init__(
        self,
        *,
        config_file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_file_path: Docker client config path. Default: $HOME/.docker/config.json
        '''
        props = DockerClientConfigProps(config_file_path=config_file_path)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addAuth")
    def add_auth(
        self,
        registry: builtins.str,
        username_env_var: typing.Optional[builtins.str] = None,
        password_env_var: typing.Optional[builtins.str] = None,
    ) -> "DockerClientConfig":
        '''Adds basic authentication ``auths`` setting to the configuration.

        This method acts a little special, because of some security aspects.
        The method, takse three arguments, ``registry``, ``username_env_var`` and ``password_env_var``.
        Arguments ending wit *_env_var, are ment to be available as a ``gcip.Job`` variable.

        :param registry: Name of the container registry to set ``creds_helper`` for.
        :param username_env_var: Name of the environment variable which as the registry username stored.
        :param password_env_var: Name of the environment variable which as the registry password stored.

        :default: REGISTRY_PASSWORD
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a16b4dbc6af5a7a4ba47b59ec2cb53f8fb6ed6b5c3898839e49ed85d425ea61)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument username_env_var", value=username_env_var, expected_type=type_hints["username_env_var"])
            check_type(argname="argument password_env_var", value=password_env_var, expected_type=type_hints["password_env_var"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "addAuth", [registry, username_env_var, password_env_var]))

    @jsii.member(jsii_name="addCredHelper")
    def add_cred_helper(
        self,
        registry: builtins.str,
        cred_helper: builtins.str,
    ) -> "DockerClientConfig":
        '''Adds a Credentials helper ``credHelpers`` for a registry.

        See `docker login#credential-helpers <https://docs.docker.com/engine/reference/commandline/login/#credential-helpers>`_

        :param registry: Name of the container registry to set ``creds_helper`` for.
        :param cred_helper: Name of the credential helper to use together with the ``registry``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfca338a2c1a05056f09278d2f0db7b0ce9db5c5286249628fdd525526c4db40)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument cred_helper", value=cred_helper, expected_type=type_hints["cred_helper"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "addCredHelper", [registry, cred_helper]))

    @jsii.member(jsii_name="addRaw")
    def add_raw(
        self,
        raw_input: typing.Mapping[builtins.str, typing.Any],
    ) -> "DockerClientConfig":
        '''Adds arbitrary settings to configuration.

        Be aware and warned! You can overwrite any predefined settings with this method.
        This method is intendet to be used, if non suitable method is available and you
        have to set a configuration setting.

        :param raw_input: Dictionary of non-available settings to be set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135e6468f74e369fb5865e1eab067d96d6111ef919e2616630228a8d67e6568f)
            check_type(argname="argument raw_input", value=raw_input, expected_type=type_hints["raw_input"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "addRaw", [raw_input]))

    @jsii.member(jsii_name="assignCredsStore")
    def assign_creds_store(self, creds_store: builtins.str) -> "DockerClientConfig":
        '''Sets the ``credsStore`` setting for clients. See `docker login#credentials-store <https://docs.docker.com/engine/reference/commandline/login/#credentials-store>`_.

        Be aware, that if you set the ``credsStore`` and add creds_helper or
        username and password authentication, those authentication methods
        are not used.

        Clients which can authenticate against a registry can handle the credential
        store itself, mostly you do not want to set the ``credsStore``.
        Use ``credsHelpers`` instead.

        :param creds_store: Should be the suffix of the program to use (i.e. everything after docker-credential-). ``osxkeychain``, to use docker-credential-osxkeychain or ``ecr-login``, to use docker-crendential-ecr-login.

        :return: DockerClientConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfa1b99ea08ac61e5f6cae6f49e0cfd6be19103a30962e4a55d362648a7c6ad)
            check_type(argname="argument creds_store", value=creds_store, expected_type=type_hints["creds_store"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "assignCredsStore", [creds_store]))

    @jsii.member(jsii_name="shellCommand")
    def shell_command(self) -> typing.List[builtins.str]:
        '''Renders the shell command for creating the docker client config.

        The render method uses ``json.dumps()`` to dump the configuration as a json
        string and escapes it for the shell. In Jobs which needed the
        configuration the rendered output should be redirected to the appropriate
        destination e.g. ~/.docker/config.json. This ensures, that environment
        variables are substituted.

        :return:

        Returns a list with ``mkdir -p config_file_path`` and a shell escaped JSON string
        echoed to ``config_file_path``/``config_file_name``
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "shellCommand", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> IDockerClientConfigType:
        '''Docker client configuration.'''
        return typing.cast(IDockerClientConfigType, jsii.get(self, "config"))

    @config.setter
    def config(self, value: IDockerClientConfigType) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956c622101e4f8531772774959f890318bfeac5a399ea3bd389ef92cdbd4fa4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        '''Docker client config path.'''
        return typing.cast(builtins.str, jsii.get(self, "configFilePath"))

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed52c1fe7e09eedf49e79aea025fe55bde8cc4141e6dbcb7aa1eb47b6c5c261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFilePath", value)


__all__ = [
    "AWSRegistryProps",
    "DockerClientConfig",
    "DockerClientConfigProps",
    "IDockerClientConfig",
    "IDockerClientConfigType",
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

def _typecheckingstub__206d2b583e918e93a1ff212d6af4cd76afeb3ac91bd0bf5e2193df801f76b70d(
    *,
    config_file_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e083816c6ae221d335e5ff8ce0e91aa7f1e31492a64baf65024fe45cd17037fd(
    value: IDockerClientConfigType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7a975cf87bb5d079e0e97120574ec688b6767aedfbaacb31d43ca74d1e4788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c06e68bf27701f47e2c6385823c047b7c48641502ed2b70c2e6cb00bf4ff745(
    value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbecbff16e0ecee4e2f306a4eaf894e4c91614f6ff695a7a129b9ea08b16ed3(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82864bc1bc4d58efa2a54428508f6ebc1c52cfd22adf629cbd02e1c714987e18(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f757d69a2d460924dab774a4f874fe7a6bcc483a62e890ea65eaa6e060088dfe(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a16b4dbc6af5a7a4ba47b59ec2cb53f8fb6ed6b5c3898839e49ed85d425ea61(
    registry: builtins.str,
    username_env_var: typing.Optional[builtins.str] = None,
    password_env_var: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfca338a2c1a05056f09278d2f0db7b0ce9db5c5286249628fdd525526c4db40(
    registry: builtins.str,
    cred_helper: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135e6468f74e369fb5865e1eab067d96d6111ef919e2616630228a8d67e6568f(
    raw_input: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfa1b99ea08ac61e5f6cae6f49e0cfd6be19103a30962e4a55d362648a7c6ad(
    creds_store: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956c622101e4f8531772774959f890318bfeac5a399ea3bd389ef92cdbd4fa4c(
    value: IDockerClientConfigType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed52c1fe7e09eedf49e79aea025fe55bde8cc4141e6dbcb7aa1eb47b6c5c261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
