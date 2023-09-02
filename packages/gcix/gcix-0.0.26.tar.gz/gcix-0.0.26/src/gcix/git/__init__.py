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


@jsii.interface(jsii_type="@gcix/gcix.git.IMirror")
class IMirror(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="gitConfigUserEmail")
    def git_config_user_email(self) -> builtins.str:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        ...

    @git_config_user_email.setter
    def git_config_user_email(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserName")
    def git_config_user_name(self) -> builtins.str:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        ...

    @git_config_user_name.setter
    def git_config_user_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="remoteRepository")
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        ...

    @remote_repository.setter
    def remote_repository(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="scriptHook")
    def script_hook(self) -> typing.List[builtins.str]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        ...

    @script_hook.setter
    def script_hook(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="privateKeyVariable")
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        ...

    @private_key_variable.setter
    def private_key_variable(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="runOnlyForRepositoryUrl")
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        ...

    @run_only_for_repository_url.setter
    def run_only_for_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IMirrorProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.git.IMirror"

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserEmail")
    def git_config_user_email(self) -> builtins.str:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserEmail"))

    @git_config_user_email.setter
    def git_config_user_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d4d68f67634e3e9996a91209e25404bf1b6efe1bb4214988bc42501cfb9112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserEmail", value)

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserName")
    def git_config_user_name(self) -> builtins.str:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserName"))

    @git_config_user_name.setter
    def git_config_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7a3ce5d06d889146e8e0855be072e2badcbdbaaadce82d2689ceca85bf5bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserName", value)

    @builtins.property
    @jsii.member(jsii_name="remoteRepository")
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        return typing.cast(builtins.str, jsii.get(self, "remoteRepository"))

    @remote_repository.setter
    def remote_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465a9a23546f70d575e901964ece806d45eba007e649f6a1fca6f85e897115c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteRepository", value)

    @builtins.property
    @jsii.member(jsii_name="scriptHook")
    def script_hook(self) -> typing.List[builtins.str]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scriptHook"))

    @script_hook.setter
    def script_hook(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354eb8c1bb243abaaefdc7aafcddc4127d59f661c247bbbebebea34f01bebdc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptHook", value)

    @builtins.property
    @jsii.member(jsii_name="privateKeyVariable")
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyVariable"))

    @private_key_variable.setter
    def private_key_variable(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51f232bc0ff211ce86532397b2ecd9c93720c6d9ff0fdcd5bb4d3c761acbfad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyVariable", value)

    @builtins.property
    @jsii.member(jsii_name="runOnlyForRepositoryUrl")
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runOnlyForRepositoryUrl"))

    @run_only_for_repository_url.setter
    def run_only_for_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28e42cfdf8865a8bc61335b6d2b048a6f872ead4da3df4999b53eecd1ab757e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOnlyForRepositoryUrl", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMirror).__jsii_proxy_class__ = lambda : _IMirrorProxy


@jsii.implements(IMirror)
class Mirror(_Job_20682b42, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.git.Mirror"):
    '''This job clones the CI_COMMIT_REF_NAME of the current repository and forcefully pushes this REF to the ``remote_repository``.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: git-mirror
    - stage: deploy
    - image: PredefinedImages.ALPINE_GIT
    '''

    def __init__(
        self,
        *,
        remote_repository: builtins.str,
        git_config_user_email: typing.Optional[builtins.str] = None,
        git_config_user_name: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        private_key_variable: typing.Optional[builtins.str] = None,
        run_only_for_repository_url: typing.Optional[builtins.str] = None,
        script_hook: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param remote_repository: The git repository the code of the pipelines repository should be mirrored to.
        :param git_config_user_email: The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.
        :param git_config_user_name: The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param private_key_variable: DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.
        :param run_only_for_repository_url: When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again. With this variable the job only runs, when its value matches the CI_REPOSITORY_URL of the current repository.
        :param script_hook: This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote. This hook is mostly meant to be for git configuration commands, required to push to the remote repository.
        '''
        props = MirrorProps(
            remote_repository=remote_repository,
            git_config_user_email=git_config_user_email,
            git_config_user_name=git_config_user_name,
            job_name=job_name,
            job_stage=job_stage,
            private_key_variable=private_key_variable,
            run_only_for_repository_url=run_only_for_repository_url,
            script_hook=script_hook,
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
    @jsii.member(jsii_name="gitConfigUserEmail")
    def git_config_user_email(self) -> builtins.str:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserEmail"))

    @git_config_user_email.setter
    def git_config_user_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509087e9fc839021fef7084cbc7ea857febc66d1b3b2774b5b5a04eec7e9fe4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserEmail", value)

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserName")
    def git_config_user_name(self) -> builtins.str:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserName"))

    @git_config_user_name.setter
    def git_config_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c36ad6ab5ea973db523f959c3ec6a01d6e267d15d071c3a72a0bd05d043f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserName", value)

    @builtins.property
    @jsii.member(jsii_name="remoteRepository")
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        return typing.cast(builtins.str, jsii.get(self, "remoteRepository"))

    @remote_repository.setter
    def remote_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33da76714e9e6ee27a11b8903f96fc4320633f87008ae906212077462e3f6a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteRepository", value)

    @builtins.property
    @jsii.member(jsii_name="scriptHook")
    def script_hook(self) -> typing.List[builtins.str]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scriptHook"))

    @script_hook.setter
    def script_hook(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc32d8201fd1abcf6e9ed45bb4ed5449afcdc089df92fee2218fbf0dcdb2e02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptHook", value)

    @builtins.property
    @jsii.member(jsii_name="privateKeyVariable")
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyVariable"))

    @private_key_variable.setter
    def private_key_variable(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6c25b4d117ce3cca8ef828b5e83022bf1235ffd61e25f729fa9573236a127f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyVariable", value)

    @builtins.property
    @jsii.member(jsii_name="runOnlyForRepositoryUrl")
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runOnlyForRepositoryUrl"))

    @run_only_for_repository_url.setter
    def run_only_for_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e47913b740e354f1c7ead1585f09e337fe47e6e6f53166d1a04daeb729b0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOnlyForRepositoryUrl", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.git.MirrorProps",
    jsii_struct_bases=[],
    name_mapping={
        "remote_repository": "remoteRepository",
        "git_config_user_email": "gitConfigUserEmail",
        "git_config_user_name": "gitConfigUserName",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "private_key_variable": "privateKeyVariable",
        "run_only_for_repository_url": "runOnlyForRepositoryUrl",
        "script_hook": "scriptHook",
    },
)
class MirrorProps:
    def __init__(
        self,
        *,
        remote_repository: builtins.str,
        git_config_user_email: typing.Optional[builtins.str] = None,
        git_config_user_name: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        private_key_variable: typing.Optional[builtins.str] = None,
        run_only_for_repository_url: typing.Optional[builtins.str] = None,
        script_hook: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param remote_repository: The git repository the code of the pipelines repository should be mirrored to.
        :param git_config_user_email: The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.
        :param git_config_user_name: The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param private_key_variable: DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.
        :param run_only_for_repository_url: When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again. With this variable the job only runs, when its value matches the CI_REPOSITORY_URL of the current repository.
        :param script_hook: This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote. This hook is mostly meant to be for git configuration commands, required to push to the remote repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fe998190c14191d7a0a8bc46c8de5e4b007e66ad88e07a407269609a498df6)
            check_type(argname="argument remote_repository", value=remote_repository, expected_type=type_hints["remote_repository"])
            check_type(argname="argument git_config_user_email", value=git_config_user_email, expected_type=type_hints["git_config_user_email"])
            check_type(argname="argument git_config_user_name", value=git_config_user_name, expected_type=type_hints["git_config_user_name"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument private_key_variable", value=private_key_variable, expected_type=type_hints["private_key_variable"])
            check_type(argname="argument run_only_for_repository_url", value=run_only_for_repository_url, expected_type=type_hints["run_only_for_repository_url"])
            check_type(argname="argument script_hook", value=script_hook, expected_type=type_hints["script_hook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_repository": remote_repository,
        }
        if git_config_user_email is not None:
            self._values["git_config_user_email"] = git_config_user_email
        if git_config_user_name is not None:
            self._values["git_config_user_name"] = git_config_user_name
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if private_key_variable is not None:
            self._values["private_key_variable"] = private_key_variable
        if run_only_for_repository_url is not None:
            self._values["run_only_for_repository_url"] = run_only_for_repository_url
        if script_hook is not None:
            self._values["script_hook"] = script_hook

    @builtins.property
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        result = self._values.get("remote_repository")
        assert result is not None, "Required property 'remote_repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_config_user_email(self) -> typing.Optional[builtins.str]:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        result = self._values.get("git_config_user_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_config_user_name(self) -> typing.Optional[builtins.str]:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        result = self._values.get("git_config_user_name")
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
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        result = self._values.get("private_key_variable")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        result = self._values.get("run_only_for_repository_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_hook(self) -> typing.Optional[typing.List[builtins.str]]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        result = self._values.get("script_hook")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MirrorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IMirror",
    "Mirror",
    "MirrorProps",
]

publication.publish()

def _typecheckingstub__f9d4d68f67634e3e9996a91209e25404bf1b6efe1bb4214988bc42501cfb9112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7a3ce5d06d889146e8e0855be072e2badcbdbaaadce82d2689ceca85bf5bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465a9a23546f70d575e901964ece806d45eba007e649f6a1fca6f85e897115c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354eb8c1bb243abaaefdc7aafcddc4127d59f661c247bbbebebea34f01bebdc7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51f232bc0ff211ce86532397b2ecd9c93720c6d9ff0fdcd5bb4d3c761acbfad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28e42cfdf8865a8bc61335b6d2b048a6f872ead4da3df4999b53eecd1ab757e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509087e9fc839021fef7084cbc7ea857febc66d1b3b2774b5b5a04eec7e9fe4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c36ad6ab5ea973db523f959c3ec6a01d6e267d15d071c3a72a0bd05d043f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33da76714e9e6ee27a11b8903f96fc4320633f87008ae906212077462e3f6a20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc32d8201fd1abcf6e9ed45bb4ed5449afcdc089df92fee2218fbf0dcdb2e02c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6c25b4d117ce3cca8ef828b5e83022bf1235ffd61e25f729fa9573236a127f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e47913b740e354f1c7ead1585f09e337fe47e6e6f53166d1a04daeb729b0d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fe998190c14191d7a0a8bc46c8de5e4b007e66ad88e07a407269609a498df6(
    *,
    remote_repository: builtins.str,
    git_config_user_email: typing.Optional[builtins.str] = None,
    git_config_user_name: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    private_key_variable: typing.Optional[builtins.str] = None,
    run_only_for_repository_url: typing.Optional[builtins.str] = None,
    script_hook: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
