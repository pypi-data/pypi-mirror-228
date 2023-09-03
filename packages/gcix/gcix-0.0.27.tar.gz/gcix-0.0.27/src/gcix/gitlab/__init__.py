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
from ..python import (
    PipInstallRequirementsProps as _PipInstallRequirementsProps_47c04e0d
)


@jsii.data_type(
    jsii_type="@gcix/gcix.gitlab.AsciiDoctorProps",
    jsii_struct_bases=[],
    name_mapping={
        "out_file": "outFile",
        "source": "source",
        "job_name": "jobName",
        "job_stage": "jobStage",
    },
)
class AsciiDoctorProps:
    def __init__(
        self,
        *,
        out_file: builtins.str,
        source: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param out_file: Output HTML file.
        :param source: Source .adoc files to translate to HTML files.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7132915104c1e28f93aaf25f2731fbbd7c6e9f854412643b5c17b300a7cca0)
            check_type(argname="argument out_file", value=out_file, expected_type=type_hints["out_file"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "out_file": out_file,
            "source": source,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        result = self._values.get("out_file")
        assert result is not None, "Required property 'out_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsciiDoctorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitlabScripts(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.gitlab.GitlabScripts",
):
    '''GitlabScripts Class Documentation.

    The ``GitlabScripts`` class provides utility methods for performing various Git-related actions in the context of GitLab.
    '''

    @jsii.member(jsii_name="cloneRepository")
    @builtins.classmethod
    def clone_repository(
        cls,
        path: builtins.str,
        branch: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Clones a repository from a remote Git server using the Git command.

        :param path: - The path of the repository to clone. Should start with a forward slash ("/").
        :param branch: - (Optional) The branch name to clone from the remote repository. Currently, only "main" is supported.

        :return: A Git clone command as a string with the provided branch and repository path.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd5b76126699d26330d7dfeb3122212a724ea05dd5a006bbd12e60b24819200)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "cloneRepository", [path, branch]))


@jsii.interface(jsii_type="@gcix/gcix.gitlab.IAsciiDoctor")
class IAsciiDoctor(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="outFile")
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        ...

    @out_file.setter
    def out_file(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        ...

    @source.setter
    def source(self, value: builtins.str) -> None:
        ...


class _IAsciiDoctorProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.gitlab.IAsciiDoctor"

    @builtins.property
    @jsii.member(jsii_name="outFile")
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        return typing.cast(builtins.str, jsii.get(self, "outFile"))

    @out_file.setter
    def out_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986e7b1c4d37953f582f0432129b370d2a8f40e7f579d7277a9b8c83ee857ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outFile", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e22bfa0393cea581ab23f65174b132decd7152b08c7c8bdfee691f32d25c1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAsciiDoctor).__jsii_proxy_class__ = lambda : _IAsciiDoctorProxy


@jsii.interface(jsii_type="@gcix/gcix.gitlab.IPdoc3")
class IPdoc3(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        ...

    @module.setter
    def module(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        ...

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        ...


class _IPdoc3Proxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.gitlab.IPdoc3"

    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        return typing.cast(builtins.str, jsii.get(self, "module"))

    @module.setter
    def module(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b4711b5ed7cc1964e02667cecaab2f8541b17b7a37fe4e685497acba0ebf77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value)

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputPath"))

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd311f71f58baa7951243c652ee544a02794ecf765e33f85ad33a86afa9afc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPdoc3).__jsii_proxy_class__ = lambda : _IPdoc3Proxy


@jsii.interface(jsii_type="@gcix/gcix.gitlab.ISphinx")
class ISphinx(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="pip")
    def pip(self) -> typing.Optional[_PipInstallRequirementsProps_47c04e0d]:
        ...

    @pip.setter
    def pip(
        self,
        value: typing.Optional[_PipInstallRequirementsProps_47c04e0d],
    ) -> None:
        ...


class _ISphinxProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.gitlab.ISphinx"

    @builtins.property
    @jsii.member(jsii_name="pip")
    def pip(self) -> typing.Optional[_PipInstallRequirementsProps_47c04e0d]:
        return typing.cast(typing.Optional[_PipInstallRequirementsProps_47c04e0d], jsii.get(self, "pip"))

    @pip.setter
    def pip(
        self,
        value: typing.Optional[_PipInstallRequirementsProps_47c04e0d],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff0c8b999a2e721d85e25b3fdc3a421a3f143339c958a75bba01a821d8669c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pip", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISphinx).__jsii_proxy_class__ = lambda : _ISphinxProxy


@jsii.implements(IPdoc3)
class Pdoc3(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.gitlab.Pdoc3",
):
    '''Generate a HTML API documentation of you python code as Gitlab Pages.

    Runs ``pdoc3 --html -f --skip-errors --output-dir public{path} {module}`` and stores the output
    as artifact under the ``public`` directory.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: pdoc3-pages
    - stage: build
    - artifacts: Path 'public'
    '''

    def __init__(
        self,
        *,
        module: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module: The Python module name. This may be an import path resolvable in the current environment, or a file path to a Python module or package.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param output_path: A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to. Defaults to "/".
        '''
        props = Pdoc3Props(
            module=module,
            job_name=job_name,
            job_stage=job_stage,
            output_path=output_path,
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
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        return typing.cast(builtins.str, jsii.get(self, "module"))

    @module.setter
    def module(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52c466b0ede169d0823465be0a6c525295bf03c780b3c1e324b5abe9f65f3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value)

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputPath"))

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2e9be7d530c14072245cfb7e09b7df8b16ac53865c00178278706f8fa969ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputPath", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.gitlab.Pdoc3Props",
    jsii_struct_bases=[],
    name_mapping={
        "module": "module",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "output_path": "outputPath",
    },
)
class Pdoc3Props:
    def __init__(
        self,
        *,
        module: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module: The Python module name. This may be an import path resolvable in the current environment, or a file path to a Python module or package.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param output_path: A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to. Defaults to "/".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894c6dd2d2099f13f1c615b1c0c615904a7bc6a67e0fbefa6d05eb75a8a4b8c9)
            check_type(argname="argument module", value=module, expected_type=type_hints["module"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument output_path", value=output_path, expected_type=type_hints["output_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module": module,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if output_path is not None:
            self._values["output_path"] = output_path

    @builtins.property
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        result = self._values.get("module")
        assert result is not None, "Required property 'module' is missing"
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
    def output_path(self) -> typing.Optional[builtins.str]:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Pdoc3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISphinx)
class Sphinx(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.gitlab.Sphinx",
):
    '''Runs ``sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}`` and installs project requirements. Uses: (``PythonScripts.PipInstallRequirements()``).

    - Requires a ``docs/requirements.txt`` in your project folder``containing at least``sphinx`
    - Creates artifacts for Gitlab Pages under ``pages``

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: sphinx-pages
    - stage: build
    - artifacts: Path 'public'
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip: typing.Optional[typing.Union[_PipInstallRequirementsProps_47c04e0d, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param pip: 
        '''
        props = SphinxProps(job_name=job_name, job_stage=job_stage, pip=pip)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="pip")
    def pip(self) -> typing.Optional[_PipInstallRequirementsProps_47c04e0d]:
        return typing.cast(typing.Optional[_PipInstallRequirementsProps_47c04e0d], jsii.get(self, "pip"))

    @pip.setter
    def pip(
        self,
        value: typing.Optional[_PipInstallRequirementsProps_47c04e0d],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba934d53021d8b677583643cf6cee657028225043062283fa4c8b381275c84b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pip", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.gitlab.SphinxProps",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage", "pip": "pip"},
)
class SphinxProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip: typing.Optional[typing.Union[_PipInstallRequirementsProps_47c04e0d, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param pip: 
        '''
        if isinstance(pip, dict):
            pip = _PipInstallRequirementsProps_47c04e0d(**pip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f6ee08585e5c3ba1f3ac41978b73084c14e1f578cd08c4a74a104559871264)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument pip", value=pip, expected_type=type_hints["pip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if pip is not None:
            self._values["pip"] = pip

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
    def pip(self) -> typing.Optional[_PipInstallRequirementsProps_47c04e0d]:
        result = self._values.get("pip")
        return typing.cast(typing.Optional[_PipInstallRequirementsProps_47c04e0d], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SphinxProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAsciiDoctor)
class AsciiDoctor(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.gitlab.AsciiDoctor",
):
    '''Translate the AsciiDoc source FILE as Gitlab Pages HTML5 file.

    Runs ``asciidoctor {source} -o public{out_file}``and stores the output
    as artifact under the ``public`` directory.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: asciidoctor-pages
    - stage: build
    - image: ruby:3-alpine
    - artifacts: Path 'public'
    '''

    def __init__(
        self,
        *,
        out_file: builtins.str,
        source: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param out_file: Output HTML file.
        :param source: Source .adoc files to translate to HTML files.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        props = AsciiDoctorProps(
            out_file=out_file, source=source, job_name=job_name, job_stage=job_stage
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
    @jsii.member(jsii_name="outFile")
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        return typing.cast(builtins.str, jsii.get(self, "outFile"))

    @out_file.setter
    def out_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8747b82406388b2026810b280565a77530dee288a4a3586657b9c4e19d081e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outFile", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e302f26bea92903bd63af19a2ca142c32aea2a1a8bdc13285bcffd3af7bc68d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)


__all__ = [
    "AsciiDoctor",
    "AsciiDoctorProps",
    "GitlabScripts",
    "IAsciiDoctor",
    "IPdoc3",
    "ISphinx",
    "Pdoc3",
    "Pdoc3Props",
    "Sphinx",
    "SphinxProps",
]

publication.publish()

def _typecheckingstub__8c7132915104c1e28f93aaf25f2731fbbd7c6e9f854412643b5c17b300a7cca0(
    *,
    out_file: builtins.str,
    source: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd5b76126699d26330d7dfeb3122212a724ea05dd5a006bbd12e60b24819200(
    path: builtins.str,
    branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986e7b1c4d37953f582f0432129b370d2a8f40e7f579d7277a9b8c83ee857ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e22bfa0393cea581ab23f65174b132decd7152b08c7c8bdfee691f32d25c1f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b4711b5ed7cc1964e02667cecaab2f8541b17b7a37fe4e685497acba0ebf77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd311f71f58baa7951243c652ee544a02794ecf765e33f85ad33a86afa9afc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff0c8b999a2e721d85e25b3fdc3a421a3f143339c958a75bba01a821d8669c9(
    value: typing.Optional[_PipInstallRequirementsProps_47c04e0d],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52c466b0ede169d0823465be0a6c525295bf03c780b3c1e324b5abe9f65f3be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2e9be7d530c14072245cfb7e09b7df8b16ac53865c00178278706f8fa969ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894c6dd2d2099f13f1c615b1c0c615904a7bc6a67e0fbefa6d05eb75a8a4b8c9(
    *,
    module: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    output_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba934d53021d8b677583643cf6cee657028225043062283fa4c8b381275c84b(
    value: typing.Optional[_PipInstallRequirementsProps_47c04e0d],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f6ee08585e5c3ba1f3ac41978b73084c14e1f578cd08c4a74a104559871264(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    pip: typing.Optional[typing.Union[_PipInstallRequirementsProps_47c04e0d, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8747b82406388b2026810b280565a77530dee288a4a3586657b9c4e19d081e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e302f26bea92903bd63af19a2ca142c32aea2a1a8bdc13285bcffd3af7bc68d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
