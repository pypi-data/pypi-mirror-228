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

from .. import Image as _Image_e46ac833, Job as _Job_20682b42


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
    jsii_type="@gcix/gcix.container.CopyProps",
    jsii_struct_bases=[],
    name_mapping={
        "dst_registry": "dstRegistry",
        "src_registry": "srcRegistry",
        "docker_client_config": "dockerClientConfig",
        "job_name": "jobName",
        "job_stage": "jobStage",
    },
)
class CopyProps:
    def __init__(
        self,
        *,
        dst_registry: builtins.str,
        src_registry: builtins.str,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param src_registry: Registry URL to copy container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79dfc53ffb33d972906763ce66cbbf69cccef3dc1f49ee46ad6fbd1d24e7cc19)
            check_type(argname="argument dst_registry", value=dst_registry, expected_type=type_hints["dst_registry"])
            check_type(argname="argument src_registry", value=src_registry, expected_type=type_hints["src_registry"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dst_registry": dst_registry,
            "src_registry": src_registry,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        result = self._values.get("dst_registry")
        assert result is not None, "Required property 'dst_registry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def src_registry(self) -> builtins.str:
        '''Registry URL to copy container image from.'''
        result = self._values.get("src_registry")
        assert result is not None, "Required property 'src_registry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CopyProps(%s)" % ", ".join(
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


@jsii.interface(jsii_type="@gcix/gcix.container.ICopy")
class ICopy(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        ...

    @dst_registry.setter
    def dst_registry(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> builtins.str:
        '''Registry URL to copy container image from.'''
        ...

    @src_registry.setter
    def src_registry(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        ...

    @docker_client_config.setter
    def docker_client_config(
        self,
        value: typing.Optional["DockerClientConfig"],
    ) -> None:
        ...


class _ICopyProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ICopy"

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        return typing.cast(builtins.str, jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094a4dbb1d3fcbf4743380bead1924c35b025946e239f396696bd2de9df999d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> builtins.str:
        '''Registry URL to copy container image from.'''
        return typing.cast(builtins.str, jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fda02f19e64059e5af6e39d4432d853e4a7215929e898f33aa17564f8e65108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        return typing.cast(typing.Optional["DockerClientConfig"], jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(
        self,
        value: typing.Optional["DockerClientConfig"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5b70a7e0bc81a640fd8095ef81182ce78417a4c5f3e7668c006b0dfef79b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICopy).__jsii_proxy_class__ = lambda : _ICopyProxy


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


@jsii.interface(jsii_type="@gcix/gcix.container.IPull")
class IPull(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image with namespace to pull from ``srcRegistry``.

        :default: PredefinedVariables.ciProjectName
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Tag of the image which will be pulled.

        :default: latest
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        ...

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to save the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        ...

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        ...


class _IPullProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IPull"

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab5f87242acaeda4ee45aeba6663f1841c3412f530586d65cc3d4ed89d4ef4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image with namespace to pull from ``srcRegistry``.

        :default: PredefinedVariables.ciProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734046bbba94c93ba2488d8b166c515d26bc5d2edd04d28fe087ad1872ea1c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Tag of the image which will be pulled.

        :default: latest
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1440ae87a9e5ea5595051c16abad92350b8e0450c8dfc3d1488f4585a7c10052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4aed9c47351f4535384bbcf5f5c8274e11ad3276d27fe62b43b76a80388aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to save the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ceb165805b79d48198a9b7d4c8a53631128f57c0b1b90e225f65b8931231040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPull).__jsii_proxy_class__ = lambda : _IPullProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IPush")
class IPush(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        ...

    @dst_registry.setter
    def dst_registry(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.ciProjectName
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to find the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        ...

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        ...


class _IPushProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IPush"

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3948caac927488c9a71534b3ce1f0ff58fdd9c5e9f18bdb8aeb2e239b7d33bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        return typing.cast(builtins.str, jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4c44b74992f3fa92ddb0684e7fcf226bb8aa2ca31ceef5fe5961cb4b7a4844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.ciProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3340f57b2b3a477a2bb9b4fa6455bb2c4983cf12d0e7608904e2890b902f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb71df34b735665b6e1abea166f3e685430e2457eaa97213b97611634d1e0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to find the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58508d46ad7648806cdec25d5d56449a01dd3ee1fd0001475781812275975cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPush).__jsii_proxy_class__ = lambda : _IPushProxy


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


@jsii.implements(IPull)
class Pull(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.Pull",
):
    '''Creates a job to pull container image from remote container registry with ``crane``.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: crane
    - stage: pull
    - image: PredefinedImages.CRANE
    '''

    def __init__(
        self,
        *,
        src_registry: typing.Union[builtins.str, "Registry"],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param src_registry: Registry URL to pull container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image with namespace to pull from ``srcRegistry``. Default: PredefinedVariables.ciProjectName
        :param image_tag: Tag of the image which will be pulled. Default: latest
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to save the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        props = PullProps(
            src_registry=src_registry,
            docker_client_config=docker_client_config,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            tar_path=tar_path,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.'''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0dfdd8d7d1f21a47b088fc181e88fe7634ca0a32314ec25673fefe5079e666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image with namespace to pull from ``srcRegistry``.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d11e56ee7f6c622da64df5cd13db12e43815c67dfc94c6261e7e1cb9694c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Tag of the image which will be pulled.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec58b6d3a9cc602c65706d3e1a30dd7ba1b194ea9e43e50097d2a5aed6b498ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59f669d08c743b56d3fc9dad89c3d1fcd69e1a3e8565e19be5707e93a7bdf9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to save the container image tarball.'''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fe16da62715039f737b178e50403126bfa7834b73c6aa27151b3e0879055d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.container.PullProps",
    jsii_struct_bases=[],
    name_mapping={
        "src_registry": "srcRegistry",
        "docker_client_config": "dockerClientConfig",
        "image_name": "imageName",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "tar_path": "tarPath",
    },
)
class PullProps:
    def __init__(
        self,
        *,
        src_registry: typing.Union[builtins.str, "Registry"],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param src_registry: Registry URL to pull container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image with namespace to pull from ``srcRegistry``. Default: PredefinedVariables.ciProjectName
        :param image_tag: Tag of the image which will be pulled. Default: latest
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to save the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5222120e26f748590221a7a7cc1f385da0c0b77e49e8cd25bcaecfacfcaef0)
            check_type(argname="argument src_registry", value=src_registry, expected_type=type_hints["src_registry"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument tar_path", value=tar_path, expected_type=type_hints["tar_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "src_registry": src_registry,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if tar_path is not None:
            self._values["tar_path"] = tar_path

    @builtins.property
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        result = self._values.get("src_registry")
        assert result is not None, "Required property 'src_registry' is missing"
        return typing.cast(typing.Union[builtins.str, "Registry"], result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Container image with namespace to pull from ``srcRegistry``.

        :default: PredefinedVariables.ciProjectName
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''Tag of the image which will be pulled.

        :default: latest
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Path where to save the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        result = self._values.get("tar_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPush)
class Push(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.Push",
):
    '''Creates a job to push container image to remote container registry with ``crane``.

    The image to copy must be in a ``tarball`` format. It gets validated with crane
    and is pushed to ``dst_registry`` destination registry.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: crane-push
    - stage: deploy
    - image: PredefinedImages.CRANE
    '''

    def __init__(
        self,
        *,
        dst_registry: builtins.str,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Defaults to a ``DockerClientConfig`` with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image name, searched for in ``imagePath`` and gets ``.tar`` appended. Default: PredefinedVariables.ciProjectName
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.ciCommitTag
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to find the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        props = PushProps(
            dst_registry=dst_registry,
            docker_client_config=docker_client_config,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            tar_path=tar_path,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16a69af2ba271c8099bd0ebb30498beb19ac80610553cfc7610129ca56b068c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        return typing.cast(builtins.str, jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327788cd9de6001c0c0fca1902099fda0d9c0cffa65767956f4315132489ed1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be2f0adaecbc1d64e5b339e84bba19d99bc6ac6fea16166d4c3d2e14647aee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b845b109484654fe12f8dcb1940b55b559d55cee03d629f40812397be0ac5484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to find the container image tarball.'''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec310c70e10c33e42f17e1e74d5aee55a7c30c8e2ead1c51802e2fd9f1152909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.container.PushProps",
    jsii_struct_bases=[],
    name_mapping={
        "dst_registry": "dstRegistry",
        "docker_client_config": "dockerClientConfig",
        "image_name": "imageName",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "tar_path": "tarPath",
    },
)
class PushProps:
    def __init__(
        self,
        *,
        dst_registry: builtins.str,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Defaults to a ``DockerClientConfig`` with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image name, searched for in ``imagePath`` and gets ``.tar`` appended. Default: PredefinedVariables.ciProjectName
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.ciCommitTag
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to find the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7454b680b0214713763c9c3f54d7ff3d70e7e0c8271b8dc6f00385f113f340f)
            check_type(argname="argument dst_registry", value=dst_registry, expected_type=type_hints["dst_registry"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument tar_path", value=tar_path, expected_type=type_hints["tar_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dst_registry": dst_registry,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if tar_path is not None:
            self._values["tar_path"] = tar_path

    @builtins.property
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        result = self._values.get("dst_registry")
        assert result is not None, "Required property 'dst_registry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.ciProjectName
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Path where to find the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        result = self._values.get("tar_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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


@jsii.implements(ICopy)
class Copy(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.Copy",
):
    '''Creates a job to copy container images with ``crane``. See ```crane`` <https://github.com/google/go-containerregistry/tree/main/cmd/crane>`_.

    Copying an image is useful, if you want to have container images as close
    as possible to your cluster or servers.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: crane-copy
    - stage: deploy
    - image: PredefinedImages.CRANE
    '''

    def __init__(
        self,
        *,
        dst_registry: builtins.str,
        src_registry: builtins.str,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param src_registry: Registry URL to copy container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        '''
        props = CopyProps(
            dst_registry=dst_registry,
            src_registry=src_registry,
            docker_client_config=docker_client_config,
            job_name=job_name,
            job_stage=job_stage,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> builtins.str:
        '''Registry URL to copy container image to.'''
        return typing.cast(builtins.str, jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542039b10d6041ca9af47159ce1b0b1ed5bff4959f5a21137bdfd24a1cf0e547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> builtins.str:
        '''Registry URL to copy container image from.'''
        return typing.cast(builtins.str, jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c665c50a22aac442f9192e31318606a0e7d23600e9fd4b8fd071a058670be235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        return typing.cast(typing.Optional["DockerClientConfig"], jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(
        self,
        value: typing.Optional["DockerClientConfig"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0854011841cf9698e8e4f970d73c9a912381179e4f515435ab05f471e9911788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)


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
    "Copy",
    "CopyProps",
    "DockerClientConfig",
    "DockerClientConfigProps",
    "ICopy",
    "IDockerClientConfig",
    "IDockerClientConfigType",
    "IPull",
    "IPush",
    "PredefinedImages",
    "Pull",
    "PullProps",
    "Push",
    "PushProps",
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

def _typecheckingstub__79dfc53ffb33d972906763ce66cbbf69cccef3dc1f49ee46ad6fbd1d24e7cc19(
    *,
    dst_registry: builtins.str,
    src_registry: builtins.str,
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206d2b583e918e93a1ff212d6af4cd76afeb3ac91bd0bf5e2193df801f76b70d(
    *,
    config_file_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094a4dbb1d3fcbf4743380bead1924c35b025946e239f396696bd2de9df999d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fda02f19e64059e5af6e39d4432d853e4a7215929e898f33aa17564f8e65108(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5b70a7e0bc81a640fd8095ef81182ce78417a4c5f3e7668c006b0dfef79b9a(
    value: typing.Optional[DockerClientConfig],
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

def _typecheckingstub__9ab5f87242acaeda4ee45aeba6663f1841c3412f530586d65cc3d4ed89d4ef4d(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734046bbba94c93ba2488d8b166c515d26bc5d2edd04d28fe087ad1872ea1c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1440ae87a9e5ea5595051c16abad92350b8e0450c8dfc3d1488f4585a7c10052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4aed9c47351f4535384bbcf5f5c8274e11ad3276d27fe62b43b76a80388aa0(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ceb165805b79d48198a9b7d4c8a53631128f57c0b1b90e225f65b8931231040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3948caac927488c9a71534b3ce1f0ff58fdd9c5e9f18bdb8aeb2e239b7d33bb(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4c44b74992f3fa92ddb0684e7fcf226bb8aa2ca31ceef5fe5961cb4b7a4844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3340f57b2b3a477a2bb9b4fa6455bb2c4983cf12d0e7608904e2890b902f19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb71df34b735665b6e1abea166f3e685430e2457eaa97213b97611634d1e0a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58508d46ad7648806cdec25d5d56449a01dd3ee1fd0001475781812275975cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0dfdd8d7d1f21a47b088fc181e88fe7634ca0a32314ec25673fefe5079e666(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d11e56ee7f6c622da64df5cd13db12e43815c67dfc94c6261e7e1cb9694c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec58b6d3a9cc602c65706d3e1a30dd7ba1b194ea9e43e50097d2a5aed6b498ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59f669d08c743b56d3fc9dad89c3d1fcd69e1a3e8565e19be5707e93a7bdf9a(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fe16da62715039f737b178e50403126bfa7834b73c6aa27151b3e0879055d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5222120e26f748590221a7a7cc1f385da0c0b77e49e8cd25bcaecfacfcaef0(
    *,
    src_registry: typing.Union[builtins.str, Registry],
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    tar_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16a69af2ba271c8099bd0ebb30498beb19ac80610553cfc7610129ca56b068c(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327788cd9de6001c0c0fca1902099fda0d9c0cffa65767956f4315132489ed1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be2f0adaecbc1d64e5b339e84bba19d99bc6ac6fea16166d4c3d2e14647aee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b845b109484654fe12f8dcb1940b55b559d55cee03d629f40812397be0ac5484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec310c70e10c33e42f17e1e74d5aee55a7c30c8e2ead1c51802e2fd9f1152909(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7454b680b0214713763c9c3f54d7ff3d70e7e0c8271b8dc6f00385f113f340f(
    *,
    dst_registry: builtins.str,
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    tar_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542039b10d6041ca9af47159ce1b0b1ed5bff4959f5a21137bdfd24a1cf0e547(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c665c50a22aac442f9192e31318606a0e7d23600e9fd4b8fd071a058670be235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0854011841cf9698e8e4f970d73c9a912381179e4f515435ab05f471e9911788(
    value: typing.Optional[DockerClientConfig],
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
