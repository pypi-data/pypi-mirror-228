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

from .. import Job as _Job_20682b42


@jsii.data_type(
    jsii_type="@gcix/gcix.python.BdistWheelProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "job_stage": "jobStage",
        "pip_requirements": "pipRequirements",
    },
)
class BdistWheelProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip_requirements: typing.Optional[typing.Union["PipInstallRequirementsProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: 
        :param job_stage: 
        :param pip_requirements: 
        '''
        if isinstance(pip_requirements, dict):
            pip_requirements = PipInstallRequirementsProps(**pip_requirements)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d09317bbb0484765b6542179f216032dc398873a4bb995805de14a1a385e48b)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument pip_requirements", value=pip_requirements, expected_type=type_hints["pip_requirements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if pip_requirements is not None:
            self._values["pip_requirements"] = pip_requirements

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pip_requirements(self) -> typing.Optional["PipInstallRequirementsProps"]:
        result = self._values.get("pip_requirements")
        return typing.cast(typing.Optional["PipInstallRequirementsProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BdistWheelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.python.Flake8Props",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage"},
)
class Flake8Props:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c4996b185aeb3da749928d11d7dd01234b95fd948279d5867fe8875bb002b9)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Flake8Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.python.IBdistWheel")
class IBdistWheel(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="requirementsFile")
    def requirements_file(self) -> typing.Optional[builtins.str]:
        ...


class _IBdistWheelProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IBdistWheel"

    @builtins.property
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipenvVersionSpecifier"))

    @builtins.property
    @jsii.member(jsii_name="requirementsFile")
    def requirements_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsFile"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBdistWheel).__jsii_proxy_class__ = lambda : _IBdistWheelProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IFlake8")
class IFlake8(typing_extensions.Protocol):
    pass


class _IFlake8Proxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IFlake8"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFlake8).__jsii_proxy_class__ = lambda : _IFlake8Proxy


@jsii.interface(jsii_type="@gcix/gcix.python.IIsort")
class IIsort(typing_extensions.Protocol):
    pass


class _IIsortProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IIsort"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIsort).__jsii_proxy_class__ = lambda : _IIsortProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IMyPy")
class IMyPy(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="packageDir")
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        ...

    @package_dir.setter
    def package_dir(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="myPyOptions")
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        ...

    @my_py_options.setter
    def my_py_options(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="myPyVersion")
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        ...

    @my_py_version.setter
    def my_py_version(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IMyPyProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IMyPy"

    @builtins.property
    @jsii.member(jsii_name="packageDir")
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        return typing.cast(builtins.str, jsii.get(self, "packageDir"))

    @package_dir.setter
    def package_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fafabc2ba82b2a1dd35865ed79c04c47ddae49469e5cf5a1b6f3fd5f78d6a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageDir", value)

    @builtins.property
    @jsii.member(jsii_name="myPyOptions")
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyOptions"))

    @my_py_options.setter
    def my_py_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e264cc9448efca860d02b69e98cff3215d667aa9f93bff16a68833513ee89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyOptions", value)

    @builtins.property
    @jsii.member(jsii_name="myPyVersion")
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyVersion"))

    @my_py_version.setter
    def my_py_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce97c4247038422ebe2e94bd6b6ddb838ba823ee5801b45fb58ba75111ee630f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyVersion", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMyPy).__jsii_proxy_class__ = lambda : _IMyPyProxy


@jsii.interface(jsii_type="@gcix/gcix.python.ITwineUpload")
class ITwineUpload(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="twinePasswordEnvVar")
    def twine_password_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        ...

    @twine_password_env_var.setter
    def twine_password_env_var(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="twineUsernameEnvVar")
    def twine_username_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        ...

    @twine_username_env_var.setter
    def twine_username_env_var(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="twineRepositoryUrl")
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        ...

    @twine_repository_url.setter
    def twine_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ITwineUploadProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.ITwineUpload"

    @builtins.property
    @jsii.member(jsii_name="twinePasswordEnvVar")
    def twine_password_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twinePasswordEnvVar"))

    @twine_password_env_var.setter
    def twine_password_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c679cf2e46e7eed880de5a8681a36607eab5c18a22d36c8523beef364c08fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twinePasswordEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineUsernameEnvVar")
    def twine_username_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twineUsernameEnvVar"))

    @twine_username_env_var.setter
    def twine_username_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07c2a4560b9698db9ae7c4b59816fa229191e09e1d852fb60e6a2426458bed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineUsernameEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineRepositoryUrl")
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "twineRepositoryUrl"))

    @twine_repository_url.setter
    def twine_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3710db20d2fd7371df4cfe0b11748d28ca4e944cd9343564394cf4acffec0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineRepositoryUrl", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITwineUpload).__jsii_proxy_class__ = lambda : _ITwineUploadProxy


@jsii.implements(IIsort)
class Isort(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.Isort",
):
    '''Runs:.

    Example::

       pip3 install --upgrade isort
       isort --check .

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: isort
    - stage: lint
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        props = IsortProps(job_name=job_name, job_stage=job_stage)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.python.IsortProps",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage"},
)
class IsortProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f98414d5eb4a87d04983c87fd97e5dd52df873dde7bcd63b64e54c824837f3f)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IsortProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMyPy)
class MyPy(_Job_20682b42, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.python.MyPy"):
    '''Install mypy if not already installed. Execute mypy for ``packageDir``.

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: mypy
    - stage: lint

    :return: - The configured ``gcip.Job`` instance.
    '''

    def __init__(
        self,
        *,
        package_dir: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        my_py_options: typing.Optional[builtins.str] = None,
        my_py_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param package_dir: Package directory to type check.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param my_py_options: Adds arguments to mypy execution.
        :param my_py_version: If ``mypy`` is not already installed, this version will be installed. Installs latest version if ``undefined``.
        '''
        props = MyPyProps(
            package_dir=package_dir,
            job_name=job_name,
            job_stage=job_stage,
            my_py_options=my_py_options,
            my_py_version=my_py_version,
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
    @jsii.member(jsii_name="packageDir")
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        return typing.cast(builtins.str, jsii.get(self, "packageDir"))

    @package_dir.setter
    def package_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f30caf51df563c8d8511bc7e5e7e84375e3e6e52a273347507df48e627f0d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageDir", value)

    @builtins.property
    @jsii.member(jsii_name="myPyOptions")
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyOptions"))

    @my_py_options.setter
    def my_py_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9b7ac4c85d2393a8cabdc87caae0f00f18d834e76be3e6e815d9c0783eccee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyOptions", value)

    @builtins.property
    @jsii.member(jsii_name="myPyVersion")
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyVersion"))

    @my_py_version.setter
    def my_py_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d474a665e7e51241473c530b17b00aab1a645a2f0223cbf477442f34b83876d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyVersion", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.MyPyProps",
    jsii_struct_bases=[],
    name_mapping={
        "package_dir": "packageDir",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "my_py_options": "myPyOptions",
        "my_py_version": "myPyVersion",
    },
)
class MyPyProps:
    def __init__(
        self,
        *,
        package_dir: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        my_py_options: typing.Optional[builtins.str] = None,
        my_py_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param package_dir: Package directory to type check.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param my_py_options: Adds arguments to mypy execution.
        :param my_py_version: If ``mypy`` is not already installed, this version will be installed. Installs latest version if ``undefined``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195526b4386e678914dec0de04f5a0aee3e52e65c2ce3d5d447397438ec6de54)
            check_type(argname="argument package_dir", value=package_dir, expected_type=type_hints["package_dir"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument my_py_options", value=my_py_options, expected_type=type_hints["my_py_options"])
            check_type(argname="argument my_py_version", value=my_py_version, expected_type=type_hints["my_py_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_dir": package_dir,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if my_py_options is not None:
            self._values["my_py_options"] = my_py_options
        if my_py_version is not None:
            self._values["my_py_version"] = my_py_version

    @builtins.property
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        result = self._values.get("package_dir")
        assert result is not None, "Required property 'package_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        result = self._values.get("my_py_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        result = self._values.get("my_py_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MyPyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PipInstallRequirementsProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipenv_version_specifier": "pipenvVersionSpecifier",
        "requirements_file": "requirementsFile",
    },
)
class PipInstallRequirementsProps:
    def __init__(
        self,
        *,
        pipenv_version_specifier: typing.Optional[builtins.str] = None,
        requirements_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents the properties for the ``pipInstallRequirements`` static method.

        :param pipenv_version_specifier: The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to an empty string, indicating installation of the latest version. Default: ""
        :param requirements_file: The location and name of the requirements file. Default: "requirements.txt"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f23b66d8083ae889fbd949745fd77545b924a5aebcc1c180cd20b8e4f447ea)
            check_type(argname="argument pipenv_version_specifier", value=pipenv_version_specifier, expected_type=type_hints["pipenv_version_specifier"])
            check_type(argname="argument requirements_file", value=requirements_file, expected_type=type_hints["requirements_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pipenv_version_specifier is not None:
            self._values["pipenv_version_specifier"] = pipenv_version_specifier
        if requirements_file is not None:
            self._values["requirements_file"] = requirements_file

    @builtins.property
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        '''The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to an empty string, indicating installation of the latest version.

        :default: ""
        '''
        result = self._values.get("pipenv_version_specifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements_file(self) -> typing.Optional[builtins.str]:
        '''The location and name of the requirements file.

        :default: "requirements.txt"
        '''
        result = self._values.get("requirements_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipInstallRequirementsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PythonScripts(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonScripts",
):
    '''Represents a collection of utility functions for scripting tasks.'''

    @jsii.member(jsii_name="pipInstallRequirements")
    @builtins.classmethod
    def pip_install_requirements(
        cls,
        *,
        pipenv_version_specifier: typing.Optional[builtins.str] = None,
        requirements_file: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Generates a shell command to install project requirements using ``pipenv`` and ``pip`` based on the presence of a ``Pipfile.lock`` or ``requirements.txt``.

        :param pipenv_version_specifier: The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to an empty string, indicating installation of the latest version. Default: ""
        :param requirements_file: The location and name of the requirements file. Default: "requirements.txt"

        :return: A shell command string for installing project requirements.
        '''
        props = PipInstallRequirementsProps(
            pipenv_version_specifier=pipenv_version_specifier,
            requirements_file=requirements_file,
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "pipInstallRequirements", [props]))


@jsii.implements(ITwineUpload)
class TwineUpload(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.TwineUpload",
):
    '''Runs:.

    Example::

       pip3 install --upgrade twine
       python3 -m twine upload --non-interactive --disable-progress-bar dist/*

    Requires artifacts from a build job under ``dist/`` (e.g. from ``BdistWheel()``)

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: twine
    - stage: deploy
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        twine_password_env_var: typing.Optional[builtins.str] = None,
        twine_repository_url: typing.Optional[builtins.str] = None,
        twine_username_env_var: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param twine_password_env_var: The name of the environment variable containing the password. **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_PASSWORD'.
        :param twine_repository_url: The URL to the PyPI repository to which the Python artifacts will be deployed. If ``undefined`` the package is published to ``https://pypi.org``.
        :param twine_username_env_var: The name of the environment variable containing the username value. **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_USERNAME'.
        '''
        props = TwineUploadProps(
            job_name=job_name,
            job_stage=job_stage,
            twine_password_env_var=twine_password_env_var,
            twine_repository_url=twine_repository_url,
            twine_username_env_var=twine_username_env_var,
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
    @jsii.member(jsii_name="twinePasswordEnvVar")
    def twine_password_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twinePasswordEnvVar"))

    @twine_password_env_var.setter
    def twine_password_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0450db1c71dd7ab15a12161540403198f825244838fa8bfa161e9da58205ea09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twinePasswordEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineUsernameEnvVar")
    def twine_username_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twineUsernameEnvVar"))

    @twine_username_env_var.setter
    def twine_username_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3f0e00e0136c1add6d5c298d0aca3622e4d2936328a99026a3c2d0f0905a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineUsernameEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineRepositoryUrl")
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "twineRepositoryUrl"))

    @twine_repository_url.setter
    def twine_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62f68aff198ea7ae0e235efd8dfd98b6b9a45efba8c79027a83c5602d6d225a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineRepositoryUrl", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.TwineUploadProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "job_stage": "jobStage",
        "twine_password_env_var": "twinePasswordEnvVar",
        "twine_repository_url": "twineRepositoryUrl",
        "twine_username_env_var": "twineUsernameEnvVar",
    },
)
class TwineUploadProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        twine_password_env_var: typing.Optional[builtins.str] = None,
        twine_repository_url: typing.Optional[builtins.str] = None,
        twine_username_env_var: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents the properties for the ``TwineUpload`` class.

        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param twine_password_env_var: The name of the environment variable containing the password. **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_PASSWORD'.
        :param twine_repository_url: The URL to the PyPI repository to which the Python artifacts will be deployed. If ``undefined`` the package is published to ``https://pypi.org``.
        :param twine_username_env_var: The name of the environment variable containing the username value. **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_USERNAME'.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f34ea659259d5eb43b22d4589a0a51ff8bec4aa23805f62bd64473ef9c56b9a)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument twine_password_env_var", value=twine_password_env_var, expected_type=type_hints["twine_password_env_var"])
            check_type(argname="argument twine_repository_url", value=twine_repository_url, expected_type=type_hints["twine_repository_url"])
            check_type(argname="argument twine_username_env_var", value=twine_username_env_var, expected_type=type_hints["twine_username_env_var"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if twine_password_env_var is not None:
            self._values["twine_password_env_var"] = twine_password_env_var
        if twine_repository_url is not None:
            self._values["twine_repository_url"] = twine_repository_url
        if twine_username_env_var is not None:
            self._values["twine_username_env_var"] = twine_username_env_var

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_password_env_var(self) -> typing.Optional[builtins.str]:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        result = self._values.get("twine_password_env_var")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        result = self._values.get("twine_repository_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_username_env_var(self) -> typing.Optional[builtins.str]:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        result = self._values.get("twine_username_env_var")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TwineUploadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IBdistWheel)
class BdistWheel(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.BdistWheel",
):
    '''Runs ``python3 setup.py bdist_wheel`` and installs project requirements Requirements are installed by ``LinuxScripts.pipInstallRequirements()``.

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: bdist_wheel
    - stage: build
    - artifacts: Path 'dist/'

    Requires a ``Pipfile.lock`` or ``requirements.txt`` in your project folder
    containing at least ``setuptools``. Creates artifacts under the path 'dist/'.

    :default:

    to an empty string, indicating
    installation of the latest version.
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip_requirements: typing.Optional[typing.Union[PipInstallRequirementsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: 
        :param job_stage: 
        :param pip_requirements: 
        '''
        props = BdistWheelProps(
            job_name=job_name, job_stage=job_stage, pip_requirements=pip_requirements
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
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipenvVersionSpecifier"))

    @builtins.property
    @jsii.member(jsii_name="requirementsFile")
    def requirements_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsFile"))


@jsii.implements(IFlake8)
class Flake8(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.Flake8",
):
    '''Runs:.

    Example::

       pip3 install --upgrade flake8
       flake8

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: flake8
    - stage: lint
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        props = Flake8Props(job_name=job_name, job_stage=job_stage)

        jsii.create(self.__class__, self, [props])


__all__ = [
    "BdistWheel",
    "BdistWheelProps",
    "Flake8",
    "Flake8Props",
    "IBdistWheel",
    "IFlake8",
    "IIsort",
    "IMyPy",
    "ITwineUpload",
    "Isort",
    "IsortProps",
    "MyPy",
    "MyPyProps",
    "PipInstallRequirementsProps",
    "PythonScripts",
    "TwineUpload",
    "TwineUploadProps",
]

publication.publish()

def _typecheckingstub__6d09317bbb0484765b6542179f216032dc398873a4bb995805de14a1a385e48b(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    pip_requirements: typing.Optional[typing.Union[PipInstallRequirementsProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c4996b185aeb3da749928d11d7dd01234b95fd948279d5867fe8875bb002b9(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fafabc2ba82b2a1dd35865ed79c04c47ddae49469e5cf5a1b6f3fd5f78d6a9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e264cc9448efca860d02b69e98cff3215d667aa9f93bff16a68833513ee89d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce97c4247038422ebe2e94bd6b6ddb838ba823ee5801b45fb58ba75111ee630f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c679cf2e46e7eed880de5a8681a36607eab5c18a22d36c8523beef364c08fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07c2a4560b9698db9ae7c4b59816fa229191e09e1d852fb60e6a2426458bed4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3710db20d2fd7371df4cfe0b11748d28ca4e944cd9343564394cf4acffec0ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f98414d5eb4a87d04983c87fd97e5dd52df873dde7bcd63b64e54c824837f3f(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f30caf51df563c8d8511bc7e5e7e84375e3e6e52a273347507df48e627f0d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9b7ac4c85d2393a8cabdc87caae0f00f18d834e76be3e6e815d9c0783eccee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d474a665e7e51241473c530b17b00aab1a645a2f0223cbf477442f34b83876d4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195526b4386e678914dec0de04f5a0aee3e52e65c2ce3d5d447397438ec6de54(
    *,
    package_dir: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    my_py_options: typing.Optional[builtins.str] = None,
    my_py_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f23b66d8083ae889fbd949745fd77545b924a5aebcc1c180cd20b8e4f447ea(
    *,
    pipenv_version_specifier: typing.Optional[builtins.str] = None,
    requirements_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0450db1c71dd7ab15a12161540403198f825244838fa8bfa161e9da58205ea09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3f0e00e0136c1add6d5c298d0aca3622e4d2936328a99026a3c2d0f0905a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62f68aff198ea7ae0e235efd8dfd98b6b9a45efba8c79027a83c5602d6d225a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f34ea659259d5eb43b22d4589a0a51ff8bec4aa23805f62bd64473ef9c56b9a(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    twine_password_env_var: typing.Optional[builtins.str] = None,
    twine_repository_url: typing.Optional[builtins.str] = None,
    twine_username_env_var: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
