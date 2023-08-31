'''
# `data_launchdarkly_segment`

Refer to the Terraform Registory for docs: [`data_launchdarkly_segment`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment).
'''
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataLaunchdarklySegment(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegment",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment launchdarkly_segment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_key: builtins.str,
        key: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentExcludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        included: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentIncludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment launchdarkly_segment} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_key: The segment's environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#env_key DataLaunchdarklySegment#env_key}
        :param key: The unique key that references the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#key DataLaunchdarklySegment#key}
        :param project_key: The segment's project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#project_key DataLaunchdarklySegment#project_key}
        :param description: The description of the segment's purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#description DataLaunchdarklySegment#description}
        :param excluded: List of user keys excluded from the segment. To target on other context kinds, use the excluded_contexts block attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#excluded DataLaunchdarklySegment#excluded}
        :param excluded_contexts: excluded_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#excluded_contexts DataLaunchdarklySegment#excluded_contexts}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#id DataLaunchdarklySegment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included: List of user keys included in the segment. To target on other context kinds, use the included_contexts block attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#included DataLaunchdarklySegment#included}
        :param included_contexts: included_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#included_contexts DataLaunchdarklySegment#included_contexts}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#rules DataLaunchdarklySegment#rules}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c837f4e960ba4b8b30bc7296b823151349e4bcea9dcd758d1931c67ce5143c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLaunchdarklySegmentConfig(
            env_key=env_key,
            key=key,
            project_key=project_key,
            description=description,
            excluded=excluded,
            excluded_contexts=excluded_contexts,
            id=id,
            included=included,
            included_contexts=included_contexts,
            rules=rules,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putExcludedContexts")
    def put_excluded_contexts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentExcludedContexts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2bf17aa778dbea45fab87f7f272ed6abb9cb002a19f0feb1d558bb9ce18cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedContexts", [value]))

    @jsii.member(jsii_name="putIncludedContexts")
    def put_included_contexts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentIncludedContexts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f94f5595f71c14598b6f0261dee41dde0d2737a61603f21ecb99d57e61a56c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncludedContexts", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddf99954cd50f7797fd24a38cfd37c3be544f2aba486d9b910c9e38039d26e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExcluded")
    def reset_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcluded", []))

    @jsii.member(jsii_name="resetExcludedContexts")
    def reset_excluded_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedContexts", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncluded")
    def reset_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncluded", []))

    @jsii.member(jsii_name="resetIncludedContexts")
    def reset_included_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedContexts", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="excludedContexts")
    def excluded_contexts(self) -> "DataLaunchdarklySegmentExcludedContextsList":
        return typing.cast("DataLaunchdarklySegmentExcludedContextsList", jsii.get(self, "excludedContexts"))

    @builtins.property
    @jsii.member(jsii_name="includedContexts")
    def included_contexts(self) -> "DataLaunchdarklySegmentIncludedContextsList":
        return typing.cast("DataLaunchdarklySegmentIncludedContextsList", jsii.get(self, "includedContexts"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataLaunchdarklySegmentRulesList":
        return typing.cast("DataLaunchdarklySegmentRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="envKeyInput")
    def env_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedContextsInput")
    def excluded_contexts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentExcludedContexts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentExcludedContexts"]]], jsii.get(self, "excludedContextsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedInput")
    def excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includedContextsInput")
    def included_contexts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentIncludedContexts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentIncludedContexts"]]], jsii.get(self, "includedContextsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedInput")
    def included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4768b266b38f10f4a8eebdfb1aeebebad63aca215a8ecd1a066c48d458a2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="envKey")
    def env_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envKey"))

    @env_key.setter
    def env_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e383cc84f32eeeb6db3ae208f5d1bd3590fdc662fbd3bba83fe2e44054af030c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envKey", value)

    @builtins.property
    @jsii.member(jsii_name="excluded")
    def excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excluded"))

    @excluded.setter
    def excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff216858a4d539c5ef58b6afa658d0b9bb9d94f419cf5e1195fe98001123c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excluded", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5acd1e57c60f7e5bc3e6d1978b84749dee9827fb53559b526840024c68388278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="included")
    def included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "included"))

    @included.setter
    def included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945eabbb09a5ed9b844c2614a9859bb33d7df1a885103cd8fd268f98fb44770e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "included", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6f1c6b1bb67cb2e326a4888d0840a0ac3be74f402857a75cde5cf9a74b72b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ca9b834f1c426cb9b9dc964ba00cbce2c89faa9f85780990e6978e57fdf81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "env_key": "envKey",
        "key": "key",
        "project_key": "projectKey",
        "description": "description",
        "excluded": "excluded",
        "excluded_contexts": "excludedContexts",
        "id": "id",
        "included": "included",
        "included_contexts": "includedContexts",
        "rules": "rules",
    },
)
class DataLaunchdarklySegmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        env_key: builtins.str,
        key: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentExcludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        included: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentIncludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_key: The segment's environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#env_key DataLaunchdarklySegment#env_key}
        :param key: The unique key that references the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#key DataLaunchdarklySegment#key}
        :param project_key: The segment's project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#project_key DataLaunchdarklySegment#project_key}
        :param description: The description of the segment's purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#description DataLaunchdarklySegment#description}
        :param excluded: List of user keys excluded from the segment. To target on other context kinds, use the excluded_contexts block attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#excluded DataLaunchdarklySegment#excluded}
        :param excluded_contexts: excluded_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#excluded_contexts DataLaunchdarklySegment#excluded_contexts}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#id DataLaunchdarklySegment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included: List of user keys included in the segment. To target on other context kinds, use the included_contexts block attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#included DataLaunchdarklySegment#included}
        :param included_contexts: included_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#included_contexts DataLaunchdarklySegment#included_contexts}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#rules DataLaunchdarklySegment#rules}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4968e8cf106963aaca9d99652b60495322567d70543e75826303606d06a6f0ab)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_key", value=env_key, expected_type=type_hints["env_key"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
            check_type(argname="argument excluded_contexts", value=excluded_contexts, expected_type=type_hints["excluded_contexts"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument included", value=included, expected_type=type_hints["included"])
            check_type(argname="argument included_contexts", value=included_contexts, expected_type=type_hints["included_contexts"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_key": env_key,
            "key": key,
            "project_key": project_key,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if description is not None:
            self._values["description"] = description
        if excluded is not None:
            self._values["excluded"] = excluded
        if excluded_contexts is not None:
            self._values["excluded_contexts"] = excluded_contexts
        if id is not None:
            self._values["id"] = id
        if included is not None:
            self._values["included"] = included
        if included_contexts is not None:
            self._values["included_contexts"] = included_contexts
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def env_key(self) -> builtins.str:
        '''The segment's environment key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#env_key DataLaunchdarklySegment#env_key}
        '''
        result = self._values.get("env_key")
        assert result is not None, "Required property 'env_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The unique key that references the segment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#key DataLaunchdarklySegment#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The segment's project key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#project_key DataLaunchdarklySegment#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the segment's purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#description DataLaunchdarklySegment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user keys excluded from the segment. To target on other context kinds, use the excluded_contexts block attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#excluded DataLaunchdarklySegment#excluded}
        '''
        result = self._values.get("excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_contexts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentExcludedContexts"]]]:
        '''excluded_contexts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#excluded_contexts DataLaunchdarklySegment#excluded_contexts}
        '''
        result = self._values.get("excluded_contexts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentExcludedContexts"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#id DataLaunchdarklySegment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user keys included in the segment. To target on other context kinds, use the included_contexts block attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#included DataLaunchdarklySegment#included}
        '''
        result = self._values.get("included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_contexts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentIncludedContexts"]]]:
        '''included_contexts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#included_contexts DataLaunchdarklySegment#included_contexts}
        '''
        result = self._values.get("included_contexts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentIncludedContexts"]]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#rules DataLaunchdarklySegment#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklySegmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentExcludedContexts",
    jsii_struct_bases=[],
    name_mapping={"context_kind": "contextKind", "values": "values"},
)
class DataLaunchdarklySegmentExcludedContexts:
    def __init__(
        self,
        *,
        context_kind: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param context_kind: The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#context_kind DataLaunchdarklySegment#context_kind}
        :param values: List of target object keys included in or excluded from the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#values DataLaunchdarklySegment#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43895aa1918d204f8a9fa02178bd67bf98f115a50c784448a8ef3482177c0c94)
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_kind": context_kind,
            "values": values,
        }

    @builtins.property
    def context_kind(self) -> builtins.str:
        '''The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#context_kind DataLaunchdarklySegment#context_kind}
        '''
        result = self._values.get("context_kind")
        assert result is not None, "Required property 'context_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of target object keys included in or excluded from the segment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#values DataLaunchdarklySegment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklySegmentExcludedContexts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklySegmentExcludedContextsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentExcludedContextsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e0360f00211ff9d100f1c51c5f8ed097e21989f195f8d2217c1e993ad7b78d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklySegmentExcludedContextsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce0bd74a9552c800b19b26ae977280c04d82648f8972021ab9c177a806f5e43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklySegmentExcludedContextsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc414f6465b5271eec9c1a8f51d27aca3711676a018e3c63c404d9011531c72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d56cf677c183192e352ca9632bf1eeb2b02e493479e02d97d28e4201c9ca5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd6660333e820526af3d9cf956f6c44e8668adc345120c7b1437d1a45adbf3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentExcludedContexts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentExcludedContexts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentExcludedContexts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9beb5e0763b331f5c4d45d5d48962022cb966f57adcfb507970a91ed3d0ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklySegmentExcludedContextsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentExcludedContextsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe4a9ba35cd1fe0cc6e62f26c58c5755f1669178b6750b5327b789305877a62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467827ac2880027b52b62d81468b67d9f73c2c66a3c2d71b6a80a22ef3cfa000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32b3945e8afade607826f023da3c208bc1da19a812eeef2acbdca1b2cd17644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentExcludedContexts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentExcludedContexts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentExcludedContexts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e7a4fe6505beb05072ea144fa0d5a10c18baa84f0e0970acd31f0670086c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentIncludedContexts",
    jsii_struct_bases=[],
    name_mapping={"context_kind": "contextKind", "values": "values"},
)
class DataLaunchdarklySegmentIncludedContexts:
    def __init__(
        self,
        *,
        context_kind: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param context_kind: The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#context_kind DataLaunchdarklySegment#context_kind}
        :param values: List of target object keys included in or excluded from the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#values DataLaunchdarklySegment#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6209c8fae46aa3d0de8df79171086bdaed2add2b58568c64baf810fe770981f4)
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_kind": context_kind,
            "values": values,
        }

    @builtins.property
    def context_kind(self) -> builtins.str:
        '''The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#context_kind DataLaunchdarklySegment#context_kind}
        '''
        result = self._values.get("context_kind")
        assert result is not None, "Required property 'context_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of target object keys included in or excluded from the segment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#values DataLaunchdarklySegment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklySegmentIncludedContexts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklySegmentIncludedContextsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentIncludedContextsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f32c5244433932b351d411e5522ba0ab5a4ae6beb1bc39273ac6a4f52037249)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklySegmentIncludedContextsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206b6b0327395711ce2dcb55dec23da787a122c9c0ae9f3113c5b456587c6837)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklySegmentIncludedContextsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6f8adc9519a929fe8fb8cced756f7d0427e5f64772a7a8d87f59a89f7bc6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524e42ff93472585df7e725f6fbeb22671c6453c6ee2a6970c9bb4c10fe4adc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744e0538b6ccaaf7b87b97288eda188739b994e79ebba0591797215365cf44ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentIncludedContexts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentIncludedContexts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentIncludedContexts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f18b32b424e123eca63f07ffe11f080ef742011864e37ea5766f107feb302f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklySegmentIncludedContextsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentIncludedContextsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a6de19301fda5a88020501abd690c3ba517ca3fd4add00b4d8e5c29d74aa87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e57dcf1be516992d1dbe99ac3f4ffb4bc30122d0b8ba4179763a4ad8df721f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da96041c2728f70d45bce64dfd998a6270c82ce1edb2286c57ffbe6d6abd141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentIncludedContexts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentIncludedContexts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentIncludedContexts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2364e333b82ccd2685d857235c82d74a24f75d967a23eac541f15f1e0a29bf16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_by": "bucketBy",
        "clauses": "clauses",
        "rollout_context_kind": "rolloutContextKind",
        "weight": "weight",
    },
)
class DataLaunchdarklySegmentRules:
    def __init__(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklySegmentRulesClauses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rollout_context_kind: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: The attribute by which to group users together. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#bucket_by DataLaunchdarklySegment#bucket_by}
        :param clauses: clauses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#clauses DataLaunchdarklySegment#clauses}
        :param rollout_context_kind: The context kind associated with this segment rule. This argument is only valid if weight is also specified. If omitted, defaults to 'user' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#rollout_context_kind DataLaunchdarklySegment#rollout_context_kind}
        :param weight: The integer weight of the rule (between 1 and 100000). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#weight DataLaunchdarklySegment#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f4f03d68b887f06222b642ffd079b9152f7d52848f03ead9ca6a86780556f7)
            check_type(argname="argument bucket_by", value=bucket_by, expected_type=type_hints["bucket_by"])
            check_type(argname="argument clauses", value=clauses, expected_type=type_hints["clauses"])
            check_type(argname="argument rollout_context_kind", value=rollout_context_kind, expected_type=type_hints["rollout_context_kind"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_by is not None:
            self._values["bucket_by"] = bucket_by
        if clauses is not None:
            self._values["clauses"] = clauses
        if rollout_context_kind is not None:
            self._values["rollout_context_kind"] = rollout_context_kind
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def bucket_by(self) -> typing.Optional[builtins.str]:
        '''The attribute by which to group users together.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#bucket_by DataLaunchdarklySegment#bucket_by}
        '''
        result = self._values.get("bucket_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clauses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentRulesClauses"]]]:
        '''clauses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#clauses DataLaunchdarklySegment#clauses}
        '''
        result = self._values.get("clauses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklySegmentRulesClauses"]]], result)

    @builtins.property
    def rollout_context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with this segment rule.

        This argument is only valid if weight is also specified. If omitted, defaults to 'user'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#rollout_context_kind DataLaunchdarklySegment#rollout_context_kind}
        '''
        result = self._values.get("rollout_context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''The integer weight of the rule (between 1 and 100000).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#weight DataLaunchdarklySegment#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklySegmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentRulesClauses",
    jsii_struct_bases=[],
    name_mapping={
        "attribute": "attribute",
        "op": "op",
        "values": "values",
        "context_kind": "contextKind",
        "negate": "negate",
        "value_type": "valueType",
    },
)
class DataLaunchdarklySegmentRulesClauses:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        op: builtins.str,
        values: typing.Sequence[builtins.str],
        context_kind: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: The user attribute to operate on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#attribute DataLaunchdarklySegment#attribute}
        :param op: The operator associated with the rule clause. Available options are ``in``, ``endsWith``, ``startsWith``, ``matches``, ``contains``, ``lessThan``, ``lessThanOrEqual``, ``greaterThanOrEqual``, ``before``, ``after``, ``segmentMatch``, ``semVerEqual``, ``semVerLessThan``, and ``semVerGreaterThan``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#op DataLaunchdarklySegment#op}
        :param values: The list of values associated with the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#values DataLaunchdarklySegment#values}
        :param context_kind: The context kind associated with this rule clause. This argument is only valid if ``rollout_weights`` is also specified. If omitted, defaults to ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#context_kind DataLaunchdarklySegment#context_kind}
        :param negate: Whether to negate the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#negate DataLaunchdarklySegment#negate}
        :param value_type: The type for each of the clause's values. Available types are ``boolean``, ``string``, and ``number``. If omitted, ``value_type`` defaults to ``string``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#value_type DataLaunchdarklySegment#value_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779e2e4abca72771dd965b3afcebbcd0e575524822f4e39a990b1acf55258917)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument op", value=op, expected_type=type_hints["op"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute": attribute,
            "op": op,
            "values": values,
        }
        if context_kind is not None:
            self._values["context_kind"] = context_kind
        if negate is not None:
            self._values["negate"] = negate
        if value_type is not None:
            self._values["value_type"] = value_type

    @builtins.property
    def attribute(self) -> builtins.str:
        '''The user attribute to operate on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#attribute DataLaunchdarklySegment#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def op(self) -> builtins.str:
        '''The operator associated with the rule clause.

        Available options are ``in``, ``endsWith``, ``startsWith``, ``matches``, ``contains``, ``lessThan``, ``lessThanOrEqual``, ``greaterThanOrEqual``, ``before``, ``after``, ``segmentMatch``, ``semVerEqual``, ``semVerLessThan``, and ``semVerGreaterThan``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#op DataLaunchdarklySegment#op}
        '''
        result = self._values.get("op")
        assert result is not None, "Required property 'op' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The list of values associated with the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#values DataLaunchdarklySegment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with this rule clause.

        This argument is only valid if ``rollout_weights`` is also specified. If omitted, defaults to ``user``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#context_kind DataLaunchdarklySegment#context_kind}
        '''
        result = self._values.get("context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to negate the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#negate DataLaunchdarklySegment#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''The type for each of the clause's values.

        Available types are ``boolean``, ``string``, and ``number``. If omitted, ``value_type`` defaults to ``string``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.15.1/docs/data-sources/segment#value_type DataLaunchdarklySegment#value_type}
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklySegmentRulesClauses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklySegmentRulesClausesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentRulesClausesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99d89e576b2e2f163039945f29eb627c900cec33396b52bf440233dbb4df054)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklySegmentRulesClausesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4ddd2fbf757e6ff4b1400c41320470a1cd2992c62ee7c44c1763a0c901360c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklySegmentRulesClausesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de589ac151ed3268a354210c3b2011ab53f9de88b0852e84c51bfe482f5dcffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecfa96a7358d9a8f6a4972fc5562e5d9f30aa79027f5ca87efa57f8ec738db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccd0d1e8c453a94c2e1e3f654c947aaea9af4f4c846667d6151864ca7ac7b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRulesClauses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRulesClauses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca537f66f2535e8a8c0707562a6359838d5b58d80cd3ddb8aaee70dc0af781d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklySegmentRulesClausesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentRulesClausesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c470acb7ed37fb7ffdcffb94bcb88003d3401a31faafece7c3e826993162e47b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContextKind")
    def reset_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextKind", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @jsii.member(jsii_name="resetValueType")
    def reset_value_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueType", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="opInput")
    def op_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2792c167315c6d7ccf3175586c50a046e8791e5446b256b246cd6f2613504dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value)

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53875da34e14a41a56e7a736318cd575b3cf483613755d34fcca9f2736c5cb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value)

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5648c28e9fe78b771cacc5ea2aadfe3dcd3070912b10c941f1def2e5aaf06cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value)

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123acb968d0b691941af13260e595cbc3735f18f8cc331e6ff02fe51944b4d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2703f51893ec174ad8d196476ef7ed4dedf4923fc222163b0557f77e0b7155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc95ad4ebec0339842b385231a28a6c0531883e0681accf8b6d85fade6bdffa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRulesClauses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRulesClauses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRulesClauses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b585bc5be53f42b0cec57307d20cd71fd9438eb9a192d898dd71191a5a678b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklySegmentRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentRulesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc9f4ff7fb6062a8dd182337b45d41be9501f43a9e12b65353fe3b69ee12b51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataLaunchdarklySegmentRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ebfe7382e6cdbc11c9a86ae44a013e5dc00dcdbf72c1eb846ce8b0639f19ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklySegmentRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519bc9cc3ee23eeb1ffa240de7530c018e2b2d56991e057da4b6bf6a63a66a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba796b485e49060c6daa00323f8db5897f69b283e045e10af2139c27439bc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28d7ab70c92e2151c73ed2ee79b211630bfd7c27ae82e0ed709bc2503d6869c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f71c2d7f6dcf17976d4a6704df4eca47f5ff0208757147f466993dc3a407c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklySegmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklySegment.DataLaunchdarklySegmentRulesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac4dff81361f21d5063fcddf6246b6069428ae607e5a55bf1a2bc4f5764b41e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClauses")
    def put_clauses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873c3bc5eca14b6615aedfc0e60888b5b333dde5657796ffddc2aa66ecafa4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClauses", [value]))

    @jsii.member(jsii_name="resetBucketBy")
    def reset_bucket_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketBy", []))

    @jsii.member(jsii_name="resetClauses")
    def reset_clauses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClauses", []))

    @jsii.member(jsii_name="resetRolloutContextKind")
    def reset_rollout_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutContextKind", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="clauses")
    def clauses(self) -> DataLaunchdarklySegmentRulesClausesList:
        return typing.cast(DataLaunchdarklySegmentRulesClausesList, jsii.get(self, "clauses"))

    @builtins.property
    @jsii.member(jsii_name="bucketByInput")
    def bucket_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketByInput"))

    @builtins.property
    @jsii.member(jsii_name="clausesInput")
    def clauses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRulesClauses]]], jsii.get(self, "clausesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutContextKindInput")
    def rollout_context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rolloutContextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @bucket_by.setter
    def bucket_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4112087707b46ccb9cb0c25bbbbab905001029a30e0f1728fa83db33e41ef5af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketBy", value)

    @builtins.property
    @jsii.member(jsii_name="rolloutContextKind")
    def rollout_context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutContextKind"))

    @rollout_context_kind.setter
    def rollout_context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1069906e214a08ea3483cce497dcb10702f52622f731fa9312d6a9e1d02174f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutContextKind", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f7d91195d3f22ea94ae3a0cc73335c40de830618f278fbb2dadf50d8cb2d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69807a1d7806f407c29fd443c264e0ec8a556aff9b5a985e96ab27b9f2cdd854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataLaunchdarklySegment",
    "DataLaunchdarklySegmentConfig",
    "DataLaunchdarklySegmentExcludedContexts",
    "DataLaunchdarklySegmentExcludedContextsList",
    "DataLaunchdarklySegmentExcludedContextsOutputReference",
    "DataLaunchdarklySegmentIncludedContexts",
    "DataLaunchdarklySegmentIncludedContextsList",
    "DataLaunchdarklySegmentIncludedContextsOutputReference",
    "DataLaunchdarklySegmentRules",
    "DataLaunchdarklySegmentRulesClauses",
    "DataLaunchdarklySegmentRulesClausesList",
    "DataLaunchdarklySegmentRulesClausesOutputReference",
    "DataLaunchdarklySegmentRulesList",
    "DataLaunchdarklySegmentRulesOutputReference",
]

publication.publish()

def _typecheckingstub__95c837f4e960ba4b8b30bc7296b823151349e4bcea9dcd758d1931c67ce5143c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_key: builtins.str,
    key: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentExcludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    included: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentIncludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2bf17aa778dbea45fab87f7f272ed6abb9cb002a19f0feb1d558bb9ce18cec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentExcludedContexts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f94f5595f71c14598b6f0261dee41dde0d2737a61603f21ecb99d57e61a56c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentIncludedContexts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddf99954cd50f7797fd24a38cfd37c3be544f2aba486d9b910c9e38039d26e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4768b266b38f10f4a8eebdfb1aeebebad63aca215a8ecd1a066c48d458a2f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e383cc84f32eeeb6db3ae208f5d1bd3590fdc662fbd3bba83fe2e44054af030c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff216858a4d539c5ef58b6afa658d0b9bb9d94f419cf5e1195fe98001123c41(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acd1e57c60f7e5bc3e6d1978b84749dee9827fb53559b526840024c68388278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945eabbb09a5ed9b844c2614a9859bb33d7df1a885103cd8fd268f98fb44770e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6f1c6b1bb67cb2e326a4888d0840a0ac3be74f402857a75cde5cf9a74b72b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ca9b834f1c426cb9b9dc964ba00cbce2c89faa9f85780990e6978e57fdf81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4968e8cf106963aaca9d99652b60495322567d70543e75826303606d06a6f0ab(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_key: builtins.str,
    key: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentExcludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    included: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentIncludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43895aa1918d204f8a9fa02178bd67bf98f115a50c784448a8ef3482177c0c94(
    *,
    context_kind: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e0360f00211ff9d100f1c51c5f8ed097e21989f195f8d2217c1e993ad7b78d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce0bd74a9552c800b19b26ae977280c04d82648f8972021ab9c177a806f5e43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc414f6465b5271eec9c1a8f51d27aca3711676a018e3c63c404d9011531c72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d56cf677c183192e352ca9632bf1eeb2b02e493479e02d97d28e4201c9ca5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd6660333e820526af3d9cf956f6c44e8668adc345120c7b1437d1a45adbf3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9beb5e0763b331f5c4d45d5d48962022cb966f57adcfb507970a91ed3d0ef8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentExcludedContexts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe4a9ba35cd1fe0cc6e62f26c58c5755f1669178b6750b5327b789305877a62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467827ac2880027b52b62d81468b67d9f73c2c66a3c2d71b6a80a22ef3cfa000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32b3945e8afade607826f023da3c208bc1da19a812eeef2acbdca1b2cd17644(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e7a4fe6505beb05072ea144fa0d5a10c18baa84f0e0970acd31f0670086c1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentExcludedContexts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6209c8fae46aa3d0de8df79171086bdaed2add2b58568c64baf810fe770981f4(
    *,
    context_kind: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f32c5244433932b351d411e5522ba0ab5a4ae6beb1bc39273ac6a4f52037249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206b6b0327395711ce2dcb55dec23da787a122c9c0ae9f3113c5b456587c6837(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6f8adc9519a929fe8fb8cced756f7d0427e5f64772a7a8d87f59a89f7bc6a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524e42ff93472585df7e725f6fbeb22671c6453c6ee2a6970c9bb4c10fe4adc5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744e0538b6ccaaf7b87b97288eda188739b994e79ebba0591797215365cf44ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f18b32b424e123eca63f07ffe11f080ef742011864e37ea5766f107feb302f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentIncludedContexts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a6de19301fda5a88020501abd690c3ba517ca3fd4add00b4d8e5c29d74aa87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e57dcf1be516992d1dbe99ac3f4ffb4bc30122d0b8ba4179763a4ad8df721f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da96041c2728f70d45bce64dfd998a6270c82ce1edb2286c57ffbe6d6abd141(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2364e333b82ccd2685d857235c82d74a24f75d967a23eac541f15f1e0a29bf16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentIncludedContexts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f4f03d68b887f06222b642ffd079b9152f7d52848f03ead9ca6a86780556f7(
    *,
    bucket_by: typing.Optional[builtins.str] = None,
    clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rollout_context_kind: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779e2e4abca72771dd965b3afcebbcd0e575524822f4e39a990b1acf55258917(
    *,
    attribute: builtins.str,
    op: builtins.str,
    values: typing.Sequence[builtins.str],
    context_kind: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99d89e576b2e2f163039945f29eb627c900cec33396b52bf440233dbb4df054(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4ddd2fbf757e6ff4b1400c41320470a1cd2992c62ee7c44c1763a0c901360c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de589ac151ed3268a354210c3b2011ab53f9de88b0852e84c51bfe482f5dcffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecfa96a7358d9a8f6a4972fc5562e5d9f30aa79027f5ca87efa57f8ec738db3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccd0d1e8c453a94c2e1e3f654c947aaea9af4f4c846667d6151864ca7ac7b8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca537f66f2535e8a8c0707562a6359838d5b58d80cd3ddb8aaee70dc0af781d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRulesClauses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470acb7ed37fb7ffdcffb94bcb88003d3401a31faafece7c3e826993162e47b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2792c167315c6d7ccf3175586c50a046e8791e5446b256b246cd6f2613504dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53875da34e14a41a56e7a736318cd575b3cf483613755d34fcca9f2736c5cb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5648c28e9fe78b771cacc5ea2aadfe3dcd3070912b10c941f1def2e5aaf06cd7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123acb968d0b691941af13260e595cbc3735f18f8cc331e6ff02fe51944b4d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2703f51893ec174ad8d196476ef7ed4dedf4923fc222163b0557f77e0b7155(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc95ad4ebec0339842b385231a28a6c0531883e0681accf8b6d85fade6bdffa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b585bc5be53f42b0cec57307d20cd71fd9438eb9a192d898dd71191a5a678b51(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRulesClauses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc9f4ff7fb6062a8dd182337b45d41be9501f43a9e12b65353fe3b69ee12b51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ebfe7382e6cdbc11c9a86ae44a013e5dc00dcdbf72c1eb846ce8b0639f19ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519bc9cc3ee23eeb1ffa240de7530c018e2b2d56991e057da4b6bf6a63a66a9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba796b485e49060c6daa00323f8db5897f69b283e045e10af2139c27439bc57(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28d7ab70c92e2151c73ed2ee79b211630bfd7c27ae82e0ed709bc2503d6869c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f71c2d7f6dcf17976d4a6704df4eca47f5ff0208757147f466993dc3a407c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklySegmentRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac4dff81361f21d5063fcddf6246b6069428ae607e5a55bf1a2bc4f5764b41e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873c3bc5eca14b6615aedfc0e60888b5b333dde5657796ffddc2aa66ecafa4cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklySegmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4112087707b46ccb9cb0c25bbbbab905001029a30e0f1728fa83db33e41ef5af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1069906e214a08ea3483cce497dcb10702f52622f731fa9312d6a9e1d02174f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f7d91195d3f22ea94ae3a0cc73335c40de830618f278fbb2dadf50d8cb2d2a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69807a1d7806f407c29fd443c264e0ec8a556aff9b5a985e96ab27b9f2cdd854(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklySegmentRules]],
) -> None:
    """Type checking stubs"""
    pass
