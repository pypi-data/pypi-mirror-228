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

from .. import Job as _Job_20682b42, JobCollection as _JobCollection_0289800c
from ..git import (
    IMirror as _IMirror_4c79aff4,
    Mirror as _Mirror_d6fa8d93,
    MirrorProps as _MirrorProps_0e4917bb,
)


class AWSAccount(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.aws.AWSAccount"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsAccountId")
    @builtins.classmethod
    def aws_account_id(cls) -> builtins.str:
        '''Retrieves the AWS Account ID associated with the current AWS credentials or environment.

        If available, it uses the environment variable
        ``AWS_ACCOUNT_ID``. Otherwise, it fetches the AWS Account ID from the caller
        identity response obtained via STS.

        :return:

        A promise that resolves to the
        AWS Account ID as a string.

        :throws: {Error} If the AWS Account ID cannot be resolved.
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "awsAccountId", []))

    @jsii.member(jsii_name="awsRegion")
    @builtins.classmethod
    def aws_region(cls) -> builtins.str:
        '''Retrieves the AWS region associated with the current AWS credentials or environment.

        If available, it uses the environment variable
        ``AWS_DEFAULT_REGION``. Otherwise, it fetches the AWS region from the caller
        identity response obtained via STS.

        :return:

        A promise that resolves to the
        AWS region as a string.

        :throws: {Error} If the AWS region cannot be resolved.
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "awsRegion", []))


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.BootstrapProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_account_id": "awsAccountId",
        "aws_region": "awsRegion",
        "qualifier": "qualifier",
        "toolkit_stack_name": "toolkitStackName",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "resource_tags": "resourceTags",
    },
)
class BootstrapProps:
    def __init__(
        self,
        *,
        aws_account_id: builtins.str,
        aws_region: builtins.str,
        qualifier: builtins.str,
        toolkit_stack_name: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Configuration properties for initializing a Bootstrap instance.

        :param aws_account_id: The AWS account ID associated with the Bootstrap configuration.
        :param aws_region: The AWS region in which the Bootstrap will be performed.
        :param qualifier: The qualifier applied to the Bootstrap.
        :param toolkit_stack_name: The name of the toolkit stack used for Bootstrap.
        :param job_name: An optional name for the Bootstrap job.
        :param job_stage: An optional stage for the Bootstrap job.
        :param resource_tags: Optional resource tags that can be applied during Bootstrap.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31070e7b2289a2717aab0ff4f0f1bed66e25c7140ed8da33f076bd9c47460b75)
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
            check_type(argname="argument toolkit_stack_name", value=toolkit_stack_name, expected_type=type_hints["toolkit_stack_name"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_account_id": aws_account_id,
            "aws_region": aws_region,
            "qualifier": qualifier,
            "toolkit_stack_name": toolkit_stack_name,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        result = self._values.get("aws_account_id")
        assert result is not None, "Required property 'aws_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        result = self._values.get("qualifier")
        assert result is not None, "Required property 'qualifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        result = self._values.get("toolkit_stack_name")
        assert result is not None, "Required property 'toolkit_stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BootstrapProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.DeployProps",
    jsii_struct_bases=[],
    name_mapping={
        "stacks": "stacks",
        "context": "context",
        "deploy_options": "deployOptions",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "strict": "strict",
        "toolkit_stack_name": "toolkitStackName",
        "wait_for_stack": "waitForStack",
        "wait_for_stack_account_id": "waitForStackAccountId",
        "wait_for_stack_assume_role": "waitForStackAssumeRole",
    },
)
class DeployProps:
    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deploy_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        strict: typing.Optional[builtins.bool] = None,
        toolkit_stack_name: typing.Optional[builtins.str] = None,
        wait_for_stack: typing.Optional[builtins.bool] = None,
        wait_for_stack_account_id: typing.Optional[builtins.str] = None,
        wait_for_stack_assume_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration properties for initializing a Deploy instance.

        :param stacks: An array of stack names to be deployed.
        :param context: Optional context values to provide additional information for deployment.
        :param deploy_options: Optional deployment options.
        :param job_name: An optional name for the Deploy job.
        :param job_stage: An optional stage for the Deploy job.
        :param strict: Enable strict deployment mode.
        :param toolkit_stack_name: Optional toolkit stack name used for deployment.
        :param wait_for_stack: Wait for stacks to complete deployment.
        :param wait_for_stack_account_id: AWS account ID for stack waiting.
        :param wait_for_stack_assume_role: AWS assume role for stack waiting.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02294d96a01f7b66a9e316c742913ece9eb4c3f6626227ac224647d11c8a3025)
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deploy_options", value=deploy_options, expected_type=type_hints["deploy_options"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument toolkit_stack_name", value=toolkit_stack_name, expected_type=type_hints["toolkit_stack_name"])
            check_type(argname="argument wait_for_stack", value=wait_for_stack, expected_type=type_hints["wait_for_stack"])
            check_type(argname="argument wait_for_stack_account_id", value=wait_for_stack_account_id, expected_type=type_hints["wait_for_stack_account_id"])
            check_type(argname="argument wait_for_stack_assume_role", value=wait_for_stack_assume_role, expected_type=type_hints["wait_for_stack_assume_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if context is not None:
            self._values["context"] = context
        if deploy_options is not None:
            self._values["deploy_options"] = deploy_options
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if strict is not None:
            self._values["strict"] = strict
        if toolkit_stack_name is not None:
            self._values["toolkit_stack_name"] = toolkit_stack_name
        if wait_for_stack is not None:
            self._values["wait_for_stack"] = wait_for_stack
        if wait_for_stack_account_id is not None:
            self._values["wait_for_stack_account_id"] = wait_for_stack_account_id
        if wait_for_stack_assume_role is not None:
            self._values["wait_for_stack_assume_role"] = wait_for_stack_assume_role

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        result = self._values.get("deploy_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''Enable strict deployment mode.'''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        result = self._values.get("toolkit_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_stack(self) -> typing.Optional[builtins.bool]:
        '''Wait for stacks to complete deployment.'''
        result = self._values.get("wait_for_stack")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        result = self._values.get("wait_for_stack_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        result = self._values.get("wait_for_stack_assume_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.DiffDeployProps",
    jsii_struct_bases=[],
    name_mapping={"stacks": "stacks", "context": "context"},
)
class DiffDeployProps:
    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Configuration properties for initializing a DiffDeploy instance.

        :param stacks: An array of stack names for which to generate a diff and perform deployment.
        :param context: Optional context values to provide additional information for the diff and deployment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d5da305316074b1a800e6eb9f104d21236b547f739ecd7c7aef8447e9de9a6)
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if context is not None:
            self._values["context"] = context

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiffDeployProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.DiffProps",
    jsii_struct_bases=[],
    name_mapping={
        "stacks": "stacks",
        "context": "context",
        "diff_options": "diffOptions",
        "job_name": "jobName",
        "job_stage": "jobStage",
    },
)
class DiffProps:
    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        diff_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration properties for initializing a Diff instance.

        :param stacks: An array of stack names for which to generate a diff.
        :param context: Optional context values to provide additional information for the diff.
        :param diff_options: Optional diff options to customize the diff process.
        :param job_name: An optional name for the Diff job.
        :param job_stage: An optional stage for the Diff job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1918e96efec6fee48e4c72f32431611193c4c817532815d6ef9a3c25a54eb6b5)
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument diff_options", value=diff_options, expected_type=type_hints["diff_options"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if context is not None:
            self._values["context"] = context
        if diff_options is not None:
            self._values["diff_options"] = diff_options
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        result = self._values.get("diff_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiffProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.aws.IBootstrap")
class IBootstrap(typing_extensions.Protocol):
    '''Represents the interface that a Bootstrap instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        ...

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        ...

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the Bootstrap job.'''
        ...

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> builtins.str:
        '''The stage of the Bootstrap job.'''
        ...

    @job_stage.setter
    def job_stage(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        ...

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        ...

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        ...

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _IBootstrapProxy:
    '''Represents the interface that a Bootstrap instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.IBootstrap"

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fdab73e4df6dcb7569b7cfcf017d4722caeb1a90d47e908c35522994ee8d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c9baddac2c982671bac064c5a6cff1e35a30831a68bec6858bbddec5746aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23c815abb83752c6d23c0eefd04ed200eac35be0e56df3650e08200d0689201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> builtins.str:
        '''The stage of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e79c5b454892e75eb3b6923ea4a41ce39dbe490ec105733da8eeb71d112d540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578ca589aa37e1ddc069e901c0dd13cd6174e0bbea8bf7d9ee0446d6c2250694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6b0414dc0584b0573515b8dd016d1ffaae794252d9c4131b3b82bcf6a5eb34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297d8e836526b09df65136bdf25d7215bc4993464da0dac8cdc95ff8a8bb59f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBootstrap).__jsii_proxy_class__ = lambda : _IBootstrapProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.IDeploy")
class IDeploy(typing_extensions.Protocol):
    '''Represents the interface that a Deploy instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        ...

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        '''Flag indicating if strict deployment mode is enabled.'''
        ...

    @strict.setter
    def strict(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="waitForStack")
    def wait_for_stack(self) -> builtins.bool:
        '''Flag indicating if the deployment should wait for stack completion.'''
        ...

    @wait_for_stack.setter
    def wait_for_stack(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        ...

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="deployOptions")
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        ...

    @deploy_options.setter
    def deploy_options(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        ...

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        ...

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        ...

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="waitForStackAccountId")
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        ...

    @wait_for_stack_account_id.setter
    def wait_for_stack_account_id(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="waitForStackAssumeRole")
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        ...

    @wait_for_stack_assume_role.setter
    def wait_for_stack_assume_role(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IDeployProxy:
    '''Represents the interface that a Deploy instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.IDeploy"

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba6699af515ffbb20e58b40d052fb131405b7e45f2782d07fef527da199e5ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        '''Flag indicating if strict deployment mode is enabled.'''
        return typing.cast(builtins.bool, jsii.get(self, "strict"))

    @strict.setter
    def strict(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e6319c3976c080acd5c7b42c242ef183a7249fa740009830c137c6d448cfe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strict", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStack")
    def wait_for_stack(self) -> builtins.bool:
        '''Flag indicating if the deployment should wait for stack completion.'''
        return typing.cast(builtins.bool, jsii.get(self, "waitForStack"))

    @wait_for_stack.setter
    def wait_for_stack(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8443a0b88a95a5df1e631df0b01b64fb17bf79fe3fe6fe077c13f6948f9e08e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStack", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fad5ae3007754ac6be19e17d3c775219705163589c47c0613434f0866a7929d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="deployOptions")
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployOptions"))

    @deploy_options.setter
    def deploy_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9512a8111e1abbd517c23412dd953f7198ef5ac52ed09040a07a45e76918477b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb69a98763245d4e1a27b7cc8a800b73bfa4ad6b37c79595a2cd009319cbd86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2ad8dc2d6ff83eaec359d73c436eb16630d51f9aad01bbfe729ef6ebc947b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080c39538ef57fbfc2d09b127c08e871886da61c14a32e117595906e52338f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAccountId")
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAccountId"))

    @wait_for_stack_account_id.setter
    def wait_for_stack_account_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bf5bc8627d673b182dac28db2014f1641a95c98f82856e5648f649d260707d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAssumeRole")
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAssumeRole"))

    @wait_for_stack_assume_role.setter
    def wait_for_stack_assume_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40dc8d3631a98fe04346b62b63e91708ceac2fc6e41fe80ceb125149c048ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAssumeRole", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeploy).__jsii_proxy_class__ = lambda : _IDeployProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.IDiff")
class IDiff(typing_extensions.Protocol):
    '''Represents the interface that a Diff instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        ...

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        ...

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="diffOptions")
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        ...

    @diff_options.setter
    def diff_options(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        ...

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        ...

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IDiffProxy:
    '''Represents the interface that a Diff instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.IDiff"

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e092ee7b487cd85bae70d35a5e8d29890aeee16f0bb566c8e4884b039c20fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5b2d4931c222352952251bec5c5221e9131be5a49877c2b38d5b87206dae9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="diffOptions")
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diffOptions"))

    @diff_options.setter
    def diff_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2a6d529aa6b390030366f1b20f27d900b4eb9ab9b6506ba8c06ff85cc3b4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cdf226605a65753319029c00ffd23b5ef8df07f035fbe123269245381222d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77158275d48ed38fa0f36eed1b6c1235198d8f23cd9acb59a63179123c54169e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDiff).__jsii_proxy_class__ = lambda : _IDiffProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.IDiffDeploy")
class IDiffDeploy(typing_extensions.Protocol):
    '''Represents the interface that a DiffDeploy instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="deployJob")
    def deploy_job(self) -> "Deploy":
        '''The instance of the Deploy job associated with this DiffDeploy instance.'''
        ...

    @deploy_job.setter
    def deploy_job(self, value: "Deploy") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="diffJob")
    def diff_job(self) -> "Diff":
        '''The instance of the Diff job associated with this DiffDeploy instance.'''
        ...

    @diff_job.setter
    def diff_job(self, value: "Diff") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        ...

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        ...

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _IDiffDeployProxy:
    '''Represents the interface that a DiffDeploy instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.IDiffDeploy"

    @builtins.property
    @jsii.member(jsii_name="deployJob")
    def deploy_job(self) -> "Deploy":
        '''The instance of the Deploy job associated with this DiffDeploy instance.'''
        return typing.cast("Deploy", jsii.get(self, "deployJob"))

    @deploy_job.setter
    def deploy_job(self, value: "Deploy") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bd20cc1696d9c36cc2fce98bde8b06e14a60b497e74c1005b5dc587f6f0d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployJob", value)

    @builtins.property
    @jsii.member(jsii_name="diffJob")
    def diff_job(self) -> "Diff":
        '''The instance of the Diff job associated with this DiffDeploy instance.'''
        return typing.cast("Diff", jsii.get(self, "diffJob"))

    @diff_job.setter
    def diff_job(self, value: "Diff") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b7d6e9815ccf9075f2d650cb50a081d15e57ac61f20099d530253a524e7199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffJob", value)

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabca68ef187c47c86acb9b35809e2c31680fc4d020a5cf23d9e2ff9bddaaa6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be798a421dfe22d560c939836430b6830e93d49855e1c029b27070b37468816c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDiffDeploy).__jsii_proxy_class__ = lambda : _IDiffDeployProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.IMirrorToCodecommit")
class IMirrorToCodecommit(_IMirror_4c79aff4, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the target Codecommit repository.

        :default: CI_PROJECT_PATH_SLUG.
        '''
        ...

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        ...

    @aws_region.setter
    def aws_region(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="infrastructureTags")
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        ...

    @infrastructure_tags.setter
    def infrastructure_tags(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IMirrorToCodecommitProxy(
    jsii.proxy_for(_IMirror_4c79aff4), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.IMirrorToCodecommit"

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the target Codecommit repository.

        :default: CI_PROJECT_PATH_SLUG.
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d47355cdbcedcd2365cd8618bb48bb85b0793e247ba4980156b49a76b922ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683cab747e03754e4d7ad716d15eb0f1819ad822fe19299bd6878083e41c40ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureTags")
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureTags"))

    @infrastructure_tags.setter
    def infrastructure_tags(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc24eae8a713c95c1b5e653f03670cdc72d0e118c3a63227e743243f25ff23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureTags", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMirrorToCodecommit).__jsii_proxy_class__ = lambda : _IMirrorToCodecommitProxy


@jsii.implements(IMirrorToCodecommit)
class MirrorToCodecommit(
    _Mirror_d6fa8d93,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.MirrorToCodecommit",
):
    '''This job clones the CI_COMMIT_REF_NAME of the current repository and forcefully pushes this REF to a AWS CodeCommit repository.

    This job requires following IAM permissions:

    - codecommit:CreateRepository
    - codecommit:GetRepository
    - codecommit:CreateBranch
    - codecommit:GitPush
    - codecommit:TagResource

    You could also limit the resource to ``!Sub arn:aws:codecommit:${AWS::Region}:${AWS::AccountId}:<repository-name>``.
    '''

    def __init__(
        self,
        *,
        aws_region: typing.Optional[builtins.str] = None,
        infrastructure_tags: typing.Optional[builtins.str] = None,
        mirror_opts: typing.Optional[typing.Union[_MirrorProps_0e4917bb, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_region: The AWS region you want to operate in. When not set, it would be curl'ed from the current EC2 instance metadata.
        :param infrastructure_tags: Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource. Changed values won't change the tags on an already existing ECR. This string must have the pattern: ``Tag1=Value1,Tag2=Value2``
        :param mirror_opts: Options for the upstream Mirror job.
        :param repository_name: The name of the target Codecommit repository. Default: CI_PROJECT_PATH_SLUG.
        '''
        props = MirrorToCodecommitProps(
            aws_region=aws_region,
            infrastructure_tags=infrastructure_tags,
            mirror_opts=mirror_opts,
            repository_name=repository_name,
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
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the target Codecommit repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750a0936b37b9d7058361a5391596a0aa87ea2c2a70779024259bf6427be23df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1ed63ef582329b14c18409a05917140b27204dbd8720088423cf7a65e8a46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureTags")
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureTags"))

    @infrastructure_tags.setter
    def infrastructure_tags(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2fc9cdeb3653408cf2db32fecbdd42af16230785aca513f9725137bcf06544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureTags", value)

    @builtins.property
    @jsii.member(jsii_name="mirrorOpts")
    def mirror_opts(self) -> typing.Optional[_MirrorProps_0e4917bb]:
        return typing.cast(typing.Optional[_MirrorProps_0e4917bb], jsii.get(self, "mirrorOpts"))

    @mirror_opts.setter
    def mirror_opts(self, value: typing.Optional[_MirrorProps_0e4917bb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ed4f8b18728fdb65dba607c6f54fa23ac31343dfe64793a4465a5c995aaf21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorOpts", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.MirrorToCodecommitProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_region": "awsRegion",
        "infrastructure_tags": "infrastructureTags",
        "mirror_opts": "mirrorOpts",
        "repository_name": "repositoryName",
    },
)
class MirrorToCodecommitProps:
    def __init__(
        self,
        *,
        aws_region: typing.Optional[builtins.str] = None,
        infrastructure_tags: typing.Optional[builtins.str] = None,
        mirror_opts: typing.Optional[typing.Union[_MirrorProps_0e4917bb, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_region: The AWS region you want to operate in. When not set, it would be curl'ed from the current EC2 instance metadata.
        :param infrastructure_tags: Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource. Changed values won't change the tags on an already existing ECR. This string must have the pattern: ``Tag1=Value1,Tag2=Value2``
        :param mirror_opts: Options for the upstream Mirror job.
        :param repository_name: The name of the target Codecommit repository. Default: CI_PROJECT_PATH_SLUG.
        '''
        if isinstance(mirror_opts, dict):
            mirror_opts = _MirrorProps_0e4917bb(**mirror_opts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6150e19564bd364764a1c6615a04c9b26f26221395c46dd1f0ec1195f091652e)
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument infrastructure_tags", value=infrastructure_tags, expected_type=type_hints["infrastructure_tags"])
            check_type(argname="argument mirror_opts", value=mirror_opts, expected_type=type_hints["mirror_opts"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_region is not None:
            self._values["aws_region"] = aws_region
        if infrastructure_tags is not None:
            self._values["infrastructure_tags"] = infrastructure_tags
        if mirror_opts is not None:
            self._values["mirror_opts"] = mirror_opts
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        result = self._values.get("infrastructure_tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mirror_opts(self) -> typing.Optional[_MirrorProps_0e4917bb]:
        '''Options for the upstream Mirror job.'''
        result = self._values.get("mirror_opts")
        return typing.cast(typing.Optional[_MirrorProps_0e4917bb], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of the target Codecommit repository.

        :default: CI_PROJECT_PATH_SLUG.
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MirrorToCodecommitProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IBootstrap)
class Bootstrap(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.Bootstrap",
):
    '''Creates an instance of Bootstrap.'''

    def __init__(
        self,
        *,
        aws_account_id: builtins.str,
        aws_region: builtins.str,
        qualifier: builtins.str,
        toolkit_stack_name: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param aws_account_id: The AWS account ID associated with the Bootstrap configuration.
        :param aws_region: The AWS region in which the Bootstrap will be performed.
        :param qualifier: The qualifier applied to the Bootstrap.
        :param toolkit_stack_name: The name of the toolkit stack used for Bootstrap.
        :param job_name: An optional name for the Bootstrap job.
        :param job_stage: An optional stage for the Bootstrap job.
        :param resource_tags: Optional resource tags that can be applied during Bootstrap.
        '''
        props = BootstrapProps(
            aws_account_id=aws_account_id,
            aws_region=aws_region,
            qualifier=qualifier,
            toolkit_stack_name=toolkit_stack_name,
            job_name=job_name,
            job_stage=job_stage,
            resource_tags=resource_tags,
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
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345629508693ced1cd94cbeb73e6a0aa45f658ad85b738f0503862375cc21929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9e8e5697d4efbb86d8b8d7efc81423974b4263d07d4b7072fa89c5cdae2b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fb7bfd901a6d81f2b66f6692ddebb90b8a5c0a24ef48500f2473e64bf19ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> builtins.str:
        '''The stage of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef002eab7fea225e4eee666f007cbba250672742a1c68fb4555e07b944268cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43432544f5b57864e32d36ab89131267846edcf3cff1e2c4beceaa95b9402183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6127b33bdfbac72509cb5a4154e09698ecd550364889728891e836da082eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c9cd711d477c97863853a6cacfb6cb381536de7b73dbce9801fea520807ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)


@jsii.implements(IDeploy)
class Deploy(_Job_20682b42, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.aws.Deploy"):
    '''A class that manages the configuration and rendering of a Deploy job.

    Inherits from the base Job class and implements the IDeploy interface.
    '''

    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deploy_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        strict: typing.Optional[builtins.bool] = None,
        toolkit_stack_name: typing.Optional[builtins.str] = None,
        wait_for_stack: typing.Optional[builtins.bool] = None,
        wait_for_stack_account_id: typing.Optional[builtins.str] = None,
        wait_for_stack_assume_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates an instance of Deploy.

        :param stacks: An array of stack names to be deployed.
        :param context: Optional context values to provide additional information for deployment.
        :param deploy_options: Optional deployment options.
        :param job_name: An optional name for the Deploy job.
        :param job_stage: An optional stage for the Deploy job.
        :param strict: Enable strict deployment mode.
        :param toolkit_stack_name: Optional toolkit stack name used for deployment.
        :param wait_for_stack: Wait for stacks to complete deployment.
        :param wait_for_stack_account_id: AWS account ID for stack waiting.
        :param wait_for_stack_assume_role: AWS assume role for stack waiting.
        '''
        props = DeployProps(
            stacks=stacks,
            context=context,
            deploy_options=deploy_options,
            job_name=job_name,
            job_stage=job_stage,
            strict=strict,
            toolkit_stack_name=toolkit_stack_name,
            wait_for_stack=wait_for_stack,
            wait_for_stack_account_id=wait_for_stack_account_id,
            wait_for_stack_assume_role=wait_for_stack_assume_role,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Renders the Deploy job's configuration and scripts.

        :return: The rendered configuration and scripts.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2797fdb224a725a4bd66059c4ab27fc34be7997465ac562fd4d5b45eaa5fee6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        '''Flag indicating if strict deployment mode is enabled.'''
        return typing.cast(builtins.bool, jsii.get(self, "strict"))

    @strict.setter
    def strict(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86facbfb66b6d909eab3201ac6daed36490a9776fb03606c898342ad49aa4066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strict", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStack")
    def wait_for_stack(self) -> builtins.bool:
        '''Flag indicating if the deployment should wait for stack completion.'''
        return typing.cast(builtins.bool, jsii.get(self, "waitForStack"))

    @wait_for_stack.setter
    def wait_for_stack(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7627d07e7ae8f46372eaea49102b22c4592e6c3433cf1fe42cf630f6de37c756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStack", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ce934efa4ea94cc6f66bcdec1445872c472f9869b14cb294289b8fd087a867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="deployOptions")
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployOptions"))

    @deploy_options.setter
    def deploy_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd72412768ccde1125b7e24d38be326d29301035b259572231c4b82b2fa8b8aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdb6a877a7b486c8644f8f5d7fb7f2f4c3b5055327b7806bcdc85aa2afd8720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0d5321d88860f3957e5ed8b1a4e73d273a7e4f88b09820b90e069c5e9a496a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf7dcae59ac9b356d035d1e6fd7ec21f9b6f54c1c6c237789066de8a61a839d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAccountId")
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAccountId"))

    @wait_for_stack_account_id.setter
    def wait_for_stack_account_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cab8ac757d8ebfc508ffb6c1de78a796434663f17bf48ec1ba0663b07d44a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAssumeRole")
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAssumeRole"))

    @wait_for_stack_assume_role.setter
    def wait_for_stack_assume_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699e329c4ac72a81d629001e45dc7f534804311fa9e09175ef432417ad69a261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAssumeRole", value)


@jsii.implements(IDiff)
class Diff(_Job_20682b42, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.aws.Diff"):
    '''A class that manages the configuration and rendering of a Diff job.

    Inherits from the base Job class and implements the IDiff interface.
    '''

    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        diff_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates an instance of Diff.

        :param stacks: An array of stack names for which to generate a diff.
        :param context: Optional context values to provide additional information for the diff.
        :param diff_options: Optional diff options to customize the diff process.
        :param job_name: An optional name for the Diff job.
        :param job_stage: An optional stage for the Diff job.
        '''
        props = DiffProps(
            stacks=stacks,
            context=context,
            diff_options=diff_options,
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
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e635c5de14cecc3715f4fb58d6e36078e0e8da141893047aecc1a68e07fa49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5faf7453069590e7f46c866a1e0383a038b6ee798ac9c0b4311f945058a77748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="diffOptions")
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diffOptions"))

    @diff_options.setter
    def diff_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d11287e4b98077c6acd17e0a413b3e993081ceaa15115d1442d6c8974167fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b7ee4f88ddf84e4e62c2251c965e6bd671647dbc1b73a30e702a231918d22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768c905ca685b663270d966338278fadfe45ae54a9a8ade341a57593b0e7a43b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)


@jsii.implements(IDiffDeploy)
class DiffDeploy(
    _JobCollection_0289800c,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.DiffDeploy",
):
    '''A class that manages the configuration and execution of combined Diff and Deploy operations.

    Inherits from the base JobCollection class and implements the IDiffDeploy interface.
    '''

    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Creates an instance of DiffDeploy.

        :param stacks: An array of stack names for which to generate a diff and perform deployment.
        :param context: Optional context values to provide additional information for the diff and deployment.
        '''
        props = DiffDeployProps(stacks=stacks, context=context)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="deployJob")
    def deploy_job(self) -> Deploy:
        '''The instance of the Deploy job associated with this DiffDeploy instance.'''
        return typing.cast(Deploy, jsii.get(self, "deployJob"))

    @deploy_job.setter
    def deploy_job(self, value: Deploy) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08de6025c9975a0cbee0cb34c80d0150391f8e7d062621c66da776f5f4241679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployJob", value)

    @builtins.property
    @jsii.member(jsii_name="diffJob")
    def diff_job(self) -> Diff:
        '''The instance of the Diff job associated with this DiffDeploy instance.'''
        return typing.cast(Diff, jsii.get(self, "diffJob"))

    @diff_job.setter
    def diff_job(self, value: Diff) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f86dcce2d11164333bc145d467996207f2a4c9d53806d8a5a4b27eb080be592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffJob", value)

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36446fe71ede06207f295ac3e774075f404420d2bc0a1e8eae4e6f55ff8621d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe43848877f621900a485ccb4c095bd653224d3355bd6dddd8827b9e9a6b1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)


__all__ = [
    "AWSAccount",
    "Bootstrap",
    "BootstrapProps",
    "Deploy",
    "DeployProps",
    "Diff",
    "DiffDeploy",
    "DiffDeployProps",
    "DiffProps",
    "IBootstrap",
    "IDeploy",
    "IDiff",
    "IDiffDeploy",
    "IMirrorToCodecommit",
    "MirrorToCodecommit",
    "MirrorToCodecommitProps",
]

publication.publish()

def _typecheckingstub__31070e7b2289a2717aab0ff4f0f1bed66e25c7140ed8da33f076bd9c47460b75(
    *,
    aws_account_id: builtins.str,
    aws_region: builtins.str,
    qualifier: builtins.str,
    toolkit_stack_name: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02294d96a01f7b66a9e316c742913ece9eb4c3f6626227ac224647d11c8a3025(
    *,
    stacks: typing.Sequence[builtins.str],
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    deploy_options: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    strict: typing.Optional[builtins.bool] = None,
    toolkit_stack_name: typing.Optional[builtins.str] = None,
    wait_for_stack: typing.Optional[builtins.bool] = None,
    wait_for_stack_account_id: typing.Optional[builtins.str] = None,
    wait_for_stack_assume_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d5da305316074b1a800e6eb9f104d21236b547f739ecd7c7aef8447e9de9a6(
    *,
    stacks: typing.Sequence[builtins.str],
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1918e96efec6fee48e4c72f32431611193c4c817532815d6ef9a3c25a54eb6b5(
    *,
    stacks: typing.Sequence[builtins.str],
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    diff_options: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fdab73e4df6dcb7569b7cfcf017d4722caeb1a90d47e908c35522994ee8d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c9baddac2c982671bac064c5a6cff1e35a30831a68bec6858bbddec5746aa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23c815abb83752c6d23c0eefd04ed200eac35be0e56df3650e08200d0689201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e79c5b454892e75eb3b6923ea4a41ce39dbe490ec105733da8eeb71d112d540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578ca589aa37e1ddc069e901c0dd13cd6174e0bbea8bf7d9ee0446d6c2250694(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6b0414dc0584b0573515b8dd016d1ffaae794252d9c4131b3b82bcf6a5eb34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297d8e836526b09df65136bdf25d7215bc4993464da0dac8cdc95ff8a8bb59f8(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba6699af515ffbb20e58b40d052fb131405b7e45f2782d07fef527da199e5ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e6319c3976c080acd5c7b42c242ef183a7249fa740009830c137c6d448cfe4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8443a0b88a95a5df1e631df0b01b64fb17bf79fe3fe6fe077c13f6948f9e08e1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fad5ae3007754ac6be19e17d3c775219705163589c47c0613434f0866a7929d(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9512a8111e1abbd517c23412dd953f7198ef5ac52ed09040a07a45e76918477b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb69a98763245d4e1a27b7cc8a800b73bfa4ad6b37c79595a2cd009319cbd86(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2ad8dc2d6ff83eaec359d73c436eb16630d51f9aad01bbfe729ef6ebc947b3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080c39538ef57fbfc2d09b127c08e871886da61c14a32e117595906e52338f4f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bf5bc8627d673b182dac28db2014f1641a95c98f82856e5648f649d260707d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40dc8d3631a98fe04346b62b63e91708ceac2fc6e41fe80ceb125149c048ee9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e092ee7b487cd85bae70d35a5e8d29890aeee16f0bb566c8e4884b039c20fa1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5b2d4931c222352952251bec5c5221e9131be5a49877c2b38d5b87206dae9b(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2a6d529aa6b390030366f1b20f27d900b4eb9ab9b6506ba8c06ff85cc3b4cc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cdf226605a65753319029c00ffd23b5ef8df07f035fbe123269245381222d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77158275d48ed38fa0f36eed1b6c1235198d8f23cd9acb59a63179123c54169e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bd20cc1696d9c36cc2fce98bde8b06e14a60b497e74c1005b5dc587f6f0d4b(
    value: Deploy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b7d6e9815ccf9075f2d650cb50a081d15e57ac61f20099d530253a524e7199(
    value: Diff,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabca68ef187c47c86acb9b35809e2c31680fc4d020a5cf23d9e2ff9bddaaa6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be798a421dfe22d560c939836430b6830e93d49855e1c029b27070b37468816c(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d47355cdbcedcd2365cd8618bb48bb85b0793e247ba4980156b49a76b922ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683cab747e03754e4d7ad716d15eb0f1819ad822fe19299bd6878083e41c40ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc24eae8a713c95c1b5e653f03670cdc72d0e118c3a63227e743243f25ff23e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750a0936b37b9d7058361a5391596a0aa87ea2c2a70779024259bf6427be23df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1ed63ef582329b14c18409a05917140b27204dbd8720088423cf7a65e8a46e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2fc9cdeb3653408cf2db32fecbdd42af16230785aca513f9725137bcf06544(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ed4f8b18728fdb65dba607c6f54fa23ac31343dfe64793a4465a5c995aaf21(
    value: typing.Optional[_MirrorProps_0e4917bb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6150e19564bd364764a1c6615a04c9b26f26221395c46dd1f0ec1195f091652e(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    infrastructure_tags: typing.Optional[builtins.str] = None,
    mirror_opts: typing.Optional[typing.Union[_MirrorProps_0e4917bb, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345629508693ced1cd94cbeb73e6a0aa45f658ad85b738f0503862375cc21929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9e8e5697d4efbb86d8b8d7efc81423974b4263d07d4b7072fa89c5cdae2b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fb7bfd901a6d81f2b66f6692ddebb90b8a5c0a24ef48500f2473e64bf19ff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef002eab7fea225e4eee666f007cbba250672742a1c68fb4555e07b944268cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43432544f5b57864e32d36ab89131267846edcf3cff1e2c4beceaa95b9402183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6127b33bdfbac72509cb5a4154e09698ecd550364889728891e836da082eac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c9cd711d477c97863853a6cacfb6cb381536de7b73dbce9801fea520807ba4(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2797fdb224a725a4bd66059c4ab27fc34be7997465ac562fd4d5b45eaa5fee6e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86facbfb66b6d909eab3201ac6daed36490a9776fb03606c898342ad49aa4066(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7627d07e7ae8f46372eaea49102b22c4592e6c3433cf1fe42cf630f6de37c756(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ce934efa4ea94cc6f66bcdec1445872c472f9869b14cb294289b8fd087a867(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd72412768ccde1125b7e24d38be326d29301035b259572231c4b82b2fa8b8aa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdb6a877a7b486c8644f8f5d7fb7f2f4c3b5055327b7806bcdc85aa2afd8720(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0d5321d88860f3957e5ed8b1a4e73d273a7e4f88b09820b90e069c5e9a496a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf7dcae59ac9b356d035d1e6fd7ec21f9b6f54c1c6c237789066de8a61a839d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cab8ac757d8ebfc508ffb6c1de78a796434663f17bf48ec1ba0663b07d44a2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699e329c4ac72a81d629001e45dc7f534804311fa9e09175ef432417ad69a261(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e635c5de14cecc3715f4fb58d6e36078e0e8da141893047aecc1a68e07fa49c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faf7453069590e7f46c866a1e0383a038b6ee798ac9c0b4311f945058a77748(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d11287e4b98077c6acd17e0a413b3e993081ceaa15115d1442d6c8974167fdf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b7ee4f88ddf84e4e62c2251c965e6bd671647dbc1b73a30e702a231918d22d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768c905ca685b663270d966338278fadfe45ae54a9a8ade341a57593b0e7a43b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08de6025c9975a0cbee0cb34c80d0150391f8e7d062621c66da776f5f4241679(
    value: Deploy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f86dcce2d11164333bc145d467996207f2a4c9d53806d8a5a4b27eb080be592(
    value: Diff,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36446fe71ede06207f295ac3e774075f404420d2bc0a1e8eae4e6f55ff8621d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe43848877f621900a485ccb4c095bd653224d3355bd6dddd8827b9e9a6b1a3(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass
