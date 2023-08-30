# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class AcquireClusterAdminRoleRequest(AbstractModel):
    """AcquireClusterAdminRole请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AcquireClusterAdminRoleResponse(AbstractModel):
    """AcquireClusterAdminRole返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class AddClusterCIDRRequest(AbstractModel):
    """AddClusterCIDR请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ClusterCIDRs: 增加的ClusterCIDR
        :type ClusterCIDRs: list of str
        :param _IgnoreClusterCIDRConflict: 是否忽略ClusterCIDR与VPC路由表的冲突
        :type IgnoreClusterCIDRConflict: bool
        """
        self._ClusterId = None
        self._ClusterCIDRs = None
        self._IgnoreClusterCIDRConflict = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterCIDRs(self):
        return self._ClusterCIDRs

    @ClusterCIDRs.setter
    def ClusterCIDRs(self, ClusterCIDRs):
        self._ClusterCIDRs = ClusterCIDRs

    @property
    def IgnoreClusterCIDRConflict(self):
        return self._IgnoreClusterCIDRConflict

    @IgnoreClusterCIDRConflict.setter
    def IgnoreClusterCIDRConflict(self, IgnoreClusterCIDRConflict):
        self._IgnoreClusterCIDRConflict = IgnoreClusterCIDRConflict


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterCIDRs = params.get("ClusterCIDRs")
        self._IgnoreClusterCIDRConflict = params.get("IgnoreClusterCIDRConflict")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddClusterCIDRResponse(AbstractModel):
    """AddClusterCIDR返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class AddExistedInstancesRequest(AbstractModel):
    """AddExistedInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _InstanceIds: 实例列表，不支持竞价实例
        :type InstanceIds: list of str
        :param _InstanceAdvancedSettings: 实例额外需要设置参数信息(默认值)
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tencentcloud.tke.v20180525.models.EnhancedService`
        :param _LoginSettings: 节点登录信息（目前仅支持使用Password或者单个KeyIds）
        :type LoginSettings: :class:`tencentcloud.tke.v20180525.models.LoginSettings`
        :param _HostName: 重装系统时，可以指定修改实例的HostName(集群为HostName模式时，此参数必传，规则名称除不支持大写字符外与[CVM创建实例](https://cloud.tencent.com/document/product/213/15730)接口HostName一致)
        :type HostName: str
        :param _SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则绑定默认安全组。（目前仅支持设置单个sgId）
        :type SecurityGroupIds: list of str
        :param _NodePool: 节点池选项
        :type NodePool: :class:`tencentcloud.tke.v20180525.models.NodePoolOption`
        :param _SkipValidateOptions: 校验规则相关选项，可配置跳过某些校验规则。目前支持GlobalRouteCIDRCheck（跳过GlobalRouter的相关校验），VpcCniCIDRCheck（跳过VpcCni相关校验）
        :type SkipValidateOptions: list of str
        :param _InstanceAdvancedSettingsOverrides: 参数InstanceAdvancedSettingsOverride数组用于定制化地配置各台instance，与InstanceIds顺序对应。当传入InstanceAdvancedSettingsOverrides数组时，将覆盖默认参数InstanceAdvancedSettings；当没有传入参数InstanceAdvancedSettingsOverrides时，InstanceAdvancedSettings参数对每台instance生效。

参数InstanceAdvancedSettingsOverride数组的长度应与InstanceIds数组一致；当长度大于InstanceIds数组长度时将报错；当长度小于InstanceIds数组时，没有对应配置的instace将使用默认配置。
        :type InstanceAdvancedSettingsOverrides: list of InstanceAdvancedSettings
        :param _ImageId: 节点镜像
        :type ImageId: str
        """
        self._ClusterId = None
        self._InstanceIds = None
        self._InstanceAdvancedSettings = None
        self._EnhancedService = None
        self._LoginSettings = None
        self._HostName = None
        self._SecurityGroupIds = None
        self._NodePool = None
        self._SkipValidateOptions = None
        self._InstanceAdvancedSettingsOverrides = None
        self._ImageId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def EnhancedService(self):
        return self._EnhancedService

    @EnhancedService.setter
    def EnhancedService(self, EnhancedService):
        self._EnhancedService = EnhancedService

    @property
    def LoginSettings(self):
        return self._LoginSettings

    @LoginSettings.setter
    def LoginSettings(self, LoginSettings):
        self._LoginSettings = LoginSettings

    @property
    def HostName(self):
        return self._HostName

    @HostName.setter
    def HostName(self, HostName):
        self._HostName = HostName

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def NodePool(self):
        return self._NodePool

    @NodePool.setter
    def NodePool(self, NodePool):
        self._NodePool = NodePool

    @property
    def SkipValidateOptions(self):
        return self._SkipValidateOptions

    @SkipValidateOptions.setter
    def SkipValidateOptions(self, SkipValidateOptions):
        self._SkipValidateOptions = SkipValidateOptions

    @property
    def InstanceAdvancedSettingsOverrides(self):
        return self._InstanceAdvancedSettingsOverrides

    @InstanceAdvancedSettingsOverrides.setter
    def InstanceAdvancedSettingsOverrides(self, InstanceAdvancedSettingsOverrides):
        self._InstanceAdvancedSettingsOverrides = InstanceAdvancedSettingsOverrides

    @property
    def ImageId(self):
        return self._ImageId

    @ImageId.setter
    def ImageId(self, ImageId):
        self._ImageId = ImageId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._InstanceIds = params.get("InstanceIds")
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("EnhancedService") is not None:
            self._EnhancedService = EnhancedService()
            self._EnhancedService._deserialize(params.get("EnhancedService"))
        if params.get("LoginSettings") is not None:
            self._LoginSettings = LoginSettings()
            self._LoginSettings._deserialize(params.get("LoginSettings"))
        self._HostName = params.get("HostName")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("NodePool") is not None:
            self._NodePool = NodePoolOption()
            self._NodePool._deserialize(params.get("NodePool"))
        self._SkipValidateOptions = params.get("SkipValidateOptions")
        if params.get("InstanceAdvancedSettingsOverrides") is not None:
            self._InstanceAdvancedSettingsOverrides = []
            for item in params.get("InstanceAdvancedSettingsOverrides"):
                obj = InstanceAdvancedSettings()
                obj._deserialize(item)
                self._InstanceAdvancedSettingsOverrides.append(obj)
        self._ImageId = params.get("ImageId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddExistedInstancesResponse(AbstractModel):
    """AddExistedInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _FailedInstanceIds: 失败的节点ID
注意：此字段可能返回 null，表示取不到有效值。
        :type FailedInstanceIds: list of str
        :param _SuccInstanceIds: 成功的节点ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SuccInstanceIds: list of str
        :param _TimeoutInstanceIds: 超时未返回出来节点的ID(可能失败，也可能成功)
注意：此字段可能返回 null，表示取不到有效值。
        :type TimeoutInstanceIds: list of str
        :param _FailedReasons: 失败的节点的失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailedReasons: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._FailedInstanceIds = None
        self._SuccInstanceIds = None
        self._TimeoutInstanceIds = None
        self._FailedReasons = None
        self._RequestId = None

    @property
    def FailedInstanceIds(self):
        return self._FailedInstanceIds

    @FailedInstanceIds.setter
    def FailedInstanceIds(self, FailedInstanceIds):
        self._FailedInstanceIds = FailedInstanceIds

    @property
    def SuccInstanceIds(self):
        return self._SuccInstanceIds

    @SuccInstanceIds.setter
    def SuccInstanceIds(self, SuccInstanceIds):
        self._SuccInstanceIds = SuccInstanceIds

    @property
    def TimeoutInstanceIds(self):
        return self._TimeoutInstanceIds

    @TimeoutInstanceIds.setter
    def TimeoutInstanceIds(self, TimeoutInstanceIds):
        self._TimeoutInstanceIds = TimeoutInstanceIds

    @property
    def FailedReasons(self):
        return self._FailedReasons

    @FailedReasons.setter
    def FailedReasons(self, FailedReasons):
        self._FailedReasons = FailedReasons

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._FailedInstanceIds = params.get("FailedInstanceIds")
        self._SuccInstanceIds = params.get("SuccInstanceIds")
        self._TimeoutInstanceIds = params.get("TimeoutInstanceIds")
        self._FailedReasons = params.get("FailedReasons")
        self._RequestId = params.get("RequestId")


class AddNodeToNodePoolRequest(AbstractModel):
    """AddNodeToNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _InstanceIds: 节点id
        :type InstanceIds: list of str
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._InstanceIds = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddNodeToNodePoolResponse(AbstractModel):
    """AddNodeToNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class AddVpcCniSubnetsRequest(AbstractModel):
    """AddVpcCniSubnets请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _SubnetIds: 为集群容器网络增加的子网列表
        :type SubnetIds: list of str
        :param _VpcId: 集群所属的VPC的ID
        :type VpcId: str
        :param _SkipAddingNonMasqueradeCIDRs: 是否同步添加 vpc 网段到 ip-masq-agent-config 的 NonMasqueradeCIDRs 字段，默认 false 会同步添加
        :type SkipAddingNonMasqueradeCIDRs: bool
        """
        self._ClusterId = None
        self._SubnetIds = None
        self._VpcId = None
        self._SkipAddingNonMasqueradeCIDRs = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SkipAddingNonMasqueradeCIDRs(self):
        return self._SkipAddingNonMasqueradeCIDRs

    @SkipAddingNonMasqueradeCIDRs.setter
    def SkipAddingNonMasqueradeCIDRs(self, SkipAddingNonMasqueradeCIDRs):
        self._SkipAddingNonMasqueradeCIDRs = SkipAddingNonMasqueradeCIDRs


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._SubnetIds = params.get("SubnetIds")
        self._VpcId = params.get("VpcId")
        self._SkipAddingNonMasqueradeCIDRs = params.get("SkipAddingNonMasqueradeCIDRs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddVpcCniSubnetsResponse(AbstractModel):
    """AddVpcCniSubnets返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class Addon(AbstractModel):
    """addon的具体描述

    """

    def __init__(self):
        r"""
        :param _AddonName: addon名称
        :type AddonName: str
        :param _AddonVersion: addon的版本
        :type AddonVersion: str
        :param _RawValues: addon的参数，是一个json格式的base64转码后的字符串
注意：此字段可能返回 null，表示取不到有效值。
        :type RawValues: str
        :param _Phase: addon的状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Phase: str
        :param _Reason: addon失败的原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        """
        self._AddonName = None
        self._AddonVersion = None
        self._RawValues = None
        self._Phase = None
        self._Reason = None

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName

    @property
    def AddonVersion(self):
        return self._AddonVersion

    @AddonVersion.setter
    def AddonVersion(self, AddonVersion):
        self._AddonVersion = AddonVersion

    @property
    def RawValues(self):
        return self._RawValues

    @RawValues.setter
    def RawValues(self, RawValues):
        self._RawValues = RawValues

    @property
    def Phase(self):
        return self._Phase

    @Phase.setter
    def Phase(self, Phase):
        self._Phase = Phase

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason


    def _deserialize(self, params):
        self._AddonName = params.get("AddonName")
        self._AddonVersion = params.get("AddonVersion")
        self._RawValues = params.get("RawValues")
        self._Phase = params.get("Phase")
        self._Reason = params.get("Reason")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AppChart(AbstractModel):
    """app所支持的chart

    """

    def __init__(self):
        r"""
        :param _Name: chart名称
        :type Name: str
        :param _Label: chart的标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Label: str
        :param _LatestVersion: chart的版本
        :type LatestVersion: str
        """
        self._Name = None
        self._Label = None
        self._LatestVersion = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Label(self):
        return self._Label

    @Label.setter
    def Label(self, Label):
        self._Label = Label

    @property
    def LatestVersion(self):
        return self._LatestVersion

    @LatestVersion.setter
    def LatestVersion(self, LatestVersion):
        self._LatestVersion = LatestVersion


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Label = params.get("Label")
        self._LatestVersion = params.get("LatestVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AutoScalingGroupRange(AbstractModel):
    """集群关联的伸缩组最大实例数最小值实例数

    """

    def __init__(self):
        r"""
        :param _MinSize: 伸缩组最小实例数
        :type MinSize: int
        :param _MaxSize: 伸缩组最大实例数
        :type MaxSize: int
        """
        self._MinSize = None
        self._MaxSize = None

    @property
    def MinSize(self):
        return self._MinSize

    @MinSize.setter
    def MinSize(self, MinSize):
        self._MinSize = MinSize

    @property
    def MaxSize(self):
        return self._MaxSize

    @MaxSize.setter
    def MaxSize(self, MaxSize):
        self._MaxSize = MaxSize


    def _deserialize(self, params):
        self._MinSize = params.get("MinSize")
        self._MaxSize = params.get("MaxSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AutoUpgradeClusterLevel(AbstractModel):
    """自动变配集群等级

    """

    def __init__(self):
        r"""
        :param _IsAutoUpgrade: 是否开启自动变配集群等级
        :type IsAutoUpgrade: bool
        """
        self._IsAutoUpgrade = None

    @property
    def IsAutoUpgrade(self):
        return self._IsAutoUpgrade

    @IsAutoUpgrade.setter
    def IsAutoUpgrade(self, IsAutoUpgrade):
        self._IsAutoUpgrade = IsAutoUpgrade


    def _deserialize(self, params):
        self._IsAutoUpgrade = params.get("IsAutoUpgrade")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AutoscalingAdded(AbstractModel):
    """自动扩所容的节点

    """

    def __init__(self):
        r"""
        :param _Joining: 正在加入中的节点数量
        :type Joining: int
        :param _Initializing: 初始化中的节点数量
        :type Initializing: int
        :param _Normal: 正常的节点数量
        :type Normal: int
        :param _Total: 节点总数
        :type Total: int
        """
        self._Joining = None
        self._Initializing = None
        self._Normal = None
        self._Total = None

    @property
    def Joining(self):
        return self._Joining

    @Joining.setter
    def Joining(self, Joining):
        self._Joining = Joining

    @property
    def Initializing(self):
        return self._Initializing

    @Initializing.setter
    def Initializing(self, Initializing):
        self._Initializing = Initializing

    @property
    def Normal(self):
        return self._Normal

    @Normal.setter
    def Normal(self, Normal):
        self._Normal = Normal

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total


    def _deserialize(self, params):
        self._Joining = params.get("Joining")
        self._Initializing = params.get("Initializing")
        self._Normal = params.get("Normal")
        self._Total = params.get("Total")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupStorageLocation(AbstractModel):
    """仓储仓库信息

    """

    def __init__(self):
        r"""
        :param _Name: 备份仓库名称	
        :type Name: str
        :param _StorageRegion: 存储仓库所属地域，比如COS广州(ap-guangzhou)	
        :type StorageRegion: str
        :param _Provider: 存储服务提供方，默认腾讯云	
注意：此字段可能返回 null，表示取不到有效值。
        :type Provider: str
        :param _Bucket: 对象存储桶名称，如果是COS必须是tke-backup-前缀开头	
注意：此字段可能返回 null，表示取不到有效值。
        :type Bucket: str
        :param _Path: 对象存储桶路径
注意：此字段可能返回 null，表示取不到有效值。
        :type Path: str
        :param _State: 存储仓库状态
注意：此字段可能返回 null，表示取不到有效值。
        :type State: str
        :param _Message: 详细状态信息	
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param _LastValidationTime: 最后一次检查时间	
注意：此字段可能返回 null，表示取不到有效值。
        :type LastValidationTime: str
        """
        self._Name = None
        self._StorageRegion = None
        self._Provider = None
        self._Bucket = None
        self._Path = None
        self._State = None
        self._Message = None
        self._LastValidationTime = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def StorageRegion(self):
        return self._StorageRegion

    @StorageRegion.setter
    def StorageRegion(self, StorageRegion):
        self._StorageRegion = StorageRegion

    @property
    def Provider(self):
        return self._Provider

    @Provider.setter
    def Provider(self, Provider):
        self._Provider = Provider

    @property
    def Bucket(self):
        return self._Bucket

    @Bucket.setter
    def Bucket(self, Bucket):
        self._Bucket = Bucket

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path

    @property
    def State(self):
        return self._State

    @State.setter
    def State(self, State):
        self._State = State

    @property
    def Message(self):
        return self._Message

    @Message.setter
    def Message(self, Message):
        self._Message = Message

    @property
    def LastValidationTime(self):
        return self._LastValidationTime

    @LastValidationTime.setter
    def LastValidationTime(self, LastValidationTime):
        self._LastValidationTime = LastValidationTime


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._StorageRegion = params.get("StorageRegion")
        self._Provider = params.get("Provider")
        self._Bucket = params.get("Bucket")
        self._Path = params.get("Path")
        self._State = params.get("State")
        self._Message = params.get("Message")
        self._LastValidationTime = params.get("LastValidationTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CUDNN(AbstractModel):
    """cuDNN的版本信息

    """

    def __init__(self):
        r"""
        :param _Version: cuDNN的版本
        :type Version: str
        :param _Name: cuDNN的名字
        :type Name: str
        :param _DocName: cuDNN的Doc名字
        :type DocName: str
        :param _DevName: cuDNN的Dev名字
        :type DevName: str
        """
        self._Version = None
        self._Name = None
        self._DocName = None
        self._DevName = None

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def DocName(self):
        return self._DocName

    @DocName.setter
    def DocName(self, DocName):
        self._DocName = DocName

    @property
    def DevName(self):
        return self._DevName

    @DevName.setter
    def DevName(self, DevName):
        self._DevName = DevName


    def _deserialize(self, params):
        self._Version = params.get("Version")
        self._Name = params.get("Name")
        self._DocName = params.get("DocName")
        self._DevName = params.get("DevName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelClusterReleaseRequest(AbstractModel):
    """CancelClusterRelease请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ID: 应用ID
        :type ID: str
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._ID = None
        self._ClusterId = None
        self._ClusterType = None

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ID = params.get("ID")
        self._ClusterId = params.get("ClusterId")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelClusterReleaseResponse(AbstractModel):
    """CancelClusterRelease返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Release: 应用信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Release: :class:`tencentcloud.tke.v20180525.models.PendingRelease`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Release = None
        self._RequestId = None

    @property
    def Release(self):
        return self._Release

    @Release.setter
    def Release(self, Release):
        self._Release = Release

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Release") is not None:
            self._Release = PendingRelease()
            self._Release._deserialize(params.get("Release"))
        self._RequestId = params.get("RequestId")


class Capabilities(AbstractModel):
    """cloudrun安全特性能力

    """

    def __init__(self):
        r"""
        :param _Add: 启用安全能力项列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Add: list of str
        :param _Drop: 禁用安全能力向列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Drop: list of str
        """
        self._Add = None
        self._Drop = None

    @property
    def Add(self):
        return self._Add

    @Add.setter
    def Add(self, Add):
        self._Add = Add

    @property
    def Drop(self):
        return self._Drop

    @Drop.setter
    def Drop(self, Drop):
        self._Drop = Drop


    def _deserialize(self, params):
        self._Add = params.get("Add")
        self._Drop = params.get("Drop")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CbsVolume(AbstractModel):
    """EKS Instnace CBS volume

    """

    def __init__(self):
        r"""
        :param _Name: cbs volume 数据卷名称
        :type Name: str
        :param _CbsDiskId: 腾讯云cbs盘Id
        :type CbsDiskId: str
        """
        self._Name = None
        self._CbsDiskId = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def CbsDiskId(self):
        return self._CbsDiskId

    @CbsDiskId.setter
    def CbsDiskId(self, CbsDiskId):
        self._CbsDiskId = CbsDiskId


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._CbsDiskId = params.get("CbsDiskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckEdgeClusterCIDRRequest(AbstractModel):
    """CheckEdgeClusterCIDR请求参数结构体

    """

    def __init__(self):
        r"""
        :param _VpcId: 集群的vpc-id
        :type VpcId: str
        :param _PodCIDR: 集群的pod CIDR
        :type PodCIDR: str
        :param _ServiceCIDR: 集群的service CIDR
        :type ServiceCIDR: str
        """
        self._VpcId = None
        self._PodCIDR = None
        self._ServiceCIDR = None

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def PodCIDR(self):
        return self._PodCIDR

    @PodCIDR.setter
    def PodCIDR(self, PodCIDR):
        self._PodCIDR = PodCIDR

    @property
    def ServiceCIDR(self):
        return self._ServiceCIDR

    @ServiceCIDR.setter
    def ServiceCIDR(self, ServiceCIDR):
        self._ServiceCIDR = ServiceCIDR


    def _deserialize(self, params):
        self._VpcId = params.get("VpcId")
        self._PodCIDR = params.get("PodCIDR")
        self._ServiceCIDR = params.get("ServiceCIDR")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckEdgeClusterCIDRResponse(AbstractModel):
    """CheckEdgeClusterCIDR返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ConflictCode: 返回码，具体如下
-1 内部错误
0 没冲突
1 vpc 和 serviceCIDR 冲突
2 vpc 和 podCIDR 冲突
3 serviceCIDR  和 podCIDR 冲突
        :type ConflictCode: int
        :param _ConflictMsg: CIDR冲突描述信息。
        :type ConflictMsg: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ConflictCode = None
        self._ConflictMsg = None
        self._RequestId = None

    @property
    def ConflictCode(self):
        return self._ConflictCode

    @ConflictCode.setter
    def ConflictCode(self, ConflictCode):
        self._ConflictCode = ConflictCode

    @property
    def ConflictMsg(self):
        return self._ConflictMsg

    @ConflictMsg.setter
    def ConflictMsg(self, ConflictMsg):
        self._ConflictMsg = ConflictMsg

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ConflictCode = params.get("ConflictCode")
        self._ConflictMsg = params.get("ConflictMsg")
        self._RequestId = params.get("RequestId")


class CheckInstancesUpgradeAbleRequest(AbstractModel):
    """CheckInstancesUpgradeAble请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _InstanceIds: 节点列表，空为全部节点
        :type InstanceIds: list of str
        :param _UpgradeType: 升级类型
        :type UpgradeType: str
        :param _Offset: 分页Offset
        :type Offset: int
        :param _Limit: 分页Limit
        :type Limit: int
        :param _Filter: 过滤
        :type Filter: list of Filter
        """
        self._ClusterId = None
        self._InstanceIds = None
        self._UpgradeType = None
        self._Offset = None
        self._Limit = None
        self._Filter = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def UpgradeType(self):
        return self._UpgradeType

    @UpgradeType.setter
    def UpgradeType(self, UpgradeType):
        self._UpgradeType = UpgradeType

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filter(self):
        return self._Filter

    @Filter.setter
    def Filter(self, Filter):
        self._Filter = Filter


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._InstanceIds = params.get("InstanceIds")
        self._UpgradeType = params.get("UpgradeType")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filter") is not None:
            self._Filter = []
            for item in params.get("Filter"):
                obj = Filter()
                obj._deserialize(item)
                self._Filter.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckInstancesUpgradeAbleResponse(AbstractModel):
    """CheckInstancesUpgradeAble返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterVersion: 集群master当前小版本
        :type ClusterVersion: str
        :param _LatestVersion: 集群master对应的大版本目前最新小版本
        :type LatestVersion: str
        :param _UpgradeAbleInstances: 可升级节点列表
注意：此字段可能返回 null，表示取不到有效值。
        :type UpgradeAbleInstances: list of UpgradeAbleInstancesItem
        :param _Total: 总数
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param _UnavailableVersionReason: 不可升级原因
注意：此字段可能返回 null，表示取不到有效值。
        :type UnavailableVersionReason: list of UnavailableReason
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterVersion = None
        self._LatestVersion = None
        self._UpgradeAbleInstances = None
        self._Total = None
        self._UnavailableVersionReason = None
        self._RequestId = None

    @property
    def ClusterVersion(self):
        return self._ClusterVersion

    @ClusterVersion.setter
    def ClusterVersion(self, ClusterVersion):
        self._ClusterVersion = ClusterVersion

    @property
    def LatestVersion(self):
        return self._LatestVersion

    @LatestVersion.setter
    def LatestVersion(self, LatestVersion):
        self._LatestVersion = LatestVersion

    @property
    def UpgradeAbleInstances(self):
        return self._UpgradeAbleInstances

    @UpgradeAbleInstances.setter
    def UpgradeAbleInstances(self, UpgradeAbleInstances):
        self._UpgradeAbleInstances = UpgradeAbleInstances

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def UnavailableVersionReason(self):
        return self._UnavailableVersionReason

    @UnavailableVersionReason.setter
    def UnavailableVersionReason(self, UnavailableVersionReason):
        self._UnavailableVersionReason = UnavailableVersionReason

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ClusterVersion = params.get("ClusterVersion")
        self._LatestVersion = params.get("LatestVersion")
        if params.get("UpgradeAbleInstances") is not None:
            self._UpgradeAbleInstances = []
            for item in params.get("UpgradeAbleInstances"):
                obj = UpgradeAbleInstancesItem()
                obj._deserialize(item)
                self._UpgradeAbleInstances.append(obj)
        self._Total = params.get("Total")
        if params.get("UnavailableVersionReason") is not None:
            self._UnavailableVersionReason = []
            for item in params.get("UnavailableVersionReason"):
                obj = UnavailableReason()
                obj._deserialize(item)
                self._UnavailableVersionReason.append(obj)
        self._RequestId = params.get("RequestId")


class Cluster(AbstractModel):
    """集群信息结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _ClusterDescription: 集群描述
        :type ClusterDescription: str
        :param _ClusterVersion: 集群版本（默认值为1.10.5）
        :type ClusterVersion: str
        :param _ClusterOs: 集群系统。centos7.2x86_64 或者 ubuntu16.04.1 LTSx86_64，默认取值为ubuntu16.04.1 LTSx86_64
        :type ClusterOs: str
        :param _ClusterType: 集群类型，托管集群：MANAGED_CLUSTER，独立集群：INDEPENDENT_CLUSTER。
        :type ClusterType: str
        :param _ClusterNetworkSettings: 集群网络相关参数
        :type ClusterNetworkSettings: :class:`tencentcloud.tke.v20180525.models.ClusterNetworkSettings`
        :param _ClusterNodeNum: 集群当前node数量
        :type ClusterNodeNum: int
        :param _ProjectId: 集群所属的项目ID
        :type ProjectId: int
        :param _TagSpecification: 标签描述列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type TagSpecification: list of TagSpecification
        :param _ClusterStatus: 集群状态 (Trading 集群开通中,Creating 创建中,Running 运行中,Deleting 删除中,Idling 闲置中,Recovering 唤醒中,Scaling 规模调整中,Upgrading 升级中,WaittingForConnect 等待注册,Trading 集群开通中,Isolated 欠费隔离中,Pause 集群升级暂停,NodeUpgrading 节点升级中,RuntimeUpgrading 节点运行时升级中,MasterScaling Master扩缩容中,ClusterLevelUpgrading 调整规格中,ResourceIsolate 隔离中,ResourceIsolated 已隔离,ResourceReverse 冲正中,Abnormal 异常)
        :type ClusterStatus: str
        :param _Property: 集群属性(包括集群不同属性的MAP，属性字段包括NodeNameType (lan-ip模式和hostname 模式，默认无lan-ip模式))
注意：此字段可能返回 null，表示取不到有效值。
        :type Property: str
        :param _ClusterMaterNodeNum: 集群当前master数量
        :type ClusterMaterNodeNum: int
        :param _ImageId: 集群使用镜像id
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageId: str
        :param _OsCustomizeType: OsCustomizeType 系统定制类型
注意：此字段可能返回 null，表示取不到有效值。
        :type OsCustomizeType: str
        :param _ContainerRuntime: 集群运行环境docker或container
注意：此字段可能返回 null，表示取不到有效值。
        :type ContainerRuntime: str
        :param _CreatedTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreatedTime: str
        :param _DeletionProtection: 删除保护开关
注意：此字段可能返回 null，表示取不到有效值。
        :type DeletionProtection: bool
        :param _EnableExternalNode: 集群是否开启第三方节点支持
注意：此字段可能返回 null，表示取不到有效值。
        :type EnableExternalNode: bool
        :param _ClusterLevel: 集群等级，针对托管集群生效
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterLevel: str
        :param _AutoUpgradeClusterLevel: 自动变配集群等级，针对托管集群生效
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoUpgradeClusterLevel: bool
        :param _QGPUShareEnable: 是否开启QGPU共享
注意：此字段可能返回 null，表示取不到有效值。
        :type QGPUShareEnable: bool
        :param _RuntimeVersion: 运行时版本
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeVersion: str
        :param _ClusterEtcdNodeNum: 集群当前etcd数量
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterEtcdNodeNum: int
        """
        self._ClusterId = None
        self._ClusterName = None
        self._ClusterDescription = None
        self._ClusterVersion = None
        self._ClusterOs = None
        self._ClusterType = None
        self._ClusterNetworkSettings = None
        self._ClusterNodeNum = None
        self._ProjectId = None
        self._TagSpecification = None
        self._ClusterStatus = None
        self._Property = None
        self._ClusterMaterNodeNum = None
        self._ImageId = None
        self._OsCustomizeType = None
        self._ContainerRuntime = None
        self._CreatedTime = None
        self._DeletionProtection = None
        self._EnableExternalNode = None
        self._ClusterLevel = None
        self._AutoUpgradeClusterLevel = None
        self._QGPUShareEnable = None
        self._RuntimeVersion = None
        self._ClusterEtcdNodeNum = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ClusterDescription(self):
        return self._ClusterDescription

    @ClusterDescription.setter
    def ClusterDescription(self, ClusterDescription):
        self._ClusterDescription = ClusterDescription

    @property
    def ClusterVersion(self):
        return self._ClusterVersion

    @ClusterVersion.setter
    def ClusterVersion(self, ClusterVersion):
        self._ClusterVersion = ClusterVersion

    @property
    def ClusterOs(self):
        return self._ClusterOs

    @ClusterOs.setter
    def ClusterOs(self, ClusterOs):
        self._ClusterOs = ClusterOs

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterNetworkSettings(self):
        return self._ClusterNetworkSettings

    @ClusterNetworkSettings.setter
    def ClusterNetworkSettings(self, ClusterNetworkSettings):
        self._ClusterNetworkSettings = ClusterNetworkSettings

    @property
    def ClusterNodeNum(self):
        return self._ClusterNodeNum

    @ClusterNodeNum.setter
    def ClusterNodeNum(self, ClusterNodeNum):
        self._ClusterNodeNum = ClusterNodeNum

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def TagSpecification(self):
        return self._TagSpecification

    @TagSpecification.setter
    def TagSpecification(self, TagSpecification):
        self._TagSpecification = TagSpecification

    @property
    def ClusterStatus(self):
        return self._ClusterStatus

    @ClusterStatus.setter
    def ClusterStatus(self, ClusterStatus):
        self._ClusterStatus = ClusterStatus

    @property
    def Property(self):
        return self._Property

    @Property.setter
    def Property(self, Property):
        self._Property = Property

    @property
    def ClusterMaterNodeNum(self):
        return self._ClusterMaterNodeNum

    @ClusterMaterNodeNum.setter
    def ClusterMaterNodeNum(self, ClusterMaterNodeNum):
        self._ClusterMaterNodeNum = ClusterMaterNodeNum

    @property
    def ImageId(self):
        return self._ImageId

    @ImageId.setter
    def ImageId(self, ImageId):
        self._ImageId = ImageId

    @property
    def OsCustomizeType(self):
        return self._OsCustomizeType

    @OsCustomizeType.setter
    def OsCustomizeType(self, OsCustomizeType):
        self._OsCustomizeType = OsCustomizeType

    @property
    def ContainerRuntime(self):
        return self._ContainerRuntime

    @ContainerRuntime.setter
    def ContainerRuntime(self, ContainerRuntime):
        self._ContainerRuntime = ContainerRuntime

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection

    @property
    def EnableExternalNode(self):
        return self._EnableExternalNode

    @EnableExternalNode.setter
    def EnableExternalNode(self, EnableExternalNode):
        self._EnableExternalNode = EnableExternalNode

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel

    @property
    def QGPUShareEnable(self):
        return self._QGPUShareEnable

    @QGPUShareEnable.setter
    def QGPUShareEnable(self, QGPUShareEnable):
        self._QGPUShareEnable = QGPUShareEnable

    @property
    def RuntimeVersion(self):
        return self._RuntimeVersion

    @RuntimeVersion.setter
    def RuntimeVersion(self, RuntimeVersion):
        self._RuntimeVersion = RuntimeVersion

    @property
    def ClusterEtcdNodeNum(self):
        return self._ClusterEtcdNodeNum

    @ClusterEtcdNodeNum.setter
    def ClusterEtcdNodeNum(self, ClusterEtcdNodeNum):
        self._ClusterEtcdNodeNum = ClusterEtcdNodeNum


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterName = params.get("ClusterName")
        self._ClusterDescription = params.get("ClusterDescription")
        self._ClusterVersion = params.get("ClusterVersion")
        self._ClusterOs = params.get("ClusterOs")
        self._ClusterType = params.get("ClusterType")
        if params.get("ClusterNetworkSettings") is not None:
            self._ClusterNetworkSettings = ClusterNetworkSettings()
            self._ClusterNetworkSettings._deserialize(params.get("ClusterNetworkSettings"))
        self._ClusterNodeNum = params.get("ClusterNodeNum")
        self._ProjectId = params.get("ProjectId")
        if params.get("TagSpecification") is not None:
            self._TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self._TagSpecification.append(obj)
        self._ClusterStatus = params.get("ClusterStatus")
        self._Property = params.get("Property")
        self._ClusterMaterNodeNum = params.get("ClusterMaterNodeNum")
        self._ImageId = params.get("ImageId")
        self._OsCustomizeType = params.get("OsCustomizeType")
        self._ContainerRuntime = params.get("ContainerRuntime")
        self._CreatedTime = params.get("CreatedTime")
        self._DeletionProtection = params.get("DeletionProtection")
        self._EnableExternalNode = params.get("EnableExternalNode")
        self._ClusterLevel = params.get("ClusterLevel")
        self._AutoUpgradeClusterLevel = params.get("AutoUpgradeClusterLevel")
        self._QGPUShareEnable = params.get("QGPUShareEnable")
        self._RuntimeVersion = params.get("RuntimeVersion")
        self._ClusterEtcdNodeNum = params.get("ClusterEtcdNodeNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterAdvancedSettings(AbstractModel):
    """集群高级配置

    """

    def __init__(self):
        r"""
        :param _IPVS: 是否启用IPVS
        :type IPVS: bool
        :param _AsEnabled: 是否启用集群节点自动扩缩容(创建集群流程不支持开启此功能)
        :type AsEnabled: bool
        :param _ContainerRuntime: 集群使用的runtime类型，包括"docker"和"containerd"两种类型，默认为"docker"
        :type ContainerRuntime: str
        :param _NodeNameType: 集群中节点NodeName类型（包括 hostname,lan-ip两种形式，默认为lan-ip。如果开启了hostname模式，创建节点时需要设置HostName参数，并且InstanceName需要和HostName一致）
        :type NodeNameType: str
        :param _ExtraArgs: 集群自定义参数
        :type ExtraArgs: :class:`tencentcloud.tke.v20180525.models.ClusterExtraArgs`
        :param _NetworkType: 集群网络类型（包括GR(全局路由)和VPC-CNI两种模式，默认为GR。
        :type NetworkType: str
        :param _IsNonStaticIpMode: 集群VPC-CNI模式是否为非固定IP，默认: FALSE 固定IP。
        :type IsNonStaticIpMode: bool
        :param _DeletionProtection: 是否启用集群删除保护
        :type DeletionProtection: bool
        :param _KubeProxyMode: 集群的网络代理模型，目前tke集群支持的网络代理模式有三种：iptables,ipvs,ipvs-bpf，此参数仅在使用ipvs-bpf模式时使用，三种网络模式的参数设置关系如下：
iptables模式：IPVS和KubeProxyMode都不设置
ipvs模式: 设置IPVS为true, KubeProxyMode不设置
ipvs-bpf模式: 设置KubeProxyMode为kube-proxy-bpf
使用ipvs-bpf的网络模式需要满足以下条件：
1. 集群版本必须为1.14及以上；
2. 系统镜像必须是: Tencent Linux 2.4；
        :type KubeProxyMode: str
        :param _AuditEnabled: 是否开启审计开关
        :type AuditEnabled: bool
        :param _AuditLogsetId: 审计日志上传到的logset日志集
        :type AuditLogsetId: str
        :param _AuditLogTopicId: 审计日志上传到的topic
        :type AuditLogTopicId: str
        :param _VpcCniType: 区分共享网卡多IP模式和独立网卡模式，共享网卡多 IP 模式填写"tke-route-eni"，独立网卡模式填写"tke-direct-eni"，默认为共享网卡模式
        :type VpcCniType: str
        :param _RuntimeVersion: 运行时版本
        :type RuntimeVersion: str
        :param _EnableCustomizedPodCIDR: 是否开节点podCIDR大小的自定义模式
        :type EnableCustomizedPodCIDR: bool
        :param _BasePodNumber: 自定义模式下的基础pod数量
        :type BasePodNumber: int
        :param _CiliumMode: 启用 CiliumMode 的模式，空值表示不启用，“clusterIP” 表示启用 Cilium 支持 ClusterIP
        :type CiliumMode: str
        :param _IsDualStack: 集群VPC-CNI模式下是否是双栈集群，默认false，表明非双栈集群。
        :type IsDualStack: bool
        :param _QGPUShareEnable: 是否开启QGPU共享
        :type QGPUShareEnable: bool
        """
        self._IPVS = None
        self._AsEnabled = None
        self._ContainerRuntime = None
        self._NodeNameType = None
        self._ExtraArgs = None
        self._NetworkType = None
        self._IsNonStaticIpMode = None
        self._DeletionProtection = None
        self._KubeProxyMode = None
        self._AuditEnabled = None
        self._AuditLogsetId = None
        self._AuditLogTopicId = None
        self._VpcCniType = None
        self._RuntimeVersion = None
        self._EnableCustomizedPodCIDR = None
        self._BasePodNumber = None
        self._CiliumMode = None
        self._IsDualStack = None
        self._QGPUShareEnable = None

    @property
    def IPVS(self):
        return self._IPVS

    @IPVS.setter
    def IPVS(self, IPVS):
        self._IPVS = IPVS

    @property
    def AsEnabled(self):
        return self._AsEnabled

    @AsEnabled.setter
    def AsEnabled(self, AsEnabled):
        self._AsEnabled = AsEnabled

    @property
    def ContainerRuntime(self):
        return self._ContainerRuntime

    @ContainerRuntime.setter
    def ContainerRuntime(self, ContainerRuntime):
        self._ContainerRuntime = ContainerRuntime

    @property
    def NodeNameType(self):
        return self._NodeNameType

    @NodeNameType.setter
    def NodeNameType(self, NodeNameType):
        self._NodeNameType = NodeNameType

    @property
    def ExtraArgs(self):
        return self._ExtraArgs

    @ExtraArgs.setter
    def ExtraArgs(self, ExtraArgs):
        self._ExtraArgs = ExtraArgs

    @property
    def NetworkType(self):
        return self._NetworkType

    @NetworkType.setter
    def NetworkType(self, NetworkType):
        self._NetworkType = NetworkType

    @property
    def IsNonStaticIpMode(self):
        return self._IsNonStaticIpMode

    @IsNonStaticIpMode.setter
    def IsNonStaticIpMode(self, IsNonStaticIpMode):
        self._IsNonStaticIpMode = IsNonStaticIpMode

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection

    @property
    def KubeProxyMode(self):
        return self._KubeProxyMode

    @KubeProxyMode.setter
    def KubeProxyMode(self, KubeProxyMode):
        self._KubeProxyMode = KubeProxyMode

    @property
    def AuditEnabled(self):
        return self._AuditEnabled

    @AuditEnabled.setter
    def AuditEnabled(self, AuditEnabled):
        self._AuditEnabled = AuditEnabled

    @property
    def AuditLogsetId(self):
        return self._AuditLogsetId

    @AuditLogsetId.setter
    def AuditLogsetId(self, AuditLogsetId):
        self._AuditLogsetId = AuditLogsetId

    @property
    def AuditLogTopicId(self):
        return self._AuditLogTopicId

    @AuditLogTopicId.setter
    def AuditLogTopicId(self, AuditLogTopicId):
        self._AuditLogTopicId = AuditLogTopicId

    @property
    def VpcCniType(self):
        return self._VpcCniType

    @VpcCniType.setter
    def VpcCniType(self, VpcCniType):
        self._VpcCniType = VpcCniType

    @property
    def RuntimeVersion(self):
        return self._RuntimeVersion

    @RuntimeVersion.setter
    def RuntimeVersion(self, RuntimeVersion):
        self._RuntimeVersion = RuntimeVersion

    @property
    def EnableCustomizedPodCIDR(self):
        return self._EnableCustomizedPodCIDR

    @EnableCustomizedPodCIDR.setter
    def EnableCustomizedPodCIDR(self, EnableCustomizedPodCIDR):
        self._EnableCustomizedPodCIDR = EnableCustomizedPodCIDR

    @property
    def BasePodNumber(self):
        return self._BasePodNumber

    @BasePodNumber.setter
    def BasePodNumber(self, BasePodNumber):
        self._BasePodNumber = BasePodNumber

    @property
    def CiliumMode(self):
        return self._CiliumMode

    @CiliumMode.setter
    def CiliumMode(self, CiliumMode):
        self._CiliumMode = CiliumMode

    @property
    def IsDualStack(self):
        return self._IsDualStack

    @IsDualStack.setter
    def IsDualStack(self, IsDualStack):
        self._IsDualStack = IsDualStack

    @property
    def QGPUShareEnable(self):
        return self._QGPUShareEnable

    @QGPUShareEnable.setter
    def QGPUShareEnable(self, QGPUShareEnable):
        self._QGPUShareEnable = QGPUShareEnable


    def _deserialize(self, params):
        self._IPVS = params.get("IPVS")
        self._AsEnabled = params.get("AsEnabled")
        self._ContainerRuntime = params.get("ContainerRuntime")
        self._NodeNameType = params.get("NodeNameType")
        if params.get("ExtraArgs") is not None:
            self._ExtraArgs = ClusterExtraArgs()
            self._ExtraArgs._deserialize(params.get("ExtraArgs"))
        self._NetworkType = params.get("NetworkType")
        self._IsNonStaticIpMode = params.get("IsNonStaticIpMode")
        self._DeletionProtection = params.get("DeletionProtection")
        self._KubeProxyMode = params.get("KubeProxyMode")
        self._AuditEnabled = params.get("AuditEnabled")
        self._AuditLogsetId = params.get("AuditLogsetId")
        self._AuditLogTopicId = params.get("AuditLogTopicId")
        self._VpcCniType = params.get("VpcCniType")
        self._RuntimeVersion = params.get("RuntimeVersion")
        self._EnableCustomizedPodCIDR = params.get("EnableCustomizedPodCIDR")
        self._BasePodNumber = params.get("BasePodNumber")
        self._CiliumMode = params.get("CiliumMode")
        self._IsDualStack = params.get("IsDualStack")
        self._QGPUShareEnable = params.get("QGPUShareEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterAsGroup(AbstractModel):
    """集群关联的伸缩组信息

    """

    def __init__(self):
        r"""
        :param _AutoScalingGroupId: 伸缩组ID
        :type AutoScalingGroupId: str
        :param _Status: 伸缩组状态(开启 enabled 开启中 enabling 关闭 disabled 关闭中 disabling 更新中 updating 删除中 deleting 开启缩容中 scaleDownEnabling 关闭缩容中 scaleDownDisabling)
        :type Status: str
        :param _IsUnschedulable: 节点是否设置成不可调度
注意：此字段可能返回 null，表示取不到有效值。
        :type IsUnschedulable: bool
        :param _Labels: 伸缩组的label列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Labels: list of Label
        :param _CreatedTime: 创建时间
        :type CreatedTime: str
        """
        self._AutoScalingGroupId = None
        self._Status = None
        self._IsUnschedulable = None
        self._Labels = None
        self._CreatedTime = None

    @property
    def AutoScalingGroupId(self):
        return self._AutoScalingGroupId

    @AutoScalingGroupId.setter
    def AutoScalingGroupId(self, AutoScalingGroupId):
        self._AutoScalingGroupId = AutoScalingGroupId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def IsUnschedulable(self):
        return self._IsUnschedulable

    @IsUnschedulable.setter
    def IsUnschedulable(self, IsUnschedulable):
        self._IsUnschedulable = IsUnschedulable

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime


    def _deserialize(self, params):
        self._AutoScalingGroupId = params.get("AutoScalingGroupId")
        self._Status = params.get("Status")
        self._IsUnschedulable = params.get("IsUnschedulable")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        self._CreatedTime = params.get("CreatedTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterAsGroupAttribute(AbstractModel):
    """集群伸缩组属性

    """

    def __init__(self):
        r"""
        :param _AutoScalingGroupId: 伸缩组ID
        :type AutoScalingGroupId: str
        :param _AutoScalingGroupEnabled: 是否开启
        :type AutoScalingGroupEnabled: bool
        :param _AutoScalingGroupRange: 伸缩组最大最小实例数
        :type AutoScalingGroupRange: :class:`tencentcloud.tke.v20180525.models.AutoScalingGroupRange`
        """
        self._AutoScalingGroupId = None
        self._AutoScalingGroupEnabled = None
        self._AutoScalingGroupRange = None

    @property
    def AutoScalingGroupId(self):
        return self._AutoScalingGroupId

    @AutoScalingGroupId.setter
    def AutoScalingGroupId(self, AutoScalingGroupId):
        self._AutoScalingGroupId = AutoScalingGroupId

    @property
    def AutoScalingGroupEnabled(self):
        return self._AutoScalingGroupEnabled

    @AutoScalingGroupEnabled.setter
    def AutoScalingGroupEnabled(self, AutoScalingGroupEnabled):
        self._AutoScalingGroupEnabled = AutoScalingGroupEnabled

    @property
    def AutoScalingGroupRange(self):
        return self._AutoScalingGroupRange

    @AutoScalingGroupRange.setter
    def AutoScalingGroupRange(self, AutoScalingGroupRange):
        self._AutoScalingGroupRange = AutoScalingGroupRange


    def _deserialize(self, params):
        self._AutoScalingGroupId = params.get("AutoScalingGroupId")
        self._AutoScalingGroupEnabled = params.get("AutoScalingGroupEnabled")
        if params.get("AutoScalingGroupRange") is not None:
            self._AutoScalingGroupRange = AutoScalingGroupRange()
            self._AutoScalingGroupRange._deserialize(params.get("AutoScalingGroupRange"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterAsGroupOption(AbstractModel):
    """集群弹性伸缩配置

    """

    def __init__(self):
        r"""
        :param _IsScaleDownEnabled: 是否开启缩容
注意：此字段可能返回 null，表示取不到有效值。
        :type IsScaleDownEnabled: bool
        :param _Expander: 多伸缩组情况下扩容选择算法(random 随机选择，most-pods 最多类型的Pod least-waste 最少的资源浪费，默认为random)
注意：此字段可能返回 null，表示取不到有效值。
        :type Expander: str
        :param _MaxEmptyBulkDelete: 最大并发缩容数
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxEmptyBulkDelete: int
        :param _ScaleDownDelay: 集群扩容后多少分钟开始判断缩容（默认为10分钟）
注意：此字段可能返回 null，表示取不到有效值。
        :type ScaleDownDelay: int
        :param _ScaleDownUnneededTime: 节点连续空闲多少分钟后被缩容（默认为 10分钟）
注意：此字段可能返回 null，表示取不到有效值。
        :type ScaleDownUnneededTime: int
        :param _ScaleDownUtilizationThreshold: 节点资源使用量低于多少(百分比)时认为空闲(默认: 50(百分比))
注意：此字段可能返回 null，表示取不到有效值。
        :type ScaleDownUtilizationThreshold: int
        :param _SkipNodesWithLocalStorage: 含有本地存储Pod的节点是否不缩容(默认： true)
注意：此字段可能返回 null，表示取不到有效值。
        :type SkipNodesWithLocalStorage: bool
        :param _SkipNodesWithSystemPods: 含有kube-system namespace下非DaemonSet管理的Pod的节点是否不缩容 (默认： true)
注意：此字段可能返回 null，表示取不到有效值。
        :type SkipNodesWithSystemPods: bool
        :param _IgnoreDaemonSetsUtilization: 计算资源使用量时是否默认忽略DaemonSet的实例(默认值: False，不忽略)
注意：此字段可能返回 null，表示取不到有效值。
        :type IgnoreDaemonSetsUtilization: bool
        :param _OkTotalUnreadyCount: CA做健康性判断的个数，默认3，即超过OkTotalUnreadyCount个数后，CA会进行健康性判断。
注意：此字段可能返回 null，表示取不到有效值。
        :type OkTotalUnreadyCount: int
        :param _MaxTotalUnreadyPercentage: 未就绪节点的最大百分比，此后CA会停止操作
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxTotalUnreadyPercentage: int
        :param _ScaleDownUnreadyTime: 表示未准备就绪的节点在有资格进行缩减之前应该停留多长时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ScaleDownUnreadyTime: int
        :param _UnregisteredNodeRemovalTime: CA删除未在Kubernetes中注册的节点之前等待的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UnregisteredNodeRemovalTime: int
        """
        self._IsScaleDownEnabled = None
        self._Expander = None
        self._MaxEmptyBulkDelete = None
        self._ScaleDownDelay = None
        self._ScaleDownUnneededTime = None
        self._ScaleDownUtilizationThreshold = None
        self._SkipNodesWithLocalStorage = None
        self._SkipNodesWithSystemPods = None
        self._IgnoreDaemonSetsUtilization = None
        self._OkTotalUnreadyCount = None
        self._MaxTotalUnreadyPercentage = None
        self._ScaleDownUnreadyTime = None
        self._UnregisteredNodeRemovalTime = None

    @property
    def IsScaleDownEnabled(self):
        return self._IsScaleDownEnabled

    @IsScaleDownEnabled.setter
    def IsScaleDownEnabled(self, IsScaleDownEnabled):
        self._IsScaleDownEnabled = IsScaleDownEnabled

    @property
    def Expander(self):
        return self._Expander

    @Expander.setter
    def Expander(self, Expander):
        self._Expander = Expander

    @property
    def MaxEmptyBulkDelete(self):
        return self._MaxEmptyBulkDelete

    @MaxEmptyBulkDelete.setter
    def MaxEmptyBulkDelete(self, MaxEmptyBulkDelete):
        self._MaxEmptyBulkDelete = MaxEmptyBulkDelete

    @property
    def ScaleDownDelay(self):
        return self._ScaleDownDelay

    @ScaleDownDelay.setter
    def ScaleDownDelay(self, ScaleDownDelay):
        self._ScaleDownDelay = ScaleDownDelay

    @property
    def ScaleDownUnneededTime(self):
        return self._ScaleDownUnneededTime

    @ScaleDownUnneededTime.setter
    def ScaleDownUnneededTime(self, ScaleDownUnneededTime):
        self._ScaleDownUnneededTime = ScaleDownUnneededTime

    @property
    def ScaleDownUtilizationThreshold(self):
        return self._ScaleDownUtilizationThreshold

    @ScaleDownUtilizationThreshold.setter
    def ScaleDownUtilizationThreshold(self, ScaleDownUtilizationThreshold):
        self._ScaleDownUtilizationThreshold = ScaleDownUtilizationThreshold

    @property
    def SkipNodesWithLocalStorage(self):
        return self._SkipNodesWithLocalStorage

    @SkipNodesWithLocalStorage.setter
    def SkipNodesWithLocalStorage(self, SkipNodesWithLocalStorage):
        self._SkipNodesWithLocalStorage = SkipNodesWithLocalStorage

    @property
    def SkipNodesWithSystemPods(self):
        return self._SkipNodesWithSystemPods

    @SkipNodesWithSystemPods.setter
    def SkipNodesWithSystemPods(self, SkipNodesWithSystemPods):
        self._SkipNodesWithSystemPods = SkipNodesWithSystemPods

    @property
    def IgnoreDaemonSetsUtilization(self):
        return self._IgnoreDaemonSetsUtilization

    @IgnoreDaemonSetsUtilization.setter
    def IgnoreDaemonSetsUtilization(self, IgnoreDaemonSetsUtilization):
        self._IgnoreDaemonSetsUtilization = IgnoreDaemonSetsUtilization

    @property
    def OkTotalUnreadyCount(self):
        return self._OkTotalUnreadyCount

    @OkTotalUnreadyCount.setter
    def OkTotalUnreadyCount(self, OkTotalUnreadyCount):
        self._OkTotalUnreadyCount = OkTotalUnreadyCount

    @property
    def MaxTotalUnreadyPercentage(self):
        return self._MaxTotalUnreadyPercentage

    @MaxTotalUnreadyPercentage.setter
    def MaxTotalUnreadyPercentage(self, MaxTotalUnreadyPercentage):
        self._MaxTotalUnreadyPercentage = MaxTotalUnreadyPercentage

    @property
    def ScaleDownUnreadyTime(self):
        return self._ScaleDownUnreadyTime

    @ScaleDownUnreadyTime.setter
    def ScaleDownUnreadyTime(self, ScaleDownUnreadyTime):
        self._ScaleDownUnreadyTime = ScaleDownUnreadyTime

    @property
    def UnregisteredNodeRemovalTime(self):
        return self._UnregisteredNodeRemovalTime

    @UnregisteredNodeRemovalTime.setter
    def UnregisteredNodeRemovalTime(self, UnregisteredNodeRemovalTime):
        self._UnregisteredNodeRemovalTime = UnregisteredNodeRemovalTime


    def _deserialize(self, params):
        self._IsScaleDownEnabled = params.get("IsScaleDownEnabled")
        self._Expander = params.get("Expander")
        self._MaxEmptyBulkDelete = params.get("MaxEmptyBulkDelete")
        self._ScaleDownDelay = params.get("ScaleDownDelay")
        self._ScaleDownUnneededTime = params.get("ScaleDownUnneededTime")
        self._ScaleDownUtilizationThreshold = params.get("ScaleDownUtilizationThreshold")
        self._SkipNodesWithLocalStorage = params.get("SkipNodesWithLocalStorage")
        self._SkipNodesWithSystemPods = params.get("SkipNodesWithSystemPods")
        self._IgnoreDaemonSetsUtilization = params.get("IgnoreDaemonSetsUtilization")
        self._OkTotalUnreadyCount = params.get("OkTotalUnreadyCount")
        self._MaxTotalUnreadyPercentage = params.get("MaxTotalUnreadyPercentage")
        self._ScaleDownUnreadyTime = params.get("ScaleDownUnreadyTime")
        self._UnregisteredNodeRemovalTime = params.get("UnregisteredNodeRemovalTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterBasicSettings(AbstractModel):
    """描述集群的基本配置信息

    """

    def __init__(self):
        r"""
        :param _ClusterOs: 集群操作系统，支持设置公共镜像(字段传相应镜像Name)和自定义镜像(字段传相应镜像ID)，详情参考：https://cloud.tencent.com/document/product/457/68289
        :type ClusterOs: str
        :param _ClusterVersion: 集群版本,默认值为1.10.5
        :type ClusterVersion: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _ClusterDescription: 集群描述
        :type ClusterDescription: str
        :param _VpcId: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type VpcId: str
        :param _ProjectId: 集群内新增资源所属项目ID。
        :type ProjectId: int
        :param _TagSpecification: 标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到集群实例。
        :type TagSpecification: list of TagSpecification
        :param _OsCustomizeType: 容器的镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
        :type OsCustomizeType: str
        :param _NeedWorkSecurityGroup: 是否开启节点的默认安全组(默认: 否，Alpha特性)
        :type NeedWorkSecurityGroup: bool
        :param _SubnetId: 当选择Cilium Overlay网络插件时，TKE会从该子网获取2个IP用来创建内网负载均衡
        :type SubnetId: str
        :param _ClusterLevel: 集群等级，针对托管集群生效
        :type ClusterLevel: str
        :param _AutoUpgradeClusterLevel: 自动变配集群等级，针对托管集群生效
        :type AutoUpgradeClusterLevel: :class:`tencentcloud.tke.v20180525.models.AutoUpgradeClusterLevel`
        """
        self._ClusterOs = None
        self._ClusterVersion = None
        self._ClusterName = None
        self._ClusterDescription = None
        self._VpcId = None
        self._ProjectId = None
        self._TagSpecification = None
        self._OsCustomizeType = None
        self._NeedWorkSecurityGroup = None
        self._SubnetId = None
        self._ClusterLevel = None
        self._AutoUpgradeClusterLevel = None

    @property
    def ClusterOs(self):
        return self._ClusterOs

    @ClusterOs.setter
    def ClusterOs(self, ClusterOs):
        self._ClusterOs = ClusterOs

    @property
    def ClusterVersion(self):
        return self._ClusterVersion

    @ClusterVersion.setter
    def ClusterVersion(self, ClusterVersion):
        self._ClusterVersion = ClusterVersion

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ClusterDescription(self):
        return self._ClusterDescription

    @ClusterDescription.setter
    def ClusterDescription(self, ClusterDescription):
        self._ClusterDescription = ClusterDescription

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def TagSpecification(self):
        return self._TagSpecification

    @TagSpecification.setter
    def TagSpecification(self, TagSpecification):
        self._TagSpecification = TagSpecification

    @property
    def OsCustomizeType(self):
        return self._OsCustomizeType

    @OsCustomizeType.setter
    def OsCustomizeType(self, OsCustomizeType):
        self._OsCustomizeType = OsCustomizeType

    @property
    def NeedWorkSecurityGroup(self):
        return self._NeedWorkSecurityGroup

    @NeedWorkSecurityGroup.setter
    def NeedWorkSecurityGroup(self, NeedWorkSecurityGroup):
        self._NeedWorkSecurityGroup = NeedWorkSecurityGroup

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel


    def _deserialize(self, params):
        self._ClusterOs = params.get("ClusterOs")
        self._ClusterVersion = params.get("ClusterVersion")
        self._ClusterName = params.get("ClusterName")
        self._ClusterDescription = params.get("ClusterDescription")
        self._VpcId = params.get("VpcId")
        self._ProjectId = params.get("ProjectId")
        if params.get("TagSpecification") is not None:
            self._TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self._TagSpecification.append(obj)
        self._OsCustomizeType = params.get("OsCustomizeType")
        self._NeedWorkSecurityGroup = params.get("NeedWorkSecurityGroup")
        self._SubnetId = params.get("SubnetId")
        self._ClusterLevel = params.get("ClusterLevel")
        if params.get("AutoUpgradeClusterLevel") is not None:
            self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel()
            self._AutoUpgradeClusterLevel._deserialize(params.get("AutoUpgradeClusterLevel"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterCIDRSettings(AbstractModel):
    """集群容器网络相关参数

    """

    def __init__(self):
        r"""
        :param _ClusterCIDR: 用于分配集群容器和服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突。且网段范围必须在内网网段内，例如:10.1.0.0/14, 192.168.0.1/18,172.16.0.0/16。
        :type ClusterCIDR: str
        :param _IgnoreClusterCIDRConflict: 是否忽略 ClusterCIDR 冲突错误, 默认不忽略
        :type IgnoreClusterCIDRConflict: bool
        :param _MaxNodePodNum: 集群中每个Node上最大的Pod数量。取值范围16～256。不为2的幂值时会向上取最接近的2的幂值。
        :type MaxNodePodNum: int
        :param _MaxClusterServiceNum: 集群最大的service数量。取值范围32～32768，不为2的幂值时会向上取最接近的2的幂值。默认值256
        :type MaxClusterServiceNum: int
        :param _ServiceCIDR: 用于分配集群服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突。且网段范围必须在内网网段内，例如:10.1.0.0/14, 192.168.0.1/18,172.16.0.0/16。
        :type ServiceCIDR: str
        :param _EniSubnetIds: VPC-CNI网络模式下，弹性网卡的子网Id。
        :type EniSubnetIds: list of str
        :param _ClaimExpiredSeconds: VPC-CNI网络模式下，弹性网卡IP的回收时间，取值范围[300,15768000)
        :type ClaimExpiredSeconds: int
        :param _IgnoreServiceCIDRConflict: 是否忽略 ServiceCIDR 冲突错误, 仅在 VPC-CNI 模式生效，默认不忽略
        :type IgnoreServiceCIDRConflict: bool
        """
        self._ClusterCIDR = None
        self._IgnoreClusterCIDRConflict = None
        self._MaxNodePodNum = None
        self._MaxClusterServiceNum = None
        self._ServiceCIDR = None
        self._EniSubnetIds = None
        self._ClaimExpiredSeconds = None
        self._IgnoreServiceCIDRConflict = None

    @property
    def ClusterCIDR(self):
        return self._ClusterCIDR

    @ClusterCIDR.setter
    def ClusterCIDR(self, ClusterCIDR):
        self._ClusterCIDR = ClusterCIDR

    @property
    def IgnoreClusterCIDRConflict(self):
        return self._IgnoreClusterCIDRConflict

    @IgnoreClusterCIDRConflict.setter
    def IgnoreClusterCIDRConflict(self, IgnoreClusterCIDRConflict):
        self._IgnoreClusterCIDRConflict = IgnoreClusterCIDRConflict

    @property
    def MaxNodePodNum(self):
        return self._MaxNodePodNum

    @MaxNodePodNum.setter
    def MaxNodePodNum(self, MaxNodePodNum):
        self._MaxNodePodNum = MaxNodePodNum

    @property
    def MaxClusterServiceNum(self):
        return self._MaxClusterServiceNum

    @MaxClusterServiceNum.setter
    def MaxClusterServiceNum(self, MaxClusterServiceNum):
        self._MaxClusterServiceNum = MaxClusterServiceNum

    @property
    def ServiceCIDR(self):
        return self._ServiceCIDR

    @ServiceCIDR.setter
    def ServiceCIDR(self, ServiceCIDR):
        self._ServiceCIDR = ServiceCIDR

    @property
    def EniSubnetIds(self):
        return self._EniSubnetIds

    @EniSubnetIds.setter
    def EniSubnetIds(self, EniSubnetIds):
        self._EniSubnetIds = EniSubnetIds

    @property
    def ClaimExpiredSeconds(self):
        return self._ClaimExpiredSeconds

    @ClaimExpiredSeconds.setter
    def ClaimExpiredSeconds(self, ClaimExpiredSeconds):
        self._ClaimExpiredSeconds = ClaimExpiredSeconds

    @property
    def IgnoreServiceCIDRConflict(self):
        return self._IgnoreServiceCIDRConflict

    @IgnoreServiceCIDRConflict.setter
    def IgnoreServiceCIDRConflict(self, IgnoreServiceCIDRConflict):
        self._IgnoreServiceCIDRConflict = IgnoreServiceCIDRConflict


    def _deserialize(self, params):
        self._ClusterCIDR = params.get("ClusterCIDR")
        self._IgnoreClusterCIDRConflict = params.get("IgnoreClusterCIDRConflict")
        self._MaxNodePodNum = params.get("MaxNodePodNum")
        self._MaxClusterServiceNum = params.get("MaxClusterServiceNum")
        self._ServiceCIDR = params.get("ServiceCIDR")
        self._EniSubnetIds = params.get("EniSubnetIds")
        self._ClaimExpiredSeconds = params.get("ClaimExpiredSeconds")
        self._IgnoreServiceCIDRConflict = params.get("IgnoreServiceCIDRConflict")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterCondition(AbstractModel):
    """集群创建过程

    """

    def __init__(self):
        r"""
        :param _Type: 集群创建过程类型
        :type Type: str
        :param _Status: 集群创建过程状态
        :type Status: str
        :param _LastProbeTime: 最后一次探测到该状态的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastProbeTime: str
        :param _LastTransitionTime: 最后一次转换到该过程的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastTransitionTime: str
        :param _Reason: 转换到该过程的简明原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param _Message: 转换到该过程的更多信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        """
        self._Type = None
        self._Status = None
        self._LastProbeTime = None
        self._LastTransitionTime = None
        self._Reason = None
        self._Message = None

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def LastProbeTime(self):
        return self._LastProbeTime

    @LastProbeTime.setter
    def LastProbeTime(self, LastProbeTime):
        self._LastProbeTime = LastProbeTime

    @property
    def LastTransitionTime(self):
        return self._LastTransitionTime

    @LastTransitionTime.setter
    def LastTransitionTime(self, LastTransitionTime):
        self._LastTransitionTime = LastTransitionTime

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason

    @property
    def Message(self):
        return self._Message

    @Message.setter
    def Message(self, Message):
        self._Message = Message


    def _deserialize(self, params):
        self._Type = params.get("Type")
        self._Status = params.get("Status")
        self._LastProbeTime = params.get("LastProbeTime")
        self._LastTransitionTime = params.get("LastTransitionTime")
        self._Reason = params.get("Reason")
        self._Message = params.get("Message")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterCredential(AbstractModel):
    """接入k8s 的认证信息

    """

    def __init__(self):
        r"""
        :param _CACert: CA 根证书
        :type CACert: str
        :param _Token: 认证用的Token
        :type Token: str
        """
        self._CACert = None
        self._Token = None

    @property
    def CACert(self):
        return self._CACert

    @CACert.setter
    def CACert(self, CACert):
        self._CACert = CACert

    @property
    def Token(self):
        return self._Token

    @Token.setter
    def Token(self, Token):
        self._Token = Token


    def _deserialize(self, params):
        self._CACert = params.get("CACert")
        self._Token = params.get("Token")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterExtraArgs(AbstractModel):
    """集群master自定义参数

    """

    def __init__(self):
        r"""
        :param _KubeAPIServer: kube-apiserver自定义参数，参数格式为["k1=v1", "k1=v2"]， 例如["max-requests-inflight=500","feature-gates=PodShareProcessNamespace=true,DynamicKubeletConfig=true"]
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeAPIServer: list of str
        :param _KubeControllerManager: kube-controller-manager自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeControllerManager: list of str
        :param _KubeScheduler: kube-scheduler自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeScheduler: list of str
        :param _Etcd: etcd自定义参数，只支持独立集群
注意：此字段可能返回 null，表示取不到有效值。
        :type Etcd: list of str
        """
        self._KubeAPIServer = None
        self._KubeControllerManager = None
        self._KubeScheduler = None
        self._Etcd = None

    @property
    def KubeAPIServer(self):
        return self._KubeAPIServer

    @KubeAPIServer.setter
    def KubeAPIServer(self, KubeAPIServer):
        self._KubeAPIServer = KubeAPIServer

    @property
    def KubeControllerManager(self):
        return self._KubeControllerManager

    @KubeControllerManager.setter
    def KubeControllerManager(self, KubeControllerManager):
        self._KubeControllerManager = KubeControllerManager

    @property
    def KubeScheduler(self):
        return self._KubeScheduler

    @KubeScheduler.setter
    def KubeScheduler(self, KubeScheduler):
        self._KubeScheduler = KubeScheduler

    @property
    def Etcd(self):
        return self._Etcd

    @Etcd.setter
    def Etcd(self, Etcd):
        self._Etcd = Etcd


    def _deserialize(self, params):
        self._KubeAPIServer = params.get("KubeAPIServer")
        self._KubeControllerManager = params.get("KubeControllerManager")
        self._KubeScheduler = params.get("KubeScheduler")
        self._Etcd = params.get("Etcd")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterInternalLB(AbstractModel):
    """弹性容器集群内网访问LB信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启内网访问LB
        :type Enabled: bool
        :param _SubnetId: 内网访问LB关联的子网Id
        :type SubnetId: str
        """
        self._Enabled = None
        self._SubnetId = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterLevelAttribute(AbstractModel):
    """托管集群等级属性

    """

    def __init__(self):
        r"""
        :param _Name: 集群等级
        :type Name: str
        :param _Alias: 等级名称
        :type Alias: str
        :param _NodeCount: 节点数量
        :type NodeCount: int
        :param _PodCount: Pod数量
        :type PodCount: int
        :param _ConfigMapCount: Configmap数量
        :type ConfigMapCount: int
        :param _RSCount: ReplicaSets数量
        :type RSCount: int
        :param _CRDCount: CRD数量
        :type CRDCount: int
        :param _Enable: 是否启用
        :type Enable: bool
        :param _OtherCount: 其他资源数量
注意：此字段可能返回 null，表示取不到有效值。
        :type OtherCount: int
        """
        self._Name = None
        self._Alias = None
        self._NodeCount = None
        self._PodCount = None
        self._ConfigMapCount = None
        self._RSCount = None
        self._CRDCount = None
        self._Enable = None
        self._OtherCount = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Alias(self):
        return self._Alias

    @Alias.setter
    def Alias(self, Alias):
        self._Alias = Alias

    @property
    def NodeCount(self):
        return self._NodeCount

    @NodeCount.setter
    def NodeCount(self, NodeCount):
        self._NodeCount = NodeCount

    @property
    def PodCount(self):
        return self._PodCount

    @PodCount.setter
    def PodCount(self, PodCount):
        self._PodCount = PodCount

    @property
    def ConfigMapCount(self):
        return self._ConfigMapCount

    @ConfigMapCount.setter
    def ConfigMapCount(self, ConfigMapCount):
        self._ConfigMapCount = ConfigMapCount

    @property
    def RSCount(self):
        return self._RSCount

    @RSCount.setter
    def RSCount(self, RSCount):
        self._RSCount = RSCount

    @property
    def CRDCount(self):
        return self._CRDCount

    @CRDCount.setter
    def CRDCount(self, CRDCount):
        self._CRDCount = CRDCount

    @property
    def Enable(self):
        return self._Enable

    @Enable.setter
    def Enable(self, Enable):
        self._Enable = Enable

    @property
    def OtherCount(self):
        return self._OtherCount

    @OtherCount.setter
    def OtherCount(self, OtherCount):
        self._OtherCount = OtherCount


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Alias = params.get("Alias")
        self._NodeCount = params.get("NodeCount")
        self._PodCount = params.get("PodCount")
        self._ConfigMapCount = params.get("ConfigMapCount")
        self._RSCount = params.get("RSCount")
        self._CRDCount = params.get("CRDCount")
        self._Enable = params.get("Enable")
        self._OtherCount = params.get("OtherCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterLevelChangeRecord(AbstractModel):
    """集群等级变配记录

    """

    def __init__(self):
        r"""
        :param _ID: 记录ID
        :type ID: str
        :param _ClusterID: 集群ID
        :type ClusterID: str
        :param _Status: 变配状态：trading 发货中,upgrading 变配中,success 变配成功,failed 变配失败。
        :type Status: str
        :param _Message: 状态描述
        :type Message: str
        :param _OldLevel: 变配前规模
        :type OldLevel: str
        :param _NewLevel: 变配后规模
        :type NewLevel: str
        :param _TriggerType: 变配触发类型：manual 手动,auto 自动
        :type TriggerType: str
        :param _CreatedAt: 创建时间
        :type CreatedAt: str
        :param _StartedAt: 开始时间
        :type StartedAt: str
        :param _EndedAt: 结束时间
        :type EndedAt: str
        """
        self._ID = None
        self._ClusterID = None
        self._Status = None
        self._Message = None
        self._OldLevel = None
        self._NewLevel = None
        self._TriggerType = None
        self._CreatedAt = None
        self._StartedAt = None
        self._EndedAt = None

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Message(self):
        return self._Message

    @Message.setter
    def Message(self, Message):
        self._Message = Message

    @property
    def OldLevel(self):
        return self._OldLevel

    @OldLevel.setter
    def OldLevel(self, OldLevel):
        self._OldLevel = OldLevel

    @property
    def NewLevel(self):
        return self._NewLevel

    @NewLevel.setter
    def NewLevel(self, NewLevel):
        self._NewLevel = NewLevel

    @property
    def TriggerType(self):
        return self._TriggerType

    @TriggerType.setter
    def TriggerType(self, TriggerType):
        self._TriggerType = TriggerType

    @property
    def CreatedAt(self):
        return self._CreatedAt

    @CreatedAt.setter
    def CreatedAt(self, CreatedAt):
        self._CreatedAt = CreatedAt

    @property
    def StartedAt(self):
        return self._StartedAt

    @StartedAt.setter
    def StartedAt(self, StartedAt):
        self._StartedAt = StartedAt

    @property
    def EndedAt(self):
        return self._EndedAt

    @EndedAt.setter
    def EndedAt(self, EndedAt):
        self._EndedAt = EndedAt


    def _deserialize(self, params):
        self._ID = params.get("ID")
        self._ClusterID = params.get("ClusterID")
        self._Status = params.get("Status")
        self._Message = params.get("Message")
        self._OldLevel = params.get("OldLevel")
        self._NewLevel = params.get("NewLevel")
        self._TriggerType = params.get("TriggerType")
        self._CreatedAt = params.get("CreatedAt")
        self._StartedAt = params.get("StartedAt")
        self._EndedAt = params.get("EndedAt")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterNetworkSettings(AbstractModel):
    """集群网络相关的参数

    """

    def __init__(self):
        r"""
        :param _ClusterCIDR: 用于分配集群容器和服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突
        :type ClusterCIDR: str
        :param _IgnoreClusterCIDRConflict: 是否忽略 ClusterCIDR 冲突错误, 默认不忽略
        :type IgnoreClusterCIDRConflict: bool
        :param _MaxNodePodNum: 集群中每个Node上最大的Pod数量(默认为256)
        :type MaxNodePodNum: int
        :param _MaxClusterServiceNum: 集群最大的service数量(默认为256)
        :type MaxClusterServiceNum: int
        :param _Ipvs: 是否启用IPVS(默认不开启)
        :type Ipvs: bool
        :param _VpcId: 集群的VPCID（如果创建空集群，为必传值，否则自动设置为和集群的节点保持一致）
        :type VpcId: str
        :param _Cni: 网络插件是否启用CNI(默认开启)
        :type Cni: bool
        :param _KubeProxyMode: service的网络模式，当前参数只适用于ipvs+bpf模式
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeProxyMode: str
        :param _ServiceCIDR: 用于分配service的IP range，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceCIDR: str
        :param _Subnets: 集群关联的容器子网
注意：此字段可能返回 null，表示取不到有效值。
        :type Subnets: list of str
        :param _IgnoreServiceCIDRConflict: 是否忽略 ServiceCIDR 冲突错误, 仅在 VPC-CNI 模式生效，默认不忽略
注意：此字段可能返回 null，表示取不到有效值。
        :type IgnoreServiceCIDRConflict: bool
        :param _IsDualStack: 集群VPC-CNI模式是否为非双栈集群，默认false，非双栈。
注意：此字段可能返回 null，表示取不到有效值。
        :type IsDualStack: bool
        :param _Ipv6ServiceCIDR: 用于分配service的IP range，由系统自动分配
注意：此字段可能返回 null，表示取不到有效值。
        :type Ipv6ServiceCIDR: str
        :param _CiliumMode: 集群Cilium Mode配置
- clusterIP
注意：此字段可能返回 null，表示取不到有效值。
        :type CiliumMode: str
        """
        self._ClusterCIDR = None
        self._IgnoreClusterCIDRConflict = None
        self._MaxNodePodNum = None
        self._MaxClusterServiceNum = None
        self._Ipvs = None
        self._VpcId = None
        self._Cni = None
        self._KubeProxyMode = None
        self._ServiceCIDR = None
        self._Subnets = None
        self._IgnoreServiceCIDRConflict = None
        self._IsDualStack = None
        self._Ipv6ServiceCIDR = None
        self._CiliumMode = None

    @property
    def ClusterCIDR(self):
        return self._ClusterCIDR

    @ClusterCIDR.setter
    def ClusterCIDR(self, ClusterCIDR):
        self._ClusterCIDR = ClusterCIDR

    @property
    def IgnoreClusterCIDRConflict(self):
        return self._IgnoreClusterCIDRConflict

    @IgnoreClusterCIDRConflict.setter
    def IgnoreClusterCIDRConflict(self, IgnoreClusterCIDRConflict):
        self._IgnoreClusterCIDRConflict = IgnoreClusterCIDRConflict

    @property
    def MaxNodePodNum(self):
        return self._MaxNodePodNum

    @MaxNodePodNum.setter
    def MaxNodePodNum(self, MaxNodePodNum):
        self._MaxNodePodNum = MaxNodePodNum

    @property
    def MaxClusterServiceNum(self):
        return self._MaxClusterServiceNum

    @MaxClusterServiceNum.setter
    def MaxClusterServiceNum(self, MaxClusterServiceNum):
        self._MaxClusterServiceNum = MaxClusterServiceNum

    @property
    def Ipvs(self):
        return self._Ipvs

    @Ipvs.setter
    def Ipvs(self, Ipvs):
        self._Ipvs = Ipvs

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def Cni(self):
        return self._Cni

    @Cni.setter
    def Cni(self, Cni):
        self._Cni = Cni

    @property
    def KubeProxyMode(self):
        return self._KubeProxyMode

    @KubeProxyMode.setter
    def KubeProxyMode(self, KubeProxyMode):
        self._KubeProxyMode = KubeProxyMode

    @property
    def ServiceCIDR(self):
        return self._ServiceCIDR

    @ServiceCIDR.setter
    def ServiceCIDR(self, ServiceCIDR):
        self._ServiceCIDR = ServiceCIDR

    @property
    def Subnets(self):
        return self._Subnets

    @Subnets.setter
    def Subnets(self, Subnets):
        self._Subnets = Subnets

    @property
    def IgnoreServiceCIDRConflict(self):
        return self._IgnoreServiceCIDRConflict

    @IgnoreServiceCIDRConflict.setter
    def IgnoreServiceCIDRConflict(self, IgnoreServiceCIDRConflict):
        self._IgnoreServiceCIDRConflict = IgnoreServiceCIDRConflict

    @property
    def IsDualStack(self):
        return self._IsDualStack

    @IsDualStack.setter
    def IsDualStack(self, IsDualStack):
        self._IsDualStack = IsDualStack

    @property
    def Ipv6ServiceCIDR(self):
        return self._Ipv6ServiceCIDR

    @Ipv6ServiceCIDR.setter
    def Ipv6ServiceCIDR(self, Ipv6ServiceCIDR):
        self._Ipv6ServiceCIDR = Ipv6ServiceCIDR

    @property
    def CiliumMode(self):
        return self._CiliumMode

    @CiliumMode.setter
    def CiliumMode(self, CiliumMode):
        self._CiliumMode = CiliumMode


    def _deserialize(self, params):
        self._ClusterCIDR = params.get("ClusterCIDR")
        self._IgnoreClusterCIDRConflict = params.get("IgnoreClusterCIDRConflict")
        self._MaxNodePodNum = params.get("MaxNodePodNum")
        self._MaxClusterServiceNum = params.get("MaxClusterServiceNum")
        self._Ipvs = params.get("Ipvs")
        self._VpcId = params.get("VpcId")
        self._Cni = params.get("Cni")
        self._KubeProxyMode = params.get("KubeProxyMode")
        self._ServiceCIDR = params.get("ServiceCIDR")
        self._Subnets = params.get("Subnets")
        self._IgnoreServiceCIDRConflict = params.get("IgnoreServiceCIDRConflict")
        self._IsDualStack = params.get("IsDualStack")
        self._Ipv6ServiceCIDR = params.get("Ipv6ServiceCIDR")
        self._CiliumMode = params.get("CiliumMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterProperty(AbstractModel):
    """集群属性

    """

    def __init__(self):
        r"""
        :param _NodeNameType: 节点hostname命名模式
注意：此字段可能返回 null，表示取不到有效值。
        :type NodeNameType: str
        """
        self._NodeNameType = None

    @property
    def NodeNameType(self):
        return self._NodeNameType

    @NodeNameType.setter
    def NodeNameType(self, NodeNameType):
        self._NodeNameType = NodeNameType


    def _deserialize(self, params):
        self._NodeNameType = params.get("NodeNameType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterPublicLB(AbstractModel):
    """弹性容器集群公网访问负载均衡信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启公网访问LB
        :type Enabled: bool
        :param _AllowFromCidrs: 允许访问的来源CIDR列表
        :type AllowFromCidrs: list of str
        :param _SecurityPolicies: 安全策略放通单个IP或CIDR(例如: "192.168.1.0/24",默认为拒绝所有)
        :type SecurityPolicies: list of str
        :param _ExtraParam: 外网访问相关的扩展参数，格式为json
        :type ExtraParam: str
        :param _SecurityGroup: 新内外网功能，需要传递安全组
        :type SecurityGroup: str
        """
        self._Enabled = None
        self._AllowFromCidrs = None
        self._SecurityPolicies = None
        self._ExtraParam = None
        self._SecurityGroup = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def AllowFromCidrs(self):
        return self._AllowFromCidrs

    @AllowFromCidrs.setter
    def AllowFromCidrs(self, AllowFromCidrs):
        self._AllowFromCidrs = AllowFromCidrs

    @property
    def SecurityPolicies(self):
        return self._SecurityPolicies

    @SecurityPolicies.setter
    def SecurityPolicies(self, SecurityPolicies):
        self._SecurityPolicies = SecurityPolicies

    @property
    def ExtraParam(self):
        return self._ExtraParam

    @ExtraParam.setter
    def ExtraParam(self, ExtraParam):
        self._ExtraParam = ExtraParam

    @property
    def SecurityGroup(self):
        return self._SecurityGroup

    @SecurityGroup.setter
    def SecurityGroup(self, SecurityGroup):
        self._SecurityGroup = SecurityGroup


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._AllowFromCidrs = params.get("AllowFromCidrs")
        self._SecurityPolicies = params.get("SecurityPolicies")
        self._ExtraParam = params.get("ExtraParam")
        self._SecurityGroup = params.get("SecurityGroup")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterStatus(AbstractModel):
    """集群状态信息

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群Id
        :type ClusterId: str
        :param _ClusterState: 集群状态
        :type ClusterState: str
        :param _ClusterInstanceState: 集群下机器实例的状态
        :type ClusterInstanceState: str
        :param _ClusterBMonitor: 集群是否开启监控
        :type ClusterBMonitor: bool
        :param _ClusterInitNodeNum: 集群创建中的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
        :type ClusterInitNodeNum: int
        :param _ClusterRunningNodeNum: 集群运行中的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
        :type ClusterRunningNodeNum: int
        :param _ClusterFailedNodeNum: 集群异常的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
        :type ClusterFailedNodeNum: int
        :param _ClusterClosedNodeNum: 集群已关机的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterClosedNodeNum: int
        :param _ClusterClosingNodeNum: 集群关机中的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterClosingNodeNum: int
        :param _ClusterDeletionProtection: 集群是否开启删除保护
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterDeletionProtection: bool
        :param _ClusterAuditEnabled: 集群是否可审计
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterAuditEnabled: bool
        """
        self._ClusterId = None
        self._ClusterState = None
        self._ClusterInstanceState = None
        self._ClusterBMonitor = None
        self._ClusterInitNodeNum = None
        self._ClusterRunningNodeNum = None
        self._ClusterFailedNodeNum = None
        self._ClusterClosedNodeNum = None
        self._ClusterClosingNodeNum = None
        self._ClusterDeletionProtection = None
        self._ClusterAuditEnabled = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterState(self):
        return self._ClusterState

    @ClusterState.setter
    def ClusterState(self, ClusterState):
        self._ClusterState = ClusterState

    @property
    def ClusterInstanceState(self):
        return self._ClusterInstanceState

    @ClusterInstanceState.setter
    def ClusterInstanceState(self, ClusterInstanceState):
        self._ClusterInstanceState = ClusterInstanceState

    @property
    def ClusterBMonitor(self):
        return self._ClusterBMonitor

    @ClusterBMonitor.setter
    def ClusterBMonitor(self, ClusterBMonitor):
        self._ClusterBMonitor = ClusterBMonitor

    @property
    def ClusterInitNodeNum(self):
        return self._ClusterInitNodeNum

    @ClusterInitNodeNum.setter
    def ClusterInitNodeNum(self, ClusterInitNodeNum):
        self._ClusterInitNodeNum = ClusterInitNodeNum

    @property
    def ClusterRunningNodeNum(self):
        return self._ClusterRunningNodeNum

    @ClusterRunningNodeNum.setter
    def ClusterRunningNodeNum(self, ClusterRunningNodeNum):
        self._ClusterRunningNodeNum = ClusterRunningNodeNum

    @property
    def ClusterFailedNodeNum(self):
        return self._ClusterFailedNodeNum

    @ClusterFailedNodeNum.setter
    def ClusterFailedNodeNum(self, ClusterFailedNodeNum):
        self._ClusterFailedNodeNum = ClusterFailedNodeNum

    @property
    def ClusterClosedNodeNum(self):
        return self._ClusterClosedNodeNum

    @ClusterClosedNodeNum.setter
    def ClusterClosedNodeNum(self, ClusterClosedNodeNum):
        self._ClusterClosedNodeNum = ClusterClosedNodeNum

    @property
    def ClusterClosingNodeNum(self):
        return self._ClusterClosingNodeNum

    @ClusterClosingNodeNum.setter
    def ClusterClosingNodeNum(self, ClusterClosingNodeNum):
        self._ClusterClosingNodeNum = ClusterClosingNodeNum

    @property
    def ClusterDeletionProtection(self):
        return self._ClusterDeletionProtection

    @ClusterDeletionProtection.setter
    def ClusterDeletionProtection(self, ClusterDeletionProtection):
        self._ClusterDeletionProtection = ClusterDeletionProtection

    @property
    def ClusterAuditEnabled(self):
        return self._ClusterAuditEnabled

    @ClusterAuditEnabled.setter
    def ClusterAuditEnabled(self, ClusterAuditEnabled):
        self._ClusterAuditEnabled = ClusterAuditEnabled


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterState = params.get("ClusterState")
        self._ClusterInstanceState = params.get("ClusterInstanceState")
        self._ClusterBMonitor = params.get("ClusterBMonitor")
        self._ClusterInitNodeNum = params.get("ClusterInitNodeNum")
        self._ClusterRunningNodeNum = params.get("ClusterRunningNodeNum")
        self._ClusterFailedNodeNum = params.get("ClusterFailedNodeNum")
        self._ClusterClosedNodeNum = params.get("ClusterClosedNodeNum")
        self._ClusterClosingNodeNum = params.get("ClusterClosingNodeNum")
        self._ClusterDeletionProtection = params.get("ClusterDeletionProtection")
        self._ClusterAuditEnabled = params.get("ClusterAuditEnabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterVersion(AbstractModel):
    """集群版本信息

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Versions: 集群主版本号列表，例如1.18.4
        :type Versions: list of str
        """
        self._ClusterId = None
        self._Versions = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Versions(self):
        return self._Versions

    @Versions.setter
    def Versions(self, Versions):
        self._Versions = Versions


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Versions = params.get("Versions")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CommonName(AbstractModel):
    """账户UIN与客户端证书CommonName的映射

    """

    def __init__(self):
        r"""
        :param _SubaccountUin: 子账户UIN
        :type SubaccountUin: str
        :param _CN: 子账户客户端证书中的CommonName字段
        :type CN: str
        """
        self._SubaccountUin = None
        self._CN = None

    @property
    def SubaccountUin(self):
        return self._SubaccountUin

    @SubaccountUin.setter
    def SubaccountUin(self, SubaccountUin):
        self._SubaccountUin = SubaccountUin

    @property
    def CN(self):
        return self._CN

    @CN.setter
    def CN(self, CN):
        self._CN = CN


    def _deserialize(self, params):
        self._SubaccountUin = params.get("SubaccountUin")
        self._CN = params.get("CN")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Container(AbstractModel):
    """EKS Instance Container容器

    """

    def __init__(self):
        r"""
        :param _Image: 镜像
        :type Image: str
        :param _Name: 容器名
        :type Name: str
        :param _Commands: 容器启动命令
        :type Commands: list of str
        :param _Args: 容器启动参数
        :type Args: list of str
        :param _EnvironmentVars: 容器内操作系统的环境变量
        :type EnvironmentVars: list of EnvironmentVariable
        :param _Cpu: CPU，制改容器最多可使用的核数，该值不可超过容器实例的总核数。单位：核。
        :type Cpu: float
        :param _Memory: 内存，限制该容器最多可使用的内存值，该值不可超过容器实例的总内存值。单位：GiB
        :type Memory: float
        :param _VolumeMounts: 数据卷挂载信息
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeMounts: list of VolumeMount
        :param _CurrentState: 当前状态
注意：此字段可能返回 null，表示取不到有效值。
        :type CurrentState: :class:`tencentcloud.tke.v20180525.models.ContainerState`
        :param _RestartCount: 重启次数
注意：此字段可能返回 null，表示取不到有效值。
        :type RestartCount: int
        :param _WorkingDir: 容器工作目录
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkingDir: str
        :param _LivenessProbe: 存活探针
注意：此字段可能返回 null，表示取不到有效值。
        :type LivenessProbe: :class:`tencentcloud.tke.v20180525.models.LivenessOrReadinessProbe`
        :param _ReadinessProbe: 就绪探针
注意：此字段可能返回 null，表示取不到有效值。
        :type ReadinessProbe: :class:`tencentcloud.tke.v20180525.models.LivenessOrReadinessProbe`
        :param _GpuLimit: Gpu限制
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuLimit: int
        :param _SecurityContext: 容器的安全上下文
注意：此字段可能返回 null，表示取不到有效值。
        :type SecurityContext: :class:`tencentcloud.tke.v20180525.models.SecurityContext`
        """
        self._Image = None
        self._Name = None
        self._Commands = None
        self._Args = None
        self._EnvironmentVars = None
        self._Cpu = None
        self._Memory = None
        self._VolumeMounts = None
        self._CurrentState = None
        self._RestartCount = None
        self._WorkingDir = None
        self._LivenessProbe = None
        self._ReadinessProbe = None
        self._GpuLimit = None
        self._SecurityContext = None

    @property
    def Image(self):
        return self._Image

    @Image.setter
    def Image(self, Image):
        self._Image = Image

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Commands(self):
        return self._Commands

    @Commands.setter
    def Commands(self, Commands):
        self._Commands = Commands

    @property
    def Args(self):
        return self._Args

    @Args.setter
    def Args(self, Args):
        self._Args = Args

    @property
    def EnvironmentVars(self):
        return self._EnvironmentVars

    @EnvironmentVars.setter
    def EnvironmentVars(self, EnvironmentVars):
        self._EnvironmentVars = EnvironmentVars

    @property
    def Cpu(self):
        return self._Cpu

    @Cpu.setter
    def Cpu(self, Cpu):
        self._Cpu = Cpu

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def VolumeMounts(self):
        return self._VolumeMounts

    @VolumeMounts.setter
    def VolumeMounts(self, VolumeMounts):
        self._VolumeMounts = VolumeMounts

    @property
    def CurrentState(self):
        return self._CurrentState

    @CurrentState.setter
    def CurrentState(self, CurrentState):
        self._CurrentState = CurrentState

    @property
    def RestartCount(self):
        return self._RestartCount

    @RestartCount.setter
    def RestartCount(self, RestartCount):
        self._RestartCount = RestartCount

    @property
    def WorkingDir(self):
        return self._WorkingDir

    @WorkingDir.setter
    def WorkingDir(self, WorkingDir):
        self._WorkingDir = WorkingDir

    @property
    def LivenessProbe(self):
        return self._LivenessProbe

    @LivenessProbe.setter
    def LivenessProbe(self, LivenessProbe):
        self._LivenessProbe = LivenessProbe

    @property
    def ReadinessProbe(self):
        return self._ReadinessProbe

    @ReadinessProbe.setter
    def ReadinessProbe(self, ReadinessProbe):
        self._ReadinessProbe = ReadinessProbe

    @property
    def GpuLimit(self):
        return self._GpuLimit

    @GpuLimit.setter
    def GpuLimit(self, GpuLimit):
        self._GpuLimit = GpuLimit

    @property
    def SecurityContext(self):
        return self._SecurityContext

    @SecurityContext.setter
    def SecurityContext(self, SecurityContext):
        self._SecurityContext = SecurityContext


    def _deserialize(self, params):
        self._Image = params.get("Image")
        self._Name = params.get("Name")
        self._Commands = params.get("Commands")
        self._Args = params.get("Args")
        if params.get("EnvironmentVars") is not None:
            self._EnvironmentVars = []
            for item in params.get("EnvironmentVars"):
                obj = EnvironmentVariable()
                obj._deserialize(item)
                self._EnvironmentVars.append(obj)
        self._Cpu = params.get("Cpu")
        self._Memory = params.get("Memory")
        if params.get("VolumeMounts") is not None:
            self._VolumeMounts = []
            for item in params.get("VolumeMounts"):
                obj = VolumeMount()
                obj._deserialize(item)
                self._VolumeMounts.append(obj)
        if params.get("CurrentState") is not None:
            self._CurrentState = ContainerState()
            self._CurrentState._deserialize(params.get("CurrentState"))
        self._RestartCount = params.get("RestartCount")
        self._WorkingDir = params.get("WorkingDir")
        if params.get("LivenessProbe") is not None:
            self._LivenessProbe = LivenessOrReadinessProbe()
            self._LivenessProbe._deserialize(params.get("LivenessProbe"))
        if params.get("ReadinessProbe") is not None:
            self._ReadinessProbe = LivenessOrReadinessProbe()
            self._ReadinessProbe._deserialize(params.get("ReadinessProbe"))
        self._GpuLimit = params.get("GpuLimit")
        if params.get("SecurityContext") is not None:
            self._SecurityContext = SecurityContext()
            self._SecurityContext._deserialize(params.get("SecurityContext"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ContainerState(AbstractModel):
    """容器状态

    """

    def __init__(self):
        r"""
        :param _StartTime: 容器运行开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param _State: 容器状态：created, running, exited, unknown
        :type State: str
        :param _FinishTime: 容器运行结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type FinishTime: str
        :param _ExitCode: 容器运行退出码
注意：此字段可能返回 null，表示取不到有效值。
        :type ExitCode: int
        :param _Reason: 容器状态 Reason
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param _Message: 容器状态信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param _RestartCount: 容器重启次数
注意：此字段可能返回 null，表示取不到有效值。
        :type RestartCount: int
        """
        self._StartTime = None
        self._State = None
        self._FinishTime = None
        self._ExitCode = None
        self._Reason = None
        self._Message = None
        self._RestartCount = None

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def State(self):
        return self._State

    @State.setter
    def State(self, State):
        self._State = State

    @property
    def FinishTime(self):
        return self._FinishTime

    @FinishTime.setter
    def FinishTime(self, FinishTime):
        self._FinishTime = FinishTime

    @property
    def ExitCode(self):
        return self._ExitCode

    @ExitCode.setter
    def ExitCode(self, ExitCode):
        self._ExitCode = ExitCode

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason

    @property
    def Message(self):
        return self._Message

    @Message.setter
    def Message(self, Message):
        self._Message = Message

    @property
    def RestartCount(self):
        return self._RestartCount

    @RestartCount.setter
    def RestartCount(self, RestartCount):
        self._RestartCount = RestartCount


    def _deserialize(self, params):
        self._StartTime = params.get("StartTime")
        self._State = params.get("State")
        self._FinishTime = params.get("FinishTime")
        self._ExitCode = params.get("ExitCode")
        self._Reason = params.get("Reason")
        self._Message = params.get("Message")
        self._RestartCount = params.get("RestartCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ControllerStatus(AbstractModel):
    """集群中控制器的状态描述

    """

    def __init__(self):
        r"""
        :param _Name: 控制器的名字
        :type Name: str
        :param _Enabled: 控制器是否开启
        :type Enabled: bool
        """
        self._Name = None
        self._Enabled = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Enabled = params.get("Enabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBackupStorageLocationRequest(AbstractModel):
    """CreateBackupStorageLocation请求参数结构体

    """

    def __init__(self):
        r"""
        :param _StorageRegion: 存储仓库所属地域，比如COS广州(ap-guangzhou)
        :type StorageRegion: str
        :param _Bucket: 对象存储桶名称，如果是COS必须是tke-backup前缀开头
        :type Bucket: str
        :param _Name: 备份仓库名称
        :type Name: str
        :param _Provider: 存储服务提供方，默认腾讯云
        :type Provider: str
        :param _Path: 对象存储桶路径
        :type Path: str
        """
        self._StorageRegion = None
        self._Bucket = None
        self._Name = None
        self._Provider = None
        self._Path = None

    @property
    def StorageRegion(self):
        return self._StorageRegion

    @StorageRegion.setter
    def StorageRegion(self, StorageRegion):
        self._StorageRegion = StorageRegion

    @property
    def Bucket(self):
        return self._Bucket

    @Bucket.setter
    def Bucket(self, Bucket):
        self._Bucket = Bucket

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Provider(self):
        return self._Provider

    @Provider.setter
    def Provider(self, Provider):
        self._Provider = Provider

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path


    def _deserialize(self, params):
        self._StorageRegion = params.get("StorageRegion")
        self._Bucket = params.get("Bucket")
        self._Name = params.get("Name")
        self._Provider = params.get("Provider")
        self._Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBackupStorageLocationResponse(AbstractModel):
    """CreateBackupStorageLocation返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateClusterEndpointRequest(AbstractModel):
    """CreateClusterEndpoint请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _SubnetId: 集群端口所在的子网ID  (仅在开启非外网访问时需要填，必须为集群所在VPC内的子网)
        :type SubnetId: str
        :param _IsExtranet: 是否为外网访问（TRUE 外网访问 FALSE 内网访问，默认值： FALSE）
        :type IsExtranet: bool
        :param _Domain: 设置域名
        :type Domain: str
        :param _SecurityGroup: 使用的安全组，只有外网访问需要传递（开启外网访问时必传）
        :type SecurityGroup: str
        :param _ExtensiveParameters: 创建lb参数，只有外网访问需要设置，是一个json格式化后的字符串：{"InternetAccessible":{"InternetChargeType":"TRAFFIC_POSTPAID_BY_HOUR","InternetMaxBandwidthOut":200},"VipIsp":"","BandwidthPackageId":""}。
各个参数意义：
InternetAccessible.InternetChargeType含义：TRAFFIC_POSTPAID_BY_HOUR按流量按小时后计费;BANDWIDTH_POSTPAID_BY_HOUR 按带宽按小时后计费;InternetAccessible.BANDWIDTH_PACKAGE 按带宽包计费。
InternetMaxBandwidthOut含义：最大出带宽，单位Mbps，范围支持0到2048，默认值10。
VipIsp含义：CMCC | CTCC | CUCC，分别对应 移动 | 电信 | 联通，如果不指定本参数，则默认使用BGP。可通过 DescribeSingleIsp 接口查询一个地域所支持的Isp。如果指定运营商，则网络计费式只能使用按带宽包计费BANDWIDTH_PACKAGE。
BandwidthPackageId含义：带宽包ID，指定此参数时，网络计费方式InternetAccessible.InternetChargeType只支持按带宽包计费BANDWIDTH_PACKAGE。
        :type ExtensiveParameters: str
        """
        self._ClusterId = None
        self._SubnetId = None
        self._IsExtranet = None
        self._Domain = None
        self._SecurityGroup = None
        self._ExtensiveParameters = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def IsExtranet(self):
        return self._IsExtranet

    @IsExtranet.setter
    def IsExtranet(self, IsExtranet):
        self._IsExtranet = IsExtranet

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def SecurityGroup(self):
        return self._SecurityGroup

    @SecurityGroup.setter
    def SecurityGroup(self, SecurityGroup):
        self._SecurityGroup = SecurityGroup

    @property
    def ExtensiveParameters(self):
        return self._ExtensiveParameters

    @ExtensiveParameters.setter
    def ExtensiveParameters(self, ExtensiveParameters):
        self._ExtensiveParameters = ExtensiveParameters


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._SubnetId = params.get("SubnetId")
        self._IsExtranet = params.get("IsExtranet")
        self._Domain = params.get("Domain")
        self._SecurityGroup = params.get("SecurityGroup")
        self._ExtensiveParameters = params.get("ExtensiveParameters")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterEndpointResponse(AbstractModel):
    """CreateClusterEndpoint返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateClusterEndpointVipRequest(AbstractModel):
    """CreateClusterEndpointVip请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _SecurityPolicies: 安全策略放通单个IP或CIDR(例如: "192.168.1.0/24",默认为拒绝所有)
        :type SecurityPolicies: list of str
        """
        self._ClusterId = None
        self._SecurityPolicies = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SecurityPolicies(self):
        return self._SecurityPolicies

    @SecurityPolicies.setter
    def SecurityPolicies(self, SecurityPolicies):
        self._SecurityPolicies = SecurityPolicies


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._SecurityPolicies = params.get("SecurityPolicies")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterEndpointVipResponse(AbstractModel):
    """CreateClusterEndpointVip返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestFlowId: 请求任务的FlowId
        :type RequestFlowId: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestFlowId = None
        self._RequestId = None

    @property
    def RequestFlowId(self):
        return self._RequestFlowId

    @RequestFlowId.setter
    def RequestFlowId(self, RequestFlowId):
        self._RequestFlowId = RequestFlowId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestFlowId = params.get("RequestFlowId")
        self._RequestId = params.get("RequestId")


class CreateClusterInstancesRequest(AbstractModel):
    """CreateClusterInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群 ID，请填写 查询集群列表 接口中返回的 clusterId 字段
        :type ClusterId: str
        :param _RunInstancePara: CVM创建透传参数，json化字符串格式，如需要保证扩展集群节点请求幂等性需要在此参数添加ClientToken字段，详见[CVM创建实例](https://cloud.tencent.com/document/product/213/15730)接口。
        :type RunInstancePara: str
        :param _InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _SkipValidateOptions: 校验规则相关选项，可配置跳过某些校验规则。目前支持GlobalRouteCIDRCheck（跳过GlobalRouter的相关校验），VpcCniCIDRCheck（跳过VpcCni相关校验）
        :type SkipValidateOptions: list of str
        """
        self._ClusterId = None
        self._RunInstancePara = None
        self._InstanceAdvancedSettings = None
        self._SkipValidateOptions = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def RunInstancePara(self):
        return self._RunInstancePara

    @RunInstancePara.setter
    def RunInstancePara(self, RunInstancePara):
        self._RunInstancePara = RunInstancePara

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def SkipValidateOptions(self):
        return self._SkipValidateOptions

    @SkipValidateOptions.setter
    def SkipValidateOptions(self, SkipValidateOptions):
        self._SkipValidateOptions = SkipValidateOptions


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._RunInstancePara = params.get("RunInstancePara")
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self._SkipValidateOptions = params.get("SkipValidateOptions")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterInstancesResponse(AbstractModel):
    """CreateClusterInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceIdSet: 节点实例ID
        :type InstanceIdSet: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._InstanceIdSet = None
        self._RequestId = None

    @property
    def InstanceIdSet(self):
        return self._InstanceIdSet

    @InstanceIdSet.setter
    def InstanceIdSet(self, InstanceIdSet):
        self._InstanceIdSet = InstanceIdSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._InstanceIdSet = params.get("InstanceIdSet")
        self._RequestId = params.get("RequestId")


class CreateClusterNodePoolRequest(AbstractModel):
    """CreateClusterNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: cluster id
        :type ClusterId: str
        :param _AutoScalingGroupPara: AutoScalingGroupPara AS组参数，参考 https://cloud.tencent.com/document/product/377/20440
        :type AutoScalingGroupPara: str
        :param _LaunchConfigurePara: LaunchConfigurePara 运行参数，参考 https://cloud.tencent.com/document/product/377/20447
        :type LaunchConfigurePara: str
        :param _InstanceAdvancedSettings: InstanceAdvancedSettings 示例参数
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _EnableAutoscale: 是否启用自动伸缩
        :type EnableAutoscale: bool
        :param _Name: 节点池名称
        :type Name: str
        :param _Labels: Labels标签
        :type Labels: list of Label
        :param _Taints: Taints互斥
        :type Taints: list of Taint
        :param _ContainerRuntime: 节点池纬度运行时类型及版本
        :type ContainerRuntime: str
        :param _RuntimeVersion: 运行时版本
        :type RuntimeVersion: str
        :param _NodePoolOs: 节点池os，当为自定义镜像时，传镜像id；否则为公共镜像的osName
        :type NodePoolOs: str
        :param _OsCustomizeType: 容器的镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
        :type OsCustomizeType: str
        :param _Tags: 资源标签
        :type Tags: list of Tag
        :param _DeletionProtection: 删除保护开关
        :type DeletionProtection: bool
        """
        self._ClusterId = None
        self._AutoScalingGroupPara = None
        self._LaunchConfigurePara = None
        self._InstanceAdvancedSettings = None
        self._EnableAutoscale = None
        self._Name = None
        self._Labels = None
        self._Taints = None
        self._ContainerRuntime = None
        self._RuntimeVersion = None
        self._NodePoolOs = None
        self._OsCustomizeType = None
        self._Tags = None
        self._DeletionProtection = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AutoScalingGroupPara(self):
        return self._AutoScalingGroupPara

    @AutoScalingGroupPara.setter
    def AutoScalingGroupPara(self, AutoScalingGroupPara):
        self._AutoScalingGroupPara = AutoScalingGroupPara

    @property
    def LaunchConfigurePara(self):
        return self._LaunchConfigurePara

    @LaunchConfigurePara.setter
    def LaunchConfigurePara(self, LaunchConfigurePara):
        self._LaunchConfigurePara = LaunchConfigurePara

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def EnableAutoscale(self):
        return self._EnableAutoscale

    @EnableAutoscale.setter
    def EnableAutoscale(self, EnableAutoscale):
        self._EnableAutoscale = EnableAutoscale

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints

    @property
    def ContainerRuntime(self):
        return self._ContainerRuntime

    @ContainerRuntime.setter
    def ContainerRuntime(self, ContainerRuntime):
        self._ContainerRuntime = ContainerRuntime

    @property
    def RuntimeVersion(self):
        return self._RuntimeVersion

    @RuntimeVersion.setter
    def RuntimeVersion(self, RuntimeVersion):
        self._RuntimeVersion = RuntimeVersion

    @property
    def NodePoolOs(self):
        return self._NodePoolOs

    @NodePoolOs.setter
    def NodePoolOs(self, NodePoolOs):
        self._NodePoolOs = NodePoolOs

    @property
    def OsCustomizeType(self):
        return self._OsCustomizeType

    @OsCustomizeType.setter
    def OsCustomizeType(self, OsCustomizeType):
        self._OsCustomizeType = OsCustomizeType

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AutoScalingGroupPara = params.get("AutoScalingGroupPara")
        self._LaunchConfigurePara = params.get("LaunchConfigurePara")
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self._EnableAutoscale = params.get("EnableAutoscale")
        self._Name = params.get("Name")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        self._ContainerRuntime = params.get("ContainerRuntime")
        self._RuntimeVersion = params.get("RuntimeVersion")
        self._NodePoolOs = params.get("NodePoolOs")
        self._OsCustomizeType = params.get("OsCustomizeType")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._DeletionProtection = params.get("DeletionProtection")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterNodePoolResponse(AbstractModel):
    """CreateClusterNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._NodePoolId = None
        self._RequestId = None

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._NodePoolId = params.get("NodePoolId")
        self._RequestId = params.get("RequestId")


class CreateClusterReleaseRequest(AbstractModel):
    """CreateClusterRelease请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用命名空间
        :type Namespace: str
        :param _Chart: 制品名称或从第三方repo 安装chart时，制品压缩包下载地址, 不支持重定向类型chart 地址，结尾为*.tgz
        :type Chart: str
        :param _Values: 自定义参数
        :type Values: :class:`tencentcloud.tke.v20180525.models.ReleaseValues`
        :param _ChartFrom: 制品来源，范围：tke-market 或 other
        :type ChartFrom: str
        :param _ChartVersion: 制品版本
        :type ChartVersion: str
        :param _ChartRepoURL: 制品仓库URL地址
        :type ChartRepoURL: str
        :param _Username: 制品访问用户名
        :type Username: str
        :param _Password: 制品访问密码
        :type Password: str
        :param _ChartNamespace: 制品命名空间
        :type ChartNamespace: str
        :param _ClusterType: 集群类型，支持传 tke, eks, tkeedge, exernal(注册集群）
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Name = None
        self._Namespace = None
        self._Chart = None
        self._Values = None
        self._ChartFrom = None
        self._ChartVersion = None
        self._ChartRepoURL = None
        self._Username = None
        self._Password = None
        self._ChartNamespace = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Chart(self):
        return self._Chart

    @Chart.setter
    def Chart(self, Chart):
        self._Chart = Chart

    @property
    def Values(self):
        return self._Values

    @Values.setter
    def Values(self, Values):
        self._Values = Values

    @property
    def ChartFrom(self):
        return self._ChartFrom

    @ChartFrom.setter
    def ChartFrom(self, ChartFrom):
        self._ChartFrom = ChartFrom

    @property
    def ChartVersion(self):
        return self._ChartVersion

    @ChartVersion.setter
    def ChartVersion(self, ChartVersion):
        self._ChartVersion = ChartVersion

    @property
    def ChartRepoURL(self):
        return self._ChartRepoURL

    @ChartRepoURL.setter
    def ChartRepoURL(self, ChartRepoURL):
        self._ChartRepoURL = ChartRepoURL

    @property
    def Username(self):
        return self._Username

    @Username.setter
    def Username(self, Username):
        self._Username = Username

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def ChartNamespace(self):
        return self._ChartNamespace

    @ChartNamespace.setter
    def ChartNamespace(self, ChartNamespace):
        self._ChartNamespace = ChartNamespace

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Chart = params.get("Chart")
        if params.get("Values") is not None:
            self._Values = ReleaseValues()
            self._Values._deserialize(params.get("Values"))
        self._ChartFrom = params.get("ChartFrom")
        self._ChartVersion = params.get("ChartVersion")
        self._ChartRepoURL = params.get("ChartRepoURL")
        self._Username = params.get("Username")
        self._Password = params.get("Password")
        self._ChartNamespace = params.get("ChartNamespace")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterReleaseResponse(AbstractModel):
    """CreateClusterRelease返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Release: 应用详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Release: :class:`tencentcloud.tke.v20180525.models.PendingRelease`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Release = None
        self._RequestId = None

    @property
    def Release(self):
        return self._Release

    @Release.setter
    def Release(self, Release):
        self._Release = Release

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Release") is not None:
            self._Release = PendingRelease()
            self._Release._deserialize(params.get("Release"))
        self._RequestId = params.get("RequestId")


class CreateClusterRequest(AbstractModel):
    """CreateCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterType: 集群类型，托管集群：MANAGED_CLUSTER，独立集群：INDEPENDENT_CLUSTER。
        :type ClusterType: str
        :param _ClusterCIDRSettings: 集群容器网络配置信息
        :type ClusterCIDRSettings: :class:`tencentcloud.tke.v20180525.models.ClusterCIDRSettings`
        :param _RunInstancesForNode: CVM创建透传参数，json化字符串格式，详见[CVM创建实例](https://cloud.tencent.com/document/product/213/15730)接口。总机型(包括地域)数量不超过10个，相同机型(地域)购买多台机器可以通过设置参数中RunInstances中InstanceCount来实现。
        :type RunInstancesForNode: list of RunInstancesForNode
        :param _ClusterBasicSettings: 集群的基本配置信息
        :type ClusterBasicSettings: :class:`tencentcloud.tke.v20180525.models.ClusterBasicSettings`
        :param _ClusterAdvancedSettings: 集群高级配置信息
        :type ClusterAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.ClusterAdvancedSettings`
        :param _InstanceAdvancedSettings: 节点高级配置信息
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _ExistedInstancesForNode: 已存在实例的配置信息。所有实例必须在同一个VPC中，最大数量不超过100，不支持添加竞价实例。
        :type ExistedInstancesForNode: list of ExistedInstancesForNode
        :param _InstanceDataDiskMountSettings: CVM类型和其对应的数据盘挂载配置信息
        :type InstanceDataDiskMountSettings: list of InstanceDataDiskMountSetting
        :param _ExtensionAddons: 需要安装的扩展组件信息
        :type ExtensionAddons: list of ExtensionAddon
        """
        self._ClusterType = None
        self._ClusterCIDRSettings = None
        self._RunInstancesForNode = None
        self._ClusterBasicSettings = None
        self._ClusterAdvancedSettings = None
        self._InstanceAdvancedSettings = None
        self._ExistedInstancesForNode = None
        self._InstanceDataDiskMountSettings = None
        self._ExtensionAddons = None

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterCIDRSettings(self):
        return self._ClusterCIDRSettings

    @ClusterCIDRSettings.setter
    def ClusterCIDRSettings(self, ClusterCIDRSettings):
        self._ClusterCIDRSettings = ClusterCIDRSettings

    @property
    def RunInstancesForNode(self):
        return self._RunInstancesForNode

    @RunInstancesForNode.setter
    def RunInstancesForNode(self, RunInstancesForNode):
        self._RunInstancesForNode = RunInstancesForNode

    @property
    def ClusterBasicSettings(self):
        return self._ClusterBasicSettings

    @ClusterBasicSettings.setter
    def ClusterBasicSettings(self, ClusterBasicSettings):
        self._ClusterBasicSettings = ClusterBasicSettings

    @property
    def ClusterAdvancedSettings(self):
        return self._ClusterAdvancedSettings

    @ClusterAdvancedSettings.setter
    def ClusterAdvancedSettings(self, ClusterAdvancedSettings):
        self._ClusterAdvancedSettings = ClusterAdvancedSettings

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def ExistedInstancesForNode(self):
        return self._ExistedInstancesForNode

    @ExistedInstancesForNode.setter
    def ExistedInstancesForNode(self, ExistedInstancesForNode):
        self._ExistedInstancesForNode = ExistedInstancesForNode

    @property
    def InstanceDataDiskMountSettings(self):
        return self._InstanceDataDiskMountSettings

    @InstanceDataDiskMountSettings.setter
    def InstanceDataDiskMountSettings(self, InstanceDataDiskMountSettings):
        self._InstanceDataDiskMountSettings = InstanceDataDiskMountSettings

    @property
    def ExtensionAddons(self):
        return self._ExtensionAddons

    @ExtensionAddons.setter
    def ExtensionAddons(self, ExtensionAddons):
        self._ExtensionAddons = ExtensionAddons


    def _deserialize(self, params):
        self._ClusterType = params.get("ClusterType")
        if params.get("ClusterCIDRSettings") is not None:
            self._ClusterCIDRSettings = ClusterCIDRSettings()
            self._ClusterCIDRSettings._deserialize(params.get("ClusterCIDRSettings"))
        if params.get("RunInstancesForNode") is not None:
            self._RunInstancesForNode = []
            for item in params.get("RunInstancesForNode"):
                obj = RunInstancesForNode()
                obj._deserialize(item)
                self._RunInstancesForNode.append(obj)
        if params.get("ClusterBasicSettings") is not None:
            self._ClusterBasicSettings = ClusterBasicSettings()
            self._ClusterBasicSettings._deserialize(params.get("ClusterBasicSettings"))
        if params.get("ClusterAdvancedSettings") is not None:
            self._ClusterAdvancedSettings = ClusterAdvancedSettings()
            self._ClusterAdvancedSettings._deserialize(params.get("ClusterAdvancedSettings"))
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("ExistedInstancesForNode") is not None:
            self._ExistedInstancesForNode = []
            for item in params.get("ExistedInstancesForNode"):
                obj = ExistedInstancesForNode()
                obj._deserialize(item)
                self._ExistedInstancesForNode.append(obj)
        if params.get("InstanceDataDiskMountSettings") is not None:
            self._InstanceDataDiskMountSettings = []
            for item in params.get("InstanceDataDiskMountSettings"):
                obj = InstanceDataDiskMountSetting()
                obj._deserialize(item)
                self._InstanceDataDiskMountSettings.append(obj)
        if params.get("ExtensionAddons") is not None:
            self._ExtensionAddons = []
            for item in params.get("ExtensionAddons"):
                obj = ExtensionAddon()
                obj._deserialize(item)
                self._ExtensionAddons.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterResponse(AbstractModel):
    """CreateCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterId = None
        self._RequestId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._RequestId = params.get("RequestId")


class CreateClusterRouteRequest(AbstractModel):
    """CreateClusterRoute请求参数结构体

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param _DestinationCidrBlock: 目的端CIDR。
        :type DestinationCidrBlock: str
        :param _GatewayIp: 下一跳地址。
        :type GatewayIp: str
        """
        self._RouteTableName = None
        self._DestinationCidrBlock = None
        self._GatewayIp = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def DestinationCidrBlock(self):
        return self._DestinationCidrBlock

    @DestinationCidrBlock.setter
    def DestinationCidrBlock(self, DestinationCidrBlock):
        self._DestinationCidrBlock = DestinationCidrBlock

    @property
    def GatewayIp(self):
        return self._GatewayIp

    @GatewayIp.setter
    def GatewayIp(self, GatewayIp):
        self._GatewayIp = GatewayIp


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        self._DestinationCidrBlock = params.get("DestinationCidrBlock")
        self._GatewayIp = params.get("GatewayIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterRouteResponse(AbstractModel):
    """CreateClusterRoute返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateClusterRouteTableRequest(AbstractModel):
    """CreateClusterRouteTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称
        :type RouteTableName: str
        :param _RouteTableCidrBlock: 路由表CIDR
        :type RouteTableCidrBlock: str
        :param _VpcId: 路由表绑定的VPC
        :type VpcId: str
        :param _IgnoreClusterCidrConflict: 是否忽略CIDR冲突
        :type IgnoreClusterCidrConflict: int
        """
        self._RouteTableName = None
        self._RouteTableCidrBlock = None
        self._VpcId = None
        self._IgnoreClusterCidrConflict = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def RouteTableCidrBlock(self):
        return self._RouteTableCidrBlock

    @RouteTableCidrBlock.setter
    def RouteTableCidrBlock(self, RouteTableCidrBlock):
        self._RouteTableCidrBlock = RouteTableCidrBlock

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def IgnoreClusterCidrConflict(self):
        return self._IgnoreClusterCidrConflict

    @IgnoreClusterCidrConflict.setter
    def IgnoreClusterCidrConflict(self, IgnoreClusterCidrConflict):
        self._IgnoreClusterCidrConflict = IgnoreClusterCidrConflict


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        self._RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self._VpcId = params.get("VpcId")
        self._IgnoreClusterCidrConflict = params.get("IgnoreClusterCidrConflict")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterRouteTableResponse(AbstractModel):
    """CreateClusterRouteTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateClusterVirtualNodePoolRequest(AbstractModel):
    """CreateClusterVirtualNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群Id
        :type ClusterId: str
        :param _Name: 节点池名称
        :type Name: str
        :param _SubnetIds: 子网ID列表
        :type SubnetIds: list of str
        :param _SecurityGroupIds: 安全组ID列表
        :type SecurityGroupIds: list of str
        :param _Labels: 虚拟节点label
        :type Labels: list of Label
        :param _Taints: 虚拟节点taint
        :type Taints: list of Taint
        :param _VirtualNodes: 节点列表
        :type VirtualNodes: list of VirtualNodeSpec
        :param _DeletionProtection: 删除保护开关
        :type DeletionProtection: bool
        :param _OS: 节点池操作系统：
- linux（默认）
- windows
        :type OS: str
        """
        self._ClusterId = None
        self._Name = None
        self._SubnetIds = None
        self._SecurityGroupIds = None
        self._Labels = None
        self._Taints = None
        self._VirtualNodes = None
        self._DeletionProtection = None
        self._OS = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints

    @property
    def VirtualNodes(self):
        return self._VirtualNodes

    @VirtualNodes.setter
    def VirtualNodes(self, VirtualNodes):
        self._VirtualNodes = VirtualNodes

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection

    @property
    def OS(self):
        return self._OS

    @OS.setter
    def OS(self, OS):
        self._OS = OS


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._SubnetIds = params.get("SubnetIds")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        if params.get("VirtualNodes") is not None:
            self._VirtualNodes = []
            for item in params.get("VirtualNodes"):
                obj = VirtualNodeSpec()
                obj._deserialize(item)
                self._VirtualNodes.append(obj)
        self._DeletionProtection = params.get("DeletionProtection")
        self._OS = params.get("OS")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterVirtualNodePoolResponse(AbstractModel):
    """CreateClusterVirtualNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _NodePoolId: 节点池ID
        :type NodePoolId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._NodePoolId = None
        self._RequestId = None

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._NodePoolId = params.get("NodePoolId")
        self._RequestId = params.get("RequestId")


class CreateClusterVirtualNodeRequest(AbstractModel):
    """CreateClusterVirtualNode请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodePoolId: 虚拟节点所属节点池
        :type NodePoolId: str
        :param _SubnetId: 虚拟节点所属子网
        :type SubnetId: str
        :param _SubnetIds: 虚拟节点子网ID列表，和参数SubnetId互斥
        :type SubnetIds: list of str
        :param _VirtualNodes: 虚拟节点列表
        :type VirtualNodes: list of VirtualNodeSpec
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._SubnetId = None
        self._SubnetIds = None
        self._VirtualNodes = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def VirtualNodes(self):
        return self._VirtualNodes

    @VirtualNodes.setter
    def VirtualNodes(self, VirtualNodes):
        self._VirtualNodes = VirtualNodes


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._SubnetId = params.get("SubnetId")
        self._SubnetIds = params.get("SubnetIds")
        if params.get("VirtualNodes") is not None:
            self._VirtualNodes = []
            for item in params.get("VirtualNodes"):
                obj = VirtualNodeSpec()
                obj._deserialize(item)
                self._VirtualNodes.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterVirtualNodeResponse(AbstractModel):
    """CreateClusterVirtualNode返回参数结构体

    """

    def __init__(self):
        r"""
        :param _NodeName: 虚拟节点名称
        :type NodeName: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._NodeName = None
        self._RequestId = None

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._NodeName = params.get("NodeName")
        self._RequestId = params.get("RequestId")


class CreateECMInstancesRequest(AbstractModel):
    """CreateECMInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群id
        :type ClusterID: str
        :param _ModuleId: 模块id
        :type ModuleId: str
        :param _ZoneInstanceCountISPSet: 需要创建实例的可用区及创建数目及运营商的列表
        :type ZoneInstanceCountISPSet: list of ECMZoneInstanceCountISP
        :param _Password: 密码
        :type Password: str
        :param _InternetMaxBandwidthOut: 公网带宽
        :type InternetMaxBandwidthOut: int
        :param _ImageId: 镜像id
        :type ImageId: str
        :param _InstanceName: 实例名称
        :type InstanceName: str
        :param _HostName: 主机名称
        :type HostName: str
        :param _EnhancedService: 增强服务，包括云镜和云监控
        :type EnhancedService: :class:`tencentcloud.tke.v20180525.models.ECMEnhancedService`
        :param _UserData: 用户自定义脚本
        :type UserData: str
        :param _External: 实例扩展信息
        :type External: str
        :param _SecurityGroupIds: 实例所属安全组
        :type SecurityGroupIds: list of str
        """
        self._ClusterID = None
        self._ModuleId = None
        self._ZoneInstanceCountISPSet = None
        self._Password = None
        self._InternetMaxBandwidthOut = None
        self._ImageId = None
        self._InstanceName = None
        self._HostName = None
        self._EnhancedService = None
        self._UserData = None
        self._External = None
        self._SecurityGroupIds = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def ModuleId(self):
        return self._ModuleId

    @ModuleId.setter
    def ModuleId(self, ModuleId):
        self._ModuleId = ModuleId

    @property
    def ZoneInstanceCountISPSet(self):
        return self._ZoneInstanceCountISPSet

    @ZoneInstanceCountISPSet.setter
    def ZoneInstanceCountISPSet(self, ZoneInstanceCountISPSet):
        self._ZoneInstanceCountISPSet = ZoneInstanceCountISPSet

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def InternetMaxBandwidthOut(self):
        return self._InternetMaxBandwidthOut

    @InternetMaxBandwidthOut.setter
    def InternetMaxBandwidthOut(self, InternetMaxBandwidthOut):
        self._InternetMaxBandwidthOut = InternetMaxBandwidthOut

    @property
    def ImageId(self):
        return self._ImageId

    @ImageId.setter
    def ImageId(self, ImageId):
        self._ImageId = ImageId

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def HostName(self):
        return self._HostName

    @HostName.setter
    def HostName(self, HostName):
        self._HostName = HostName

    @property
    def EnhancedService(self):
        return self._EnhancedService

    @EnhancedService.setter
    def EnhancedService(self, EnhancedService):
        self._EnhancedService = EnhancedService

    @property
    def UserData(self):
        return self._UserData

    @UserData.setter
    def UserData(self, UserData):
        self._UserData = UserData

    @property
    def External(self):
        return self._External

    @External.setter
    def External(self, External):
        self._External = External

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        self._ModuleId = params.get("ModuleId")
        if params.get("ZoneInstanceCountISPSet") is not None:
            self._ZoneInstanceCountISPSet = []
            for item in params.get("ZoneInstanceCountISPSet"):
                obj = ECMZoneInstanceCountISP()
                obj._deserialize(item)
                self._ZoneInstanceCountISPSet.append(obj)
        self._Password = params.get("Password")
        self._InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self._ImageId = params.get("ImageId")
        self._InstanceName = params.get("InstanceName")
        self._HostName = params.get("HostName")
        if params.get("EnhancedService") is not None:
            self._EnhancedService = ECMEnhancedService()
            self._EnhancedService._deserialize(params.get("EnhancedService"))
        self._UserData = params.get("UserData")
        self._External = params.get("External")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateECMInstancesResponse(AbstractModel):
    """CreateECMInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _EcmIdSet: ecm id 列表
        :type EcmIdSet: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._EcmIdSet = None
        self._RequestId = None

    @property
    def EcmIdSet(self):
        return self._EcmIdSet

    @EcmIdSet.setter
    def EcmIdSet(self, EcmIdSet):
        self._EcmIdSet = EcmIdSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._EcmIdSet = params.get("EcmIdSet")
        self._RequestId = params.get("RequestId")


class CreateEKSClusterRequest(AbstractModel):
    """CreateEKSCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _K8SVersion: k8s版本号。可为1.18.4 1.20.6。
        :type K8SVersion: str
        :param _VpcId: vpc 的Id
        :type VpcId: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _SubnetIds: 子网Id 列表
        :type SubnetIds: list of str
        :param _ClusterDesc: 集群描述信息
        :type ClusterDesc: str
        :param _ServiceSubnetId: Service CIDR 或 Serivce 所在子网Id
        :type ServiceSubnetId: str
        :param _DnsServers: 集群自定义的Dns服务器信息
        :type DnsServers: list of DnsServerConf
        :param _ExtraParam: 扩展参数。须是map[string]string 的json 格式。
        :type ExtraParam: str
        :param _EnableVpcCoreDNS: 是否在用户集群内开启Dns。默认为true
        :type EnableVpcCoreDNS: bool
        :param _TagSpecification: 标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到集群实例。
        :type TagSpecification: list of TagSpecification
        :param _SubnetInfos: 子网信息列表
        :type SubnetInfos: list of SubnetInfos
        """
        self._K8SVersion = None
        self._VpcId = None
        self._ClusterName = None
        self._SubnetIds = None
        self._ClusterDesc = None
        self._ServiceSubnetId = None
        self._DnsServers = None
        self._ExtraParam = None
        self._EnableVpcCoreDNS = None
        self._TagSpecification = None
        self._SubnetInfos = None

    @property
    def K8SVersion(self):
        return self._K8SVersion

    @K8SVersion.setter
    def K8SVersion(self, K8SVersion):
        self._K8SVersion = K8SVersion

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def ServiceSubnetId(self):
        return self._ServiceSubnetId

    @ServiceSubnetId.setter
    def ServiceSubnetId(self, ServiceSubnetId):
        self._ServiceSubnetId = ServiceSubnetId

    @property
    def DnsServers(self):
        return self._DnsServers

    @DnsServers.setter
    def DnsServers(self, DnsServers):
        self._DnsServers = DnsServers

    @property
    def ExtraParam(self):
        return self._ExtraParam

    @ExtraParam.setter
    def ExtraParam(self, ExtraParam):
        self._ExtraParam = ExtraParam

    @property
    def EnableVpcCoreDNS(self):
        return self._EnableVpcCoreDNS

    @EnableVpcCoreDNS.setter
    def EnableVpcCoreDNS(self, EnableVpcCoreDNS):
        self._EnableVpcCoreDNS = EnableVpcCoreDNS

    @property
    def TagSpecification(self):
        return self._TagSpecification

    @TagSpecification.setter
    def TagSpecification(self, TagSpecification):
        self._TagSpecification = TagSpecification

    @property
    def SubnetInfos(self):
        return self._SubnetInfos

    @SubnetInfos.setter
    def SubnetInfos(self, SubnetInfos):
        self._SubnetInfos = SubnetInfos


    def _deserialize(self, params):
        self._K8SVersion = params.get("K8SVersion")
        self._VpcId = params.get("VpcId")
        self._ClusterName = params.get("ClusterName")
        self._SubnetIds = params.get("SubnetIds")
        self._ClusterDesc = params.get("ClusterDesc")
        self._ServiceSubnetId = params.get("ServiceSubnetId")
        if params.get("DnsServers") is not None:
            self._DnsServers = []
            for item in params.get("DnsServers"):
                obj = DnsServerConf()
                obj._deserialize(item)
                self._DnsServers.append(obj)
        self._ExtraParam = params.get("ExtraParam")
        self._EnableVpcCoreDNS = params.get("EnableVpcCoreDNS")
        if params.get("TagSpecification") is not None:
            self._TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self._TagSpecification.append(obj)
        if params.get("SubnetInfos") is not None:
            self._SubnetInfos = []
            for item in params.get("SubnetInfos"):
                obj = SubnetInfos()
                obj._deserialize(item)
                self._SubnetInfos.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEKSClusterResponse(AbstractModel):
    """CreateEKSCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 弹性集群Id
        :type ClusterId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterId = None
        self._RequestId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._RequestId = params.get("RequestId")


class CreateEKSContainerInstancesRequest(AbstractModel):
    """CreateEKSContainerInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Containers: 容器组
        :type Containers: list of Container
        :param _EksCiName: EKS Container Instance容器实例名称
        :type EksCiName: str
        :param _SecurityGroupIds: 指定新创建实例所属于的安全组Id
        :type SecurityGroupIds: list of str
        :param _SubnetId: 实例所属子网Id
        :type SubnetId: str
        :param _VpcId: 实例所属VPC的Id
        :type VpcId: str
        :param _Memory: 内存，单位：GiB。可参考[资源规格](https://cloud.tencent.com/document/product/457/39808)文档
        :type Memory: float
        :param _Cpu: CPU，单位：核。可参考[资源规格](https://cloud.tencent.com/document/product/457/39808)文档
        :type Cpu: float
        :param _RestartPolicy: 实例重启策略： Always(总是重启)、Never(从不重启)、OnFailure(失败时重启)，默认：Always。
        :type RestartPolicy: str
        :param _ImageRegistryCredentials: 镜像仓库凭证数组
        :type ImageRegistryCredentials: list of ImageRegistryCredential
        :param _EksCiVolume: 数据卷，包含NfsVolume数组和CbsVolume数组
        :type EksCiVolume: :class:`tencentcloud.tke.v20180525.models.EksCiVolume`
        :param _Replicas: 实例副本数，默认为1
        :type Replicas: int
        :param _InitContainers: Init 容器
        :type InitContainers: list of Container
        :param _DnsConfig: 自定义DNS配置
        :type DnsConfig: :class:`tencentcloud.tke.v20180525.models.DNSConfig`
        :param _ExistedEipIds: 用来绑定容器实例的已有EIP的列表。如传值，需要保证数值和Replicas相等。
另外此参数和AutoCreateEipAttribute互斥。
        :type ExistedEipIds: list of str
        :param _AutoCreateEipAttribute: 自动创建EIP的可选参数。若传此参数，则会自动创建EIP。
另外此参数和ExistedEipIds互斥
        :type AutoCreateEipAttribute: :class:`tencentcloud.tke.v20180525.models.EipAttribute`
        :param _AutoCreateEip: 是否为容器实例自动创建EIP，默认为false。若传true，则此参数和ExistedEipIds互斥
        :type AutoCreateEip: bool
        :param _CpuType: Pod 所需的 CPU 资源型号，如果不填写则默认不强制指定 CPU 类型。目前支持型号如下：
intel
amd
- 支持优先级顺序写法，如 “amd,intel” 表示优先创建 amd 资源 Pod，如果所选地域可用区 amd 资源不足，则会创建 intel 资源 Pod。
        :type CpuType: str
        :param _GpuType: 容器实例所需的 GPU 资源型号，目前支持型号如下：
1/4\*V100
1/2\*V100
V100
1/4\*T4
1/2\*T4
T4
        :type GpuType: str
        :param _GpuCount: Pod 所需的 GPU 数量，如填写，请确保为支持的规格。默认单位为卡，无需再次注明。
        :type GpuCount: int
        :param _CamRoleName: 为容器实例关联 CAM 角色，value 填写 CAM 角色名称，容器实例可获取该 CAM 角色包含的权限策略，方便 容器实例 内的程序进行如购买资源、读写存储等云资源操作。
        :type CamRoleName: str
        """
        self._Containers = None
        self._EksCiName = None
        self._SecurityGroupIds = None
        self._SubnetId = None
        self._VpcId = None
        self._Memory = None
        self._Cpu = None
        self._RestartPolicy = None
        self._ImageRegistryCredentials = None
        self._EksCiVolume = None
        self._Replicas = None
        self._InitContainers = None
        self._DnsConfig = None
        self._ExistedEipIds = None
        self._AutoCreateEipAttribute = None
        self._AutoCreateEip = None
        self._CpuType = None
        self._GpuType = None
        self._GpuCount = None
        self._CamRoleName = None

    @property
    def Containers(self):
        return self._Containers

    @Containers.setter
    def Containers(self, Containers):
        self._Containers = Containers

    @property
    def EksCiName(self):
        return self._EksCiName

    @EksCiName.setter
    def EksCiName(self, EksCiName):
        self._EksCiName = EksCiName

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Cpu(self):
        return self._Cpu

    @Cpu.setter
    def Cpu(self, Cpu):
        self._Cpu = Cpu

    @property
    def RestartPolicy(self):
        return self._RestartPolicy

    @RestartPolicy.setter
    def RestartPolicy(self, RestartPolicy):
        self._RestartPolicy = RestartPolicy

    @property
    def ImageRegistryCredentials(self):
        return self._ImageRegistryCredentials

    @ImageRegistryCredentials.setter
    def ImageRegistryCredentials(self, ImageRegistryCredentials):
        self._ImageRegistryCredentials = ImageRegistryCredentials

    @property
    def EksCiVolume(self):
        return self._EksCiVolume

    @EksCiVolume.setter
    def EksCiVolume(self, EksCiVolume):
        self._EksCiVolume = EksCiVolume

    @property
    def Replicas(self):
        return self._Replicas

    @Replicas.setter
    def Replicas(self, Replicas):
        self._Replicas = Replicas

    @property
    def InitContainers(self):
        return self._InitContainers

    @InitContainers.setter
    def InitContainers(self, InitContainers):
        self._InitContainers = InitContainers

    @property
    def DnsConfig(self):
        return self._DnsConfig

    @DnsConfig.setter
    def DnsConfig(self, DnsConfig):
        self._DnsConfig = DnsConfig

    @property
    def ExistedEipIds(self):
        return self._ExistedEipIds

    @ExistedEipIds.setter
    def ExistedEipIds(self, ExistedEipIds):
        self._ExistedEipIds = ExistedEipIds

    @property
    def AutoCreateEipAttribute(self):
        return self._AutoCreateEipAttribute

    @AutoCreateEipAttribute.setter
    def AutoCreateEipAttribute(self, AutoCreateEipAttribute):
        self._AutoCreateEipAttribute = AutoCreateEipAttribute

    @property
    def AutoCreateEip(self):
        return self._AutoCreateEip

    @AutoCreateEip.setter
    def AutoCreateEip(self, AutoCreateEip):
        self._AutoCreateEip = AutoCreateEip

    @property
    def CpuType(self):
        return self._CpuType

    @CpuType.setter
    def CpuType(self, CpuType):
        self._CpuType = CpuType

    @property
    def GpuType(self):
        return self._GpuType

    @GpuType.setter
    def GpuType(self, GpuType):
        self._GpuType = GpuType

    @property
    def GpuCount(self):
        return self._GpuCount

    @GpuCount.setter
    def GpuCount(self, GpuCount):
        self._GpuCount = GpuCount

    @property
    def CamRoleName(self):
        return self._CamRoleName

    @CamRoleName.setter
    def CamRoleName(self, CamRoleName):
        self._CamRoleName = CamRoleName


    def _deserialize(self, params):
        if params.get("Containers") is not None:
            self._Containers = []
            for item in params.get("Containers"):
                obj = Container()
                obj._deserialize(item)
                self._Containers.append(obj)
        self._EksCiName = params.get("EksCiName")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        self._SubnetId = params.get("SubnetId")
        self._VpcId = params.get("VpcId")
        self._Memory = params.get("Memory")
        self._Cpu = params.get("Cpu")
        self._RestartPolicy = params.get("RestartPolicy")
        if params.get("ImageRegistryCredentials") is not None:
            self._ImageRegistryCredentials = []
            for item in params.get("ImageRegistryCredentials"):
                obj = ImageRegistryCredential()
                obj._deserialize(item)
                self._ImageRegistryCredentials.append(obj)
        if params.get("EksCiVolume") is not None:
            self._EksCiVolume = EksCiVolume()
            self._EksCiVolume._deserialize(params.get("EksCiVolume"))
        self._Replicas = params.get("Replicas")
        if params.get("InitContainers") is not None:
            self._InitContainers = []
            for item in params.get("InitContainers"):
                obj = Container()
                obj._deserialize(item)
                self._InitContainers.append(obj)
        if params.get("DnsConfig") is not None:
            self._DnsConfig = DNSConfig()
            self._DnsConfig._deserialize(params.get("DnsConfig"))
        self._ExistedEipIds = params.get("ExistedEipIds")
        if params.get("AutoCreateEipAttribute") is not None:
            self._AutoCreateEipAttribute = EipAttribute()
            self._AutoCreateEipAttribute._deserialize(params.get("AutoCreateEipAttribute"))
        self._AutoCreateEip = params.get("AutoCreateEip")
        self._CpuType = params.get("CpuType")
        self._GpuType = params.get("GpuType")
        self._GpuCount = params.get("GpuCount")
        self._CamRoleName = params.get("CamRoleName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEKSContainerInstancesResponse(AbstractModel):
    """CreateEKSContainerInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiIds: EKS Container Instance Id集合，格式为eksci-xxx，是容器实例的唯一标识。
        :type EksCiIds: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._EksCiIds = None
        self._RequestId = None

    @property
    def EksCiIds(self):
        return self._EksCiIds

    @EksCiIds.setter
    def EksCiIds(self, EksCiIds):
        self._EksCiIds = EksCiIds

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._EksCiIds = params.get("EksCiIds")
        self._RequestId = params.get("RequestId")


class CreateEdgeCVMInstancesRequest(AbstractModel):
    """CreateEdgeCVMInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群id
        :type ClusterID: str
        :param _RunInstancePara: CVM创建透传参数，json化字符串格式，如需要保证扩展集群节点请求幂等性需要在此参数添加ClientToken字段，详见[CVM创建实例](https://cloud.tencent.com/document/product/213/15730)接口。
        :type RunInstancePara: str
        :param _CvmRegion: CVM所属Region
        :type CvmRegion: str
        :param _CvmCount: CVM数量
        :type CvmCount: int
        :param _External: 实例扩展信息
        :type External: str
        :param _UserScript: 用户自定义脚本
        :type UserScript: str
        :param _EnableEni: 是否开启弹性网卡功能
        :type EnableEni: bool
        """
        self._ClusterID = None
        self._RunInstancePara = None
        self._CvmRegion = None
        self._CvmCount = None
        self._External = None
        self._UserScript = None
        self._EnableEni = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def RunInstancePara(self):
        return self._RunInstancePara

    @RunInstancePara.setter
    def RunInstancePara(self, RunInstancePara):
        self._RunInstancePara = RunInstancePara

    @property
    def CvmRegion(self):
        return self._CvmRegion

    @CvmRegion.setter
    def CvmRegion(self, CvmRegion):
        self._CvmRegion = CvmRegion

    @property
    def CvmCount(self):
        return self._CvmCount

    @CvmCount.setter
    def CvmCount(self, CvmCount):
        self._CvmCount = CvmCount

    @property
    def External(self):
        return self._External

    @External.setter
    def External(self, External):
        self._External = External

    @property
    def UserScript(self):
        return self._UserScript

    @UserScript.setter
    def UserScript(self, UserScript):
        self._UserScript = UserScript

    @property
    def EnableEni(self):
        return self._EnableEni

    @EnableEni.setter
    def EnableEni(self, EnableEni):
        self._EnableEni = EnableEni


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        self._RunInstancePara = params.get("RunInstancePara")
        self._CvmRegion = params.get("CvmRegion")
        self._CvmCount = params.get("CvmCount")
        self._External = params.get("External")
        self._UserScript = params.get("UserScript")
        self._EnableEni = params.get("EnableEni")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEdgeCVMInstancesResponse(AbstractModel):
    """CreateEdgeCVMInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _CvmIdSet: cvm id 列表
        :type CvmIdSet: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._CvmIdSet = None
        self._RequestId = None

    @property
    def CvmIdSet(self):
        return self._CvmIdSet

    @CvmIdSet.setter
    def CvmIdSet(self, CvmIdSet):
        self._CvmIdSet = CvmIdSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._CvmIdSet = params.get("CvmIdSet")
        self._RequestId = params.get("RequestId")


class CreateEdgeLogConfigRequest(AbstractModel):
    """CreateEdgeLogConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _LogConfig: 日志采集配置的json表达
        :type LogConfig: str
        :param _LogsetId: CLS日志集ID
        :type LogsetId: str
        """
        self._ClusterId = None
        self._LogConfig = None
        self._LogsetId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def LogConfig(self):
        return self._LogConfig

    @LogConfig.setter
    def LogConfig(self, LogConfig):
        self._LogConfig = LogConfig

    @property
    def LogsetId(self):
        return self._LogsetId

    @LogsetId.setter
    def LogsetId(self, LogsetId):
        self._LogsetId = LogsetId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._LogConfig = params.get("LogConfig")
        self._LogsetId = params.get("LogsetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEdgeLogConfigResponse(AbstractModel):
    """CreateEdgeLogConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateImageCacheRequest(AbstractModel):
    """CreateImageCache请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Images: 用于制作镜像缓存的容器镜像列表
        :type Images: list of str
        :param _SubnetId: 实例所属子网Id
        :type SubnetId: str
        :param _VpcId: 实例所属VPC Id
        :type VpcId: str
        :param _ImageCacheName: 镜像缓存名称
        :type ImageCacheName: str
        :param _SecurityGroupIds: 安全组Id
        :type SecurityGroupIds: list of str
        :param _ImageRegistryCredentials: 镜像仓库凭证数组
        :type ImageRegistryCredentials: list of ImageRegistryCredential
        :param _ExistedEipId: 用来绑定容器实例的已有EIP
        :type ExistedEipId: str
        :param _AutoCreateEip: 是否为容器实例自动创建EIP，默认为false。若传true，则此参数和ExistedEipIds互斥
        :type AutoCreateEip: bool
        :param _AutoCreateEipAttribute: 自动创建EIP的可选参数。若传此参数，则会自动创建EIP。
另外此参数和ExistedEipIds互斥
        :type AutoCreateEipAttribute: :class:`tencentcloud.tke.v20180525.models.EipAttribute`
        :param _ImageCacheSize: 镜像缓存的大小。默认为20 GiB。取值范围参考[云硬盘类型](https://cloud.tencent.com/document/product/362/2353)中的高性能云盘类型的大小限制。
        :type ImageCacheSize: int
        :param _RetentionDays: 镜像缓存保留时间天数，过期将会自动清理，默认为0，永不过期。
        :type RetentionDays: int
        :param _RegistrySkipVerifyList: 指定拉取镜像仓库的镜像时不校验证书。如["harbor.example.com"]。
        :type RegistrySkipVerifyList: list of str
        :param _RegistryHttpEndPointList: 指定拉取镜像仓库的镜像时使用 HTTP 协议。如["harbor.example.com"]。
        :type RegistryHttpEndPointList: list of str
        :param _ResolveConfig: 自定义制作镜像缓存过程中容器实例的宿主机上的 DNS。如：
"nameserver 4.4.4.4\nnameserver 8.8.8.8"
        :type ResolveConfig: str
        """
        self._Images = None
        self._SubnetId = None
        self._VpcId = None
        self._ImageCacheName = None
        self._SecurityGroupIds = None
        self._ImageRegistryCredentials = None
        self._ExistedEipId = None
        self._AutoCreateEip = None
        self._AutoCreateEipAttribute = None
        self._ImageCacheSize = None
        self._RetentionDays = None
        self._RegistrySkipVerifyList = None
        self._RegistryHttpEndPointList = None
        self._ResolveConfig = None

    @property
    def Images(self):
        return self._Images

    @Images.setter
    def Images(self, Images):
        self._Images = Images

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def ImageCacheName(self):
        return self._ImageCacheName

    @ImageCacheName.setter
    def ImageCacheName(self, ImageCacheName):
        self._ImageCacheName = ImageCacheName

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def ImageRegistryCredentials(self):
        return self._ImageRegistryCredentials

    @ImageRegistryCredentials.setter
    def ImageRegistryCredentials(self, ImageRegistryCredentials):
        self._ImageRegistryCredentials = ImageRegistryCredentials

    @property
    def ExistedEipId(self):
        return self._ExistedEipId

    @ExistedEipId.setter
    def ExistedEipId(self, ExistedEipId):
        self._ExistedEipId = ExistedEipId

    @property
    def AutoCreateEip(self):
        return self._AutoCreateEip

    @AutoCreateEip.setter
    def AutoCreateEip(self, AutoCreateEip):
        self._AutoCreateEip = AutoCreateEip

    @property
    def AutoCreateEipAttribute(self):
        return self._AutoCreateEipAttribute

    @AutoCreateEipAttribute.setter
    def AutoCreateEipAttribute(self, AutoCreateEipAttribute):
        self._AutoCreateEipAttribute = AutoCreateEipAttribute

    @property
    def ImageCacheSize(self):
        return self._ImageCacheSize

    @ImageCacheSize.setter
    def ImageCacheSize(self, ImageCacheSize):
        self._ImageCacheSize = ImageCacheSize

    @property
    def RetentionDays(self):
        return self._RetentionDays

    @RetentionDays.setter
    def RetentionDays(self, RetentionDays):
        self._RetentionDays = RetentionDays

    @property
    def RegistrySkipVerifyList(self):
        return self._RegistrySkipVerifyList

    @RegistrySkipVerifyList.setter
    def RegistrySkipVerifyList(self, RegistrySkipVerifyList):
        self._RegistrySkipVerifyList = RegistrySkipVerifyList

    @property
    def RegistryHttpEndPointList(self):
        return self._RegistryHttpEndPointList

    @RegistryHttpEndPointList.setter
    def RegistryHttpEndPointList(self, RegistryHttpEndPointList):
        self._RegistryHttpEndPointList = RegistryHttpEndPointList

    @property
    def ResolveConfig(self):
        return self._ResolveConfig

    @ResolveConfig.setter
    def ResolveConfig(self, ResolveConfig):
        self._ResolveConfig = ResolveConfig


    def _deserialize(self, params):
        self._Images = params.get("Images")
        self._SubnetId = params.get("SubnetId")
        self._VpcId = params.get("VpcId")
        self._ImageCacheName = params.get("ImageCacheName")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("ImageRegistryCredentials") is not None:
            self._ImageRegistryCredentials = []
            for item in params.get("ImageRegistryCredentials"):
                obj = ImageRegistryCredential()
                obj._deserialize(item)
                self._ImageRegistryCredentials.append(obj)
        self._ExistedEipId = params.get("ExistedEipId")
        self._AutoCreateEip = params.get("AutoCreateEip")
        if params.get("AutoCreateEipAttribute") is not None:
            self._AutoCreateEipAttribute = EipAttribute()
            self._AutoCreateEipAttribute._deserialize(params.get("AutoCreateEipAttribute"))
        self._ImageCacheSize = params.get("ImageCacheSize")
        self._RetentionDays = params.get("RetentionDays")
        self._RegistrySkipVerifyList = params.get("RegistrySkipVerifyList")
        self._RegistryHttpEndPointList = params.get("RegistryHttpEndPointList")
        self._ResolveConfig = params.get("ResolveConfig")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateImageCacheResponse(AbstractModel):
    """CreateImageCache返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ImageCacheId: 镜像缓存Id
        :type ImageCacheId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ImageCacheId = None
        self._RequestId = None

    @property
    def ImageCacheId(self):
        return self._ImageCacheId

    @ImageCacheId.setter
    def ImageCacheId(self, ImageCacheId):
        self._ImageCacheId = ImageCacheId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ImageCacheId = params.get("ImageCacheId")
        self._RequestId = params.get("RequestId")


class CreatePrometheusAlertPolicyRequest(AbstractModel):
    """CreatePrometheusAlertPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _AlertRule: 告警配置
        :type AlertRule: :class:`tencentcloud.tke.v20180525.models.PrometheusAlertPolicyItem`
        """
        self._InstanceId = None
        self._AlertRule = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def AlertRule(self):
        return self._AlertRule

    @AlertRule.setter
    def AlertRule(self, AlertRule):
        self._AlertRule = AlertRule


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("AlertRule") is not None:
            self._AlertRule = PrometheusAlertPolicyItem()
            self._AlertRule._deserialize(params.get("AlertRule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusAlertPolicyResponse(AbstractModel):
    """CreatePrometheusAlertPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Id: 告警id
        :type Id: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Id = None
        self._RequestId = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Id = params.get("Id")
        self._RequestId = params.get("RequestId")


class CreatePrometheusAlertRuleRequest(AbstractModel):
    """CreatePrometheusAlertRule请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _AlertRule: 告警配置
        :type AlertRule: :class:`tencentcloud.tke.v20180525.models.PrometheusAlertRuleDetail`
        """
        self._InstanceId = None
        self._AlertRule = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def AlertRule(self):
        return self._AlertRule

    @AlertRule.setter
    def AlertRule(self, AlertRule):
        self._AlertRule = AlertRule


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("AlertRule") is not None:
            self._AlertRule = PrometheusAlertRuleDetail()
            self._AlertRule._deserialize(params.get("AlertRule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusAlertRuleResponse(AbstractModel):
    """CreatePrometheusAlertRule返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Id: 告警id
        :type Id: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Id = None
        self._RequestId = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Id = params.get("Id")
        self._RequestId = params.get("RequestId")


class CreatePrometheusClusterAgentRequest(AbstractModel):
    """CreatePrometheusClusterAgent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _Agents: agent列表
        :type Agents: list of PrometheusClusterAgentBasic
        """
        self._InstanceId = None
        self._Agents = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Agents(self):
        return self._Agents

    @Agents.setter
    def Agents(self, Agents):
        self._Agents = Agents


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("Agents") is not None:
            self._Agents = []
            for item in params.get("Agents"):
                obj = PrometheusClusterAgentBasic()
                obj._deserialize(item)
                self._Agents.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusClusterAgentResponse(AbstractModel):
    """CreatePrometheusClusterAgent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreatePrometheusConfigRequest(AbstractModel):
    """CreatePrometheusConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _ServiceMonitors: ServiceMonitors配置
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: PodMonitors配置
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: prometheus原生Job配置
        :type RawJobs: list of PrometheusConfigItem
        """
        self._InstanceId = None
        self._ClusterType = None
        self._ClusterId = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusConfigResponse(AbstractModel):
    """CreatePrometheusConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreatePrometheusDashboardRequest(AbstractModel):
    """CreatePrometheusDashboard请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _DashboardName: 面板组名称
        :type DashboardName: str
        :param _Contents: 面板列表
每一项是一个grafana dashboard的json定义
        :type Contents: list of str
        """
        self._InstanceId = None
        self._DashboardName = None
        self._Contents = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def DashboardName(self):
        return self._DashboardName

    @DashboardName.setter
    def DashboardName(self, DashboardName):
        self._DashboardName = DashboardName

    @property
    def Contents(self):
        return self._Contents

    @Contents.setter
    def Contents(self, Contents):
        self._Contents = Contents


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._DashboardName = params.get("DashboardName")
        self._Contents = params.get("Contents")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusDashboardResponse(AbstractModel):
    """CreatePrometheusDashboard返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreatePrometheusGlobalNotificationRequest(AbstractModel):
    """CreatePrometheusGlobalNotification请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _Notification: 告警通知渠道
        :type Notification: :class:`tencentcloud.tke.v20180525.models.PrometheusNotificationItem`
        """
        self._InstanceId = None
        self._Notification = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Notification(self):
        return self._Notification

    @Notification.setter
    def Notification(self, Notification):
        self._Notification = Notification


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("Notification") is not None:
            self._Notification = PrometheusNotificationItem()
            self._Notification._deserialize(params.get("Notification"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusGlobalNotificationResponse(AbstractModel):
    """CreatePrometheusGlobalNotification返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Id: 全局告警通知渠道ID
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Id = None
        self._RequestId = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Id = params.get("Id")
        self._RequestId = params.get("RequestId")


class CreatePrometheusRecordRuleYamlRequest(AbstractModel):
    """CreatePrometheusRecordRuleYaml请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Content: yaml的内容
        :type Content: str
        """
        self._InstanceId = None
        self._Content = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Content(self):
        return self._Content

    @Content.setter
    def Content(self, Content):
        self._Content = Content


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Content = params.get("Content")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusRecordRuleYamlResponse(AbstractModel):
    """CreatePrometheusRecordRuleYaml返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreatePrometheusTempRequest(AbstractModel):
    """CreatePrometheusTemp请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Template: 模板设置
        :type Template: :class:`tencentcloud.tke.v20180525.models.PrometheusTemp`
        """
        self._Template = None

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template


    def _deserialize(self, params):
        if params.get("Template") is not None:
            self._Template = PrometheusTemp()
            self._Template._deserialize(params.get("Template"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusTempResponse(AbstractModel):
    """CreatePrometheusTemp返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板Id
        :type TemplateId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TemplateId = None
        self._RequestId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        self._RequestId = params.get("RequestId")


class CreatePrometheusTemplateRequest(AbstractModel):
    """CreatePrometheusTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Template: 模板设置
        :type Template: :class:`tencentcloud.tke.v20180525.models.PrometheusTemplate`
        """
        self._Template = None

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template


    def _deserialize(self, params):
        if params.get("Template") is not None:
            self._Template = PrometheusTemplate()
            self._Template._deserialize(params.get("Template"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePrometheusTemplateResponse(AbstractModel):
    """CreatePrometheusTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板Id
        :type TemplateId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TemplateId = None
        self._RequestId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        self._RequestId = params.get("RequestId")


class CreateTKEEdgeClusterRequest(AbstractModel):
    """CreateTKEEdgeCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _K8SVersion: k8s版本号
        :type K8SVersion: str
        :param _VpcId: vpc 的Id
        :type VpcId: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _PodCIDR: 集群pod cidr
        :type PodCIDR: str
        :param _ServiceCIDR: 集群service cidr
        :type ServiceCIDR: str
        :param _ClusterDesc: 集群描述信息
        :type ClusterDesc: str
        :param _ClusterAdvancedSettings: 集群高级设置
        :type ClusterAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.EdgeClusterAdvancedSettings`
        :param _MaxNodePodNum: 节点上最大Pod数量
        :type MaxNodePodNum: int
        :param _PublicLB: 边缘计算集群公网访问LB信息
        :type PublicLB: :class:`tencentcloud.tke.v20180525.models.EdgeClusterPublicLB`
        :param _ClusterLevel: 集群的级别
        :type ClusterLevel: str
        :param _AutoUpgradeClusterLevel: 集群是否支持自动升配
        :type AutoUpgradeClusterLevel: bool
        :param _ChargeType: 集群计费方式
        :type ChargeType: str
        :param _EdgeVersion: 边缘集群版本，此版本区别于k8s版本，是整个集群各组件版本集合
        :type EdgeVersion: str
        :param _RegistryPrefix: 边缘组件镜像仓库前缀
        :type RegistryPrefix: str
        :param _TagSpecification: 集群绑定的云标签
        :type TagSpecification: :class:`tencentcloud.tke.v20180525.models.TagSpecification`
        """
        self._K8SVersion = None
        self._VpcId = None
        self._ClusterName = None
        self._PodCIDR = None
        self._ServiceCIDR = None
        self._ClusterDesc = None
        self._ClusterAdvancedSettings = None
        self._MaxNodePodNum = None
        self._PublicLB = None
        self._ClusterLevel = None
        self._AutoUpgradeClusterLevel = None
        self._ChargeType = None
        self._EdgeVersion = None
        self._RegistryPrefix = None
        self._TagSpecification = None

    @property
    def K8SVersion(self):
        return self._K8SVersion

    @K8SVersion.setter
    def K8SVersion(self, K8SVersion):
        self._K8SVersion = K8SVersion

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def PodCIDR(self):
        return self._PodCIDR

    @PodCIDR.setter
    def PodCIDR(self, PodCIDR):
        self._PodCIDR = PodCIDR

    @property
    def ServiceCIDR(self):
        return self._ServiceCIDR

    @ServiceCIDR.setter
    def ServiceCIDR(self, ServiceCIDR):
        self._ServiceCIDR = ServiceCIDR

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def ClusterAdvancedSettings(self):
        return self._ClusterAdvancedSettings

    @ClusterAdvancedSettings.setter
    def ClusterAdvancedSettings(self, ClusterAdvancedSettings):
        self._ClusterAdvancedSettings = ClusterAdvancedSettings

    @property
    def MaxNodePodNum(self):
        return self._MaxNodePodNum

    @MaxNodePodNum.setter
    def MaxNodePodNum(self, MaxNodePodNum):
        self._MaxNodePodNum = MaxNodePodNum

    @property
    def PublicLB(self):
        return self._PublicLB

    @PublicLB.setter
    def PublicLB(self, PublicLB):
        self._PublicLB = PublicLB

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel

    @property
    def ChargeType(self):
        return self._ChargeType

    @ChargeType.setter
    def ChargeType(self, ChargeType):
        self._ChargeType = ChargeType

    @property
    def EdgeVersion(self):
        return self._EdgeVersion

    @EdgeVersion.setter
    def EdgeVersion(self, EdgeVersion):
        self._EdgeVersion = EdgeVersion

    @property
    def RegistryPrefix(self):
        return self._RegistryPrefix

    @RegistryPrefix.setter
    def RegistryPrefix(self, RegistryPrefix):
        self._RegistryPrefix = RegistryPrefix

    @property
    def TagSpecification(self):
        return self._TagSpecification

    @TagSpecification.setter
    def TagSpecification(self, TagSpecification):
        self._TagSpecification = TagSpecification


    def _deserialize(self, params):
        self._K8SVersion = params.get("K8SVersion")
        self._VpcId = params.get("VpcId")
        self._ClusterName = params.get("ClusterName")
        self._PodCIDR = params.get("PodCIDR")
        self._ServiceCIDR = params.get("ServiceCIDR")
        self._ClusterDesc = params.get("ClusterDesc")
        if params.get("ClusterAdvancedSettings") is not None:
            self._ClusterAdvancedSettings = EdgeClusterAdvancedSettings()
            self._ClusterAdvancedSettings._deserialize(params.get("ClusterAdvancedSettings"))
        self._MaxNodePodNum = params.get("MaxNodePodNum")
        if params.get("PublicLB") is not None:
            self._PublicLB = EdgeClusterPublicLB()
            self._PublicLB._deserialize(params.get("PublicLB"))
        self._ClusterLevel = params.get("ClusterLevel")
        self._AutoUpgradeClusterLevel = params.get("AutoUpgradeClusterLevel")
        self._ChargeType = params.get("ChargeType")
        self._EdgeVersion = params.get("EdgeVersion")
        self._RegistryPrefix = params.get("RegistryPrefix")
        if params.get("TagSpecification") is not None:
            self._TagSpecification = TagSpecification()
            self._TagSpecification._deserialize(params.get("TagSpecification"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTKEEdgeClusterResponse(AbstractModel):
    """CreateTKEEdgeCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 边缘计算集群Id
        :type ClusterId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterId = None
        self._RequestId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._RequestId = params.get("RequestId")


class CustomDriver(AbstractModel):
    """自定义驱动信息

    """

    def __init__(self):
        r"""
        :param _Address: 自定义GPU驱动地址链接
注意：此字段可能返回 null，表示取不到有效值。
        :type Address: str
        """
        self._Address = None

    @property
    def Address(self):
        return self._Address

    @Address.setter
    def Address(self, Address):
        self._Address = Address


    def _deserialize(self, params):
        self._Address = params.get("Address")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DNSConfig(AbstractModel):
    """自定义DNS配置

    """

    def __init__(self):
        r"""
        :param _Nameservers: DNS 服务器IP地址列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Nameservers: list of str
        :param _Searches: DNS搜索域列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Searches: list of str
        :param _Options: 对象选项列表，每个对象由name和value（可选）构成
注意：此字段可能返回 null，表示取不到有效值。
        :type Options: list of DNSConfigOption
        """
        self._Nameservers = None
        self._Searches = None
        self._Options = None

    @property
    def Nameservers(self):
        return self._Nameservers

    @Nameservers.setter
    def Nameservers(self, Nameservers):
        self._Nameservers = Nameservers

    @property
    def Searches(self):
        return self._Searches

    @Searches.setter
    def Searches(self, Searches):
        self._Searches = Searches

    @property
    def Options(self):
        return self._Options

    @Options.setter
    def Options(self, Options):
        self._Options = Options


    def _deserialize(self, params):
        self._Nameservers = params.get("Nameservers")
        self._Searches = params.get("Searches")
        if params.get("Options") is not None:
            self._Options = []
            for item in params.get("Options"):
                obj = DNSConfigOption()
                obj._deserialize(item)
                self._Options.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DNSConfigOption(AbstractModel):
    """DNS配置选项

    """

    def __init__(self):
        r"""
        :param _Name: 配置项名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _Value: 项值
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: str
        """
        self._Name = None
        self._Value = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, Value):
        self._Value = Value


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataDisk(AbstractModel):
    """描述了k8s节点数据盘相关配置与信息。

    """

    def __init__(self):
        r"""
        :param _DiskType: 云盘类型
注意：此字段可能返回 null，表示取不到有效值。
        :type DiskType: str
        :param _FileSystem: 文件系统(ext3/ext4/xfs)
注意：此字段可能返回 null，表示取不到有效值。
        :type FileSystem: str
        :param _DiskSize: 云盘大小(G）
注意：此字段可能返回 null，表示取不到有效值。
        :type DiskSize: int
        :param _AutoFormatAndMount: 是否自动化格式盘并挂载
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoFormatAndMount: bool
        :param _MountTarget: 挂载目录
注意：此字段可能返回 null，表示取不到有效值。
        :type MountTarget: str
        :param _DiskPartition: 挂载设备名或分区名，当且仅当添加已有节点时需要
注意：此字段可能返回 null，表示取不到有效值。
        :type DiskPartition: str
        """
        self._DiskType = None
        self._FileSystem = None
        self._DiskSize = None
        self._AutoFormatAndMount = None
        self._MountTarget = None
        self._DiskPartition = None

    @property
    def DiskType(self):
        return self._DiskType

    @DiskType.setter
    def DiskType(self, DiskType):
        self._DiskType = DiskType

    @property
    def FileSystem(self):
        return self._FileSystem

    @FileSystem.setter
    def FileSystem(self, FileSystem):
        self._FileSystem = FileSystem

    @property
    def DiskSize(self):
        return self._DiskSize

    @DiskSize.setter
    def DiskSize(self, DiskSize):
        self._DiskSize = DiskSize

    @property
    def AutoFormatAndMount(self):
        return self._AutoFormatAndMount

    @AutoFormatAndMount.setter
    def AutoFormatAndMount(self, AutoFormatAndMount):
        self._AutoFormatAndMount = AutoFormatAndMount

    @property
    def MountTarget(self):
        return self._MountTarget

    @MountTarget.setter
    def MountTarget(self, MountTarget):
        self._MountTarget = MountTarget

    @property
    def DiskPartition(self):
        return self._DiskPartition

    @DiskPartition.setter
    def DiskPartition(self, DiskPartition):
        self._DiskPartition = DiskPartition


    def _deserialize(self, params):
        self._DiskType = params.get("DiskType")
        self._FileSystem = params.get("FileSystem")
        self._DiskSize = params.get("DiskSize")
        self._AutoFormatAndMount = params.get("AutoFormatAndMount")
        self._MountTarget = params.get("MountTarget")
        self._DiskPartition = params.get("DiskPartition")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAddonRequest(AbstractModel):
    """DeleteAddon请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _AddonName: addon名称
        :type AddonName: str
        """
        self._ClusterId = None
        self._AddonName = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AddonName = params.get("AddonName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAddonResponse(AbstractModel):
    """DeleteAddon返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteBackupStorageLocationRequest(AbstractModel):
    """DeleteBackupStorageLocation请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Name: 备份仓库名称
        :type Name: str
        """
        self._Name = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name


    def _deserialize(self, params):
        self._Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBackupStorageLocationResponse(AbstractModel):
    """DeleteBackupStorageLocation返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterAsGroupsRequest(AbstractModel):
    """DeleteClusterAsGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID，通过[DescribeClusters](https://cloud.tencent.com/document/api/457/31862)接口获取。
        :type ClusterId: str
        :param _AutoScalingGroupIds: 集群伸缩组ID的列表
        :type AutoScalingGroupIds: list of str
        :param _KeepInstance: 是否保留伸缩组中的节点(默认值： false(不保留))
        :type KeepInstance: bool
        """
        self._ClusterId = None
        self._AutoScalingGroupIds = None
        self._KeepInstance = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AutoScalingGroupIds(self):
        return self._AutoScalingGroupIds

    @AutoScalingGroupIds.setter
    def AutoScalingGroupIds(self, AutoScalingGroupIds):
        self._AutoScalingGroupIds = AutoScalingGroupIds

    @property
    def KeepInstance(self):
        return self._KeepInstance

    @KeepInstance.setter
    def KeepInstance(self, KeepInstance):
        self._KeepInstance = KeepInstance


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AutoScalingGroupIds = params.get("AutoScalingGroupIds")
        self._KeepInstance = params.get("KeepInstance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterAsGroupsResponse(AbstractModel):
    """DeleteClusterAsGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterEndpointRequest(AbstractModel):
    """DeleteClusterEndpoint请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _IsExtranet: 是否为外网访问（TRUE 外网访问 FALSE 内网访问，默认值： FALSE）
        :type IsExtranet: bool
        """
        self._ClusterId = None
        self._IsExtranet = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def IsExtranet(self):
        return self._IsExtranet

    @IsExtranet.setter
    def IsExtranet(self, IsExtranet):
        self._IsExtranet = IsExtranet


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._IsExtranet = params.get("IsExtranet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterEndpointResponse(AbstractModel):
    """DeleteClusterEndpoint返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterEndpointVipRequest(AbstractModel):
    """DeleteClusterEndpointVip请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterEndpointVipResponse(AbstractModel):
    """DeleteClusterEndpointVip返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterInstancesRequest(AbstractModel):
    """DeleteClusterInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _InstanceIds: 主机InstanceId列表
        :type InstanceIds: list of str
        :param _InstanceDeleteMode: 集群实例删除时的策略：terminate（销毁实例，仅支持按量计费云主机实例） retain （仅移除，保留实例）
        :type InstanceDeleteMode: str
        :param _ForceDelete: 是否强制删除(当节点在初始化时，可以指定参数为TRUE)
        :type ForceDelete: bool
        """
        self._ClusterId = None
        self._InstanceIds = None
        self._InstanceDeleteMode = None
        self._ForceDelete = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceDeleteMode(self):
        return self._InstanceDeleteMode

    @InstanceDeleteMode.setter
    def InstanceDeleteMode(self, InstanceDeleteMode):
        self._InstanceDeleteMode = InstanceDeleteMode

    @property
    def ForceDelete(self):
        return self._ForceDelete

    @ForceDelete.setter
    def ForceDelete(self, ForceDelete):
        self._ForceDelete = ForceDelete


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._InstanceIds = params.get("InstanceIds")
        self._InstanceDeleteMode = params.get("InstanceDeleteMode")
        self._ForceDelete = params.get("ForceDelete")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterInstancesResponse(AbstractModel):
    """DeleteClusterInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _SuccInstanceIds: 删除成功的实例ID列表
注意：此字段可能返回 null，表示取不到有效值。
        :type SuccInstanceIds: list of str
        :param _FailedInstanceIds: 删除失败的实例ID列表
注意：此字段可能返回 null，表示取不到有效值。
        :type FailedInstanceIds: list of str
        :param _NotFoundInstanceIds: 未匹配到的实例ID列表
注意：此字段可能返回 null，表示取不到有效值。
        :type NotFoundInstanceIds: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._SuccInstanceIds = None
        self._FailedInstanceIds = None
        self._NotFoundInstanceIds = None
        self._RequestId = None

    @property
    def SuccInstanceIds(self):
        return self._SuccInstanceIds

    @SuccInstanceIds.setter
    def SuccInstanceIds(self, SuccInstanceIds):
        self._SuccInstanceIds = SuccInstanceIds

    @property
    def FailedInstanceIds(self):
        return self._FailedInstanceIds

    @FailedInstanceIds.setter
    def FailedInstanceIds(self, FailedInstanceIds):
        self._FailedInstanceIds = FailedInstanceIds

    @property
    def NotFoundInstanceIds(self):
        return self._NotFoundInstanceIds

    @NotFoundInstanceIds.setter
    def NotFoundInstanceIds(self, NotFoundInstanceIds):
        self._NotFoundInstanceIds = NotFoundInstanceIds

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._SuccInstanceIds = params.get("SuccInstanceIds")
        self._FailedInstanceIds = params.get("FailedInstanceIds")
        self._NotFoundInstanceIds = params.get("NotFoundInstanceIds")
        self._RequestId = params.get("RequestId")


class DeleteClusterNodePoolRequest(AbstractModel):
    """DeleteClusterNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 节点池对应的 ClusterId
        :type ClusterId: str
        :param _NodePoolIds: 需要删除的节点池 Id 列表
        :type NodePoolIds: list of str
        :param _KeepInstance: 删除节点池时是否保留节点池内节点(节点仍然会被移出集群，但对应的实例不会被销毁)
        :type KeepInstance: bool
        """
        self._ClusterId = None
        self._NodePoolIds = None
        self._KeepInstance = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolIds(self):
        return self._NodePoolIds

    @NodePoolIds.setter
    def NodePoolIds(self, NodePoolIds):
        self._NodePoolIds = NodePoolIds

    @property
    def KeepInstance(self):
        return self._KeepInstance

    @KeepInstance.setter
    def KeepInstance(self, KeepInstance):
        self._KeepInstance = KeepInstance


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolIds = params.get("NodePoolIds")
        self._KeepInstance = params.get("KeepInstance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterNodePoolResponse(AbstractModel):
    """DeleteClusterNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterRequest(AbstractModel):
    """DeleteCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _InstanceDeleteMode: 集群实例删除时的策略：terminate（销毁实例，仅支持按量计费云主机实例） retain （仅移除，保留实例）
        :type InstanceDeleteMode: str
        :param _ResourceDeleteOptions: 集群删除时资源的删除策略，目前支持CBS（默认保留CBS）
        :type ResourceDeleteOptions: list of ResourceDeleteOption
        """
        self._ClusterId = None
        self._InstanceDeleteMode = None
        self._ResourceDeleteOptions = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def InstanceDeleteMode(self):
        return self._InstanceDeleteMode

    @InstanceDeleteMode.setter
    def InstanceDeleteMode(self, InstanceDeleteMode):
        self._InstanceDeleteMode = InstanceDeleteMode

    @property
    def ResourceDeleteOptions(self):
        return self._ResourceDeleteOptions

    @ResourceDeleteOptions.setter
    def ResourceDeleteOptions(self, ResourceDeleteOptions):
        self._ResourceDeleteOptions = ResourceDeleteOptions


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._InstanceDeleteMode = params.get("InstanceDeleteMode")
        if params.get("ResourceDeleteOptions") is not None:
            self._ResourceDeleteOptions = []
            for item in params.get("ResourceDeleteOptions"):
                obj = ResourceDeleteOption()
                obj._deserialize(item)
                self._ResourceDeleteOptions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterResponse(AbstractModel):
    """DeleteCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterRouteRequest(AbstractModel):
    """DeleteClusterRoute请求参数结构体

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param _GatewayIp: 下一跳地址。
        :type GatewayIp: str
        :param _DestinationCidrBlock: 目的端CIDR。
        :type DestinationCidrBlock: str
        """
        self._RouteTableName = None
        self._GatewayIp = None
        self._DestinationCidrBlock = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def GatewayIp(self):
        return self._GatewayIp

    @GatewayIp.setter
    def GatewayIp(self, GatewayIp):
        self._GatewayIp = GatewayIp

    @property
    def DestinationCidrBlock(self):
        return self._DestinationCidrBlock

    @DestinationCidrBlock.setter
    def DestinationCidrBlock(self, DestinationCidrBlock):
        self._DestinationCidrBlock = DestinationCidrBlock


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        self._GatewayIp = params.get("GatewayIp")
        self._DestinationCidrBlock = params.get("DestinationCidrBlock")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterRouteResponse(AbstractModel):
    """DeleteClusterRoute返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterRouteTableRequest(AbstractModel):
    """DeleteClusterRouteTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称
        :type RouteTableName: str
        """
        self._RouteTableName = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterRouteTableResponse(AbstractModel):
    """DeleteClusterRouteTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterVirtualNodePoolRequest(AbstractModel):
    """DeleteClusterVirtualNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodePoolIds: 虚拟节点池ID列表
        :type NodePoolIds: list of str
        :param _Force: 是否强制删除，在虚拟节点上有pod的情况下，如果选择非强制删除，则删除会失败
        :type Force: bool
        """
        self._ClusterId = None
        self._NodePoolIds = None
        self._Force = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolIds(self):
        return self._NodePoolIds

    @NodePoolIds.setter
    def NodePoolIds(self, NodePoolIds):
        self._NodePoolIds = NodePoolIds

    @property
    def Force(self):
        return self._Force

    @Force.setter
    def Force(self, Force):
        self._Force = Force


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolIds = params.get("NodePoolIds")
        self._Force = params.get("Force")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterVirtualNodePoolResponse(AbstractModel):
    """DeleteClusterVirtualNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteClusterVirtualNodeRequest(AbstractModel):
    """DeleteClusterVirtualNode请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodeNames: 虚拟节点列表
        :type NodeNames: list of str
        :param _Force: 是否强制删除：如果虚拟节点上有运行中Pod，则非强制删除状态下不会进行删除
        :type Force: bool
        """
        self._ClusterId = None
        self._NodeNames = None
        self._Force = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodeNames(self):
        return self._NodeNames

    @NodeNames.setter
    def NodeNames(self, NodeNames):
        self._NodeNames = NodeNames

    @property
    def Force(self):
        return self._Force

    @Force.setter
    def Force(self, Force):
        self._Force = Force


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodeNames = params.get("NodeNames")
        self._Force = params.get("Force")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteClusterVirtualNodeResponse(AbstractModel):
    """DeleteClusterVirtualNode返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteECMInstancesRequest(AbstractModel):
    """DeleteECMInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群ID
        :type ClusterID: str
        :param _EcmIdSet: ecm id集合
        :type EcmIdSet: list of str
        """
        self._ClusterID = None
        self._EcmIdSet = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def EcmIdSet(self):
        return self._EcmIdSet

    @EcmIdSet.setter
    def EcmIdSet(self, EcmIdSet):
        self._EcmIdSet = EcmIdSet


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        self._EcmIdSet = params.get("EcmIdSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteECMInstancesResponse(AbstractModel):
    """DeleteECMInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteEKSClusterRequest(AbstractModel):
    """DeleteEKSCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 弹性集群Id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEKSClusterResponse(AbstractModel):
    """DeleteEKSCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteEKSContainerInstancesRequest(AbstractModel):
    """DeleteEKSContainerInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiIds: 需要删除的EksCi的Id。 最大数量不超过20
        :type EksCiIds: list of str
        :param _ReleaseAutoCreatedEip: 是否释放为EksCi自动创建的Eip
        :type ReleaseAutoCreatedEip: bool
        """
        self._EksCiIds = None
        self._ReleaseAutoCreatedEip = None

    @property
    def EksCiIds(self):
        return self._EksCiIds

    @EksCiIds.setter
    def EksCiIds(self, EksCiIds):
        self._EksCiIds = EksCiIds

    @property
    def ReleaseAutoCreatedEip(self):
        return self._ReleaseAutoCreatedEip

    @ReleaseAutoCreatedEip.setter
    def ReleaseAutoCreatedEip(self, ReleaseAutoCreatedEip):
        self._ReleaseAutoCreatedEip = ReleaseAutoCreatedEip


    def _deserialize(self, params):
        self._EksCiIds = params.get("EksCiIds")
        self._ReleaseAutoCreatedEip = params.get("ReleaseAutoCreatedEip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEKSContainerInstancesResponse(AbstractModel):
    """DeleteEKSContainerInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteEdgeCVMInstancesRequest(AbstractModel):
    """DeleteEdgeCVMInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群ID
        :type ClusterID: str
        :param _CvmIdSet: cvm id集合
        :type CvmIdSet: list of str
        """
        self._ClusterID = None
        self._CvmIdSet = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def CvmIdSet(self):
        return self._CvmIdSet

    @CvmIdSet.setter
    def CvmIdSet(self, CvmIdSet):
        self._CvmIdSet = CvmIdSet


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        self._CvmIdSet = params.get("CvmIdSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEdgeCVMInstancesResponse(AbstractModel):
    """DeleteEdgeCVMInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteEdgeClusterInstancesRequest(AbstractModel):
    """DeleteEdgeClusterInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _InstanceIds: 待删除实例ID数组
        :type InstanceIds: list of str
        """
        self._ClusterId = None
        self._InstanceIds = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEdgeClusterInstancesResponse(AbstractModel):
    """DeleteEdgeClusterInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteImageCachesRequest(AbstractModel):
    """DeleteImageCaches请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ImageCacheIds: 镜像缓存Id数组
        :type ImageCacheIds: list of str
        """
        self._ImageCacheIds = None

    @property
    def ImageCacheIds(self):
        return self._ImageCacheIds

    @ImageCacheIds.setter
    def ImageCacheIds(self, ImageCacheIds):
        self._ImageCacheIds = ImageCacheIds


    def _deserialize(self, params):
        self._ImageCacheIds = params.get("ImageCacheIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteImageCachesResponse(AbstractModel):
    """DeleteImageCaches返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusAlertPolicyRequest(AbstractModel):
    """DeletePrometheusAlertPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _AlertIds: 告警策略id列表
        :type AlertIds: list of str
        :param _Names: 告警策略名称
        :type Names: list of str
        """
        self._InstanceId = None
        self._AlertIds = None
        self._Names = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def AlertIds(self):
        return self._AlertIds

    @AlertIds.setter
    def AlertIds(self, AlertIds):
        self._AlertIds = AlertIds

    @property
    def Names(self):
        return self._Names

    @Names.setter
    def Names(self, Names):
        self._Names = Names


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._AlertIds = params.get("AlertIds")
        self._Names = params.get("Names")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusAlertPolicyResponse(AbstractModel):
    """DeletePrometheusAlertPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusAlertRuleRequest(AbstractModel):
    """DeletePrometheusAlertRule请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _AlertIds: 告警规则id列表
        :type AlertIds: list of str
        """
        self._InstanceId = None
        self._AlertIds = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def AlertIds(self):
        return self._AlertIds

    @AlertIds.setter
    def AlertIds(self, AlertIds):
        self._AlertIds = AlertIds


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._AlertIds = params.get("AlertIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusAlertRuleResponse(AbstractModel):
    """DeletePrometheusAlertRule返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusClusterAgentRequest(AbstractModel):
    """DeletePrometheusClusterAgent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Agents: agent列表
        :type Agents: list of PrometheusAgentInfo
        :param _InstanceId: 实例id
        :type InstanceId: str
        """
        self._Agents = None
        self._InstanceId = None

    @property
    def Agents(self):
        return self._Agents

    @Agents.setter
    def Agents(self, Agents):
        self._Agents = Agents

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        if params.get("Agents") is not None:
            self._Agents = []
            for item in params.get("Agents"):
                obj = PrometheusAgentInfo()
                obj._deserialize(item)
                self._Agents.append(obj)
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusClusterAgentResponse(AbstractModel):
    """DeletePrometheusClusterAgent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusConfigRequest(AbstractModel):
    """DeletePrometheusConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _ServiceMonitors: 要删除的ServiceMonitor名字列表
        :type ServiceMonitors: list of str
        :param _PodMonitors: 要删除的PodMonitor名字列表
        :type PodMonitors: list of str
        :param _RawJobs: 要删除的RawJobs名字列表
        :type RawJobs: list of str
        """
        self._InstanceId = None
        self._ClusterType = None
        self._ClusterId = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        self._ServiceMonitors = params.get("ServiceMonitors")
        self._PodMonitors = params.get("PodMonitors")
        self._RawJobs = params.get("RawJobs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusConfigResponse(AbstractModel):
    """DeletePrometheusConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusRecordRuleYamlRequest(AbstractModel):
    """DeletePrometheusRecordRuleYaml请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Names: 聚合规则列表
        :type Names: list of str
        """
        self._InstanceId = None
        self._Names = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Names(self):
        return self._Names

    @Names.setter
    def Names(self, Names):
        self._Names = Names


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Names = params.get("Names")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusRecordRuleYamlResponse(AbstractModel):
    """DeletePrometheusRecordRuleYaml返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusTempRequest(AbstractModel):
    """DeletePrometheusTemp请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板id
        :type TemplateId: str
        """
        self._TemplateId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusTempResponse(AbstractModel):
    """DeletePrometheusTemp返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusTempSyncRequest(AbstractModel):
    """DeletePrometheusTempSync请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板id
        :type TemplateId: str
        :param _Targets: 取消同步的对象列表
        :type Targets: list of PrometheusTemplateSyncTarget
        """
        self._TemplateId = None
        self._Targets = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTemplateSyncTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusTempSyncResponse(AbstractModel):
    """DeletePrometheusTempSync返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusTemplateRequest(AbstractModel):
    """DeletePrometheusTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板id
        :type TemplateId: str
        """
        self._TemplateId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusTemplateResponse(AbstractModel):
    """DeletePrometheusTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeletePrometheusTemplateSyncRequest(AbstractModel):
    """DeletePrometheusTemplateSync请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板id
        :type TemplateId: str
        :param _Targets: 取消同步的对象列表
        :type Targets: list of PrometheusTemplateSyncTarget
        """
        self._TemplateId = None
        self._Targets = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTemplateSyncTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePrometheusTemplateSyncResponse(AbstractModel):
    """DeletePrometheusTemplateSync返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteTKEEdgeClusterRequest(AbstractModel):
    """DeleteTKEEdgeCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTKEEdgeClusterResponse(AbstractModel):
    """DeleteTKEEdgeCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DescribeAddonRequest(AbstractModel):
    """DescribeAddon请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _AddonName: addon名称（不传时会返回集群下全部的addon）
        :type AddonName: str
        """
        self._ClusterId = None
        self._AddonName = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AddonName = params.get("AddonName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAddonResponse(AbstractModel):
    """DescribeAddon返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Addons: addon列表
        :type Addons: list of Addon
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Addons = None
        self._RequestId = None

    @property
    def Addons(self):
        return self._Addons

    @Addons.setter
    def Addons(self, Addons):
        self._Addons = Addons

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Addons") is not None:
            self._Addons = []
            for item in params.get("Addons"):
                obj = Addon()
                obj._deserialize(item)
                self._Addons.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeAddonValuesRequest(AbstractModel):
    """DescribeAddonValues请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _AddonName: addon名称
        :type AddonName: str
        """
        self._ClusterId = None
        self._AddonName = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AddonName = params.get("AddonName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAddonValuesResponse(AbstractModel):
    """DescribeAddonValues返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Values: 参数列表，如果addon已安装，会使用已设置的的参数做渲染，是一个json格式的字符串
        :type Values: str
        :param _DefaultValues: addon支持的参数列表，使用默认值，是一个json格式的字符串
        :type DefaultValues: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Values = None
        self._DefaultValues = None
        self._RequestId = None

    @property
    def Values(self):
        return self._Values

    @Values.setter
    def Values(self, Values):
        self._Values = Values

    @property
    def DefaultValues(self):
        return self._DefaultValues

    @DefaultValues.setter
    def DefaultValues(self, DefaultValues):
        self._DefaultValues = DefaultValues

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Values = params.get("Values")
        self._DefaultValues = params.get("DefaultValues")
        self._RequestId = params.get("RequestId")


class DescribeAvailableClusterVersionRequest(AbstractModel):
    """DescribeAvailableClusterVersion请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群 Id
        :type ClusterId: str
        :param _ClusterIds: 集群 Id 列表
        :type ClusterIds: list of str
        """
        self._ClusterId = None
        self._ClusterIds = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterIds = params.get("ClusterIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAvailableClusterVersionResponse(AbstractModel):
    """DescribeAvailableClusterVersion返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Versions: 可升级的集群版本号
注意：此字段可能返回 null，表示取不到有效值。
        :type Versions: list of str
        :param _Clusters: 集群信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Clusters: list of ClusterVersion
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Versions = None
        self._Clusters = None
        self._RequestId = None

    @property
    def Versions(self):
        return self._Versions

    @Versions.setter
    def Versions(self, Versions):
        self._Versions = Versions

    @property
    def Clusters(self):
        return self._Clusters

    @Clusters.setter
    def Clusters(self, Clusters):
        self._Clusters = Clusters

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Versions = params.get("Versions")
        if params.get("Clusters") is not None:
            self._Clusters = []
            for item in params.get("Clusters"):
                obj = ClusterVersion()
                obj._deserialize(item)
                self._Clusters.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeAvailableTKEEdgeVersionRequest(AbstractModel):
    """DescribeAvailableTKEEdgeVersion请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 填写ClusterId获取当前集群各个组件版本和最新版本
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAvailableTKEEdgeVersionResponse(AbstractModel):
    """DescribeAvailableTKEEdgeVersion返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Versions: 版本列表
        :type Versions: list of str
        :param _EdgeVersionLatest: 边缘集群最新版本
注意：此字段可能返回 null，表示取不到有效值。
        :type EdgeVersionLatest: str
        :param _EdgeVersionCurrent: 边缘集群当前版本
注意：此字段可能返回 null，表示取不到有效值。
        :type EdgeVersionCurrent: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Versions = None
        self._EdgeVersionLatest = None
        self._EdgeVersionCurrent = None
        self._RequestId = None

    @property
    def Versions(self):
        return self._Versions

    @Versions.setter
    def Versions(self, Versions):
        self._Versions = Versions

    @property
    def EdgeVersionLatest(self):
        return self._EdgeVersionLatest

    @EdgeVersionLatest.setter
    def EdgeVersionLatest(self, EdgeVersionLatest):
        self._EdgeVersionLatest = EdgeVersionLatest

    @property
    def EdgeVersionCurrent(self):
        return self._EdgeVersionCurrent

    @EdgeVersionCurrent.setter
    def EdgeVersionCurrent(self, EdgeVersionCurrent):
        self._EdgeVersionCurrent = EdgeVersionCurrent

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Versions = params.get("Versions")
        self._EdgeVersionLatest = params.get("EdgeVersionLatest")
        self._EdgeVersionCurrent = params.get("EdgeVersionCurrent")
        self._RequestId = params.get("RequestId")


class DescribeBackupStorageLocationsRequest(AbstractModel):
    """DescribeBackupStorageLocations请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Names: 多个备份仓库名称，如果不填写，默认返回当前地域所有存储仓库名称
        :type Names: list of str
        """
        self._Names = None

    @property
    def Names(self):
        return self._Names

    @Names.setter
    def Names(self, Names):
        self._Names = Names


    def _deserialize(self, params):
        self._Names = params.get("Names")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupStorageLocationsResponse(AbstractModel):
    """DescribeBackupStorageLocations返回参数结构体

    """

    def __init__(self):
        r"""
        :param _BackupStorageLocationSet: 详细备份仓库信息
注意：此字段可能返回 null，表示取不到有效值。
        :type BackupStorageLocationSet: list of BackupStorageLocation
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._BackupStorageLocationSet = None
        self._RequestId = None

    @property
    def BackupStorageLocationSet(self):
        return self._BackupStorageLocationSet

    @BackupStorageLocationSet.setter
    def BackupStorageLocationSet(self, BackupStorageLocationSet):
        self._BackupStorageLocationSet = BackupStorageLocationSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("BackupStorageLocationSet") is not None:
            self._BackupStorageLocationSet = []
            for item in params.get("BackupStorageLocationSet"):
                obj = BackupStorageLocation()
                obj._deserialize(item)
                self._BackupStorageLocationSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterAsGroupOptionRequest(AbstractModel):
    """DescribeClusterAsGroupOption请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterAsGroupOptionResponse(AbstractModel):
    """DescribeClusterAsGroupOption返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterAsGroupOption: 集群弹性伸缩属性
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterAsGroupOption: :class:`tencentcloud.tke.v20180525.models.ClusterAsGroupOption`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterAsGroupOption = None
        self._RequestId = None

    @property
    def ClusterAsGroupOption(self):
        return self._ClusterAsGroupOption

    @ClusterAsGroupOption.setter
    def ClusterAsGroupOption(self, ClusterAsGroupOption):
        self._ClusterAsGroupOption = ClusterAsGroupOption

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ClusterAsGroupOption") is not None:
            self._ClusterAsGroupOption = ClusterAsGroupOption()
            self._ClusterAsGroupOption._deserialize(params.get("ClusterAsGroupOption"))
        self._RequestId = params.get("RequestId")


class DescribeClusterAsGroupsRequest(AbstractModel):
    """DescribeClusterAsGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _AutoScalingGroupIds: 伸缩组ID列表，如果为空，表示拉取集群关联的所有伸缩组。
        :type AutoScalingGroupIds: list of str
        :param _Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API [简介](https://cloud.tencent.com/document/api/213/15688)中的相关小节。
        :type Offset: int
        :param _Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API [简介](https://cloud.tencent.com/document/api/213/15688)中的相关小节。
        :type Limit: int
        """
        self._ClusterId = None
        self._AutoScalingGroupIds = None
        self._Offset = None
        self._Limit = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AutoScalingGroupIds(self):
        return self._AutoScalingGroupIds

    @AutoScalingGroupIds.setter
    def AutoScalingGroupIds(self, AutoScalingGroupIds):
        self._AutoScalingGroupIds = AutoScalingGroupIds

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AutoScalingGroupIds = params.get("AutoScalingGroupIds")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterAsGroupsResponse(AbstractModel):
    """DescribeClusterAsGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 集群关联的伸缩组总数
        :type TotalCount: int
        :param _ClusterAsGroupSet: 集群关联的伸缩组列表
        :type ClusterAsGroupSet: list of ClusterAsGroup
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._ClusterAsGroupSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def ClusterAsGroupSet(self):
        return self._ClusterAsGroupSet

    @ClusterAsGroupSet.setter
    def ClusterAsGroupSet(self, ClusterAsGroupSet):
        self._ClusterAsGroupSet = ClusterAsGroupSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("ClusterAsGroupSet") is not None:
            self._ClusterAsGroupSet = []
            for item in params.get("ClusterAsGroupSet"):
                obj = ClusterAsGroup()
                obj._deserialize(item)
                self._ClusterAsGroupSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterAuthenticationOptionsRequest(AbstractModel):
    """DescribeClusterAuthenticationOptions请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterAuthenticationOptionsResponse(AbstractModel):
    """DescribeClusterAuthenticationOptions返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ServiceAccounts: ServiceAccount认证配置
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceAccounts: :class:`tencentcloud.tke.v20180525.models.ServiceAccountAuthenticationOptions`
        :param _LatestOperationState: 最近一次修改操作结果，返回值可能为：Updating，Success，Failed，TimeOut
注意：此字段可能返回 null，表示取不到有效值。
        :type LatestOperationState: str
        :param _OIDCConfig: OIDC认证配置
注意：此字段可能返回 null，表示取不到有效值。
        :type OIDCConfig: :class:`tencentcloud.tke.v20180525.models.OIDCConfigAuthenticationOptions`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ServiceAccounts = None
        self._LatestOperationState = None
        self._OIDCConfig = None
        self._RequestId = None

    @property
    def ServiceAccounts(self):
        return self._ServiceAccounts

    @ServiceAccounts.setter
    def ServiceAccounts(self, ServiceAccounts):
        self._ServiceAccounts = ServiceAccounts

    @property
    def LatestOperationState(self):
        return self._LatestOperationState

    @LatestOperationState.setter
    def LatestOperationState(self, LatestOperationState):
        self._LatestOperationState = LatestOperationState

    @property
    def OIDCConfig(self):
        return self._OIDCConfig

    @OIDCConfig.setter
    def OIDCConfig(self, OIDCConfig):
        self._OIDCConfig = OIDCConfig

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ServiceAccounts") is not None:
            self._ServiceAccounts = ServiceAccountAuthenticationOptions()
            self._ServiceAccounts._deserialize(params.get("ServiceAccounts"))
        self._LatestOperationState = params.get("LatestOperationState")
        if params.get("OIDCConfig") is not None:
            self._OIDCConfig = OIDCConfigAuthenticationOptions()
            self._OIDCConfig._deserialize(params.get("OIDCConfig"))
        self._RequestId = params.get("RequestId")


class DescribeClusterCommonNamesRequest(AbstractModel):
    """DescribeClusterCommonNames请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _SubaccountUins: 子账户列表，不可超出最大值50
        :type SubaccountUins: list of str
        :param _RoleIds: 角色ID列表，不可超出最大值50
        :type RoleIds: list of str
        """
        self._ClusterId = None
        self._SubaccountUins = None
        self._RoleIds = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SubaccountUins(self):
        return self._SubaccountUins

    @SubaccountUins.setter
    def SubaccountUins(self, SubaccountUins):
        self._SubaccountUins = SubaccountUins

    @property
    def RoleIds(self):
        return self._RoleIds

    @RoleIds.setter
    def RoleIds(self, RoleIds):
        self._RoleIds = RoleIds


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._SubaccountUins = params.get("SubaccountUins")
        self._RoleIds = params.get("RoleIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterCommonNamesResponse(AbstractModel):
    """DescribeClusterCommonNames返回参数结构体

    """

    def __init__(self):
        r"""
        :param _CommonNames: 子账户Uin与其客户端证书的CN字段映射
        :type CommonNames: list of CommonName
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._CommonNames = None
        self._RequestId = None

    @property
    def CommonNames(self):
        return self._CommonNames

    @CommonNames.setter
    def CommonNames(self, CommonNames):
        self._CommonNames = CommonNames

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("CommonNames") is not None:
            self._CommonNames = []
            for item in params.get("CommonNames"):
                obj = CommonName()
                obj._deserialize(item)
                self._CommonNames.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterControllersRequest(AbstractModel):
    """DescribeClusterControllers请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterControllersResponse(AbstractModel):
    """DescribeClusterControllers返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ControllerStatusSet: 描述集群中各个控制器的状态
        :type ControllerStatusSet: list of ControllerStatus
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ControllerStatusSet = None
        self._RequestId = None

    @property
    def ControllerStatusSet(self):
        return self._ControllerStatusSet

    @ControllerStatusSet.setter
    def ControllerStatusSet(self, ControllerStatusSet):
        self._ControllerStatusSet = ControllerStatusSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ControllerStatusSet") is not None:
            self._ControllerStatusSet = []
            for item in params.get("ControllerStatusSet"):
                obj = ControllerStatus()
                obj._deserialize(item)
                self._ControllerStatusSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterEndpointStatusRequest(AbstractModel):
    """DescribeClusterEndpointStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _IsExtranet: 是否为外网访问（TRUE 外网访问 FALSE 内网访问，默认值： FALSE）
        :type IsExtranet: bool
        """
        self._ClusterId = None
        self._IsExtranet = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def IsExtranet(self):
        return self._IsExtranet

    @IsExtranet.setter
    def IsExtranet(self, IsExtranet):
        self._IsExtranet = IsExtranet


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._IsExtranet = params.get("IsExtranet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterEndpointStatusResponse(AbstractModel):
    """DescribeClusterEndpointStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 查询集群访问端口状态（Created 开启成功，Creating 开启中，NotFound 未开启）
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _ErrorMsg: 开启访问入口失败信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._ErrorMsg = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ErrorMsg(self):
        return self._ErrorMsg

    @ErrorMsg.setter
    def ErrorMsg(self, ErrorMsg):
        self._ErrorMsg = ErrorMsg

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        self._ErrorMsg = params.get("ErrorMsg")
        self._RequestId = params.get("RequestId")


class DescribeClusterEndpointVipStatusRequest(AbstractModel):
    """DescribeClusterEndpointVipStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterEndpointVipStatusResponse(AbstractModel):
    """DescribeClusterEndpointVipStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 端口操作状态 (Creating 创建中  CreateFailed 创建失败 Created 创建完成 Deleting 删除中 DeletedFailed 删除失败 Deleted 已删除 NotFound 未发现操作 )
        :type Status: str
        :param _ErrorMsg: 操作失败的原因
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._ErrorMsg = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ErrorMsg(self):
        return self._ErrorMsg

    @ErrorMsg.setter
    def ErrorMsg(self, ErrorMsg):
        self._ErrorMsg = ErrorMsg

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        self._ErrorMsg = params.get("ErrorMsg")
        self._RequestId = params.get("RequestId")


class DescribeClusterEndpointsRequest(AbstractModel):
    """DescribeClusterEndpoints请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterEndpointsResponse(AbstractModel):
    """DescribeClusterEndpoints返回参数结构体

    """

    def __init__(self):
        r"""
        :param _CertificationAuthority: 集群APIServer的CA证书
        :type CertificationAuthority: str
        :param _ClusterExternalEndpoint: 集群APIServer的外网访问地址
        :type ClusterExternalEndpoint: str
        :param _ClusterIntranetEndpoint: 集群APIServer的内网访问地址
        :type ClusterIntranetEndpoint: str
        :param _ClusterDomain: 集群APIServer的域名
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterDomain: str
        :param _ClusterExternalACL: 集群APIServer的外网访问ACL列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterExternalACL: list of str
        :param _ClusterExternalDomain: 外网域名
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterExternalDomain: str
        :param _ClusterIntranetDomain: 内网域名
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterIntranetDomain: str
        :param _SecurityGroup: 外网安全组
注意：此字段可能返回 null，表示取不到有效值。
        :type SecurityGroup: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._CertificationAuthority = None
        self._ClusterExternalEndpoint = None
        self._ClusterIntranetEndpoint = None
        self._ClusterDomain = None
        self._ClusterExternalACL = None
        self._ClusterExternalDomain = None
        self._ClusterIntranetDomain = None
        self._SecurityGroup = None
        self._RequestId = None

    @property
    def CertificationAuthority(self):
        return self._CertificationAuthority

    @CertificationAuthority.setter
    def CertificationAuthority(self, CertificationAuthority):
        self._CertificationAuthority = CertificationAuthority

    @property
    def ClusterExternalEndpoint(self):
        return self._ClusterExternalEndpoint

    @ClusterExternalEndpoint.setter
    def ClusterExternalEndpoint(self, ClusterExternalEndpoint):
        self._ClusterExternalEndpoint = ClusterExternalEndpoint

    @property
    def ClusterIntranetEndpoint(self):
        return self._ClusterIntranetEndpoint

    @ClusterIntranetEndpoint.setter
    def ClusterIntranetEndpoint(self, ClusterIntranetEndpoint):
        self._ClusterIntranetEndpoint = ClusterIntranetEndpoint

    @property
    def ClusterDomain(self):
        return self._ClusterDomain

    @ClusterDomain.setter
    def ClusterDomain(self, ClusterDomain):
        self._ClusterDomain = ClusterDomain

    @property
    def ClusterExternalACL(self):
        return self._ClusterExternalACL

    @ClusterExternalACL.setter
    def ClusterExternalACL(self, ClusterExternalACL):
        self._ClusterExternalACL = ClusterExternalACL

    @property
    def ClusterExternalDomain(self):
        return self._ClusterExternalDomain

    @ClusterExternalDomain.setter
    def ClusterExternalDomain(self, ClusterExternalDomain):
        self._ClusterExternalDomain = ClusterExternalDomain

    @property
    def ClusterIntranetDomain(self):
        return self._ClusterIntranetDomain

    @ClusterIntranetDomain.setter
    def ClusterIntranetDomain(self, ClusterIntranetDomain):
        self._ClusterIntranetDomain = ClusterIntranetDomain

    @property
    def SecurityGroup(self):
        return self._SecurityGroup

    @SecurityGroup.setter
    def SecurityGroup(self, SecurityGroup):
        self._SecurityGroup = SecurityGroup

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._CertificationAuthority = params.get("CertificationAuthority")
        self._ClusterExternalEndpoint = params.get("ClusterExternalEndpoint")
        self._ClusterIntranetEndpoint = params.get("ClusterIntranetEndpoint")
        self._ClusterDomain = params.get("ClusterDomain")
        self._ClusterExternalACL = params.get("ClusterExternalACL")
        self._ClusterExternalDomain = params.get("ClusterExternalDomain")
        self._ClusterIntranetDomain = params.get("ClusterIntranetDomain")
        self._SecurityGroup = params.get("SecurityGroup")
        self._RequestId = params.get("RequestId")


class DescribeClusterInspectionResultsOverviewRequest(AbstractModel):
    """DescribeClusterInspectionResultsOverview请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: Array of String	目标集群列表，为空查询用户所有集群

        :type ClusterIds: list of str
        :param _GroupBy: 聚合字段信息，概览结果按照 GroupBy 信息聚合后返回，可选参数：
catalogue.first：按一级分类聚合
catalogue.second：按二级分类聚合
        :type GroupBy: list of str
        """
        self._ClusterIds = None
        self._GroupBy = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds

    @property
    def GroupBy(self):
        return self._GroupBy

    @GroupBy.setter
    def GroupBy(self, GroupBy):
        self._GroupBy = GroupBy


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        self._GroupBy = params.get("GroupBy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterInspectionResultsOverviewResponse(AbstractModel):
    """DescribeClusterInspectionResultsOverview返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Statistics: 诊断结果统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Statistics: list of KubeJarvisStateStatistic
        :param _Diagnostics: 诊断结果概览
注意：此字段可能返回 null，表示取不到有效值。
        :type Diagnostics: list of KubeJarvisStateDiagnosticOverview
        :param _InspectionOverview: 集群诊断结果概览
注意：此字段可能返回 null，表示取不到有效值。
        :type InspectionOverview: list of KubeJarvisStateInspectionOverview
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Statistics = None
        self._Diagnostics = None
        self._InspectionOverview = None
        self._RequestId = None

    @property
    def Statistics(self):
        return self._Statistics

    @Statistics.setter
    def Statistics(self, Statistics):
        self._Statistics = Statistics

    @property
    def Diagnostics(self):
        return self._Diagnostics

    @Diagnostics.setter
    def Diagnostics(self, Diagnostics):
        self._Diagnostics = Diagnostics

    @property
    def InspectionOverview(self):
        return self._InspectionOverview

    @InspectionOverview.setter
    def InspectionOverview(self, InspectionOverview):
        self._InspectionOverview = InspectionOverview

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Statistics") is not None:
            self._Statistics = []
            for item in params.get("Statistics"):
                obj = KubeJarvisStateStatistic()
                obj._deserialize(item)
                self._Statistics.append(obj)
        if params.get("Diagnostics") is not None:
            self._Diagnostics = []
            for item in params.get("Diagnostics"):
                obj = KubeJarvisStateDiagnosticOverview()
                obj._deserialize(item)
                self._Diagnostics.append(obj)
        if params.get("InspectionOverview") is not None:
            self._InspectionOverview = []
            for item in params.get("InspectionOverview"):
                obj = KubeJarvisStateInspectionOverview()
                obj._deserialize(item)
                self._InspectionOverview.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterInstancesRequest(AbstractModel):
    """DescribeClusterInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API [简介](https://cloud.tencent.com/document/api/213/15688)中的相关小节。
        :type Offset: int
        :param _Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API [简介](https://cloud.tencent.com/document/api/213/15688)中的相关小节。
        :type Limit: int
        :param _InstanceIds: 需要获取的节点实例Id列表。如果为空，表示拉取集群下所有节点实例。
        :type InstanceIds: list of str
        :param _InstanceRole: 节点角色, MASTER, WORKER, ETCD, MASTER_ETCD,ALL, 默认为WORKER。默认为WORKER类型。
        :type InstanceRole: str
        :param _Filters: 过滤条件列表；Name的可选值为nodepool-id、nodepool-instance-type；Name为nodepool-id表示根据节点池id过滤机器，Value的值为具体的节点池id，Name为nodepool-instance-type表示节点加入节点池的方式，Value的值为MANUALLY_ADDED（手动加入节点池）、AUTOSCALING_ADDED（伸缩组扩容方式加入节点池）、ALL（手动加入节点池 和 伸缩组扩容方式加入节点池）
        :type Filters: list of Filter
        """
        self._ClusterId = None
        self._Offset = None
        self._Limit = None
        self._InstanceIds = None
        self._InstanceRole = None
        self._Filters = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceRole(self):
        return self._InstanceRole

    @InstanceRole.setter
    def InstanceRole(self, InstanceRole):
        self._InstanceRole = InstanceRole

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        self._InstanceIds = params.get("InstanceIds")
        self._InstanceRole = params.get("InstanceRole")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterInstancesResponse(AbstractModel):
    """DescribeClusterInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 集群中实例总数
        :type TotalCount: int
        :param _InstanceSet: 集群中实例列表
        :type InstanceSet: list of Instance
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._InstanceSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def InstanceSet(self):
        return self._InstanceSet

    @InstanceSet.setter
    def InstanceSet(self, InstanceSet):
        self._InstanceSet = InstanceSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("InstanceSet") is not None:
            self._InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = Instance()
                obj._deserialize(item)
                self._InstanceSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterKubeconfigRequest(AbstractModel):
    """DescribeClusterKubeconfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _IsExtranet: 默认false 获取内网，是否获取外网访问的kubeconfig
        :type IsExtranet: bool
        """
        self._ClusterId = None
        self._IsExtranet = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def IsExtranet(self):
        return self._IsExtranet

    @IsExtranet.setter
    def IsExtranet(self, IsExtranet):
        self._IsExtranet = IsExtranet


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._IsExtranet = params.get("IsExtranet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterKubeconfigResponse(AbstractModel):
    """DescribeClusterKubeconfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Kubeconfig: 子账户kubeconfig文件，可用于直接访问集群kube-apiserver（入参IsExtranet为false，返回内网访问的kubeconfig，没开内网的情况下server会是一个默认域名；入参IsExtranet为true，返回外网的kubeconfig，没开外网的情况下server会是一个默认域名。默认域名默认不可达，需要自行处理）
        :type Kubeconfig: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Kubeconfig = None
        self._RequestId = None

    @property
    def Kubeconfig(self):
        return self._Kubeconfig

    @Kubeconfig.setter
    def Kubeconfig(self, Kubeconfig):
        self._Kubeconfig = Kubeconfig

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Kubeconfig = params.get("Kubeconfig")
        self._RequestId = params.get("RequestId")


class DescribeClusterLevelAttributeRequest(AbstractModel):
    """DescribeClusterLevelAttribute请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群ID，变配时使用
        :type ClusterID: str
        """
        self._ClusterID = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterLevelAttributeResponse(AbstractModel):
    """DescribeClusterLevelAttribute返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 总数
        :type TotalCount: int
        :param _Items: 集群规模
        :type Items: list of ClusterLevelAttribute
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._Items = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Items(self):
        return self._Items

    @Items.setter
    def Items(self, Items):
        self._Items = Items

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self._Items = []
            for item in params.get("Items"):
                obj = ClusterLevelAttribute()
                obj._deserialize(item)
                self._Items.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterLevelChangeRecordsRequest(AbstractModel):
    """DescribeClusterLevelChangeRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群ID
        :type ClusterID: str
        :param _StartAt: 开始时间
        :type StartAt: str
        :param _EndAt: 结束时间
        :type EndAt: str
        :param _Offset: 偏移量,默认0
        :type Offset: int
        :param _Limit: 最大输出条数，默认20
        :type Limit: int
        """
        self._ClusterID = None
        self._StartAt = None
        self._EndAt = None
        self._Offset = None
        self._Limit = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def StartAt(self):
        return self._StartAt

    @StartAt.setter
    def StartAt(self, StartAt):
        self._StartAt = StartAt

    @property
    def EndAt(self):
        return self._EndAt

    @EndAt.setter
    def EndAt(self, EndAt):
        self._EndAt = EndAt

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        self._StartAt = params.get("StartAt")
        self._EndAt = params.get("EndAt")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterLevelChangeRecordsResponse(AbstractModel):
    """DescribeClusterLevelChangeRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 总数
        :type TotalCount: int
        :param _Items: 集群规模
        :type Items: list of ClusterLevelChangeRecord
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._Items = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Items(self):
        return self._Items

    @Items.setter
    def Items(self, Items):
        self._Items = Items

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self._Items = []
            for item in params.get("Items"):
                obj = ClusterLevelChangeRecord()
                obj._deserialize(item)
                self._Items.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterNodePoolDetailRequest(AbstractModel):
    """DescribeClusterNodePoolDetail请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        """
        self._ClusterId = None
        self._NodePoolId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterNodePoolDetailResponse(AbstractModel):
    """DescribeClusterNodePoolDetail返回参数结构体

    """

    def __init__(self):
        r"""
        :param _NodePool: 节点池详情
        :type NodePool: :class:`tencentcloud.tke.v20180525.models.NodePool`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._NodePool = None
        self._RequestId = None

    @property
    def NodePool(self):
        return self._NodePool

    @NodePool.setter
    def NodePool(self, NodePool):
        self._NodePool = NodePool

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("NodePool") is not None:
            self._NodePool = NodePool()
            self._NodePool._deserialize(params.get("NodePool"))
        self._RequestId = params.get("RequestId")


class DescribeClusterNodePoolsRequest(AbstractModel):
    """DescribeClusterNodePools请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: ClusterId（集群id）
        :type ClusterId: str
        :param _Filters: ·  NodePoolsName
    按照【节点池名】进行过滤。
    类型：String
    必选：否

·  NodePoolsId
    按照【节点池id】进行过滤。
    类型：String
    必选：否

·  tags
    按照【标签键值对】进行过滤。
    类型：String
    必选：否

·  tag:tag-key
    按照【标签键值对】进行过滤。
    类型：String
    必选：否
        :type Filters: list of Filter
        """
        self._ClusterId = None
        self._Filters = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterNodePoolsResponse(AbstractModel):
    """DescribeClusterNodePools返回参数结构体

    """

    def __init__(self):
        r"""
        :param _NodePoolSet: NodePools（节点池列表）
注意：此字段可能返回 null，表示取不到有效值。
        :type NodePoolSet: list of NodePool
        :param _TotalCount: 资源总数
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._NodePoolSet = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def NodePoolSet(self):
        return self._NodePoolSet

    @NodePoolSet.setter
    def NodePoolSet(self, NodePoolSet):
        self._NodePoolSet = NodePoolSet

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("NodePoolSet") is not None:
            self._NodePoolSet = []
            for item in params.get("NodePoolSet"):
                obj = NodePool()
                obj._deserialize(item)
                self._NodePoolSet.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeClusterPendingReleasesRequest(AbstractModel):
    """DescribeClusterPendingReleases请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Limit: 返回数量限制，默认20，最大100
        :type Limit: int
        :param _Offset: 偏移量，默认0
        :type Offset: int
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Limit = None
        self._Offset = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterPendingReleasesResponse(AbstractModel):
    """DescribeClusterPendingReleases返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ReleaseSet: 正在安装中应用列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ReleaseSet: list of PendingRelease
        :param _Limit: 每页返回数量限制
注意：此字段可能返回 null，表示取不到有效值。
        :type Limit: int
        :param _Offset: 页偏移量
注意：此字段可能返回 null，表示取不到有效值。
        :type Offset: int
        :param _Total: 总数量
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ReleaseSet = None
        self._Limit = None
        self._Offset = None
        self._Total = None
        self._RequestId = None

    @property
    def ReleaseSet(self):
        return self._ReleaseSet

    @ReleaseSet.setter
    def ReleaseSet(self, ReleaseSet):
        self._ReleaseSet = ReleaseSet

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ReleaseSet") is not None:
            self._ReleaseSet = []
            for item in params.get("ReleaseSet"):
                obj = PendingRelease()
                obj._deserialize(item)
                self._ReleaseSet.append(obj)
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribeClusterReleaseDetailsRequest(AbstractModel):
    """DescribeClusterReleaseDetails请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用所在命名空间
        :type Namespace: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Name = None
        self._Namespace = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterReleaseDetailsResponse(AbstractModel):
    """DescribeClusterReleaseDetails返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Release: 应用详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Release: :class:`tencentcloud.tke.v20180525.models.ReleaseDetails`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Release = None
        self._RequestId = None

    @property
    def Release(self):
        return self._Release

    @Release.setter
    def Release(self, Release):
        self._Release = Release

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Release") is not None:
            self._Release = ReleaseDetails()
            self._Release._deserialize(params.get("Release"))
        self._RequestId = params.get("RequestId")


class DescribeClusterReleaseHistoryRequest(AbstractModel):
    """DescribeClusterReleaseHistory请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用所在命名空间
        :type Namespace: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Name = None
        self._Namespace = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterReleaseHistoryResponse(AbstractModel):
    """DescribeClusterReleaseHistory返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ReleaseHistorySet: 已安装应用版本历史
注意：此字段可能返回 null，表示取不到有效值。
        :type ReleaseHistorySet: list of ReleaseHistory
        :param _Total: 总数量
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ReleaseHistorySet = None
        self._Total = None
        self._RequestId = None

    @property
    def ReleaseHistorySet(self):
        return self._ReleaseHistorySet

    @ReleaseHistorySet.setter
    def ReleaseHistorySet(self, ReleaseHistorySet):
        self._ReleaseHistorySet = ReleaseHistorySet

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ReleaseHistorySet") is not None:
            self._ReleaseHistorySet = []
            for item in params.get("ReleaseHistorySet"):
                obj = ReleaseHistory()
                obj._deserialize(item)
                self._ReleaseHistorySet.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribeClusterReleasesRequest(AbstractModel):
    """DescribeClusterReleases请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _Limit: 每页数量限制
        :type Limit: int
        :param _Offset: 页偏移量
        :type Offset: int
        :param _ClusterType: 集群类型, 目前支持传入 tke, eks, tkeedge, external 
        :type ClusterType: str
        :param _Namespace: helm Release 安装的namespace
        :type Namespace: str
        :param _ReleaseName: helm Release 的名字
        :type ReleaseName: str
        :param _ChartName: helm Chart 的名字
        :type ChartName: str
        """
        self._ClusterId = None
        self._Limit = None
        self._Offset = None
        self._ClusterType = None
        self._Namespace = None
        self._ReleaseName = None
        self._ChartName = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def ReleaseName(self):
        return self._ReleaseName

    @ReleaseName.setter
    def ReleaseName(self, ReleaseName):
        self._ReleaseName = ReleaseName

    @property
    def ChartName(self):
        return self._ChartName

    @ChartName.setter
    def ChartName(self, ChartName):
        self._ChartName = ChartName


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        self._ClusterType = params.get("ClusterType")
        self._Namespace = params.get("Namespace")
        self._ReleaseName = params.get("ReleaseName")
        self._ChartName = params.get("ChartName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterReleasesResponse(AbstractModel):
    """DescribeClusterReleases返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Limit: 数量限制
注意：此字段可能返回 null，表示取不到有效值。
        :type Limit: int
        :param _Offset: 偏移量
注意：此字段可能返回 null，表示取不到有效值。
        :type Offset: int
        :param _ReleaseSet: 已安装应用列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ReleaseSet: list of Release
        :param _Total: 已安装应用总数量
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Limit = None
        self._Offset = None
        self._ReleaseSet = None
        self._Total = None
        self._RequestId = None

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def ReleaseSet(self):
        return self._ReleaseSet

    @ReleaseSet.setter
    def ReleaseSet(self, ReleaseSet):
        self._ReleaseSet = ReleaseSet

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        if params.get("ReleaseSet") is not None:
            self._ReleaseSet = []
            for item in params.get("ReleaseSet"):
                obj = Release()
                obj._deserialize(item)
                self._ReleaseSet.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribeClusterRouteTablesRequest(AbstractModel):
    """DescribeClusterRouteTables请求参数结构体

    """


class DescribeClusterRouteTablesResponse(AbstractModel):
    """DescribeClusterRouteTables返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param _RouteTableSet: 集群路由表对象。
        :type RouteTableSet: list of RouteTableInfo
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._RouteTableSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RouteTableSet(self):
        return self._RouteTableSet

    @RouteTableSet.setter
    def RouteTableSet(self, RouteTableSet):
        self._RouteTableSet = RouteTableSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("RouteTableSet") is not None:
            self._RouteTableSet = []
            for item in params.get("RouteTableSet"):
                obj = RouteTableInfo()
                obj._deserialize(item)
                self._RouteTableSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterRoutesRequest(AbstractModel):
    """DescribeClusterRoutes请求参数结构体

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param _Filters: 过滤条件,当前只支持按照单个条件GatewayIP进行过滤（可选）
        :type Filters: list of Filter
        """
        self._RouteTableName = None
        self._Filters = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterRoutesResponse(AbstractModel):
    """DescribeClusterRoutes返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param _RouteSet: 集群路由对象。
        :type RouteSet: list of RouteInfo
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._RouteSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RouteSet(self):
        return self._RouteSet

    @RouteSet.setter
    def RouteSet(self, RouteSet):
        self._RouteSet = RouteSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("RouteSet") is not None:
            self._RouteSet = []
            for item in params.get("RouteSet"):
                obj = RouteInfo()
                obj._deserialize(item)
                self._RouteSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterSecurityRequest(AbstractModel):
    """DescribeClusterSecurity请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群 ID，请填写 查询集群列表 接口中返回的 clusterId 字段
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterSecurityResponse(AbstractModel):
    """DescribeClusterSecurity返回参数结构体

    """

    def __init__(self):
        r"""
        :param _UserName: 集群的账号名称
        :type UserName: str
        :param _Password: 集群的访问密码
        :type Password: str
        :param _CertificationAuthority: 集群访问CA证书
        :type CertificationAuthority: str
        :param _ClusterExternalEndpoint: 集群访问的地址
        :type ClusterExternalEndpoint: str
        :param _Domain: 集群访问的域名
        :type Domain: str
        :param _PgwEndpoint: 集群Endpoint地址
        :type PgwEndpoint: str
        :param _SecurityPolicy: 集群访问策略组
注意：此字段可能返回 null，表示取不到有效值。
        :type SecurityPolicy: list of str
        :param _Kubeconfig: 集群Kubeconfig文件
注意：此字段可能返回 null，表示取不到有效值。
        :type Kubeconfig: str
        :param _JnsGwEndpoint: 集群JnsGw的访问地址
注意：此字段可能返回 null，表示取不到有效值。
        :type JnsGwEndpoint: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._UserName = None
        self._Password = None
        self._CertificationAuthority = None
        self._ClusterExternalEndpoint = None
        self._Domain = None
        self._PgwEndpoint = None
        self._SecurityPolicy = None
        self._Kubeconfig = None
        self._JnsGwEndpoint = None
        self._RequestId = None

    @property
    def UserName(self):
        return self._UserName

    @UserName.setter
    def UserName(self, UserName):
        self._UserName = UserName

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def CertificationAuthority(self):
        return self._CertificationAuthority

    @CertificationAuthority.setter
    def CertificationAuthority(self, CertificationAuthority):
        self._CertificationAuthority = CertificationAuthority

    @property
    def ClusterExternalEndpoint(self):
        return self._ClusterExternalEndpoint

    @ClusterExternalEndpoint.setter
    def ClusterExternalEndpoint(self, ClusterExternalEndpoint):
        self._ClusterExternalEndpoint = ClusterExternalEndpoint

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def PgwEndpoint(self):
        return self._PgwEndpoint

    @PgwEndpoint.setter
    def PgwEndpoint(self, PgwEndpoint):
        self._PgwEndpoint = PgwEndpoint

    @property
    def SecurityPolicy(self):
        return self._SecurityPolicy

    @SecurityPolicy.setter
    def SecurityPolicy(self, SecurityPolicy):
        self._SecurityPolicy = SecurityPolicy

    @property
    def Kubeconfig(self):
        return self._Kubeconfig

    @Kubeconfig.setter
    def Kubeconfig(self, Kubeconfig):
        self._Kubeconfig = Kubeconfig

    @property
    def JnsGwEndpoint(self):
        return self._JnsGwEndpoint

    @JnsGwEndpoint.setter
    def JnsGwEndpoint(self, JnsGwEndpoint):
        self._JnsGwEndpoint = JnsGwEndpoint

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._UserName = params.get("UserName")
        self._Password = params.get("Password")
        self._CertificationAuthority = params.get("CertificationAuthority")
        self._ClusterExternalEndpoint = params.get("ClusterExternalEndpoint")
        self._Domain = params.get("Domain")
        self._PgwEndpoint = params.get("PgwEndpoint")
        self._SecurityPolicy = params.get("SecurityPolicy")
        self._Kubeconfig = params.get("Kubeconfig")
        self._JnsGwEndpoint = params.get("JnsGwEndpoint")
        self._RequestId = params.get("RequestId")


class DescribeClusterStatusRequest(AbstractModel):
    """DescribeClusterStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: 集群ID列表，不传默认拉取所有集群
        :type ClusterIds: list of str
        """
        self._ClusterIds = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterStatusResponse(AbstractModel):
    """DescribeClusterStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterStatusSet: 集群状态列表
        :type ClusterStatusSet: list of ClusterStatus
        :param _TotalCount: 集群个数
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterStatusSet = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def ClusterStatusSet(self):
        return self._ClusterStatusSet

    @ClusterStatusSet.setter
    def ClusterStatusSet(self, ClusterStatusSet):
        self._ClusterStatusSet = ClusterStatusSet

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ClusterStatusSet") is not None:
            self._ClusterStatusSet = []
            for item in params.get("ClusterStatusSet"):
                obj = ClusterStatus()
                obj._deserialize(item)
                self._ClusterStatusSet.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeClusterVirtualNodePoolsRequest(AbstractModel):
    """DescribeClusterVirtualNodePools请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterVirtualNodePoolsResponse(AbstractModel):
    """DescribeClusterVirtualNodePools返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 节点池总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param _NodePoolSet: 虚拟节点池列表
注意：此字段可能返回 null，表示取不到有效值。
        :type NodePoolSet: list of VirtualNodePool
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._NodePoolSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def NodePoolSet(self):
        return self._NodePoolSet

    @NodePoolSet.setter
    def NodePoolSet(self, NodePoolSet):
        self._NodePoolSet = NodePoolSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("NodePoolSet") is not None:
            self._NodePoolSet = []
            for item in params.get("NodePoolSet"):
                obj = VirtualNodePool()
                obj._deserialize(item)
                self._NodePoolSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeClusterVirtualNodeRequest(AbstractModel):
    """DescribeClusterVirtualNode请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodePoolId: 节点池ID
        :type NodePoolId: str
        :param _NodeNames: 节点名称
        :type NodeNames: list of str
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._NodeNames = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def NodeNames(self):
        return self._NodeNames

    @NodeNames.setter
    def NodeNames(self, NodeNames):
        self._NodeNames = NodeNames


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._NodeNames = params.get("NodeNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterVirtualNodeResponse(AbstractModel):
    """DescribeClusterVirtualNode返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Nodes: 节点列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Nodes: list of VirtualNode
        :param _TotalCount: 节点总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Nodes = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def Nodes(self):
        return self._Nodes

    @Nodes.setter
    def Nodes(self, Nodes):
        self._Nodes = Nodes

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Nodes") is not None:
            self._Nodes = []
            for item in params.get("Nodes"):
                obj = VirtualNode()
                obj._deserialize(item)
                self._Nodes.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeClustersRequest(AbstractModel):
    """DescribeClusters请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: 集群ID列表(为空时，
表示获取账号下所有集群)
        :type ClusterIds: list of str
        :param _Offset: 偏移量,默认0
        :type Offset: int
        :param _Limit: 最大输出条数，默认20，最大为100
        :type Limit: int
        :param _Filters: ·  ClusterName
    按照【集群名】进行过滤。
    类型：String
    必选：否

·  ClusterType
    按照【集群类型】进行过滤。
    类型：String
    必选：否

·  ClusterStatus
    按照【集群状态】进行过滤。
    类型：String
    必选：否

·  Tags
    按照【标签键值对】进行过滤。
    类型：String
    必选：否

·  vpc-id
    按照【VPC】进行过滤。
    类型：String
    必选：否

·  tag-key
    按照【标签键】进行过滤。
    类型：String
    必选：否

·  tag-value
    按照【标签值】进行过滤。
    类型：String
    必选：否

·  tag:tag-key
    按照【标签键值对】进行过滤。
    类型：String
    必选：否
        :type Filters: list of Filter
        :param _ClusterType: 集群类型，例如：MANAGED_CLUSTER
        :type ClusterType: str
        """
        self._ClusterIds = None
        self._Offset = None
        self._Limit = None
        self._Filters = None
        self._ClusterType = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClustersResponse(AbstractModel):
    """DescribeClusters返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 集群总个数
        :type TotalCount: int
        :param _Clusters: 集群信息列表
        :type Clusters: list of Cluster
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._Clusters = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Clusters(self):
        return self._Clusters

    @Clusters.setter
    def Clusters(self, Clusters):
        self._Clusters = Clusters

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Clusters") is not None:
            self._Clusters = []
            for item in params.get("Clusters"):
                obj = Cluster()
                obj._deserialize(item)
                self._Clusters.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeECMInstancesRequest(AbstractModel):
    """DescribeECMInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群id
        :type ClusterID: str
        :param _Filters: 过滤条件
仅支持ecm-id过滤
        :type Filters: list of Filter
        """
        self._ClusterID = None
        self._Filters = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeECMInstancesResponse(AbstractModel):
    """DescribeECMInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 返回的实例相关信息列表的长度
        :type TotalCount: int
        :param _InstanceInfoSet: 返回的实例相关信息列表
        :type InstanceInfoSet: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._InstanceInfoSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def InstanceInfoSet(self):
        return self._InstanceInfoSet

    @InstanceInfoSet.setter
    def InstanceInfoSet(self, InstanceInfoSet):
        self._InstanceInfoSet = InstanceInfoSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        self._InstanceInfoSet = params.get("InstanceInfoSet")
        self._RequestId = params.get("RequestId")


class DescribeEKSClusterCredentialRequest(AbstractModel):
    """DescribeEKSClusterCredential请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群Id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEKSClusterCredentialResponse(AbstractModel):
    """DescribeEKSClusterCredential返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Addresses: 集群的接入地址信息
        :type Addresses: list of IPAddress
        :param _Credential: 集群的认证信息（token只有请求是主账号才返回，子账户请使用返回的kubeconfig）
        :type Credential: :class:`tencentcloud.tke.v20180525.models.ClusterCredential`
        :param _PublicLB: 集群的公网访问信息
        :type PublicLB: :class:`tencentcloud.tke.v20180525.models.ClusterPublicLB`
        :param _InternalLB: 集群的内网访问信息
        :type InternalLB: :class:`tencentcloud.tke.v20180525.models.ClusterInternalLB`
        :param _ProxyLB: 标记是否新的内外网功能
        :type ProxyLB: bool
        :param _Kubeconfig: 连接用户集群k8s 的Config
        :type Kubeconfig: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Addresses = None
        self._Credential = None
        self._PublicLB = None
        self._InternalLB = None
        self._ProxyLB = None
        self._Kubeconfig = None
        self._RequestId = None

    @property
    def Addresses(self):
        return self._Addresses

    @Addresses.setter
    def Addresses(self, Addresses):
        self._Addresses = Addresses

    @property
    def Credential(self):
        return self._Credential

    @Credential.setter
    def Credential(self, Credential):
        self._Credential = Credential

    @property
    def PublicLB(self):
        return self._PublicLB

    @PublicLB.setter
    def PublicLB(self, PublicLB):
        self._PublicLB = PublicLB

    @property
    def InternalLB(self):
        return self._InternalLB

    @InternalLB.setter
    def InternalLB(self, InternalLB):
        self._InternalLB = InternalLB

    @property
    def ProxyLB(self):
        return self._ProxyLB

    @ProxyLB.setter
    def ProxyLB(self, ProxyLB):
        self._ProxyLB = ProxyLB

    @property
    def Kubeconfig(self):
        return self._Kubeconfig

    @Kubeconfig.setter
    def Kubeconfig(self, Kubeconfig):
        self._Kubeconfig = Kubeconfig

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Addresses") is not None:
            self._Addresses = []
            for item in params.get("Addresses"):
                obj = IPAddress()
                obj._deserialize(item)
                self._Addresses.append(obj)
        if params.get("Credential") is not None:
            self._Credential = ClusterCredential()
            self._Credential._deserialize(params.get("Credential"))
        if params.get("PublicLB") is not None:
            self._PublicLB = ClusterPublicLB()
            self._PublicLB._deserialize(params.get("PublicLB"))
        if params.get("InternalLB") is not None:
            self._InternalLB = ClusterInternalLB()
            self._InternalLB._deserialize(params.get("InternalLB"))
        self._ProxyLB = params.get("ProxyLB")
        self._Kubeconfig = params.get("Kubeconfig")
        self._RequestId = params.get("RequestId")


class DescribeEKSClustersRequest(AbstractModel):
    """DescribeEKSClusters请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: 集群ID列表(为空时，
表示获取账号下所有集群)
        :type ClusterIds: list of str
        :param _Offset: 偏移量,默认0
        :type Offset: int
        :param _Limit: 最大输出条数，默认20
        :type Limit: int
        :param _Filters: 过滤条件,当前只支持按照单个条件ClusterName进行过滤
        :type Filters: list of Filter
        """
        self._ClusterIds = None
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEKSClustersResponse(AbstractModel):
    """DescribeEKSClusters返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 集群总个数
        :type TotalCount: int
        :param _Clusters: 集群信息列表
        :type Clusters: list of EksCluster
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._Clusters = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Clusters(self):
        return self._Clusters

    @Clusters.setter
    def Clusters(self, Clusters):
        self._Clusters = Clusters

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Clusters") is not None:
            self._Clusters = []
            for item in params.get("Clusters"):
                obj = EksCluster()
                obj._deserialize(item)
                self._Clusters.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeEKSContainerInstanceEventRequest(AbstractModel):
    """DescribeEKSContainerInstanceEvent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiId: 容器实例id
        :type EksCiId: str
        :param _Limit: 最大事件数量。默认为50，最大取值100。
        :type Limit: int
        """
        self._EksCiId = None
        self._Limit = None

    @property
    def EksCiId(self):
        return self._EksCiId

    @EksCiId.setter
    def EksCiId(self, EksCiId):
        self._EksCiId = EksCiId

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._EksCiId = params.get("EksCiId")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEKSContainerInstanceEventResponse(AbstractModel):
    """DescribeEKSContainerInstanceEvent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Events: 事件集合
        :type Events: list of Event
        :param _EksCiId: 容器实例id
        :type EksCiId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Events = None
        self._EksCiId = None
        self._RequestId = None

    @property
    def Events(self):
        return self._Events

    @Events.setter
    def Events(self, Events):
        self._Events = Events

    @property
    def EksCiId(self):
        return self._EksCiId

    @EksCiId.setter
    def EksCiId(self, EksCiId):
        self._EksCiId = EksCiId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Events") is not None:
            self._Events = []
            for item in params.get("Events"):
                obj = Event()
                obj._deserialize(item)
                self._Events.append(obj)
        self._EksCiId = params.get("EksCiId")
        self._RequestId = params.get("RequestId")


class DescribeEKSContainerInstanceRegionsRequest(AbstractModel):
    """DescribeEKSContainerInstanceRegions请求参数结构体

    """


class DescribeEKSContainerInstanceRegionsResponse(AbstractModel):
    """DescribeEKSContainerInstanceRegions返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Regions: EKS Container Instance支持的地域信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Regions: list of EksCiRegionInfo
        :param _TotalCount: 总数
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Regions = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def Regions(self):
        return self._Regions

    @Regions.setter
    def Regions(self, Regions):
        self._Regions = Regions

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Regions") is not None:
            self._Regions = []
            for item in params.get("Regions"):
                obj = EksCiRegionInfo()
                obj._deserialize(item)
                self._Regions.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeEKSContainerInstancesRequest(AbstractModel):
    """DescribeEKSContainerInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Limit: 限定此次返回资源的数量。如果不设定，默认返回20，最大不能超过100
        :type Limit: int
        :param _Offset: 偏移量,默认0
        :type Offset: int
        :param _Filters: 过滤条件，可条件：
(1)实例名称
KeyName: eks-ci-name
类型：String

(2)实例状态
KeyName: status
类型：String
可选值："Pending", "Running", "Succeeded", "Failed"

(3)内网ip
KeyName: private-ip
类型：String

(4)EIP地址
KeyName: eip-address
类型：String

(5)VpcId
KeyName: vpc-id
类型：String
        :type Filters: list of Filter
        :param _EksCiIds: 容器实例 ID 数组
        :type EksCiIds: list of str
        """
        self._Limit = None
        self._Offset = None
        self._Filters = None
        self._EksCiIds = None

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters

    @property
    def EksCiIds(self):
        return self._EksCiIds

    @EksCiIds.setter
    def EksCiIds(self, EksCiIds):
        self._EksCiIds = EksCiIds


    def _deserialize(self, params):
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        self._EksCiIds = params.get("EksCiIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEKSContainerInstancesResponse(AbstractModel):
    """DescribeEKSContainerInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 容器组总数
        :type TotalCount: int
        :param _EksCis: 容器组列表
        :type EksCis: list of EksCi
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._EksCis = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def EksCis(self):
        return self._EksCis

    @EksCis.setter
    def EksCis(self, EksCis):
        self._EksCis = EksCis

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("EksCis") is not None:
            self._EksCis = []
            for item in params.get("EksCis"):
                obj = EksCi()
                obj._deserialize(item)
                self._EksCis.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeEdgeAvailableExtraArgsRequest(AbstractModel):
    """DescribeEdgeAvailableExtraArgs请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterVersion: 集群版本
        :type ClusterVersion: str
        """
        self._ClusterVersion = None

    @property
    def ClusterVersion(self):
        return self._ClusterVersion

    @ClusterVersion.setter
    def ClusterVersion(self, ClusterVersion):
        self._ClusterVersion = ClusterVersion


    def _deserialize(self, params):
        self._ClusterVersion = params.get("ClusterVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEdgeAvailableExtraArgsResponse(AbstractModel):
    """DescribeEdgeAvailableExtraArgs返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterVersion: 集群版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterVersion: str
        :param _AvailableExtraArgs: 可用的自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type AvailableExtraArgs: :class:`tencentcloud.tke.v20180525.models.EdgeAvailableExtraArgs`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterVersion = None
        self._AvailableExtraArgs = None
        self._RequestId = None

    @property
    def ClusterVersion(self):
        return self._ClusterVersion

    @ClusterVersion.setter
    def ClusterVersion(self, ClusterVersion):
        self._ClusterVersion = ClusterVersion

    @property
    def AvailableExtraArgs(self):
        return self._AvailableExtraArgs

    @AvailableExtraArgs.setter
    def AvailableExtraArgs(self, AvailableExtraArgs):
        self._AvailableExtraArgs = AvailableExtraArgs

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ClusterVersion = params.get("ClusterVersion")
        if params.get("AvailableExtraArgs") is not None:
            self._AvailableExtraArgs = EdgeAvailableExtraArgs()
            self._AvailableExtraArgs._deserialize(params.get("AvailableExtraArgs"))
        self._RequestId = params.get("RequestId")


class DescribeEdgeCVMInstancesRequest(AbstractModel):
    """DescribeEdgeCVMInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群id
        :type ClusterID: str
        :param _Filters: 过滤条件
仅支持cvm-id过滤
        :type Filters: list of Filter
        """
        self._ClusterID = None
        self._Filters = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEdgeCVMInstancesResponse(AbstractModel):
    """DescribeEdgeCVMInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 返回的实例相关信息列表的长度
        :type TotalCount: int
        :param _InstanceInfoSet: 返回的实例相关信息列表
        :type InstanceInfoSet: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._InstanceInfoSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def InstanceInfoSet(self):
        return self._InstanceInfoSet

    @InstanceInfoSet.setter
    def InstanceInfoSet(self, InstanceInfoSet):
        self._InstanceInfoSet = InstanceInfoSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        self._InstanceInfoSet = params.get("InstanceInfoSet")
        self._RequestId = params.get("RequestId")


class DescribeEdgeClusterExtraArgsRequest(AbstractModel):
    """DescribeEdgeClusterExtraArgs请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEdgeClusterExtraArgsResponse(AbstractModel):
    """DescribeEdgeClusterExtraArgs返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterExtraArgs: 集群自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterExtraArgs: :class:`tencentcloud.tke.v20180525.models.EdgeClusterExtraArgs`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ClusterExtraArgs = None
        self._RequestId = None

    @property
    def ClusterExtraArgs(self):
        return self._ClusterExtraArgs

    @ClusterExtraArgs.setter
    def ClusterExtraArgs(self, ClusterExtraArgs):
        self._ClusterExtraArgs = ClusterExtraArgs

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ClusterExtraArgs") is not None:
            self._ClusterExtraArgs = EdgeClusterExtraArgs()
            self._ClusterExtraArgs._deserialize(params.get("ClusterExtraArgs"))
        self._RequestId = params.get("RequestId")


class DescribeEdgeClusterInstancesRequest(AbstractModel):
    """DescribeEdgeClusterInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterID: 集群id
        :type ClusterID: str
        :param _Limit: 查询总数
        :type Limit: int
        :param _Offset: 偏移量
        :type Offset: int
        :param _Filters: 过滤条件，仅支持NodeName过滤
        :type Filters: list of Filter
        """
        self._ClusterID = None
        self._Limit = None
        self._Offset = None
        self._Filters = None

    @property
    def ClusterID(self):
        return self._ClusterID

    @ClusterID.setter
    def ClusterID(self, ClusterID):
        self._ClusterID = ClusterID

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterID = params.get("ClusterID")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEdgeClusterInstancesResponse(AbstractModel):
    """DescribeEdgeClusterInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 该集群总数
        :type TotalCount: int
        :param _InstanceInfoSet: 节点信息集合
        :type InstanceInfoSet: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._InstanceInfoSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def InstanceInfoSet(self):
        return self._InstanceInfoSet

    @InstanceInfoSet.setter
    def InstanceInfoSet(self, InstanceInfoSet):
        self._InstanceInfoSet = InstanceInfoSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        self._InstanceInfoSet = params.get("InstanceInfoSet")
        self._RequestId = params.get("RequestId")


class DescribeEdgeClusterUpgradeInfoRequest(AbstractModel):
    """DescribeEdgeClusterUpgradeInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _EdgeVersion: 要升级到的TKEEdge版本
        :type EdgeVersion: str
        """
        self._ClusterId = None
        self._EdgeVersion = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def EdgeVersion(self):
        return self._EdgeVersion

    @EdgeVersion.setter
    def EdgeVersion(self, EdgeVersion):
        self._EdgeVersion = EdgeVersion


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._EdgeVersion = params.get("EdgeVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEdgeClusterUpgradeInfoResponse(AbstractModel):
    """DescribeEdgeClusterUpgradeInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ComponentVersion: 可升级的集群组件和
注意：此字段可能返回 null，表示取不到有效值。
        :type ComponentVersion: str
        :param _EdgeVersionCurrent: 边缘集群当前版本
注意：此字段可能返回 null，表示取不到有效值。
        :type EdgeVersionCurrent: str
        :param _RegistryPrefix: 边缘组件镜像仓库地址前缀，包含域名和命名空间
注意：此字段可能返回 null，表示取不到有效值。
        :type RegistryPrefix: str
        :param _ClusterUpgradeStatus: 集群升级状态，可能值：running、updating、failed
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterUpgradeStatus: str
        :param _ClusterUpgradeStatusReason: 集群升级中状态或者失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterUpgradeStatusReason: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ComponentVersion = None
        self._EdgeVersionCurrent = None
        self._RegistryPrefix = None
        self._ClusterUpgradeStatus = None
        self._ClusterUpgradeStatusReason = None
        self._RequestId = None

    @property
    def ComponentVersion(self):
        return self._ComponentVersion

    @ComponentVersion.setter
    def ComponentVersion(self, ComponentVersion):
        self._ComponentVersion = ComponentVersion

    @property
    def EdgeVersionCurrent(self):
        return self._EdgeVersionCurrent

    @EdgeVersionCurrent.setter
    def EdgeVersionCurrent(self, EdgeVersionCurrent):
        self._EdgeVersionCurrent = EdgeVersionCurrent

    @property
    def RegistryPrefix(self):
        return self._RegistryPrefix

    @RegistryPrefix.setter
    def RegistryPrefix(self, RegistryPrefix):
        self._RegistryPrefix = RegistryPrefix

    @property
    def ClusterUpgradeStatus(self):
        return self._ClusterUpgradeStatus

    @ClusterUpgradeStatus.setter
    def ClusterUpgradeStatus(self, ClusterUpgradeStatus):
        self._ClusterUpgradeStatus = ClusterUpgradeStatus

    @property
    def ClusterUpgradeStatusReason(self):
        return self._ClusterUpgradeStatusReason

    @ClusterUpgradeStatusReason.setter
    def ClusterUpgradeStatusReason(self, ClusterUpgradeStatusReason):
        self._ClusterUpgradeStatusReason = ClusterUpgradeStatusReason

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ComponentVersion = params.get("ComponentVersion")
        self._EdgeVersionCurrent = params.get("EdgeVersionCurrent")
        self._RegistryPrefix = params.get("RegistryPrefix")
        self._ClusterUpgradeStatus = params.get("ClusterUpgradeStatus")
        self._ClusterUpgradeStatusReason = params.get("ClusterUpgradeStatusReason")
        self._RequestId = params.get("RequestId")


class DescribeEdgeLogSwitchesRequest(AbstractModel):
    """DescribeEdgeLogSwitches请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: 集群ID列表
        :type ClusterIds: list of str
        """
        self._ClusterIds = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEdgeLogSwitchesResponse(AbstractModel):
    """DescribeEdgeLogSwitches返回参数结构体

    """

    def __init__(self):
        r"""
        :param _SwitchSet: 集群日志开关集合
注意：此字段可能返回 null，表示取不到有效值。
        :type SwitchSet: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._SwitchSet = None
        self._RequestId = None

    @property
    def SwitchSet(self):
        return self._SwitchSet

    @SwitchSet.setter
    def SwitchSet(self, SwitchSet):
        self._SwitchSet = SwitchSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._SwitchSet = params.get("SwitchSet")
        self._RequestId = params.get("RequestId")


class DescribeEksContainerInstanceLogRequest(AbstractModel):
    """DescribeEksContainerInstanceLog请求参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiId: Eks Container Instance Id，即容器实例Id
        :type EksCiId: str
        :param _ContainerName: 容器名称，单容器的实例可选填。如果为多容器实例，请指定容器名称。
        :type ContainerName: str
        :param _Tail: 返回最新日志行数，默认500，最大2000。日志内容最大返回 1M 数据。
        :type Tail: int
        :param _StartTime: UTC时间，RFC3339标准
        :type StartTime: str
        :param _Previous: 是否是查上一个容器（如果容器退出重启了）
        :type Previous: bool
        :param _SinceSeconds: 查询最近多少秒内的日志
        :type SinceSeconds: int
        :param _LimitBytes: 日志总大小限制
        :type LimitBytes: int
        """
        self._EksCiId = None
        self._ContainerName = None
        self._Tail = None
        self._StartTime = None
        self._Previous = None
        self._SinceSeconds = None
        self._LimitBytes = None

    @property
    def EksCiId(self):
        return self._EksCiId

    @EksCiId.setter
    def EksCiId(self, EksCiId):
        self._EksCiId = EksCiId

    @property
    def ContainerName(self):
        return self._ContainerName

    @ContainerName.setter
    def ContainerName(self, ContainerName):
        self._ContainerName = ContainerName

    @property
    def Tail(self):
        return self._Tail

    @Tail.setter
    def Tail(self, Tail):
        self._Tail = Tail

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def Previous(self):
        return self._Previous

    @Previous.setter
    def Previous(self, Previous):
        self._Previous = Previous

    @property
    def SinceSeconds(self):
        return self._SinceSeconds

    @SinceSeconds.setter
    def SinceSeconds(self, SinceSeconds):
        self._SinceSeconds = SinceSeconds

    @property
    def LimitBytes(self):
        return self._LimitBytes

    @LimitBytes.setter
    def LimitBytes(self, LimitBytes):
        self._LimitBytes = LimitBytes


    def _deserialize(self, params):
        self._EksCiId = params.get("EksCiId")
        self._ContainerName = params.get("ContainerName")
        self._Tail = params.get("Tail")
        self._StartTime = params.get("StartTime")
        self._Previous = params.get("Previous")
        self._SinceSeconds = params.get("SinceSeconds")
        self._LimitBytes = params.get("LimitBytes")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEksContainerInstanceLogResponse(AbstractModel):
    """DescribeEksContainerInstanceLog返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ContainerName: 容器名称
        :type ContainerName: str
        :param _LogContent: 日志内容
        :type LogContent: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ContainerName = None
        self._LogContent = None
        self._RequestId = None

    @property
    def ContainerName(self):
        return self._ContainerName

    @ContainerName.setter
    def ContainerName(self, ContainerName):
        self._ContainerName = ContainerName

    @property
    def LogContent(self):
        return self._LogContent

    @LogContent.setter
    def LogContent(self, LogContent):
        self._LogContent = LogContent

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ContainerName = params.get("ContainerName")
        self._LogContent = params.get("LogContent")
        self._RequestId = params.get("RequestId")


class DescribeEnableVpcCniProgressRequest(AbstractModel):
    """DescribeEnableVpcCniProgress请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 开启vpc-cni的集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEnableVpcCniProgressResponse(AbstractModel):
    """DescribeEnableVpcCniProgress返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 任务进度的描述：Running/Succeed/Failed
        :type Status: str
        :param _ErrorMessage: 当任务进度为Failed时，对任务状态的进一步描述，例如IPAMD组件安装失败
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMessage: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._ErrorMessage = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ErrorMessage(self):
        return self._ErrorMessage

    @ErrorMessage.setter
    def ErrorMessage(self, ErrorMessage):
        self._ErrorMessage = ErrorMessage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        self._ErrorMessage = params.get("ErrorMessage")
        self._RequestId = params.get("RequestId")


class DescribeEncryptionStatusRequest(AbstractModel):
    """DescribeEncryptionStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEncryptionStatusResponse(AbstractModel):
    """DescribeEncryptionStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 加密状态
        :type Status: str
        :param _ErrorMsg: 加密错误信息
        :type ErrorMsg: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._ErrorMsg = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ErrorMsg(self):
        return self._ErrorMsg

    @ErrorMsg.setter
    def ErrorMsg(self, ErrorMsg):
        self._ErrorMsg = ErrorMsg

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        self._ErrorMsg = params.get("ErrorMsg")
        self._RequestId = params.get("RequestId")


class DescribeExistedInstancesRequest(AbstractModel):
    """DescribeExistedInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群 ID，请填写查询集群列表 接口中返回的 ClusterId 字段（仅通过ClusterId获取需要过滤条件中的VPCID。节点状态比较时会使用该地域下所有集群中的节点进行比较。参数不支持同时指定InstanceIds和ClusterId。
        :type ClusterId: str
        :param _InstanceIds: 按照一个或者多个实例ID查询。实例ID形如：ins-xxxxxxxx。（此参数的具体格式可参考API简介的id.N一节）。每次请求的实例的上限为100。参数不支持同时指定InstanceIds和Filters。
        :type InstanceIds: list of str
        :param _Filters: 过滤条件,字段和详见[CVM查询实例](https://cloud.tencent.com/document/api/213/15728)如果设置了ClusterId，会附加集群的VPCID作为查询字段，在此情况下如果在Filter中指定了"vpc-id"作为过滤字段，指定的VPCID必须与集群的VPCID相同。
        :type Filters: list of Filter
        :param _VagueIpAddress: 实例IP进行过滤(同时支持内网IP和外网IP)
        :type VagueIpAddress: str
        :param _VagueInstanceName: 实例名称进行过滤
        :type VagueInstanceName: str
        :param _Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API [简介](https://cloud.tencent.com/document/api/213/15688)中的相关小节。
        :type Offset: int
        :param _Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API [简介](https://cloud.tencent.com/document/api/213/15688)中的相关小节。
        :type Limit: int
        :param _IpAddresses: 根据多个实例IP进行过滤
        :type IpAddresses: list of str
        """
        self._ClusterId = None
        self._InstanceIds = None
        self._Filters = None
        self._VagueIpAddress = None
        self._VagueInstanceName = None
        self._Offset = None
        self._Limit = None
        self._IpAddresses = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters

    @property
    def VagueIpAddress(self):
        return self._VagueIpAddress

    @VagueIpAddress.setter
    def VagueIpAddress(self, VagueIpAddress):
        self._VagueIpAddress = VagueIpAddress

    @property
    def VagueInstanceName(self):
        return self._VagueInstanceName

    @VagueInstanceName.setter
    def VagueInstanceName(self, VagueInstanceName):
        self._VagueInstanceName = VagueInstanceName

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def IpAddresses(self):
        return self._IpAddresses

    @IpAddresses.setter
    def IpAddresses(self, IpAddresses):
        self._IpAddresses = IpAddresses


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._InstanceIds = params.get("InstanceIds")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        self._VagueIpAddress = params.get("VagueIpAddress")
        self._VagueInstanceName = params.get("VagueInstanceName")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        self._IpAddresses = params.get("IpAddresses")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeExistedInstancesResponse(AbstractModel):
    """DescribeExistedInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ExistedInstanceSet: 已经存在的实例信息数组。
注意：此字段可能返回 null，表示取不到有效值。
        :type ExistedInstanceSet: list of ExistedInstance
        :param _TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ExistedInstanceSet = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def ExistedInstanceSet(self):
        return self._ExistedInstanceSet

    @ExistedInstanceSet.setter
    def ExistedInstanceSet(self, ExistedInstanceSet):
        self._ExistedInstanceSet = ExistedInstanceSet

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ExistedInstanceSet") is not None:
            self._ExistedInstanceSet = []
            for item in params.get("ExistedInstanceSet"):
                obj = ExistedInstance()
                obj._deserialize(item)
                self._ExistedInstanceSet.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeExternalClusterSpecRequest(AbstractModel):
    """DescribeExternalClusterSpec请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 注册集群ID
        :type ClusterId: str
        :param _IsExtranet: 默认false 获取内网，是否获取外网版注册命令
        :type IsExtranet: bool
        :param _IsRefreshExpirationTime: 默认false 不刷新有效时间 ，true刷新有效时间
        :type IsRefreshExpirationTime: bool
        """
        self._ClusterId = None
        self._IsExtranet = None
        self._IsRefreshExpirationTime = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def IsExtranet(self):
        return self._IsExtranet

    @IsExtranet.setter
    def IsExtranet(self, IsExtranet):
        self._IsExtranet = IsExtranet

    @property
    def IsRefreshExpirationTime(self):
        return self._IsRefreshExpirationTime

    @IsRefreshExpirationTime.setter
    def IsRefreshExpirationTime(self, IsRefreshExpirationTime):
        self._IsRefreshExpirationTime = IsRefreshExpirationTime


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._IsExtranet = params.get("IsExtranet")
        self._IsRefreshExpirationTime = params.get("IsRefreshExpirationTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeExternalClusterSpecResponse(AbstractModel):
    """DescribeExternalClusterSpec返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Spec: 导入第三方集群YAML定义
        :type Spec: str
        :param _Expiration: agent.yaml文件过期时间字符串，时区UTC
        :type Expiration: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Spec = None
        self._Expiration = None
        self._RequestId = None

    @property
    def Spec(self):
        return self._Spec

    @Spec.setter
    def Spec(self, Spec):
        self._Spec = Spec

    @property
    def Expiration(self):
        return self._Expiration

    @Expiration.setter
    def Expiration(self, Expiration):
        self._Expiration = Expiration

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Spec = params.get("Spec")
        self._Expiration = params.get("Expiration")
        self._RequestId = params.get("RequestId")


class DescribeImageCachesRequest(AbstractModel):
    """DescribeImageCaches请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ImageCacheIds: 镜像缓存Id数组
        :type ImageCacheIds: list of str
        :param _ImageCacheNames: 镜像缓存名称数组
        :type ImageCacheNames: list of str
        :param _Limit: 限定此次返回资源的数量。如果不设定，默认返回20，最大不能超过50
        :type Limit: int
        :param _Offset: 偏移量,默认0
        :type Offset: int
        :param _Filters: 过滤条件，可选条件：
(1)实例名称
KeyName: image-cache-name
类型：String
        :type Filters: list of Filter
        """
        self._ImageCacheIds = None
        self._ImageCacheNames = None
        self._Limit = None
        self._Offset = None
        self._Filters = None

    @property
    def ImageCacheIds(self):
        return self._ImageCacheIds

    @ImageCacheIds.setter
    def ImageCacheIds(self, ImageCacheIds):
        self._ImageCacheIds = ImageCacheIds

    @property
    def ImageCacheNames(self):
        return self._ImageCacheNames

    @ImageCacheNames.setter
    def ImageCacheNames(self, ImageCacheNames):
        self._ImageCacheNames = ImageCacheNames

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ImageCacheIds = params.get("ImageCacheIds")
        self._ImageCacheNames = params.get("ImageCacheNames")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeImageCachesResponse(AbstractModel):
    """DescribeImageCaches返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 镜像缓存总数
        :type TotalCount: int
        :param _ImageCaches: 镜像缓存信息列表
        :type ImageCaches: list of ImageCache
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._ImageCaches = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def ImageCaches(self):
        return self._ImageCaches

    @ImageCaches.setter
    def ImageCaches(self, ImageCaches):
        self._ImageCaches = ImageCaches

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("ImageCaches") is not None:
            self._ImageCaches = []
            for item in params.get("ImageCaches"):
                obj = ImageCache()
                obj._deserialize(item)
                self._ImageCaches.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeImagesRequest(AbstractModel):
    """DescribeImages请求参数结构体

    """


class DescribeImagesResponse(AbstractModel):
    """DescribeImages返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 镜像数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param _ImageInstanceSet: 镜像信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageInstanceSet: list of ImageInstance
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._ImageInstanceSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def ImageInstanceSet(self):
        return self._ImageInstanceSet

    @ImageInstanceSet.setter
    def ImageInstanceSet(self, ImageInstanceSet):
        self._ImageInstanceSet = ImageInstanceSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("ImageInstanceSet") is not None:
            self._ImageInstanceSet = []
            for item in params.get("ImageInstanceSet"):
                obj = ImageInstance()
                obj._deserialize(item)
                self._ImageInstanceSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribePrometheusAgentInstancesRequest(AbstractModel):
    """DescribePrometheusAgentInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
可以是tke, eks, edge的集群id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusAgentInstancesResponse(AbstractModel):
    """DescribePrometheusAgentInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Instances: 关联该集群的实例列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Instances: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Instances = None
        self._RequestId = None

    @property
    def Instances(self):
        return self._Instances

    @Instances.setter
    def Instances(self, Instances):
        self._Instances = Instances

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Instances = params.get("Instances")
        self._RequestId = params.get("RequestId")


class DescribePrometheusAgentsRequest(AbstractModel):
    """DescribePrometheusAgents请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Offset: 用于分页
        :type Offset: int
        :param _Limit: 用于分页
        :type Limit: int
        """
        self._InstanceId = None
        self._Offset = None
        self._Limit = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusAgentsResponse(AbstractModel):
    """DescribePrometheusAgents返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Agents: 被关联集群信息
        :type Agents: list of PrometheusAgentOverview
        :param _Total: 被关联集群总量
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Agents = None
        self._Total = None
        self._RequestId = None

    @property
    def Agents(self):
        return self._Agents

    @Agents.setter
    def Agents(self, Agents):
        self._Agents = Agents

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Agents") is not None:
            self._Agents = []
            for item in params.get("Agents"):
                obj = PrometheusAgentOverview()
                obj._deserialize(item)
                self._Agents.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusAlertHistoryRequest(AbstractModel):
    """DescribePrometheusAlertHistory请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _RuleName: 告警名称
        :type RuleName: str
        :param _StartTime: 开始时间
        :type StartTime: str
        :param _EndTime: 结束时间
        :type EndTime: str
        :param _Labels: label集合
        :type Labels: str
        :param _Offset: 分片
        :type Offset: int
        :param _Limit: 分片
        :type Limit: int
        """
        self._InstanceId = None
        self._RuleName = None
        self._StartTime = None
        self._EndTime = None
        self._Labels = None
        self._Offset = None
        self._Limit = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def RuleName(self):
        return self._RuleName

    @RuleName.setter
    def RuleName(self, RuleName):
        self._RuleName = RuleName

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._RuleName = params.get("RuleName")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._Labels = params.get("Labels")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusAlertHistoryResponse(AbstractModel):
    """DescribePrometheusAlertHistory返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Items: 告警历史
        :type Items: list of PrometheusAlertHistoryItem
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Items = None
        self._Total = None
        self._RequestId = None

    @property
    def Items(self):
        return self._Items

    @Items.setter
    def Items(self, Items):
        self._Items = Items

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Items") is not None:
            self._Items = []
            for item in params.get("Items"):
                obj = PrometheusAlertHistoryItem()
                obj._deserialize(item)
                self._Items.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusAlertPolicyRequest(AbstractModel):
    """DescribePrometheusAlertPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Offset: 分页
        :type Offset: int
        :param _Limit: 分页
        :type Limit: int
        :param _Filters: 过滤
支持ID，Name
        :type Filters: list of Filter
        """
        self._InstanceId = None
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusAlertPolicyResponse(AbstractModel):
    """DescribePrometheusAlertPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AlertRules: 告警详情
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertRules: list of PrometheusAlertPolicyItem
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AlertRules = None
        self._Total = None
        self._RequestId = None

    @property
    def AlertRules(self):
        return self._AlertRules

    @AlertRules.setter
    def AlertRules(self, AlertRules):
        self._AlertRules = AlertRules

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("AlertRules") is not None:
            self._AlertRules = []
            for item in params.get("AlertRules"):
                obj = PrometheusAlertPolicyItem()
                obj._deserialize(item)
                self._AlertRules.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusAlertRuleRequest(AbstractModel):
    """DescribePrometheusAlertRule请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Offset: 分页
        :type Offset: int
        :param _Limit: 分页
        :type Limit: int
        :param _Filters: 过滤
支持ID，Name
        :type Filters: list of Filter
        """
        self._InstanceId = None
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusAlertRuleResponse(AbstractModel):
    """DescribePrometheusAlertRule返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AlertRules: 告警详情
        :type AlertRules: list of PrometheusAlertRuleDetail
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AlertRules = None
        self._Total = None
        self._RequestId = None

    @property
    def AlertRules(self):
        return self._AlertRules

    @AlertRules.setter
    def AlertRules(self, AlertRules):
        self._AlertRules = AlertRules

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("AlertRules") is not None:
            self._AlertRules = []
            for item in params.get("AlertRules"):
                obj = PrometheusAlertRuleDetail()
                obj._deserialize(item)
                self._AlertRules.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusClusterAgentsRequest(AbstractModel):
    """DescribePrometheusClusterAgents请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Offset: 用于分页
        :type Offset: int
        :param _Limit: 用于分页
        :type Limit: int
        """
        self._InstanceId = None
        self._Offset = None
        self._Limit = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusClusterAgentsResponse(AbstractModel):
    """DescribePrometheusClusterAgents返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Agents: 被关联集群信息
        :type Agents: list of PrometheusAgentOverview
        :param _Total: 被关联集群总量
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Agents = None
        self._Total = None
        self._RequestId = None

    @property
    def Agents(self):
        return self._Agents

    @Agents.setter
    def Agents(self, Agents):
        self._Agents = Agents

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Agents") is not None:
            self._Agents = []
            for item in params.get("Agents"):
                obj = PrometheusAgentOverview()
                obj._deserialize(item)
                self._Agents.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusConfigRequest(AbstractModel):
    """DescribePrometheusConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._InstanceId = None
        self._ClusterId = None
        self._ClusterType = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._ClusterId = params.get("ClusterId")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusConfigResponse(AbstractModel):
    """DescribePrometheusConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Config: 全局配置
        :type Config: str
        :param _ServiceMonitors: ServiceMonitor配置
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: PodMonitor配置
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: 原生Job
        :type RawJobs: list of PrometheusConfigItem
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Config = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None
        self._RequestId = None

    @property
    def Config(self):
        return self._Config

    @Config.setter
    def Config(self, Config):
        self._Config = Config

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Config = params.get("Config")
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        self._RequestId = params.get("RequestId")


class DescribePrometheusGlobalConfigRequest(AbstractModel):
    """DescribePrometheusGlobalConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例级别抓取配置
        :type InstanceId: str
        :param _DisableStatistics: 是否禁用统计
        :type DisableStatistics: bool
        """
        self._InstanceId = None
        self._DisableStatistics = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def DisableStatistics(self):
        return self._DisableStatistics

    @DisableStatistics.setter
    def DisableStatistics(self, DisableStatistics):
        self._DisableStatistics = DisableStatistics


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._DisableStatistics = params.get("DisableStatistics")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusGlobalConfigResponse(AbstractModel):
    """DescribePrometheusGlobalConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Config: 配置内容
        :type Config: str
        :param _ServiceMonitors: ServiceMonitors列表以及对应targets信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: PodMonitors列表以及对应targets信息
注意：此字段可能返回 null，表示取不到有效值。
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: RawJobs列表以及对应targets信息
注意：此字段可能返回 null，表示取不到有效值。
        :type RawJobs: list of PrometheusConfigItem
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Config = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None
        self._RequestId = None

    @property
    def Config(self):
        return self._Config

    @Config.setter
    def Config(self, Config):
        self._Config = Config

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Config = params.get("Config")
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        self._RequestId = params.get("RequestId")


class DescribePrometheusGlobalNotificationRequest(AbstractModel):
    """DescribePrometheusGlobalNotification请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusGlobalNotificationResponse(AbstractModel):
    """DescribePrometheusGlobalNotification返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Notification: 全局告警通知渠道
注意：此字段可能返回 null，表示取不到有效值。
        :type Notification: :class:`tencentcloud.tke.v20180525.models.PrometheusNotificationItem`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Notification = None
        self._RequestId = None

    @property
    def Notification(self):
        return self._Notification

    @Notification.setter
    def Notification(self, Notification):
        self._Notification = Notification

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Notification") is not None:
            self._Notification = PrometheusNotificationItem()
            self._Notification._deserialize(params.get("Notification"))
        self._RequestId = params.get("RequestId")


class DescribePrometheusInstanceInitStatusRequest(AbstractModel):
    """DescribePrometheusInstanceInitStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusInstanceInitStatusResponse(AbstractModel):
    """DescribePrometheusInstanceInitStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Status: 实例初始化状态，取值：
uninitialized 未初始化 
initializing 初始化中
running 初始化完成，运行中
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _Steps: 初始化任务步骤
注意：此字段可能返回 null，表示取不到有效值。
        :type Steps: list of TaskStepInfo
        :param _EksClusterId: 实例eks集群ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EksClusterId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Status = None
        self._Steps = None
        self._EksClusterId = None
        self._RequestId = None

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Steps(self):
        return self._Steps

    @Steps.setter
    def Steps(self, Steps):
        self._Steps = Steps

    @property
    def EksClusterId(self):
        return self._EksClusterId

    @EksClusterId.setter
    def EksClusterId(self, EksClusterId):
        self._EksClusterId = EksClusterId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Status = params.get("Status")
        if params.get("Steps") is not None:
            self._Steps = []
            for item in params.get("Steps"):
                obj = TaskStepInfo()
                obj._deserialize(item)
                self._Steps.append(obj)
        self._EksClusterId = params.get("EksClusterId")
        self._RequestId = params.get("RequestId")


class DescribePrometheusInstanceRequest(AbstractModel):
    """DescribePrometheusInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        """
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusInstanceResponse(AbstractModel):
    """DescribePrometheusInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Name: 实例名称
        :type Name: str
        :param _VpcId: 私有网络id
        :type VpcId: str
        :param _SubnetId: 子网id
        :type SubnetId: str
        :param _COSBucket: cos桶名称
        :type COSBucket: str
        :param _QueryAddress: 数据查询地址
        :type QueryAddress: str
        :param _Grafana: 实例中grafana相关的信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Grafana: :class:`tencentcloud.tke.v20180525.models.PrometheusGrafanaInfo`
        :param _AlertManagerUrl: 用户自定义alertmanager
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertManagerUrl: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._InstanceId = None
        self._Name = None
        self._VpcId = None
        self._SubnetId = None
        self._COSBucket = None
        self._QueryAddress = None
        self._Grafana = None
        self._AlertManagerUrl = None
        self._RequestId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def COSBucket(self):
        return self._COSBucket

    @COSBucket.setter
    def COSBucket(self, COSBucket):
        self._COSBucket = COSBucket

    @property
    def QueryAddress(self):
        return self._QueryAddress

    @QueryAddress.setter
    def QueryAddress(self, QueryAddress):
        self._QueryAddress = QueryAddress

    @property
    def Grafana(self):
        return self._Grafana

    @Grafana.setter
    def Grafana(self, Grafana):
        self._Grafana = Grafana

    @property
    def AlertManagerUrl(self):
        return self._AlertManagerUrl

    @AlertManagerUrl.setter
    def AlertManagerUrl(self, AlertManagerUrl):
        self._AlertManagerUrl = AlertManagerUrl

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Name = params.get("Name")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._COSBucket = params.get("COSBucket")
        self._QueryAddress = params.get("QueryAddress")
        if params.get("Grafana") is not None:
            self._Grafana = PrometheusGrafanaInfo()
            self._Grafana._deserialize(params.get("Grafana"))
        self._AlertManagerUrl = params.get("AlertManagerUrl")
        self._RequestId = params.get("RequestId")


class DescribePrometheusInstancesOverviewRequest(AbstractModel):
    """DescribePrometheusInstancesOverview请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Offset: 用于分页
        :type Offset: int
        :param _Limit: 用于分页
        :type Limit: int
        :param _Filters: 过滤实例，目前支持：
ID: 通过实例ID来过滤 
Name: 通过实例名称来过滤
        :type Filters: list of Filter
        """
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusInstancesOverviewResponse(AbstractModel):
    """DescribePrometheusInstancesOverview返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Instances: 实例列表
        :type Instances: list of PrometheusInstancesOverview
        :param _Total: 实例总数
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Instances = None
        self._Total = None
        self._RequestId = None

    @property
    def Instances(self):
        return self._Instances

    @Instances.setter
    def Instances(self, Instances):
        self._Instances = Instances

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Instances") is not None:
            self._Instances = []
            for item in params.get("Instances"):
                obj = PrometheusInstancesOverview()
                obj._deserialize(item)
                self._Instances.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusOverviewsRequest(AbstractModel):
    """DescribePrometheusOverviews请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Offset: 用于分页
        :type Offset: int
        :param _Limit: 用于分页
        :type Limit: int
        :param _Filters: 过滤实例，目前支持：
ID: 通过实例ID来过滤 
Name: 通过实例名称来过滤
        :type Filters: list of Filter
        """
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusOverviewsResponse(AbstractModel):
    """DescribePrometheusOverviews返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Instances: 实例列表
        :type Instances: list of PrometheusInstanceOverview
        :param _Total: 实例总数
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Instances = None
        self._Total = None
        self._RequestId = None

    @property
    def Instances(self):
        return self._Instances

    @Instances.setter
    def Instances(self, Instances):
        self._Instances = Instances

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Instances") is not None:
            self._Instances = []
            for item in params.get("Instances"):
                obj = PrometheusInstanceOverview()
                obj._deserialize(item)
                self._Instances.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusRecordRulesRequest(AbstractModel):
    """DescribePrometheusRecordRules请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Offset: 分页
        :type Offset: int
        :param _Limit: 分页
        :type Limit: int
        :param _Filters: 过滤
        :type Filters: list of Filter
        """
        self._InstanceId = None
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusRecordRulesResponse(AbstractModel):
    """DescribePrometheusRecordRules返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Records: 聚合规则
        :type Records: list of PrometheusRecordRuleYamlItem
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Records = None
        self._Total = None
        self._RequestId = None

    @property
    def Records(self):
        return self._Records

    @Records.setter
    def Records(self, Records):
        self._Records = Records

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Records") is not None:
            self._Records = []
            for item in params.get("Records"):
                obj = PrometheusRecordRuleYamlItem()
                obj._deserialize(item)
                self._Records.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusTargetsRequest(AbstractModel):
    """DescribePrometheusTargets请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _Filters: 过滤条件，当前支持
Name=state
Value=up, down, unknown
        :type Filters: list of Filter
        """
        self._InstanceId = None
        self._ClusterType = None
        self._ClusterId = None
        self._Filters = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusTargetsResponse(AbstractModel):
    """DescribePrometheusTargets返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Jobs: 所有Job的targets信息
        :type Jobs: list of PrometheusJobTargets
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Jobs = None
        self._RequestId = None

    @property
    def Jobs(self):
        return self._Jobs

    @Jobs.setter
    def Jobs(self, Jobs):
        self._Jobs = Jobs

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Jobs") is not None:
            self._Jobs = []
            for item in params.get("Jobs"):
                obj = PrometheusJobTargets()
                obj._deserialize(item)
                self._Jobs.append(obj)
        self._RequestId = params.get("RequestId")


class DescribePrometheusTempRequest(AbstractModel):
    """DescribePrometheusTemp请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Filters: 模糊过滤条件，支持
Level 按模板级别过滤
Name 按名称过滤
Describe 按描述过滤
ID 按templateId过滤
        :type Filters: list of Filter
        :param _Offset: 分页偏移
        :type Offset: int
        :param _Limit: 总数限制
        :type Limit: int
        """
        self._Filters = None
        self._Offset = None
        self._Limit = None

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusTempResponse(AbstractModel):
    """DescribePrometheusTemp返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Templates: 模板列表
        :type Templates: list of PrometheusTemp
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Templates = None
        self._Total = None
        self._RequestId = None

    @property
    def Templates(self):
        return self._Templates

    @Templates.setter
    def Templates(self, Templates):
        self._Templates = Templates

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Templates") is not None:
            self._Templates = []
            for item in params.get("Templates"):
                obj = PrometheusTemp()
                obj._deserialize(item)
                self._Templates.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribePrometheusTempSyncRequest(AbstractModel):
    """DescribePrometheusTempSync请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        """
        self._TemplateId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusTempSyncResponse(AbstractModel):
    """DescribePrometheusTempSync返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Targets: 同步目标详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Targets: list of PrometheusTemplateSyncTarget
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Targets = None
        self._RequestId = None

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTemplateSyncTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        self._RequestId = params.get("RequestId")


class DescribePrometheusTemplateSyncRequest(AbstractModel):
    """DescribePrometheusTemplateSync请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        """
        self._TemplateId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusTemplateSyncResponse(AbstractModel):
    """DescribePrometheusTemplateSync返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Targets: 同步目标详情
        :type Targets: list of PrometheusTemplateSyncTarget
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Targets = None
        self._RequestId = None

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTemplateSyncTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        self._RequestId = params.get("RequestId")


class DescribePrometheusTemplatesRequest(AbstractModel):
    """DescribePrometheusTemplates请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Filters: 模糊过滤条件，支持
Level 按模板级别过滤
Name 按名称过滤
Describe 按描述过滤
ID 按templateId过滤
        :type Filters: list of Filter
        :param _Offset: 分页偏移
        :type Offset: int
        :param _Limit: 总数限制
        :type Limit: int
        """
        self._Filters = None
        self._Offset = None
        self._Limit = None

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePrometheusTemplatesResponse(AbstractModel):
    """DescribePrometheusTemplates返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Templates: 模板列表
        :type Templates: list of PrometheusTemplate
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Templates = None
        self._Total = None
        self._RequestId = None

    @property
    def Templates(self):
        return self._Templates

    @Templates.setter
    def Templates(self, Templates):
        self._Templates = Templates

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Templates") is not None:
            self._Templates = []
            for item in params.get("Templates"):
                obj = PrometheusTemplate()
                obj._deserialize(item)
                self._Templates.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions请求参数结构体

    """


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 地域的数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param _RegionInstanceSet: 地域列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RegionInstanceSet: list of RegionInstance
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._RegionInstanceSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RegionInstanceSet(self):
        return self._RegionInstanceSet

    @RegionInstanceSet.setter
    def RegionInstanceSet(self, RegionInstanceSet):
        self._RegionInstanceSet = RegionInstanceSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("RegionInstanceSet") is not None:
            self._RegionInstanceSet = []
            for item in params.get("RegionInstanceSet"):
                obj = RegionInstance()
                obj._deserialize(item)
                self._RegionInstanceSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeResourceUsageRequest(AbstractModel):
    """DescribeResourceUsage请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResourceUsageResponse(AbstractModel):
    """DescribeResourceUsage返回参数结构体

    """

    def __init__(self):
        r"""
        :param _CRDUsage: CRD使用量
        :type CRDUsage: :class:`tencentcloud.tke.v20180525.models.ResourceUsage`
        :param _PodUsage: Pod使用量
        :type PodUsage: int
        :param _RSUsage: ReplicaSet使用量
        :type RSUsage: int
        :param _ConfigMapUsage: ConfigMap使用量
        :type ConfigMapUsage: int
        :param _OtherUsage: 其他资源使用量
        :type OtherUsage: :class:`tencentcloud.tke.v20180525.models.ResourceUsage`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._CRDUsage = None
        self._PodUsage = None
        self._RSUsage = None
        self._ConfigMapUsage = None
        self._OtherUsage = None
        self._RequestId = None

    @property
    def CRDUsage(self):
        return self._CRDUsage

    @CRDUsage.setter
    def CRDUsage(self, CRDUsage):
        self._CRDUsage = CRDUsage

    @property
    def PodUsage(self):
        return self._PodUsage

    @PodUsage.setter
    def PodUsage(self, PodUsage):
        self._PodUsage = PodUsage

    @property
    def RSUsage(self):
        return self._RSUsage

    @RSUsage.setter
    def RSUsage(self, RSUsage):
        self._RSUsage = RSUsage

    @property
    def ConfigMapUsage(self):
        return self._ConfigMapUsage

    @ConfigMapUsage.setter
    def ConfigMapUsage(self, ConfigMapUsage):
        self._ConfigMapUsage = ConfigMapUsage

    @property
    def OtherUsage(self):
        return self._OtherUsage

    @OtherUsage.setter
    def OtherUsage(self, OtherUsage):
        self._OtherUsage = OtherUsage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("CRDUsage") is not None:
            self._CRDUsage = ResourceUsage()
            self._CRDUsage._deserialize(params.get("CRDUsage"))
        self._PodUsage = params.get("PodUsage")
        self._RSUsage = params.get("RSUsage")
        self._ConfigMapUsage = params.get("ConfigMapUsage")
        if params.get("OtherUsage") is not None:
            self._OtherUsage = ResourceUsage()
            self._OtherUsage._deserialize(params.get("OtherUsage"))
        self._RequestId = params.get("RequestId")


class DescribeRouteTableConflictsRequest(AbstractModel):
    """DescribeRouteTableConflicts请求参数结构体

    """

    def __init__(self):
        r"""
        :param _RouteTableCidrBlock: 路由表CIDR
        :type RouteTableCidrBlock: str
        :param _VpcId: 路由表绑定的VPC
        :type VpcId: str
        """
        self._RouteTableCidrBlock = None
        self._VpcId = None

    @property
    def RouteTableCidrBlock(self):
        return self._RouteTableCidrBlock

    @RouteTableCidrBlock.setter
    def RouteTableCidrBlock(self, RouteTableCidrBlock):
        self._RouteTableCidrBlock = RouteTableCidrBlock

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId


    def _deserialize(self, params):
        self._RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self._VpcId = params.get("VpcId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRouteTableConflictsResponse(AbstractModel):
    """DescribeRouteTableConflicts返回参数结构体

    """

    def __init__(self):
        r"""
        :param _HasConflict: 路由表是否冲突。
        :type HasConflict: bool
        :param _RouteTableConflictSet: 路由表冲突列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type RouteTableConflictSet: list of RouteTableConflict
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._HasConflict = None
        self._RouteTableConflictSet = None
        self._RequestId = None

    @property
    def HasConflict(self):
        return self._HasConflict

    @HasConflict.setter
    def HasConflict(self, HasConflict):
        self._HasConflict = HasConflict

    @property
    def RouteTableConflictSet(self):
        return self._RouteTableConflictSet

    @RouteTableConflictSet.setter
    def RouteTableConflictSet(self, RouteTableConflictSet):
        self._RouteTableConflictSet = RouteTableConflictSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._HasConflict = params.get("HasConflict")
        if params.get("RouteTableConflictSet") is not None:
            self._RouteTableConflictSet = []
            for item in params.get("RouteTableConflictSet"):
                obj = RouteTableConflict()
                obj._deserialize(item)
                self._RouteTableConflictSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeTKEEdgeClusterCredentialRequest(AbstractModel):
    """DescribeTKEEdgeClusterCredential请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群Id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTKEEdgeClusterCredentialResponse(AbstractModel):
    """DescribeTKEEdgeClusterCredential返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Addresses: 集群的接入地址信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Addresses: list of IPAddress
        :param _Credential: 集群的认证信息
        :type Credential: :class:`tencentcloud.tke.v20180525.models.ClusterCredential`
        :param _PublicLB: 集群的公网访问信息
        :type PublicLB: :class:`tencentcloud.tke.v20180525.models.EdgeClusterPublicLB`
        :param _InternalLB: 集群的内网访问信息
        :type InternalLB: :class:`tencentcloud.tke.v20180525.models.EdgeClusterInternalLB`
        :param _CoreDns: 集群的CoreDns部署信息
        :type CoreDns: str
        :param _HealthRegion: 集群的健康检查多地域部署信息
        :type HealthRegion: str
        :param _Health: 集群的健康检查部署信息
        :type Health: str
        :param _GridDaemon: 是否部署GridDaemon以支持headless service
        :type GridDaemon: str
        :param _UnitCluster: 公网访问kins集群
        :type UnitCluster: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Addresses = None
        self._Credential = None
        self._PublicLB = None
        self._InternalLB = None
        self._CoreDns = None
        self._HealthRegion = None
        self._Health = None
        self._GridDaemon = None
        self._UnitCluster = None
        self._RequestId = None

    @property
    def Addresses(self):
        return self._Addresses

    @Addresses.setter
    def Addresses(self, Addresses):
        self._Addresses = Addresses

    @property
    def Credential(self):
        return self._Credential

    @Credential.setter
    def Credential(self, Credential):
        self._Credential = Credential

    @property
    def PublicLB(self):
        return self._PublicLB

    @PublicLB.setter
    def PublicLB(self, PublicLB):
        self._PublicLB = PublicLB

    @property
    def InternalLB(self):
        return self._InternalLB

    @InternalLB.setter
    def InternalLB(self, InternalLB):
        self._InternalLB = InternalLB

    @property
    def CoreDns(self):
        return self._CoreDns

    @CoreDns.setter
    def CoreDns(self, CoreDns):
        self._CoreDns = CoreDns

    @property
    def HealthRegion(self):
        return self._HealthRegion

    @HealthRegion.setter
    def HealthRegion(self, HealthRegion):
        self._HealthRegion = HealthRegion

    @property
    def Health(self):
        return self._Health

    @Health.setter
    def Health(self, Health):
        self._Health = Health

    @property
    def GridDaemon(self):
        return self._GridDaemon

    @GridDaemon.setter
    def GridDaemon(self, GridDaemon):
        self._GridDaemon = GridDaemon

    @property
    def UnitCluster(self):
        return self._UnitCluster

    @UnitCluster.setter
    def UnitCluster(self, UnitCluster):
        self._UnitCluster = UnitCluster

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Addresses") is not None:
            self._Addresses = []
            for item in params.get("Addresses"):
                obj = IPAddress()
                obj._deserialize(item)
                self._Addresses.append(obj)
        if params.get("Credential") is not None:
            self._Credential = ClusterCredential()
            self._Credential._deserialize(params.get("Credential"))
        if params.get("PublicLB") is not None:
            self._PublicLB = EdgeClusterPublicLB()
            self._PublicLB._deserialize(params.get("PublicLB"))
        if params.get("InternalLB") is not None:
            self._InternalLB = EdgeClusterInternalLB()
            self._InternalLB._deserialize(params.get("InternalLB"))
        self._CoreDns = params.get("CoreDns")
        self._HealthRegion = params.get("HealthRegion")
        self._Health = params.get("Health")
        self._GridDaemon = params.get("GridDaemon")
        self._UnitCluster = params.get("UnitCluster")
        self._RequestId = params.get("RequestId")


class DescribeTKEEdgeClusterStatusRequest(AbstractModel):
    """DescribeTKEEdgeClusterStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 边缘计算容器集群Id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTKEEdgeClusterStatusResponse(AbstractModel):
    """DescribeTKEEdgeClusterStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Phase: 集群当前状态
        :type Phase: str
        :param _Conditions: 集群过程数组
        :type Conditions: list of ClusterCondition
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Phase = None
        self._Conditions = None
        self._RequestId = None

    @property
    def Phase(self):
        return self._Phase

    @Phase.setter
    def Phase(self, Phase):
        self._Phase = Phase

    @property
    def Conditions(self):
        return self._Conditions

    @Conditions.setter
    def Conditions(self, Conditions):
        self._Conditions = Conditions

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Phase = params.get("Phase")
        if params.get("Conditions") is not None:
            self._Conditions = []
            for item in params.get("Conditions"):
                obj = ClusterCondition()
                obj._deserialize(item)
                self._Conditions.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeTKEEdgeClustersRequest(AbstractModel):
    """DescribeTKEEdgeClusters请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: 集群ID列表(为空时，
表示获取账号下所有集群)
        :type ClusterIds: list of str
        :param _Offset: 偏移量,默认0
        :type Offset: int
        :param _Limit: 最大输出条数，默认20
        :type Limit: int
        :param _Filters: 过滤条件,当前只支持按照ClusterName和云标签进行过滤,云标签过滤格式Tags:["key1:value1","key2:value2"]
        :type Filters: list of Filter
        """
        self._ClusterIds = None
        self._Offset = None
        self._Limit = None
        self._Filters = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Filters(self):
        return self._Filters

    @Filters.setter
    def Filters(self, Filters):
        self._Filters = Filters


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self._Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self._Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTKEEdgeClustersResponse(AbstractModel):
    """DescribeTKEEdgeClusters返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 集群总个数
        :type TotalCount: int
        :param _Clusters: 集群信息列表
        :type Clusters: list of EdgeCluster
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._Clusters = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Clusters(self):
        return self._Clusters

    @Clusters.setter
    def Clusters(self, Clusters):
        self._Clusters = Clusters

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Clusters") is not None:
            self._Clusters = []
            for item in params.get("Clusters"):
                obj = EdgeCluster()
                obj._deserialize(item)
                self._Clusters.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeTKEEdgeExternalKubeconfigRequest(AbstractModel):
    """DescribeTKEEdgeExternalKubeconfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTKEEdgeExternalKubeconfigResponse(AbstractModel):
    """DescribeTKEEdgeExternalKubeconfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Kubeconfig: kubeconfig文件内容
        :type Kubeconfig: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Kubeconfig = None
        self._RequestId = None

    @property
    def Kubeconfig(self):
        return self._Kubeconfig

    @Kubeconfig.setter
    def Kubeconfig(self, Kubeconfig):
        self._Kubeconfig = Kubeconfig

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Kubeconfig = params.get("Kubeconfig")
        self._RequestId = params.get("RequestId")


class DescribeTKEEdgeScriptRequest(AbstractModel):
    """DescribeTKEEdgeScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _Interface: 网卡名
        :type Interface: str
        :param _NodeName: 节点名字
        :type NodeName: str
        :param _Config: json格式的节点配置
        :type Config: str
        :param _ScriptVersion: 可以下载某个历史版本的edgectl脚本，默认下载最新版本，edgectl版本信息可以在脚本里查看
        :type ScriptVersion: str
        """
        self._ClusterId = None
        self._Interface = None
        self._NodeName = None
        self._Config = None
        self._ScriptVersion = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Interface(self):
        return self._Interface

    @Interface.setter
    def Interface(self, Interface):
        self._Interface = Interface

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName

    @property
    def Config(self):
        return self._Config

    @Config.setter
    def Config(self, Config):
        self._Config = Config

    @property
    def ScriptVersion(self):
        return self._ScriptVersion

    @ScriptVersion.setter
    def ScriptVersion(self, ScriptVersion):
        self._ScriptVersion = ScriptVersion


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Interface = params.get("Interface")
        self._NodeName = params.get("NodeName")
        self._Config = params.get("Config")
        self._ScriptVersion = params.get("ScriptVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTKEEdgeScriptResponse(AbstractModel):
    """DescribeTKEEdgeScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Link: 下载链接
        :type Link: str
        :param _Token: 下载需要的token
        :type Token: str
        :param _Command: 下载命令
        :type Command: str
        :param _ScriptVersion: edgectl脚本版本，默认拉取最新版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ScriptVersion: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Link = None
        self._Token = None
        self._Command = None
        self._ScriptVersion = None
        self._RequestId = None

    @property
    def Link(self):
        return self._Link

    @Link.setter
    def Link(self, Link):
        self._Link = Link

    @property
    def Token(self):
        return self._Token

    @Token.setter
    def Token(self, Token):
        self._Token = Token

    @property
    def Command(self):
        return self._Command

    @Command.setter
    def Command(self, Command):
        self._Command = Command

    @property
    def ScriptVersion(self):
        return self._ScriptVersion

    @ScriptVersion.setter
    def ScriptVersion(self, ScriptVersion):
        self._ScriptVersion = ScriptVersion

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Link = params.get("Link")
        self._Token = params.get("Token")
        self._Command = params.get("Command")
        self._ScriptVersion = params.get("ScriptVersion")
        self._RequestId = params.get("RequestId")


class DescribeVersionsRequest(AbstractModel):
    """DescribeVersions请求参数结构体

    """


class DescribeVersionsResponse(AbstractModel):
    """DescribeVersions返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 版本数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param _VersionInstanceSet: 版本列表
注意：此字段可能返回 null，表示取不到有效值。
        :type VersionInstanceSet: list of VersionInstance
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._VersionInstanceSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def VersionInstanceSet(self):
        return self._VersionInstanceSet

    @VersionInstanceSet.setter
    def VersionInstanceSet(self, VersionInstanceSet):
        self._VersionInstanceSet = VersionInstanceSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("VersionInstanceSet") is not None:
            self._VersionInstanceSet = []
            for item in params.get("VersionInstanceSet"):
                obj = VersionInstance()
                obj._deserialize(item)
                self._VersionInstanceSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeVpcCniPodLimitsRequest(AbstractModel):
    """DescribeVpcCniPodLimits请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Zone: 查询的机型所在可用区，如：ap-guangzhou-3，默认为空，即不按可用区过滤信息
        :type Zone: str
        :param _InstanceFamily: 查询的实例机型系列信息，如：S5，默认为空，即不按机型系列过滤信息
        :type InstanceFamily: str
        :param _InstanceType: 查询的实例机型信息，如：S5.LARGE8，默认为空，即不按机型过滤信息
        :type InstanceType: str
        """
        self._Zone = None
        self._InstanceFamily = None
        self._InstanceType = None

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def InstanceFamily(self):
        return self._InstanceFamily

    @InstanceFamily.setter
    def InstanceFamily(self, InstanceFamily):
        self._InstanceFamily = InstanceFamily

    @property
    def InstanceType(self):
        return self._InstanceType

    @InstanceType.setter
    def InstanceType(self, InstanceType):
        self._InstanceType = InstanceType


    def _deserialize(self, params):
        self._Zone = params.get("Zone")
        self._InstanceFamily = params.get("InstanceFamily")
        self._InstanceType = params.get("InstanceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeVpcCniPodLimitsResponse(AbstractModel):
    """DescribeVpcCniPodLimits返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 机型数据数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param _PodLimitsInstanceSet: 机型信息及其可支持的最大VPC-CNI模式Pod数量信息
注意：此字段可能返回 null，表示取不到有效值。
        :type PodLimitsInstanceSet: list of PodLimitsInstance
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._PodLimitsInstanceSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def PodLimitsInstanceSet(self):
        return self._PodLimitsInstanceSet

    @PodLimitsInstanceSet.setter
    def PodLimitsInstanceSet(self, PodLimitsInstanceSet):
        self._PodLimitsInstanceSet = PodLimitsInstanceSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("PodLimitsInstanceSet") is not None:
            self._PodLimitsInstanceSet = []
            for item in params.get("PodLimitsInstanceSet"):
                obj = PodLimitsInstance()
                obj._deserialize(item)
                self._PodLimitsInstanceSet.append(obj)
        self._RequestId = params.get("RequestId")


class DisableClusterAuditRequest(AbstractModel):
    """DisableClusterAudit请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _DeleteLogSetAndTopic: 取值为true代表关闭集群审计时删除默认创建的日志集和主题，false代表不删除
        :type DeleteLogSetAndTopic: bool
        """
        self._ClusterId = None
        self._DeleteLogSetAndTopic = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def DeleteLogSetAndTopic(self):
        return self._DeleteLogSetAndTopic

    @DeleteLogSetAndTopic.setter
    def DeleteLogSetAndTopic(self, DeleteLogSetAndTopic):
        self._DeleteLogSetAndTopic = DeleteLogSetAndTopic


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._DeleteLogSetAndTopic = params.get("DeleteLogSetAndTopic")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisableClusterAuditResponse(AbstractModel):
    """DisableClusterAudit返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DisableClusterDeletionProtectionRequest(AbstractModel):
    """DisableClusterDeletionProtection请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisableClusterDeletionProtectionResponse(AbstractModel):
    """DisableClusterDeletionProtection返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DisableEncryptionProtectionRequest(AbstractModel):
    """DisableEncryptionProtection请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisableEncryptionProtectionResponse(AbstractModel):
    """DisableEncryptionProtection返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DisableEventPersistenceRequest(AbstractModel):
    """DisableEventPersistence请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _DeleteLogSetAndTopic: 取值为true代表关闭集群审计时删除默认创建的日志集和主题，false代表不删除
        :type DeleteLogSetAndTopic: bool
        """
        self._ClusterId = None
        self._DeleteLogSetAndTopic = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def DeleteLogSetAndTopic(self):
        return self._DeleteLogSetAndTopic

    @DeleteLogSetAndTopic.setter
    def DeleteLogSetAndTopic(self, DeleteLogSetAndTopic):
        self._DeleteLogSetAndTopic = DeleteLogSetAndTopic


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._DeleteLogSetAndTopic = params.get("DeleteLogSetAndTopic")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisableEventPersistenceResponse(AbstractModel):
    """DisableEventPersistence返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DisableVpcCniNetworkTypeRequest(AbstractModel):
    """DisableVpcCniNetworkType请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisableVpcCniNetworkTypeResponse(AbstractModel):
    """DisableVpcCniNetworkType返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DnsServerConf(AbstractModel):
    """Eks 自定义域名服务器 配置

    """

    def __init__(self):
        r"""
        :param _Domain: 域名。空字符串表示所有域名。
        :type Domain: str
        :param _DnsServers: dns 服务器地址列表。地址格式 ip:port
        :type DnsServers: list of str
        """
        self._Domain = None
        self._DnsServers = None

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def DnsServers(self):
        return self._DnsServers

    @DnsServers.setter
    def DnsServers(self, DnsServers):
        self._DnsServers = DnsServers


    def _deserialize(self, params):
        self._Domain = params.get("Domain")
        self._DnsServers = params.get("DnsServers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DrainClusterVirtualNodeRequest(AbstractModel):
    """DrainClusterVirtualNode请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodeName: 节点名
        :type NodeName: str
        """
        self._ClusterId = None
        self._NodeName = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodeName = params.get("NodeName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DrainClusterVirtualNodeResponse(AbstractModel):
    """DrainClusterVirtualNode返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DriverVersion(AbstractModel):
    """GPU驱动和CUDA的版本信息

    """

    def __init__(self):
        r"""
        :param _Version: GPU驱动或者CUDA的版本
        :type Version: str
        :param _Name: GPU驱动或者CUDA的名字
        :type Name: str
        """
        self._Version = None
        self._Name = None

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name


    def _deserialize(self, params):
        self._Version = params.get("Version")
        self._Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ECMEnhancedService(AbstractModel):
    """ECM增强服务

    """

    def __init__(self):
        r"""
        :param _SecurityService: 是否开启云监控服务
        :type SecurityService: :class:`tencentcloud.tke.v20180525.models.ECMRunMonitorServiceEnabled`
        :param _MonitorService: 是否开启云镜服务
        :type MonitorService: :class:`tencentcloud.tke.v20180525.models.ECMRunSecurityServiceEnabled`
        """
        self._SecurityService = None
        self._MonitorService = None

    @property
    def SecurityService(self):
        return self._SecurityService

    @SecurityService.setter
    def SecurityService(self, SecurityService):
        self._SecurityService = SecurityService

    @property
    def MonitorService(self):
        return self._MonitorService

    @MonitorService.setter
    def MonitorService(self, MonitorService):
        self._MonitorService = MonitorService


    def _deserialize(self, params):
        if params.get("SecurityService") is not None:
            self._SecurityService = ECMRunMonitorServiceEnabled()
            self._SecurityService._deserialize(params.get("SecurityService"))
        if params.get("MonitorService") is not None:
            self._MonitorService = ECMRunSecurityServiceEnabled()
            self._MonitorService._deserialize(params.get("MonitorService"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ECMRunMonitorServiceEnabled(AbstractModel):
    """ECM云监控服务

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启
        :type Enabled: bool
        """
        self._Enabled = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ECMRunSecurityServiceEnabled(AbstractModel):
    """ECM云镜服务

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启
        :type Enabled: bool
        :param _Version: 云镜版本：0 基础版，1 专业版
        :type Version: int
        """
        self._Enabled = None
        self._Version = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._Version = params.get("Version")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ECMZoneInstanceCountISP(AbstractModel):
    """ECM实例可用区及对应的实例创建数目及运营商的组合

    """

    def __init__(self):
        r"""
        :param _Zone: 创建实例的可用区
        :type Zone: str
        :param _InstanceCount: 在当前可用区欲创建的实例数目
        :type InstanceCount: int
        :param _ISP: 运营商
        :type ISP: str
        """
        self._Zone = None
        self._InstanceCount = None
        self._ISP = None

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def InstanceCount(self):
        return self._InstanceCount

    @InstanceCount.setter
    def InstanceCount(self, InstanceCount):
        self._InstanceCount = InstanceCount

    @property
    def ISP(self):
        return self._ISP

    @ISP.setter
    def ISP(self, ISP):
        self._ISP = ISP


    def _deserialize(self, params):
        self._Zone = params.get("Zone")
        self._InstanceCount = params.get("InstanceCount")
        self._ISP = params.get("ISP")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeArgsFlag(AbstractModel):
    """边缘容器参数描述

    """

    def __init__(self):
        r"""
        :param _Name: 参数名
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _Type: 参数类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param _Usage: 参数描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Usage: str
        :param _Default: 参数默认值
注意：此字段可能返回 null，表示取不到有效值。
        :type Default: str
        :param _Constraint: 参数可选范围（目前包含range和in两种，"[]"代表range，如"[1, 5]"表示参数必须>=1且 <=5, "()"代表in， 如"('aa', 'bb')"表示参数只能为字符串'aa'或者'bb'，该参数为空表示不校验）
注意：此字段可能返回 null，表示取不到有效值。
        :type Constraint: str
        """
        self._Name = None
        self._Type = None
        self._Usage = None
        self._Default = None
        self._Constraint = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Usage(self):
        return self._Usage

    @Usage.setter
    def Usage(self, Usage):
        self._Usage = Usage

    @property
    def Default(self):
        return self._Default

    @Default.setter
    def Default(self, Default):
        self._Default = Default

    @property
    def Constraint(self):
        return self._Constraint

    @Constraint.setter
    def Constraint(self, Constraint):
        self._Constraint = Constraint


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Type = params.get("Type")
        self._Usage = params.get("Usage")
        self._Default = params.get("Default")
        self._Constraint = params.get("Constraint")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeAvailableExtraArgs(AbstractModel):
    """边缘容器集群可用的自定义参数

    """

    def __init__(self):
        r"""
        :param _KubeAPIServer: kube-apiserver可用的自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeAPIServer: list of EdgeArgsFlag
        :param _KubeControllerManager: kube-controller-manager可用的自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeControllerManager: list of EdgeArgsFlag
        :param _KubeScheduler: kube-scheduler可用的自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeScheduler: list of EdgeArgsFlag
        :param _Kubelet: kubelet可用的自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Kubelet: list of EdgeArgsFlag
        """
        self._KubeAPIServer = None
        self._KubeControllerManager = None
        self._KubeScheduler = None
        self._Kubelet = None

    @property
    def KubeAPIServer(self):
        return self._KubeAPIServer

    @KubeAPIServer.setter
    def KubeAPIServer(self, KubeAPIServer):
        self._KubeAPIServer = KubeAPIServer

    @property
    def KubeControllerManager(self):
        return self._KubeControllerManager

    @KubeControllerManager.setter
    def KubeControllerManager(self, KubeControllerManager):
        self._KubeControllerManager = KubeControllerManager

    @property
    def KubeScheduler(self):
        return self._KubeScheduler

    @KubeScheduler.setter
    def KubeScheduler(self, KubeScheduler):
        self._KubeScheduler = KubeScheduler

    @property
    def Kubelet(self):
        return self._Kubelet

    @Kubelet.setter
    def Kubelet(self, Kubelet):
        self._Kubelet = Kubelet


    def _deserialize(self, params):
        if params.get("KubeAPIServer") is not None:
            self._KubeAPIServer = []
            for item in params.get("KubeAPIServer"):
                obj = EdgeArgsFlag()
                obj._deserialize(item)
                self._KubeAPIServer.append(obj)
        if params.get("KubeControllerManager") is not None:
            self._KubeControllerManager = []
            for item in params.get("KubeControllerManager"):
                obj = EdgeArgsFlag()
                obj._deserialize(item)
                self._KubeControllerManager.append(obj)
        if params.get("KubeScheduler") is not None:
            self._KubeScheduler = []
            for item in params.get("KubeScheduler"):
                obj = EdgeArgsFlag()
                obj._deserialize(item)
                self._KubeScheduler.append(obj)
        if params.get("Kubelet") is not None:
            self._Kubelet = []
            for item in params.get("Kubelet"):
                obj = EdgeArgsFlag()
                obj._deserialize(item)
                self._Kubelet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeCluster(AbstractModel):
    """边缘计算集群信息

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群Id
        :type ClusterId: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _VpcId: Vpc Id
        :type VpcId: str
        :param _PodCIDR: 集群pod cidr
        :type PodCIDR: str
        :param _ServiceCIDR: 集群 service cidr
        :type ServiceCIDR: str
        :param _K8SVersion: k8s 版本号
        :type K8SVersion: str
        :param _Status: 集群状态
        :type Status: str
        :param _ClusterDesc: 集群描述信息
        :type ClusterDesc: str
        :param _CreatedTime: 集群创建时间
        :type CreatedTime: str
        :param _EdgeClusterVersion: 边缘集群版本
        :type EdgeClusterVersion: str
        :param _MaxNodePodNum: 节点最大Pod数
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxNodePodNum: int
        :param _ClusterAdvancedSettings: 集群高级设置
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.EdgeClusterAdvancedSettings`
        :param _Level: 边缘容器集群级别
注意：此字段可能返回 null，表示取不到有效值。
        :type Level: str
        :param _AutoUpgradeClusterLevel: 是否支持自动提升集群配置
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoUpgradeClusterLevel: bool
        :param _ChargeType: 集群付费模式，支持POSTPAID_BY_HOUR或者PREPAID
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param _EdgeVersion: 边缘集群组件的版本
注意：此字段可能返回 null，表示取不到有效值。
        :type EdgeVersion: str
        :param _TagSpecification: 集群绑定的云标签
注意：此字段可能返回 null，表示取不到有效值。
        :type TagSpecification: :class:`tencentcloud.tke.v20180525.models.TagSpecification`
        """
        self._ClusterId = None
        self._ClusterName = None
        self._VpcId = None
        self._PodCIDR = None
        self._ServiceCIDR = None
        self._K8SVersion = None
        self._Status = None
        self._ClusterDesc = None
        self._CreatedTime = None
        self._EdgeClusterVersion = None
        self._MaxNodePodNum = None
        self._ClusterAdvancedSettings = None
        self._Level = None
        self._AutoUpgradeClusterLevel = None
        self._ChargeType = None
        self._EdgeVersion = None
        self._TagSpecification = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def PodCIDR(self):
        return self._PodCIDR

    @PodCIDR.setter
    def PodCIDR(self, PodCIDR):
        self._PodCIDR = PodCIDR

    @property
    def ServiceCIDR(self):
        return self._ServiceCIDR

    @ServiceCIDR.setter
    def ServiceCIDR(self, ServiceCIDR):
        self._ServiceCIDR = ServiceCIDR

    @property
    def K8SVersion(self):
        return self._K8SVersion

    @K8SVersion.setter
    def K8SVersion(self, K8SVersion):
        self._K8SVersion = K8SVersion

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime

    @property
    def EdgeClusterVersion(self):
        return self._EdgeClusterVersion

    @EdgeClusterVersion.setter
    def EdgeClusterVersion(self, EdgeClusterVersion):
        self._EdgeClusterVersion = EdgeClusterVersion

    @property
    def MaxNodePodNum(self):
        return self._MaxNodePodNum

    @MaxNodePodNum.setter
    def MaxNodePodNum(self, MaxNodePodNum):
        self._MaxNodePodNum = MaxNodePodNum

    @property
    def ClusterAdvancedSettings(self):
        return self._ClusterAdvancedSettings

    @ClusterAdvancedSettings.setter
    def ClusterAdvancedSettings(self, ClusterAdvancedSettings):
        self._ClusterAdvancedSettings = ClusterAdvancedSettings

    @property
    def Level(self):
        return self._Level

    @Level.setter
    def Level(self, Level):
        self._Level = Level

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel

    @property
    def ChargeType(self):
        return self._ChargeType

    @ChargeType.setter
    def ChargeType(self, ChargeType):
        self._ChargeType = ChargeType

    @property
    def EdgeVersion(self):
        return self._EdgeVersion

    @EdgeVersion.setter
    def EdgeVersion(self, EdgeVersion):
        self._EdgeVersion = EdgeVersion

    @property
    def TagSpecification(self):
        return self._TagSpecification

    @TagSpecification.setter
    def TagSpecification(self, TagSpecification):
        self._TagSpecification = TagSpecification


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterName = params.get("ClusterName")
        self._VpcId = params.get("VpcId")
        self._PodCIDR = params.get("PodCIDR")
        self._ServiceCIDR = params.get("ServiceCIDR")
        self._K8SVersion = params.get("K8SVersion")
        self._Status = params.get("Status")
        self._ClusterDesc = params.get("ClusterDesc")
        self._CreatedTime = params.get("CreatedTime")
        self._EdgeClusterVersion = params.get("EdgeClusterVersion")
        self._MaxNodePodNum = params.get("MaxNodePodNum")
        if params.get("ClusterAdvancedSettings") is not None:
            self._ClusterAdvancedSettings = EdgeClusterAdvancedSettings()
            self._ClusterAdvancedSettings._deserialize(params.get("ClusterAdvancedSettings"))
        self._Level = params.get("Level")
        self._AutoUpgradeClusterLevel = params.get("AutoUpgradeClusterLevel")
        self._ChargeType = params.get("ChargeType")
        self._EdgeVersion = params.get("EdgeVersion")
        if params.get("TagSpecification") is not None:
            self._TagSpecification = TagSpecification()
            self._TagSpecification._deserialize(params.get("TagSpecification"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeClusterAdvancedSettings(AbstractModel):
    """边缘容器集群高级配置

    """

    def __init__(self):
        r"""
        :param _ExtraArgs: 集群自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type ExtraArgs: :class:`tencentcloud.tke.v20180525.models.EdgeClusterExtraArgs`
        :param _Runtime: 运行时类型，支持"docker"和"containerd"，默认为docker
注意：此字段可能返回 null，表示取不到有效值。
        :type Runtime: str
        :param _ProxyMode: 集群kube-proxy转发模式，支持"iptables"和"ipvs"，默认为iptables
注意：此字段可能返回 null，表示取不到有效值。
        :type ProxyMode: str
        """
        self._ExtraArgs = None
        self._Runtime = None
        self._ProxyMode = None

    @property
    def ExtraArgs(self):
        return self._ExtraArgs

    @ExtraArgs.setter
    def ExtraArgs(self, ExtraArgs):
        self._ExtraArgs = ExtraArgs

    @property
    def Runtime(self):
        return self._Runtime

    @Runtime.setter
    def Runtime(self, Runtime):
        self._Runtime = Runtime

    @property
    def ProxyMode(self):
        return self._ProxyMode

    @ProxyMode.setter
    def ProxyMode(self, ProxyMode):
        self._ProxyMode = ProxyMode


    def _deserialize(self, params):
        if params.get("ExtraArgs") is not None:
            self._ExtraArgs = EdgeClusterExtraArgs()
            self._ExtraArgs._deserialize(params.get("ExtraArgs"))
        self._Runtime = params.get("Runtime")
        self._ProxyMode = params.get("ProxyMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeClusterExtraArgs(AbstractModel):
    """边缘容器集群master自定义参数

    """

    def __init__(self):
        r"""
        :param _KubeAPIServer: kube-apiserver自定义参数，参数格式为["k1=v1", "k1=v2"]， 例如["max-requests-inflight=500","feature-gates=PodShareProcessNamespace=true,DynamicKubeletConfig=true"]
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeAPIServer: list of str
        :param _KubeControllerManager: kube-controller-manager自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeControllerManager: list of str
        :param _KubeScheduler: kube-scheduler自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type KubeScheduler: list of str
        """
        self._KubeAPIServer = None
        self._KubeControllerManager = None
        self._KubeScheduler = None

    @property
    def KubeAPIServer(self):
        return self._KubeAPIServer

    @KubeAPIServer.setter
    def KubeAPIServer(self, KubeAPIServer):
        self._KubeAPIServer = KubeAPIServer

    @property
    def KubeControllerManager(self):
        return self._KubeControllerManager

    @KubeControllerManager.setter
    def KubeControllerManager(self, KubeControllerManager):
        self._KubeControllerManager = KubeControllerManager

    @property
    def KubeScheduler(self):
        return self._KubeScheduler

    @KubeScheduler.setter
    def KubeScheduler(self, KubeScheduler):
        self._KubeScheduler = KubeScheduler


    def _deserialize(self, params):
        self._KubeAPIServer = params.get("KubeAPIServer")
        self._KubeControllerManager = params.get("KubeControllerManager")
        self._KubeScheduler = params.get("KubeScheduler")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeClusterInternalLB(AbstractModel):
    """边缘计算集群内网访问LB信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启内网访问LB
注意：此字段可能返回 null，表示取不到有效值。
        :type Enabled: bool
        :param _SubnetId: 内网访问LB关联的子网Id
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: list of str
        """
        self._Enabled = None
        self._SubnetId = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EdgeClusterPublicLB(AbstractModel):
    """边缘计算集群公网访问负载均衡信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启公网访问LB
注意：此字段可能返回 null，表示取不到有效值。
        :type Enabled: bool
        :param _AllowFromCidrs: 允许访问的公网cidr
注意：此字段可能返回 null，表示取不到有效值。
        :type AllowFromCidrs: list of str
        """
        self._Enabled = None
        self._AllowFromCidrs = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def AllowFromCidrs(self):
        return self._AllowFromCidrs

    @AllowFromCidrs.setter
    def AllowFromCidrs(self, AllowFromCidrs):
        self._AllowFromCidrs = AllowFromCidrs


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._AllowFromCidrs = params.get("AllowFromCidrs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EipAttribute(AbstractModel):
    """用以帮助用户自动创建EIP的配置

    """

    def __init__(self):
        r"""
        :param _DeletePolicy: 容器实例删除后，EIP是否释放。
Never表示不释放，其他任意值（包括空字符串）表示释放。
        :type DeletePolicy: str
        :param _InternetServiceProvider: EIP线路类型。默认值：BGP。
已开通静态单线IP白名单的用户，可选值：
CMCC：中国移动
CTCC：中国电信
CUCC：中国联通
注意：仅部分地域支持静态单线IP。
注意：此字段可能返回 null，表示取不到有效值。
        :type InternetServiceProvider: str
        :param _InternetMaxBandwidthOut: EIP出带宽上限，单位：Mbps。
注意：此字段可能返回 null，表示取不到有效值。
        :type InternetMaxBandwidthOut: int
        """
        self._DeletePolicy = None
        self._InternetServiceProvider = None
        self._InternetMaxBandwidthOut = None

    @property
    def DeletePolicy(self):
        return self._DeletePolicy

    @DeletePolicy.setter
    def DeletePolicy(self, DeletePolicy):
        self._DeletePolicy = DeletePolicy

    @property
    def InternetServiceProvider(self):
        return self._InternetServiceProvider

    @InternetServiceProvider.setter
    def InternetServiceProvider(self, InternetServiceProvider):
        self._InternetServiceProvider = InternetServiceProvider

    @property
    def InternetMaxBandwidthOut(self):
        return self._InternetMaxBandwidthOut

    @InternetMaxBandwidthOut.setter
    def InternetMaxBandwidthOut(self, InternetMaxBandwidthOut):
        self._InternetMaxBandwidthOut = InternetMaxBandwidthOut


    def _deserialize(self, params):
        self._DeletePolicy = params.get("DeletePolicy")
        self._InternetServiceProvider = params.get("InternetServiceProvider")
        self._InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EksCi(AbstractModel):
    """EksContainerInstance实例类型

    """

    def __init__(self):
        r"""
        :param _EksCiId: EKS Cotainer Instance Id
        :type EksCiId: str
        :param _EksCiName: EKS Cotainer Instance Name
        :type EksCiName: str
        :param _Memory: 内存大小
        :type Memory: float
        :param _Cpu: CPU大小
        :type Cpu: float
        :param _SecurityGroupIds: 安全组ID
        :type SecurityGroupIds: list of str
        :param _RestartPolicy: 容器组的重启策略
注意：此字段可能返回 null，表示取不到有效值。
        :type RestartPolicy: str
        :param _Status: 返回容器组创建状态：Pending，Running，Succeeded，Failed。其中：
Failed （运行失败）指的容器组退出，RestartPolilcy为Never， 有容器exitCode非0；
Succeeded（运行成功）指的是容器组退出了，RestartPolicy为Never或onFailure，所有容器exitCode都为0；
Failed和Succeeded这两种状态都会停止运行，停止计费。
Pending是创建中，Running是 运行中。
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _CreationTime: 接到请求后的系统创建时间。
注意：此字段可能返回 null，表示取不到有效值。
        :type CreationTime: str
        :param _SucceededTime: 容器全部成功退出后的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type SucceededTime: str
        :param _Containers: 容器列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Containers: list of Container
        :param _EksCiVolume: 数据卷信息
注意：此字段可能返回 null，表示取不到有效值。
        :type EksCiVolume: :class:`tencentcloud.tke.v20180525.models.EksCiVolume`
        :param _SecurityContext: 容器组运行的安全上下文
注意：此字段可能返回 null，表示取不到有效值。
        :type SecurityContext: :class:`tencentcloud.tke.v20180525.models.SecurityContext`
        :param _PrivateIp: 内网ip地址
注意：此字段可能返回 null，表示取不到有效值。
        :type PrivateIp: str
        :param _EipAddress: 容器实例绑定的Eip地址，注意可能为空
注意：此字段可能返回 null，表示取不到有效值。
        :type EipAddress: str
        :param _GpuType: GPU类型。如无使用GPU则不返回
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuType: str
        :param _CpuType: CPU类型
注意：此字段可能返回 null，表示取不到有效值。
        :type CpuType: str
        :param _GpuCount: GPU卡数量
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuCount: int
        :param _VpcId: 实例所属VPC的Id
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param _SubnetId: 实例所属子网Id
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: str
        :param _InitContainers: 初始化容器列表
注意：此字段可能返回 null，表示取不到有效值。
        :type InitContainers: list of Container
        :param _CamRoleName: 为容器实例关联 CAM 角色，value 填写 CAM 角色名称，容器实例可获取该 CAM 角色包含的权限策略，方便 容器实例 内的程序进行如购买资源、读写存储等云资源操作。
注意：此字段可能返回 null，表示取不到有效值。
        :type CamRoleName: str
        :param _AutoCreatedEipId: 自动为用户创建的EipId
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoCreatedEipId: str
        :param _PersistStatus: 容器状态是否持久化
注意：此字段可能返回 null，表示取不到有效值。
        :type PersistStatus: bool
        """
        self._EksCiId = None
        self._EksCiName = None
        self._Memory = None
        self._Cpu = None
        self._SecurityGroupIds = None
        self._RestartPolicy = None
        self._Status = None
        self._CreationTime = None
        self._SucceededTime = None
        self._Containers = None
        self._EksCiVolume = None
        self._SecurityContext = None
        self._PrivateIp = None
        self._EipAddress = None
        self._GpuType = None
        self._CpuType = None
        self._GpuCount = None
        self._VpcId = None
        self._SubnetId = None
        self._InitContainers = None
        self._CamRoleName = None
        self._AutoCreatedEipId = None
        self._PersistStatus = None

    @property
    def EksCiId(self):
        return self._EksCiId

    @EksCiId.setter
    def EksCiId(self, EksCiId):
        self._EksCiId = EksCiId

    @property
    def EksCiName(self):
        return self._EksCiName

    @EksCiName.setter
    def EksCiName(self, EksCiName):
        self._EksCiName = EksCiName

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def Cpu(self):
        return self._Cpu

    @Cpu.setter
    def Cpu(self, Cpu):
        self._Cpu = Cpu

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def RestartPolicy(self):
        return self._RestartPolicy

    @RestartPolicy.setter
    def RestartPolicy(self, RestartPolicy):
        self._RestartPolicy = RestartPolicy

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def CreationTime(self):
        return self._CreationTime

    @CreationTime.setter
    def CreationTime(self, CreationTime):
        self._CreationTime = CreationTime

    @property
    def SucceededTime(self):
        return self._SucceededTime

    @SucceededTime.setter
    def SucceededTime(self, SucceededTime):
        self._SucceededTime = SucceededTime

    @property
    def Containers(self):
        return self._Containers

    @Containers.setter
    def Containers(self, Containers):
        self._Containers = Containers

    @property
    def EksCiVolume(self):
        return self._EksCiVolume

    @EksCiVolume.setter
    def EksCiVolume(self, EksCiVolume):
        self._EksCiVolume = EksCiVolume

    @property
    def SecurityContext(self):
        return self._SecurityContext

    @SecurityContext.setter
    def SecurityContext(self, SecurityContext):
        self._SecurityContext = SecurityContext

    @property
    def PrivateIp(self):
        return self._PrivateIp

    @PrivateIp.setter
    def PrivateIp(self, PrivateIp):
        self._PrivateIp = PrivateIp

    @property
    def EipAddress(self):
        return self._EipAddress

    @EipAddress.setter
    def EipAddress(self, EipAddress):
        self._EipAddress = EipAddress

    @property
    def GpuType(self):
        return self._GpuType

    @GpuType.setter
    def GpuType(self, GpuType):
        self._GpuType = GpuType

    @property
    def CpuType(self):
        return self._CpuType

    @CpuType.setter
    def CpuType(self, CpuType):
        self._CpuType = CpuType

    @property
    def GpuCount(self):
        return self._GpuCount

    @GpuCount.setter
    def GpuCount(self, GpuCount):
        self._GpuCount = GpuCount

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def InitContainers(self):
        return self._InitContainers

    @InitContainers.setter
    def InitContainers(self, InitContainers):
        self._InitContainers = InitContainers

    @property
    def CamRoleName(self):
        return self._CamRoleName

    @CamRoleName.setter
    def CamRoleName(self, CamRoleName):
        self._CamRoleName = CamRoleName

    @property
    def AutoCreatedEipId(self):
        return self._AutoCreatedEipId

    @AutoCreatedEipId.setter
    def AutoCreatedEipId(self, AutoCreatedEipId):
        self._AutoCreatedEipId = AutoCreatedEipId

    @property
    def PersistStatus(self):
        return self._PersistStatus

    @PersistStatus.setter
    def PersistStatus(self, PersistStatus):
        self._PersistStatus = PersistStatus


    def _deserialize(self, params):
        self._EksCiId = params.get("EksCiId")
        self._EksCiName = params.get("EksCiName")
        self._Memory = params.get("Memory")
        self._Cpu = params.get("Cpu")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        self._RestartPolicy = params.get("RestartPolicy")
        self._Status = params.get("Status")
        self._CreationTime = params.get("CreationTime")
        self._SucceededTime = params.get("SucceededTime")
        if params.get("Containers") is not None:
            self._Containers = []
            for item in params.get("Containers"):
                obj = Container()
                obj._deserialize(item)
                self._Containers.append(obj)
        if params.get("EksCiVolume") is not None:
            self._EksCiVolume = EksCiVolume()
            self._EksCiVolume._deserialize(params.get("EksCiVolume"))
        if params.get("SecurityContext") is not None:
            self._SecurityContext = SecurityContext()
            self._SecurityContext._deserialize(params.get("SecurityContext"))
        self._PrivateIp = params.get("PrivateIp")
        self._EipAddress = params.get("EipAddress")
        self._GpuType = params.get("GpuType")
        self._CpuType = params.get("CpuType")
        self._GpuCount = params.get("GpuCount")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        if params.get("InitContainers") is not None:
            self._InitContainers = []
            for item in params.get("InitContainers"):
                obj = Container()
                obj._deserialize(item)
                self._InitContainers.append(obj)
        self._CamRoleName = params.get("CamRoleName")
        self._AutoCreatedEipId = params.get("AutoCreatedEipId")
        self._PersistStatus = params.get("PersistStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EksCiRegionInfo(AbstractModel):
    """EksCi地域信息

    """

    def __init__(self):
        r"""
        :param _Alias: 地域别名，形如gz
        :type Alias: str
        :param _RegionName: 地域名，形如ap-guangzhou
        :type RegionName: str
        :param _RegionId: 地域ID
        :type RegionId: int
        """
        self._Alias = None
        self._RegionName = None
        self._RegionId = None

    @property
    def Alias(self):
        return self._Alias

    @Alias.setter
    def Alias(self, Alias):
        self._Alias = Alias

    @property
    def RegionName(self):
        return self._RegionName

    @RegionName.setter
    def RegionName(self, RegionName):
        self._RegionName = RegionName

    @property
    def RegionId(self):
        return self._RegionId

    @RegionId.setter
    def RegionId(self, RegionId):
        self._RegionId = RegionId


    def _deserialize(self, params):
        self._Alias = params.get("Alias")
        self._RegionName = params.get("RegionName")
        self._RegionId = params.get("RegionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EksCiVolume(AbstractModel):
    """EKS Instance Volume,  可选包括CbsVolume和NfsVolume

    """

    def __init__(self):
        r"""
        :param _CbsVolumes: Cbs Volume
注意：此字段可能返回 null，表示取不到有效值。
        :type CbsVolumes: list of CbsVolume
        :param _NfsVolumes: Nfs Volume
注意：此字段可能返回 null，表示取不到有效值。
        :type NfsVolumes: list of NfsVolume
        """
        self._CbsVolumes = None
        self._NfsVolumes = None

    @property
    def CbsVolumes(self):
        return self._CbsVolumes

    @CbsVolumes.setter
    def CbsVolumes(self, CbsVolumes):
        self._CbsVolumes = CbsVolumes

    @property
    def NfsVolumes(self):
        return self._NfsVolumes

    @NfsVolumes.setter
    def NfsVolumes(self, NfsVolumes):
        self._NfsVolumes = NfsVolumes


    def _deserialize(self, params):
        if params.get("CbsVolumes") is not None:
            self._CbsVolumes = []
            for item in params.get("CbsVolumes"):
                obj = CbsVolume()
                obj._deserialize(item)
                self._CbsVolumes.append(obj)
        if params.get("NfsVolumes") is not None:
            self._NfsVolumes = []
            for item in params.get("NfsVolumes"):
                obj = NfsVolume()
                obj._deserialize(item)
                self._NfsVolumes.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EksCluster(AbstractModel):
    """弹性集群信息

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群Id
        :type ClusterId: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _VpcId: Vpc Id
        :type VpcId: str
        :param _SubnetIds: 子网列表
        :type SubnetIds: list of str
        :param _K8SVersion: k8s 版本号
        :type K8SVersion: str
        :param _Status: 集群状态(running运行中，initializing 初始化中，failed异常)
        :type Status: str
        :param _ClusterDesc: 集群描述信息
        :type ClusterDesc: str
        :param _CreatedTime: 集群创建时间
        :type CreatedTime: str
        :param _ServiceSubnetId: Service 子网Id
        :type ServiceSubnetId: str
        :param _DnsServers: 集群的自定义dns 服务器信息
        :type DnsServers: list of DnsServerConf
        :param _NeedDeleteCbs: 将来删除集群时是否要删除cbs。默认为 FALSE
        :type NeedDeleteCbs: bool
        :param _EnableVpcCoreDNS: 是否在用户集群内开启Dns。默认为TRUE
        :type EnableVpcCoreDNS: bool
        :param _TagSpecification: 标签描述列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type TagSpecification: list of TagSpecification
        """
        self._ClusterId = None
        self._ClusterName = None
        self._VpcId = None
        self._SubnetIds = None
        self._K8SVersion = None
        self._Status = None
        self._ClusterDesc = None
        self._CreatedTime = None
        self._ServiceSubnetId = None
        self._DnsServers = None
        self._NeedDeleteCbs = None
        self._EnableVpcCoreDNS = None
        self._TagSpecification = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def K8SVersion(self):
        return self._K8SVersion

    @K8SVersion.setter
    def K8SVersion(self, K8SVersion):
        self._K8SVersion = K8SVersion

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime

    @property
    def ServiceSubnetId(self):
        return self._ServiceSubnetId

    @ServiceSubnetId.setter
    def ServiceSubnetId(self, ServiceSubnetId):
        self._ServiceSubnetId = ServiceSubnetId

    @property
    def DnsServers(self):
        return self._DnsServers

    @DnsServers.setter
    def DnsServers(self, DnsServers):
        self._DnsServers = DnsServers

    @property
    def NeedDeleteCbs(self):
        return self._NeedDeleteCbs

    @NeedDeleteCbs.setter
    def NeedDeleteCbs(self, NeedDeleteCbs):
        self._NeedDeleteCbs = NeedDeleteCbs

    @property
    def EnableVpcCoreDNS(self):
        return self._EnableVpcCoreDNS

    @EnableVpcCoreDNS.setter
    def EnableVpcCoreDNS(self, EnableVpcCoreDNS):
        self._EnableVpcCoreDNS = EnableVpcCoreDNS

    @property
    def TagSpecification(self):
        return self._TagSpecification

    @TagSpecification.setter
    def TagSpecification(self, TagSpecification):
        self._TagSpecification = TagSpecification


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterName = params.get("ClusterName")
        self._VpcId = params.get("VpcId")
        self._SubnetIds = params.get("SubnetIds")
        self._K8SVersion = params.get("K8SVersion")
        self._Status = params.get("Status")
        self._ClusterDesc = params.get("ClusterDesc")
        self._CreatedTime = params.get("CreatedTime")
        self._ServiceSubnetId = params.get("ServiceSubnetId")
        if params.get("DnsServers") is not None:
            self._DnsServers = []
            for item in params.get("DnsServers"):
                obj = DnsServerConf()
                obj._deserialize(item)
                self._DnsServers.append(obj)
        self._NeedDeleteCbs = params.get("NeedDeleteCbs")
        self._EnableVpcCoreDNS = params.get("EnableVpcCoreDNS")
        if params.get("TagSpecification") is not None:
            self._TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self._TagSpecification.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableClusterAuditRequest(AbstractModel):
    """EnableClusterAudit请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _LogsetId: CLS日志集ID
        :type LogsetId: str
        :param _TopicId: CLS日志主题ID
        :type TopicId: str
        :param _TopicRegion: topic所在region，默认为集群当前region
        :type TopicRegion: str
        """
        self._ClusterId = None
        self._LogsetId = None
        self._TopicId = None
        self._TopicRegion = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def LogsetId(self):
        return self._LogsetId

    @LogsetId.setter
    def LogsetId(self, LogsetId):
        self._LogsetId = LogsetId

    @property
    def TopicId(self):
        return self._TopicId

    @TopicId.setter
    def TopicId(self, TopicId):
        self._TopicId = TopicId

    @property
    def TopicRegion(self):
        return self._TopicRegion

    @TopicRegion.setter
    def TopicRegion(self, TopicRegion):
        self._TopicRegion = TopicRegion


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._LogsetId = params.get("LogsetId")
        self._TopicId = params.get("TopicId")
        self._TopicRegion = params.get("TopicRegion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableClusterAuditResponse(AbstractModel):
    """EnableClusterAudit返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class EnableClusterDeletionProtectionRequest(AbstractModel):
    """EnableClusterDeletionProtection请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableClusterDeletionProtectionResponse(AbstractModel):
    """EnableClusterDeletionProtection返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class EnableEncryptionProtectionRequest(AbstractModel):
    """EnableEncryptionProtection请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _KMSConfiguration: kms加密配置
        :type KMSConfiguration: :class:`tencentcloud.tke.v20180525.models.KMSConfiguration`
        """
        self._ClusterId = None
        self._KMSConfiguration = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def KMSConfiguration(self):
        return self._KMSConfiguration

    @KMSConfiguration.setter
    def KMSConfiguration(self, KMSConfiguration):
        self._KMSConfiguration = KMSConfiguration


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("KMSConfiguration") is not None:
            self._KMSConfiguration = KMSConfiguration()
            self._KMSConfiguration._deserialize(params.get("KMSConfiguration"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableEncryptionProtectionResponse(AbstractModel):
    """EnableEncryptionProtection返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class EnableEventPersistenceRequest(AbstractModel):
    """EnableEventPersistence请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _LogsetId: cls服务的logsetID
        :type LogsetId: str
        :param _TopicId: cls服务的topicID
        :type TopicId: str
        :param _TopicRegion: topic所在地域，默认为集群所在地域
        :type TopicRegion: str
        """
        self._ClusterId = None
        self._LogsetId = None
        self._TopicId = None
        self._TopicRegion = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def LogsetId(self):
        return self._LogsetId

    @LogsetId.setter
    def LogsetId(self, LogsetId):
        self._LogsetId = LogsetId

    @property
    def TopicId(self):
        return self._TopicId

    @TopicId.setter
    def TopicId(self, TopicId):
        self._TopicId = TopicId

    @property
    def TopicRegion(self):
        return self._TopicRegion

    @TopicRegion.setter
    def TopicRegion(self, TopicRegion):
        self._TopicRegion = TopicRegion


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._LogsetId = params.get("LogsetId")
        self._TopicId = params.get("TopicId")
        self._TopicRegion = params.get("TopicRegion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableEventPersistenceResponse(AbstractModel):
    """EnableEventPersistence返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class EnableVpcCniNetworkTypeRequest(AbstractModel):
    """EnableVpcCniNetworkType请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _VpcCniType: 开启vpc-cni的模式，tke-route-eni开启的是策略路由模式，tke-direct-eni开启的是独立网卡模式
        :type VpcCniType: str
        :param _EnableStaticIp: 是否开启固定IP模式
        :type EnableStaticIp: bool
        :param _Subnets: 使用的容器子网
        :type Subnets: list of str
        :param _ExpiredSeconds: 在固定IP模式下，Pod销毁后退还IP的时间，传参必须大于300；不传默认IP永不销毁。
        :type ExpiredSeconds: int
        :param _SkipAddingNonMasqueradeCIDRs: 是否同步添加 vpc 网段到 ip-masq-agent-config 的 NonMasqueradeCIDRs 字段，默认 false 会同步添加
        :type SkipAddingNonMasqueradeCIDRs: bool
        """
        self._ClusterId = None
        self._VpcCniType = None
        self._EnableStaticIp = None
        self._Subnets = None
        self._ExpiredSeconds = None
        self._SkipAddingNonMasqueradeCIDRs = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def VpcCniType(self):
        return self._VpcCniType

    @VpcCniType.setter
    def VpcCniType(self, VpcCniType):
        self._VpcCniType = VpcCniType

    @property
    def EnableStaticIp(self):
        return self._EnableStaticIp

    @EnableStaticIp.setter
    def EnableStaticIp(self, EnableStaticIp):
        self._EnableStaticIp = EnableStaticIp

    @property
    def Subnets(self):
        return self._Subnets

    @Subnets.setter
    def Subnets(self, Subnets):
        self._Subnets = Subnets

    @property
    def ExpiredSeconds(self):
        return self._ExpiredSeconds

    @ExpiredSeconds.setter
    def ExpiredSeconds(self, ExpiredSeconds):
        self._ExpiredSeconds = ExpiredSeconds

    @property
    def SkipAddingNonMasqueradeCIDRs(self):
        return self._SkipAddingNonMasqueradeCIDRs

    @SkipAddingNonMasqueradeCIDRs.setter
    def SkipAddingNonMasqueradeCIDRs(self, SkipAddingNonMasqueradeCIDRs):
        self._SkipAddingNonMasqueradeCIDRs = SkipAddingNonMasqueradeCIDRs


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._VpcCniType = params.get("VpcCniType")
        self._EnableStaticIp = params.get("EnableStaticIp")
        self._Subnets = params.get("Subnets")
        self._ExpiredSeconds = params.get("ExpiredSeconds")
        self._SkipAddingNonMasqueradeCIDRs = params.get("SkipAddingNonMasqueradeCIDRs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableVpcCniNetworkTypeResponse(AbstractModel):
    """EnableVpcCniNetworkType返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class EnhancedService(AbstractModel):
    """描述了实例的增强服务启用情况与其设置，如云安全，云监控等实例 Agent

    """

    def __init__(self):
        r"""
        :param _SecurityService: 开启云安全服务。若不指定该参数，则默认开启云安全服务。
        :type SecurityService: :class:`tencentcloud.tke.v20180525.models.RunSecurityServiceEnabled`
        :param _MonitorService: 开启云监控服务。若不指定该参数，则默认开启云监控服务。
        :type MonitorService: :class:`tencentcloud.tke.v20180525.models.RunMonitorServiceEnabled`
        :param _AutomationService: 开启云自动化助手服务（TencentCloud Automation Tools，TAT）。若不指定该参数，则公共镜像默认开启云自动化助手服务，其他镜像默认不开启云自动化助手服务。
        :type AutomationService: :class:`tencentcloud.tke.v20180525.models.RunAutomationServiceEnabled`
        """
        self._SecurityService = None
        self._MonitorService = None
        self._AutomationService = None

    @property
    def SecurityService(self):
        return self._SecurityService

    @SecurityService.setter
    def SecurityService(self, SecurityService):
        self._SecurityService = SecurityService

    @property
    def MonitorService(self):
        return self._MonitorService

    @MonitorService.setter
    def MonitorService(self, MonitorService):
        self._MonitorService = MonitorService

    @property
    def AutomationService(self):
        return self._AutomationService

    @AutomationService.setter
    def AutomationService(self, AutomationService):
        self._AutomationService = AutomationService


    def _deserialize(self, params):
        if params.get("SecurityService") is not None:
            self._SecurityService = RunSecurityServiceEnabled()
            self._SecurityService._deserialize(params.get("SecurityService"))
        if params.get("MonitorService") is not None:
            self._MonitorService = RunMonitorServiceEnabled()
            self._MonitorService._deserialize(params.get("MonitorService"))
        if params.get("AutomationService") is not None:
            self._AutomationService = RunAutomationServiceEnabled()
            self._AutomationService._deserialize(params.get("AutomationService"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnvironmentVariable(AbstractModel):
    """EnvironmentVariable

    """

    def __init__(self):
        r"""
        :param _Name: key
        :type Name: str
        :param _Value: val
        :type Value: str
        """
        self._Name = None
        self._Value = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, Value):
        self._Value = Value


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Event(AbstractModel):
    """服务事件

    """

    def __init__(self):
        r"""
        :param _PodName: pod名称
        :type PodName: str
        :param _Reason: 事件原因内容
        :type Reason: str
        :param _Type: 事件类型
        :type Type: str
        :param _Count: 事件出现次数
        :type Count: int
        :param _FirstTimestamp: 事件第一次出现时间
        :type FirstTimestamp: str
        :param _LastTimestamp: 事件最后一次出现时间
        :type LastTimestamp: str
        :param _Message: 事件内容
        :type Message: str
        """
        self._PodName = None
        self._Reason = None
        self._Type = None
        self._Count = None
        self._FirstTimestamp = None
        self._LastTimestamp = None
        self._Message = None

    @property
    def PodName(self):
        return self._PodName

    @PodName.setter
    def PodName(self, PodName):
        self._PodName = PodName

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Count(self):
        return self._Count

    @Count.setter
    def Count(self, Count):
        self._Count = Count

    @property
    def FirstTimestamp(self):
        return self._FirstTimestamp

    @FirstTimestamp.setter
    def FirstTimestamp(self, FirstTimestamp):
        self._FirstTimestamp = FirstTimestamp

    @property
    def LastTimestamp(self):
        return self._LastTimestamp

    @LastTimestamp.setter
    def LastTimestamp(self, LastTimestamp):
        self._LastTimestamp = LastTimestamp

    @property
    def Message(self):
        return self._Message

    @Message.setter
    def Message(self, Message):
        self._Message = Message


    def _deserialize(self, params):
        self._PodName = params.get("PodName")
        self._Reason = params.get("Reason")
        self._Type = params.get("Type")
        self._Count = params.get("Count")
        self._FirstTimestamp = params.get("FirstTimestamp")
        self._LastTimestamp = params.get("LastTimestamp")
        self._Message = params.get("Message")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Exec(AbstractModel):
    """探针在容器内执行检测命令参数类型

    """

    def __init__(self):
        r"""
        :param _Commands: 容器内检测的命令
注意：此字段可能返回 null，表示取不到有效值。
        :type Commands: list of str
        """
        self._Commands = None

    @property
    def Commands(self):
        return self._Commands

    @Commands.setter
    def Commands(self, Commands):
        self._Commands = Commands


    def _deserialize(self, params):
        self._Commands = params.get("Commands")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExistedInstance(AbstractModel):
    """已经存在的实例信息

    """

    def __init__(self):
        r"""
        :param _Usable: 实例是否支持加入集群(TRUE 可以加入 FALSE 不能加入)。
注意：此字段可能返回 null，表示取不到有效值。
        :type Usable: bool
        :param _UnusableReason: 实例不支持加入的原因。
注意：此字段可能返回 null，表示取不到有效值。
        :type UnusableReason: str
        :param _AlreadyInCluster: 实例已经所在的集群ID。
注意：此字段可能返回 null，表示取不到有效值。
        :type AlreadyInCluster: str
        :param _InstanceId: 实例ID形如：ins-xxxxxxxx。
        :type InstanceId: str
        :param _InstanceName: 实例名称。
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        :param _PrivateIpAddresses: 实例主网卡的内网IP列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type PrivateIpAddresses: list of str
        :param _PublicIpAddresses: 实例主网卡的公网IP列表。
注意：此字段可能返回 null，表示取不到有效值。
注意：此字段可能返回 null，表示取不到有效值。
        :type PublicIpAddresses: list of str
        :param _CreatedTime: 创建时间。按照ISO8601标准表示，并且使用UTC时间。格式为：YYYY-MM-DDThh:mm:ssZ。
注意：此字段可能返回 null，表示取不到有效值。
        :type CreatedTime: str
        :param _CPU: 实例的CPU核数，单位：核。
注意：此字段可能返回 null，表示取不到有效值。
        :type CPU: int
        :param _Memory: 实例内存容量，单位：GB。
注意：此字段可能返回 null，表示取不到有效值。
        :type Memory: int
        :param _OsName: 操作系统名称。
注意：此字段可能返回 null，表示取不到有效值。
        :type OsName: str
        :param _InstanceType: 实例机型。
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceType: str
        :param _AutoscalingGroupId: 伸缩组ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoscalingGroupId: str
        :param _InstanceChargeType: 实例计费模式。取值范围： PREPAID：表示预付费，即包年包月 POSTPAID_BY_HOUR：表示后付费，即按量计费 CDHPAID：CDH付费，即只对CDH计费，不对CDH上的实例计费。
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceChargeType: str
        :param _IPv6Addresses: 实例的IPv6地址。
注意：此字段可能返回 null，表示取不到有效值。
注意：此字段可能返回 null，表示取不到有效值。
        :type IPv6Addresses: list of str
        """
        self._Usable = None
        self._UnusableReason = None
        self._AlreadyInCluster = None
        self._InstanceId = None
        self._InstanceName = None
        self._PrivateIpAddresses = None
        self._PublicIpAddresses = None
        self._CreatedTime = None
        self._CPU = None
        self._Memory = None
        self._OsName = None
        self._InstanceType = None
        self._AutoscalingGroupId = None
        self._InstanceChargeType = None
        self._IPv6Addresses = None

    @property
    def Usable(self):
        return self._Usable

    @Usable.setter
    def Usable(self, Usable):
        self._Usable = Usable

    @property
    def UnusableReason(self):
        return self._UnusableReason

    @UnusableReason.setter
    def UnusableReason(self, UnusableReason):
        self._UnusableReason = UnusableReason

    @property
    def AlreadyInCluster(self):
        return self._AlreadyInCluster

    @AlreadyInCluster.setter
    def AlreadyInCluster(self, AlreadyInCluster):
        self._AlreadyInCluster = AlreadyInCluster

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def PrivateIpAddresses(self):
        return self._PrivateIpAddresses

    @PrivateIpAddresses.setter
    def PrivateIpAddresses(self, PrivateIpAddresses):
        self._PrivateIpAddresses = PrivateIpAddresses

    @property
    def PublicIpAddresses(self):
        return self._PublicIpAddresses

    @PublicIpAddresses.setter
    def PublicIpAddresses(self, PublicIpAddresses):
        self._PublicIpAddresses = PublicIpAddresses

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime

    @property
    def CPU(self):
        return self._CPU

    @CPU.setter
    def CPU(self, CPU):
        self._CPU = CPU

    @property
    def Memory(self):
        return self._Memory

    @Memory.setter
    def Memory(self, Memory):
        self._Memory = Memory

    @property
    def OsName(self):
        return self._OsName

    @OsName.setter
    def OsName(self, OsName):
        self._OsName = OsName

    @property
    def InstanceType(self):
        return self._InstanceType

    @InstanceType.setter
    def InstanceType(self, InstanceType):
        self._InstanceType = InstanceType

    @property
    def AutoscalingGroupId(self):
        return self._AutoscalingGroupId

    @AutoscalingGroupId.setter
    def AutoscalingGroupId(self, AutoscalingGroupId):
        self._AutoscalingGroupId = AutoscalingGroupId

    @property
    def InstanceChargeType(self):
        return self._InstanceChargeType

    @InstanceChargeType.setter
    def InstanceChargeType(self, InstanceChargeType):
        self._InstanceChargeType = InstanceChargeType

    @property
    def IPv6Addresses(self):
        return self._IPv6Addresses

    @IPv6Addresses.setter
    def IPv6Addresses(self, IPv6Addresses):
        self._IPv6Addresses = IPv6Addresses


    def _deserialize(self, params):
        self._Usable = params.get("Usable")
        self._UnusableReason = params.get("UnusableReason")
        self._AlreadyInCluster = params.get("AlreadyInCluster")
        self._InstanceId = params.get("InstanceId")
        self._InstanceName = params.get("InstanceName")
        self._PrivateIpAddresses = params.get("PrivateIpAddresses")
        self._PublicIpAddresses = params.get("PublicIpAddresses")
        self._CreatedTime = params.get("CreatedTime")
        self._CPU = params.get("CPU")
        self._Memory = params.get("Memory")
        self._OsName = params.get("OsName")
        self._InstanceType = params.get("InstanceType")
        self._AutoscalingGroupId = params.get("AutoscalingGroupId")
        self._InstanceChargeType = params.get("InstanceChargeType")
        self._IPv6Addresses = params.get("IPv6Addresses")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExistedInstancesForNode(AbstractModel):
    """不同角色的已存在节点配置参数

    """

    def __init__(self):
        r"""
        :param _NodeRole: 节点角色，取值:MASTER_ETCD, WORKER。MASTER_ETCD只有在创建 INDEPENDENT_CLUSTER 独立集群时需要指定。MASTER_ETCD节点数量为3～7，建议为奇数。MASTER_ETCD最小配置为4C8G。
        :type NodeRole: str
        :param _ExistedInstancesPara: 已存在实例的重装参数
        :type ExistedInstancesPara: :class:`tencentcloud.tke.v20180525.models.ExistedInstancesPara`
        :param _InstanceAdvancedSettingsOverride: 节点高级设置，会覆盖集群级别设置的InstanceAdvancedSettings（当前只对节点自定义参数ExtraArgs生效）
        :type InstanceAdvancedSettingsOverride: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _DesiredPodNumbers: 自定义模式集群，可指定每个节点的pod数量
        :type DesiredPodNumbers: list of int
        """
        self._NodeRole = None
        self._ExistedInstancesPara = None
        self._InstanceAdvancedSettingsOverride = None
        self._DesiredPodNumbers = None

    @property
    def NodeRole(self):
        return self._NodeRole

    @NodeRole.setter
    def NodeRole(self, NodeRole):
        self._NodeRole = NodeRole

    @property
    def ExistedInstancesPara(self):
        return self._ExistedInstancesPara

    @ExistedInstancesPara.setter
    def ExistedInstancesPara(self, ExistedInstancesPara):
        self._ExistedInstancesPara = ExistedInstancesPara

    @property
    def InstanceAdvancedSettingsOverride(self):
        return self._InstanceAdvancedSettingsOverride

    @InstanceAdvancedSettingsOverride.setter
    def InstanceAdvancedSettingsOverride(self, InstanceAdvancedSettingsOverride):
        self._InstanceAdvancedSettingsOverride = InstanceAdvancedSettingsOverride

    @property
    def DesiredPodNumbers(self):
        return self._DesiredPodNumbers

    @DesiredPodNumbers.setter
    def DesiredPodNumbers(self, DesiredPodNumbers):
        self._DesiredPodNumbers = DesiredPodNumbers


    def _deserialize(self, params):
        self._NodeRole = params.get("NodeRole")
        if params.get("ExistedInstancesPara") is not None:
            self._ExistedInstancesPara = ExistedInstancesPara()
            self._ExistedInstancesPara._deserialize(params.get("ExistedInstancesPara"))
        if params.get("InstanceAdvancedSettingsOverride") is not None:
            self._InstanceAdvancedSettingsOverride = InstanceAdvancedSettings()
            self._InstanceAdvancedSettingsOverride._deserialize(params.get("InstanceAdvancedSettingsOverride"))
        self._DesiredPodNumbers = params.get("DesiredPodNumbers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExistedInstancesPara(AbstractModel):
    """已存在实例的重装参数

    """

    def __init__(self):
        r"""
        :param _InstanceIds: 集群ID
        :type InstanceIds: list of str
        :param _InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tencentcloud.tke.v20180525.models.EnhancedService`
        :param _LoginSettings: 节点登录信息（目前仅支持使用Password或者单个KeyIds）
        :type LoginSettings: :class:`tencentcloud.tke.v20180525.models.LoginSettings`
        :param _SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则绑定默认安全组。
        :type SecurityGroupIds: list of str
        :param _HostName: 重装系统时，可以指定修改实例的HostName(集群为HostName模式时，此参数必传，规则名称除不支持大写字符外与[CVM创建实例](https://cloud.tencent.com/document/product/213/15730)接口HostName一致)
        :type HostName: str
        """
        self._InstanceIds = None
        self._InstanceAdvancedSettings = None
        self._EnhancedService = None
        self._LoginSettings = None
        self._SecurityGroupIds = None
        self._HostName = None

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def EnhancedService(self):
        return self._EnhancedService

    @EnhancedService.setter
    def EnhancedService(self, EnhancedService):
        self._EnhancedService = EnhancedService

    @property
    def LoginSettings(self):
        return self._LoginSettings

    @LoginSettings.setter
    def LoginSettings(self, LoginSettings):
        self._LoginSettings = LoginSettings

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def HostName(self):
        return self._HostName

    @HostName.setter
    def HostName(self, HostName):
        self._HostName = HostName


    def _deserialize(self, params):
        self._InstanceIds = params.get("InstanceIds")
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("EnhancedService") is not None:
            self._EnhancedService = EnhancedService()
            self._EnhancedService._deserialize(params.get("EnhancedService"))
        if params.get("LoginSettings") is not None:
            self._LoginSettings = LoginSettings()
            self._LoginSettings._deserialize(params.get("LoginSettings"))
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        self._HostName = params.get("HostName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExtensionAddon(AbstractModel):
    """创建集群时，选择安装的扩展组件的信息

    """

    def __init__(self):
        r"""
        :param _AddonName: 扩展组件名称
        :type AddonName: str
        :param _AddonParam: 扩展组件信息(扩展组件资源对象的json字符串描述)
        :type AddonParam: str
        """
        self._AddonName = None
        self._AddonParam = None

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName

    @property
    def AddonParam(self):
        return self._AddonParam

    @AddonParam.setter
    def AddonParam(self, AddonParam):
        self._AddonParam = AddonParam


    def _deserialize(self, params):
        self._AddonName = params.get("AddonName")
        self._AddonParam = params.get("AddonParam")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filter(AbstractModel):
    """过滤器

    """

    def __init__(self):
        r"""
        :param _Name: 属性名称, 若存在多个Filter时，Filter间的关系为逻辑与（AND）关系。
        :type Name: str
        :param _Values: 属性值, 若同一个Filter存在多个Values，同一Filter下Values间的关系为逻辑或（OR）关系。
        :type Values: list of str
        """
        self._Name = None
        self._Values = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Values(self):
        return self._Values

    @Values.setter
    def Values(self, Values):
        self._Values = Values


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ForwardApplicationRequestV3Request(AbstractModel):
    """ForwardApplicationRequestV3请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Method: 请求集群addon的访问
        :type Method: str
        :param _Path: 请求集群addon的路径
        :type Path: str
        :param _Accept: 请求集群addon后允许接收的数据格式
        :type Accept: str
        :param _ContentType: 请求集群addon的数据格式
        :type ContentType: str
        :param _RequestBody: 请求集群addon的数据
        :type RequestBody: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _EncodedBody: 是否编码请求内容
        :type EncodedBody: str
        """
        self._Method = None
        self._Path = None
        self._Accept = None
        self._ContentType = None
        self._RequestBody = None
        self._ClusterName = None
        self._EncodedBody = None

    @property
    def Method(self):
        return self._Method

    @Method.setter
    def Method(self, Method):
        self._Method = Method

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path

    @property
    def Accept(self):
        return self._Accept

    @Accept.setter
    def Accept(self, Accept):
        self._Accept = Accept

    @property
    def ContentType(self):
        return self._ContentType

    @ContentType.setter
    def ContentType(self, ContentType):
        self._ContentType = ContentType

    @property
    def RequestBody(self):
        return self._RequestBody

    @RequestBody.setter
    def RequestBody(self, RequestBody):
        self._RequestBody = RequestBody

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def EncodedBody(self):
        return self._EncodedBody

    @EncodedBody.setter
    def EncodedBody(self, EncodedBody):
        self._EncodedBody = EncodedBody


    def _deserialize(self, params):
        self._Method = params.get("Method")
        self._Path = params.get("Path")
        self._Accept = params.get("Accept")
        self._ContentType = params.get("ContentType")
        self._RequestBody = params.get("RequestBody")
        self._ClusterName = params.get("ClusterName")
        self._EncodedBody = params.get("EncodedBody")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ForwardApplicationRequestV3Response(AbstractModel):
    """ForwardApplicationRequestV3返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResponseBody: 请求集群addon后返回的数据
        :type ResponseBody: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResponseBody = None
        self._RequestId = None

    @property
    def ResponseBody(self):
        return self._ResponseBody

    @ResponseBody.setter
    def ResponseBody(self, ResponseBody):
        self._ResponseBody = ResponseBody

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResponseBody = params.get("ResponseBody")
        self._RequestId = params.get("RequestId")


class ForwardTKEEdgeApplicationRequestV3Request(AbstractModel):
    """ForwardTKEEdgeApplicationRequestV3请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Method: 请求集群addon的访问
        :type Method: str
        :param _Path: 请求集群addon的路径
        :type Path: str
        :param _Accept: 请求集群addon后允许接收的数据格式
        :type Accept: str
        :param _ContentType: 请求集群addon的数据格式
        :type ContentType: str
        :param _RequestBody: 请求集群addon的数据
        :type RequestBody: str
        :param _ClusterName: 集群名称，例如cls-1234abcd
        :type ClusterName: str
        :param _EncodedBody: 是否编码请求内容
        :type EncodedBody: str
        """
        self._Method = None
        self._Path = None
        self._Accept = None
        self._ContentType = None
        self._RequestBody = None
        self._ClusterName = None
        self._EncodedBody = None

    @property
    def Method(self):
        return self._Method

    @Method.setter
    def Method(self, Method):
        self._Method = Method

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path

    @property
    def Accept(self):
        return self._Accept

    @Accept.setter
    def Accept(self, Accept):
        self._Accept = Accept

    @property
    def ContentType(self):
        return self._ContentType

    @ContentType.setter
    def ContentType(self, ContentType):
        self._ContentType = ContentType

    @property
    def RequestBody(self):
        return self._RequestBody

    @RequestBody.setter
    def RequestBody(self, RequestBody):
        self._RequestBody = RequestBody

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def EncodedBody(self):
        return self._EncodedBody

    @EncodedBody.setter
    def EncodedBody(self, EncodedBody):
        self._EncodedBody = EncodedBody


    def _deserialize(self, params):
        self._Method = params.get("Method")
        self._Path = params.get("Path")
        self._Accept = params.get("Accept")
        self._ContentType = params.get("ContentType")
        self._RequestBody = params.get("RequestBody")
        self._ClusterName = params.get("ClusterName")
        self._EncodedBody = params.get("EncodedBody")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ForwardTKEEdgeApplicationRequestV3Response(AbstractModel):
    """ForwardTKEEdgeApplicationRequestV3返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResponseBody: 请求集群addon后返回的数据
        :type ResponseBody: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResponseBody = None
        self._RequestId = None

    @property
    def ResponseBody(self):
        return self._ResponseBody

    @ResponseBody.setter
    def ResponseBody(self, ResponseBody):
        self._ResponseBody = ResponseBody

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResponseBody = params.get("ResponseBody")
        self._RequestId = params.get("RequestId")


class GPUArgs(AbstractModel):
    """GPU相关的参数，包括驱动版本，CUDA版本，cuDNN版本以及是否开启MIG

    """

    def __init__(self):
        r"""
        :param _MIGEnable: 是否启用MIG特性
注意：此字段可能返回 null，表示取不到有效值。
        :type MIGEnable: bool
        :param _Driver: GPU驱动版本信息
        :type Driver: :class:`tencentcloud.tke.v20180525.models.DriverVersion`
        :param _CUDA: CUDA版本信息
注意：此字段可能返回 null，表示取不到有效值。
        :type CUDA: :class:`tencentcloud.tke.v20180525.models.DriverVersion`
        :param _CUDNN: cuDNN版本信息
注意：此字段可能返回 null，表示取不到有效值。
        :type CUDNN: :class:`tencentcloud.tke.v20180525.models.CUDNN`
        :param _CustomDriver: 自定义GPU驱动信息
注意：此字段可能返回 null，表示取不到有效值。
        :type CustomDriver: :class:`tencentcloud.tke.v20180525.models.CustomDriver`
        """
        self._MIGEnable = None
        self._Driver = None
        self._CUDA = None
        self._CUDNN = None
        self._CustomDriver = None

    @property
    def MIGEnable(self):
        return self._MIGEnable

    @MIGEnable.setter
    def MIGEnable(self, MIGEnable):
        self._MIGEnable = MIGEnable

    @property
    def Driver(self):
        return self._Driver

    @Driver.setter
    def Driver(self, Driver):
        self._Driver = Driver

    @property
    def CUDA(self):
        return self._CUDA

    @CUDA.setter
    def CUDA(self, CUDA):
        self._CUDA = CUDA

    @property
    def CUDNN(self):
        return self._CUDNN

    @CUDNN.setter
    def CUDNN(self, CUDNN):
        self._CUDNN = CUDNN

    @property
    def CustomDriver(self):
        return self._CustomDriver

    @CustomDriver.setter
    def CustomDriver(self, CustomDriver):
        self._CustomDriver = CustomDriver


    def _deserialize(self, params):
        self._MIGEnable = params.get("MIGEnable")
        if params.get("Driver") is not None:
            self._Driver = DriverVersion()
            self._Driver._deserialize(params.get("Driver"))
        if params.get("CUDA") is not None:
            self._CUDA = DriverVersion()
            self._CUDA._deserialize(params.get("CUDA"))
        if params.get("CUDNN") is not None:
            self._CUDNN = CUDNN()
            self._CUDNN._deserialize(params.get("CUDNN"))
        if params.get("CustomDriver") is not None:
            self._CustomDriver = CustomDriver()
            self._CustomDriver._deserialize(params.get("CustomDriver"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetClusterLevelPriceRequest(AbstractModel):
    """GetClusterLevelPrice请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterLevel: 集群规格，托管集群询价
        :type ClusterLevel: str
        """
        self._ClusterLevel = None

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel


    def _deserialize(self, params):
        self._ClusterLevel = params.get("ClusterLevel")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetClusterLevelPriceResponse(AbstractModel):
    """GetClusterLevelPrice返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Cost: 询价结果，单位：分，打折后
        :type Cost: int
        :param _TotalCost: 询价结果，单位：分，折扣前
        :type TotalCost: int
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Cost = None
        self._TotalCost = None
        self._RequestId = None

    @property
    def Cost(self):
        return self._Cost

    @Cost.setter
    def Cost(self, Cost):
        self._Cost = Cost

    @property
    def TotalCost(self):
        return self._TotalCost

    @TotalCost.setter
    def TotalCost(self, TotalCost):
        self._TotalCost = TotalCost

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Cost = params.get("Cost")
        self._TotalCost = params.get("TotalCost")
        self._RequestId = params.get("RequestId")


class GetMostSuitableImageCacheRequest(AbstractModel):
    """GetMostSuitableImageCache请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Images: 容器镜像列表
        :type Images: list of str
        """
        self._Images = None

    @property
    def Images(self):
        return self._Images

    @Images.setter
    def Images(self, Images):
        self._Images = Images


    def _deserialize(self, params):
        self._Images = params.get("Images")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetMostSuitableImageCacheResponse(AbstractModel):
    """GetMostSuitableImageCache返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Found: 是否有匹配的镜像缓存
        :type Found: bool
        :param _ImageCache: 匹配的镜像缓存
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageCache: :class:`tencentcloud.tke.v20180525.models.ImageCache`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Found = None
        self._ImageCache = None
        self._RequestId = None

    @property
    def Found(self):
        return self._Found

    @Found.setter
    def Found(self, Found):
        self._Found = Found

    @property
    def ImageCache(self):
        return self._ImageCache

    @ImageCache.setter
    def ImageCache(self, ImageCache):
        self._ImageCache = ImageCache

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Found = params.get("Found")
        if params.get("ImageCache") is not None:
            self._ImageCache = ImageCache()
            self._ImageCache._deserialize(params.get("ImageCache"))
        self._RequestId = params.get("RequestId")


class GetTkeAppChartListRequest(AbstractModel):
    """GetTkeAppChartList请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Kind: app类型，取值log,scheduler,network,storage,monitor,dns,image,other,invisible
        :type Kind: str
        :param _Arch: app支持的操作系统，取值arm32、arm64、amd64
        :type Arch: str
        :param _ClusterType: 集群类型，取值tke、eks
        :type ClusterType: str
        """
        self._Kind = None
        self._Arch = None
        self._ClusterType = None

    @property
    def Kind(self):
        return self._Kind

    @Kind.setter
    def Kind(self, Kind):
        self._Kind = Kind

    @property
    def Arch(self):
        return self._Arch

    @Arch.setter
    def Arch(self, Arch):
        self._Arch = Arch

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._Kind = params.get("Kind")
        self._Arch = params.get("Arch")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetTkeAppChartListResponse(AbstractModel):
    """GetTkeAppChartList返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AppCharts: 所支持的chart列表
注意：此字段可能返回 null，表示取不到有效值。
        :type AppCharts: list of AppChart
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AppCharts = None
        self._RequestId = None

    @property
    def AppCharts(self):
        return self._AppCharts

    @AppCharts.setter
    def AppCharts(self, AppCharts):
        self._AppCharts = AppCharts

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("AppCharts") is not None:
            self._AppCharts = []
            for item in params.get("AppCharts"):
                obj = AppChart()
                obj._deserialize(item)
                self._AppCharts.append(obj)
        self._RequestId = params.get("RequestId")


class GetUpgradeInstanceProgressRequest(AbstractModel):
    """GetUpgradeInstanceProgress请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Limit: 最多获取多少个节点的进度
        :type Limit: int
        :param _Offset: 从第几个节点开始获取进度
        :type Offset: int
        """
        self._ClusterId = None
        self._Limit = None
        self._Offset = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetUpgradeInstanceProgressResponse(AbstractModel):
    """GetUpgradeInstanceProgress返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Total: 升级节点总数
        :type Total: int
        :param _Done: 已升级节点总数
        :type Done: int
        :param _LifeState: 升级任务生命周期
process 运行中
paused 已停止
pauing 正在停止
done  已完成
timeout 已超时
aborted 已取消
        :type LifeState: str
        :param _Instances: 各节点升级进度详情
        :type Instances: list of InstanceUpgradeProgressItem
        :param _ClusterStatus: 集群当前状态
        :type ClusterStatus: :class:`tencentcloud.tke.v20180525.models.InstanceUpgradeClusterStatus`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Total = None
        self._Done = None
        self._LifeState = None
        self._Instances = None
        self._ClusterStatus = None
        self._RequestId = None

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def Done(self):
        return self._Done

    @Done.setter
    def Done(self, Done):
        self._Done = Done

    @property
    def LifeState(self):
        return self._LifeState

    @LifeState.setter
    def LifeState(self, LifeState):
        self._LifeState = LifeState

    @property
    def Instances(self):
        return self._Instances

    @Instances.setter
    def Instances(self, Instances):
        self._Instances = Instances

    @property
    def ClusterStatus(self):
        return self._ClusterStatus

    @ClusterStatus.setter
    def ClusterStatus(self, ClusterStatus):
        self._ClusterStatus = ClusterStatus

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Total = params.get("Total")
        self._Done = params.get("Done")
        self._LifeState = params.get("LifeState")
        if params.get("Instances") is not None:
            self._Instances = []
            for item in params.get("Instances"):
                obj = InstanceUpgradeProgressItem()
                obj._deserialize(item)
                self._Instances.append(obj)
        if params.get("ClusterStatus") is not None:
            self._ClusterStatus = InstanceUpgradeClusterStatus()
            self._ClusterStatus._deserialize(params.get("ClusterStatus"))
        self._RequestId = params.get("RequestId")


class HttpGet(AbstractModel):
    """Probe中的HttpGet

    """

    def __init__(self):
        r"""
        :param _Path: HttpGet检测的路径
注意：此字段可能返回 null，表示取不到有效值。
        :type Path: str
        :param _Port: HttpGet检测的端口号
注意：此字段可能返回 null，表示取不到有效值。
        :type Port: int
        :param _Scheme: HTTP or HTTPS
注意：此字段可能返回 null，表示取不到有效值。
        :type Scheme: str
        """
        self._Path = None
        self._Port = None
        self._Scheme = None

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path

    @property
    def Port(self):
        return self._Port

    @Port.setter
    def Port(self, Port):
        self._Port = Port

    @property
    def Scheme(self):
        return self._Scheme

    @Scheme.setter
    def Scheme(self, Scheme):
        self._Scheme = Scheme


    def _deserialize(self, params):
        self._Path = params.get("Path")
        self._Port = params.get("Port")
        self._Scheme = params.get("Scheme")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IPAddress(AbstractModel):
    """IP 地址

    """

    def __init__(self):
        r"""
        :param _Type: Ip 地址的类型。可为 advertise, public 等
        :type Type: str
        :param _Ip: Ip 地址
        :type Ip: str
        :param _Port: 网络端口
        :type Port: int
        """
        self._Type = None
        self._Ip = None
        self._Port = None

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Ip(self):
        return self._Ip

    @Ip.setter
    def Ip(self, Ip):
        self._Ip = Ip

    @property
    def Port(self):
        return self._Port

    @Port.setter
    def Port(self, Port):
        self._Port = Port


    def _deserialize(self, params):
        self._Type = params.get("Type")
        self._Ip = params.get("Ip")
        self._Port = params.get("Port")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageCache(AbstractModel):
    """镜像缓存的信息

    """

    def __init__(self):
        r"""
        :param _ImageCacheId: 镜像缓存Id
        :type ImageCacheId: str
        :param _ImageCacheName: 镜像缓存名称
        :type ImageCacheName: str
        :param _ImageCacheSize: 镜像缓存大小。单位：GiB
        :type ImageCacheSize: int
        :param _Images: 镜像缓存包含的镜像列表
        :type Images: list of str
        :param _CreationTime: 创建时间
        :type CreationTime: str
        :param _ExpireDateTime: 到期时间
        :type ExpireDateTime: str
        :param _Events: 镜像缓存事件信息
        :type Events: list of ImageCacheEvent
        :param _LastMatchedTime: 最新一次匹配到镜像缓存的时间
        :type LastMatchedTime: str
        :param _SnapshotId: 镜像缓存对应的快照Id
        :type SnapshotId: str
        :param _Status: 镜像缓存状态，可能取值：
Pending：创建中
Ready：创建完成
Failed：创建失败
Updating：更新中
UpdateFailed：更新失败
只有状态为Ready时，才能正常使用镜像缓存
        :type Status: str
        """
        self._ImageCacheId = None
        self._ImageCacheName = None
        self._ImageCacheSize = None
        self._Images = None
        self._CreationTime = None
        self._ExpireDateTime = None
        self._Events = None
        self._LastMatchedTime = None
        self._SnapshotId = None
        self._Status = None

    @property
    def ImageCacheId(self):
        return self._ImageCacheId

    @ImageCacheId.setter
    def ImageCacheId(self, ImageCacheId):
        self._ImageCacheId = ImageCacheId

    @property
    def ImageCacheName(self):
        return self._ImageCacheName

    @ImageCacheName.setter
    def ImageCacheName(self, ImageCacheName):
        self._ImageCacheName = ImageCacheName

    @property
    def ImageCacheSize(self):
        return self._ImageCacheSize

    @ImageCacheSize.setter
    def ImageCacheSize(self, ImageCacheSize):
        self._ImageCacheSize = ImageCacheSize

    @property
    def Images(self):
        return self._Images

    @Images.setter
    def Images(self, Images):
        self._Images = Images

    @property
    def CreationTime(self):
        return self._CreationTime

    @CreationTime.setter
    def CreationTime(self, CreationTime):
        self._CreationTime = CreationTime

    @property
    def ExpireDateTime(self):
        return self._ExpireDateTime

    @ExpireDateTime.setter
    def ExpireDateTime(self, ExpireDateTime):
        self._ExpireDateTime = ExpireDateTime

    @property
    def Events(self):
        return self._Events

    @Events.setter
    def Events(self, Events):
        self._Events = Events

    @property
    def LastMatchedTime(self):
        return self._LastMatchedTime

    @LastMatchedTime.setter
    def LastMatchedTime(self, LastMatchedTime):
        self._LastMatchedTime = LastMatchedTime

    @property
    def SnapshotId(self):
        return self._SnapshotId

    @SnapshotId.setter
    def SnapshotId(self, SnapshotId):
        self._SnapshotId = SnapshotId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._ImageCacheId = params.get("ImageCacheId")
        self._ImageCacheName = params.get("ImageCacheName")
        self._ImageCacheSize = params.get("ImageCacheSize")
        self._Images = params.get("Images")
        self._CreationTime = params.get("CreationTime")
        self._ExpireDateTime = params.get("ExpireDateTime")
        if params.get("Events") is not None:
            self._Events = []
            for item in params.get("Events"):
                obj = ImageCacheEvent()
                obj._deserialize(item)
                self._Events.append(obj)
        self._LastMatchedTime = params.get("LastMatchedTime")
        self._SnapshotId = params.get("SnapshotId")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageCacheEvent(AbstractModel):
    """镜像缓存的事件

    """

    def __init__(self):
        r"""
        :param _ImageCacheId: 镜像缓存Id
        :type ImageCacheId: str
        :param _Type: 事件类型, Normal或者Warning
        :type Type: str
        :param _Reason: 事件原因简述
        :type Reason: str
        :param _Message: 事件原因详述
        :type Message: str
        :param _FirstTimestamp: 事件第一次出现时间
        :type FirstTimestamp: str
        :param _LastTimestamp: 事件最后一次出现时间
        :type LastTimestamp: str
        """
        self._ImageCacheId = None
        self._Type = None
        self._Reason = None
        self._Message = None
        self._FirstTimestamp = None
        self._LastTimestamp = None

    @property
    def ImageCacheId(self):
        return self._ImageCacheId

    @ImageCacheId.setter
    def ImageCacheId(self, ImageCacheId):
        self._ImageCacheId = ImageCacheId

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason

    @property
    def Message(self):
        return self._Message

    @Message.setter
    def Message(self, Message):
        self._Message = Message

    @property
    def FirstTimestamp(self):
        return self._FirstTimestamp

    @FirstTimestamp.setter
    def FirstTimestamp(self, FirstTimestamp):
        self._FirstTimestamp = FirstTimestamp

    @property
    def LastTimestamp(self):
        return self._LastTimestamp

    @LastTimestamp.setter
    def LastTimestamp(self, LastTimestamp):
        self._LastTimestamp = LastTimestamp


    def _deserialize(self, params):
        self._ImageCacheId = params.get("ImageCacheId")
        self._Type = params.get("Type")
        self._Reason = params.get("Reason")
        self._Message = params.get("Message")
        self._FirstTimestamp = params.get("FirstTimestamp")
        self._LastTimestamp = params.get("LastTimestamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageInstance(AbstractModel):
    """镜像信息

    """

    def __init__(self):
        r"""
        :param _Alias: 镜像别名
注意：此字段可能返回 null，表示取不到有效值。
        :type Alias: str
        :param _OsName: 操作系统名称
注意：此字段可能返回 null，表示取不到有效值。
        :type OsName: str
        :param _ImageId: 镜像ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageId: str
        :param _OsCustomizeType: 容器的镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
注意：此字段可能返回 null，表示取不到有效值。
        :type OsCustomizeType: str
        """
        self._Alias = None
        self._OsName = None
        self._ImageId = None
        self._OsCustomizeType = None

    @property
    def Alias(self):
        return self._Alias

    @Alias.setter
    def Alias(self, Alias):
        self._Alias = Alias

    @property
    def OsName(self):
        return self._OsName

    @OsName.setter
    def OsName(self, OsName):
        self._OsName = OsName

    @property
    def ImageId(self):
        return self._ImageId

    @ImageId.setter
    def ImageId(self, ImageId):
        self._ImageId = ImageId

    @property
    def OsCustomizeType(self):
        return self._OsCustomizeType

    @OsCustomizeType.setter
    def OsCustomizeType(self, OsCustomizeType):
        self._OsCustomizeType = OsCustomizeType


    def _deserialize(self, params):
        self._Alias = params.get("Alias")
        self._OsName = params.get("OsName")
        self._ImageId = params.get("ImageId")
        self._OsCustomizeType = params.get("OsCustomizeType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageRegistryCredential(AbstractModel):
    """从镜像仓库拉取镜像的凭据

    """

    def __init__(self):
        r"""
        :param _Server: 镜像仓库地址
        :type Server: str
        :param _Username: 用户名
        :type Username: str
        :param _Password: 密码
        :type Password: str
        :param _Name: ImageRegistryCredential的名字
        :type Name: str
        """
        self._Server = None
        self._Username = None
        self._Password = None
        self._Name = None

    @property
    def Server(self):
        return self._Server

    @Server.setter
    def Server(self, Server):
        self._Server = Server

    @property
    def Username(self):
        return self._Username

    @Username.setter
    def Username(self, Username):
        self._Username = Username

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name


    def _deserialize(self, params):
        self._Server = params.get("Server")
        self._Username = params.get("Username")
        self._Password = params.get("Password")
        self._Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstallAddonRequest(AbstractModel):
    """InstallAddon请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _AddonName: addon名称
        :type AddonName: str
        :param _AddonVersion: addon版本（不传默认安装最新版本）
        :type AddonVersion: str
        :param _RawValues: addon的参数，是一个json格式的base64转码后的字符串（addon参数由DescribeAddonValues获取）
        :type RawValues: str
        """
        self._ClusterId = None
        self._AddonName = None
        self._AddonVersion = None
        self._RawValues = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName

    @property
    def AddonVersion(self):
        return self._AddonVersion

    @AddonVersion.setter
    def AddonVersion(self, AddonVersion):
        self._AddonVersion = AddonVersion

    @property
    def RawValues(self):
        return self._RawValues

    @RawValues.setter
    def RawValues(self, RawValues):
        self._RawValues = RawValues


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AddonName = params.get("AddonName")
        self._AddonVersion = params.get("AddonVersion")
        self._RawValues = params.get("RawValues")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstallAddonResponse(AbstractModel):
    """InstallAddon返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class InstallEdgeLogAgentRequest(AbstractModel):
    """InstallEdgeLogAgent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstallEdgeLogAgentResponse(AbstractModel):
    """InstallEdgeLogAgent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class InstallLogAgentRequest(AbstractModel):
    """InstallLogAgent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: TKE集群ID
        :type ClusterId: str
        :param _KubeletRootDir: kubelet根目录
        :type KubeletRootDir: str
        """
        self._ClusterId = None
        self._KubeletRootDir = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def KubeletRootDir(self):
        return self._KubeletRootDir

    @KubeletRootDir.setter
    def KubeletRootDir(self, KubeletRootDir):
        self._KubeletRootDir = KubeletRootDir


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._KubeletRootDir = params.get("KubeletRootDir")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstallLogAgentResponse(AbstractModel):
    """InstallLogAgent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class Instance(AbstractModel):
    """集群的实例信息

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _InstanceRole: 节点角色, MASTER, WORKER, ETCD, MASTER_ETCD,ALL, 默认为WORKER
        :type InstanceRole: str
        :param _FailedReason: 实例异常(或者处于初始化中)的原因
        :type FailedReason: str
        :param _InstanceState: 实例的状态（running 运行中，initializing 初始化中，failed 异常）
        :type InstanceState: str
        :param _DrainStatus: 实例是否封锁状态
注意：此字段可能返回 null，表示取不到有效值。
        :type DrainStatus: str
        :param _InstanceAdvancedSettings: 节点配置
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _CreatedTime: 添加时间
        :type CreatedTime: str
        :param _LanIP: 节点内网IP
注意：此字段可能返回 null，表示取不到有效值。
        :type LanIP: str
        :param _NodePoolId: 资源池ID
注意：此字段可能返回 null，表示取不到有效值。
        :type NodePoolId: str
        :param _AutoscalingGroupId: 自动伸缩组ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoscalingGroupId: str
        """
        self._InstanceId = None
        self._InstanceRole = None
        self._FailedReason = None
        self._InstanceState = None
        self._DrainStatus = None
        self._InstanceAdvancedSettings = None
        self._CreatedTime = None
        self._LanIP = None
        self._NodePoolId = None
        self._AutoscalingGroupId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def InstanceRole(self):
        return self._InstanceRole

    @InstanceRole.setter
    def InstanceRole(self, InstanceRole):
        self._InstanceRole = InstanceRole

    @property
    def FailedReason(self):
        return self._FailedReason

    @FailedReason.setter
    def FailedReason(self, FailedReason):
        self._FailedReason = FailedReason

    @property
    def InstanceState(self):
        return self._InstanceState

    @InstanceState.setter
    def InstanceState(self, InstanceState):
        self._InstanceState = InstanceState

    @property
    def DrainStatus(self):
        return self._DrainStatus

    @DrainStatus.setter
    def DrainStatus(self, DrainStatus):
        self._DrainStatus = DrainStatus

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime

    @property
    def LanIP(self):
        return self._LanIP

    @LanIP.setter
    def LanIP(self, LanIP):
        self._LanIP = LanIP

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def AutoscalingGroupId(self):
        return self._AutoscalingGroupId

    @AutoscalingGroupId.setter
    def AutoscalingGroupId(self, AutoscalingGroupId):
        self._AutoscalingGroupId = AutoscalingGroupId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._InstanceRole = params.get("InstanceRole")
        self._FailedReason = params.get("FailedReason")
        self._InstanceState = params.get("InstanceState")
        self._DrainStatus = params.get("DrainStatus")
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self._CreatedTime = params.get("CreatedTime")
        self._LanIP = params.get("LanIP")
        self._NodePoolId = params.get("NodePoolId")
        self._AutoscalingGroupId = params.get("AutoscalingGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceAdvancedSettings(AbstractModel):
    """描述了k8s集群相关配置与信息。

    """

    def __init__(self):
        r"""
        :param _DesiredPodNumber: 该节点属于podCIDR大小自定义模式时，可指定节点上运行的pod数量上限
注意：此字段可能返回 null，表示取不到有效值。
        :type DesiredPodNumber: int
        :param _GPUArgs: GPU驱动相关参数,相关的GPU参数获取:https://cloud.tencent.com/document/api/213/15715
注意：此字段可能返回 null，表示取不到有效值。
        :type GPUArgs: :class:`tencentcloud.tke.v20180525.models.GPUArgs`
        :param _PreStartUserScript: base64 编码的用户脚本，在初始化节点之前执行，目前只对添加已有节点生效
注意：此字段可能返回 null，表示取不到有效值。
        :type PreStartUserScript: str
        :param _Taints: 节点污点
注意：此字段可能返回 null，表示取不到有效值。
        :type Taints: list of Taint
        :param _MountTarget: 数据盘挂载点, 默认不挂载数据盘. 已格式化的 ext3，ext4，xfs 文件系统的数据盘将直接挂载，其他文件系统或未格式化的数据盘将自动格式化为ext4 (tlinux系统格式化成xfs)并挂载，请注意备份数据! 无数据盘或有多块数据盘的云主机此设置不生效。
注意，注意，多盘场景请使用下方的DataDisks数据结构，设置对应的云盘类型、云盘大小、挂载路径、是否格式化等信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type MountTarget: str
        :param _DockerGraphPath: dockerd --graph 指定值, 默认为 /var/lib/docker
注意：此字段可能返回 null，表示取不到有效值。
        :type DockerGraphPath: str
        :param _UserScript: base64 编码的用户脚本, 此脚本会在 k8s 组件运行后执行, 需要用户保证脚本的可重入及重试逻辑, 脚本及其生成的日志文件可在节点的 /data/ccs_userscript/ 路径查看, 如果要求节点需要在进行初始化完成后才可加入调度, 可配合 unschedulable 参数使用, 在 userScript 最后初始化完成后, 添加 kubectl uncordon nodename --kubeconfig=/root/.kube/config 命令使节点加入调度
注意：此字段可能返回 null，表示取不到有效值。
        :type UserScript: str
        :param _Unschedulable: 设置加入的节点是否参与调度，默认值为0，表示参与调度；非0表示不参与调度, 待节点初始化完成之后, 可执行kubectl uncordon nodename使node加入调度.
        :type Unschedulable: int
        :param _Labels: 节点Label数组
注意：此字段可能返回 null，表示取不到有效值。
        :type Labels: list of Label
        :param _DataDisks: 多盘数据盘挂载信息：新建节点时请确保购买CVM的参数传递了购买多个数据盘的信息，如CreateClusterInstances API的RunInstancesPara下的DataDisks也需要设置购买多个数据盘, 具体可以参考CreateClusterInstances接口的添加集群节点(多块数据盘)样例；添加已有节点时，请确保填写的分区信息在节点上真实存在
注意：此字段可能返回 null，表示取不到有效值。
        :type DataDisks: list of DataDisk
        :param _ExtraArgs: 节点相关的自定义参数信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ExtraArgs: :class:`tencentcloud.tke.v20180525.models.InstanceExtraArgs`
        """
        self._DesiredPodNumber = None
        self._GPUArgs = None
        self._PreStartUserScript = None
        self._Taints = None
        self._MountTarget = None
        self._DockerGraphPath = None
        self._UserScript = None
        self._Unschedulable = None
        self._Labels = None
        self._DataDisks = None
        self._ExtraArgs = None

    @property
    def DesiredPodNumber(self):
        return self._DesiredPodNumber

    @DesiredPodNumber.setter
    def DesiredPodNumber(self, DesiredPodNumber):
        self._DesiredPodNumber = DesiredPodNumber

    @property
    def GPUArgs(self):
        return self._GPUArgs

    @GPUArgs.setter
    def GPUArgs(self, GPUArgs):
        self._GPUArgs = GPUArgs

    @property
    def PreStartUserScript(self):
        return self._PreStartUserScript

    @PreStartUserScript.setter
    def PreStartUserScript(self, PreStartUserScript):
        self._PreStartUserScript = PreStartUserScript

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints

    @property
    def MountTarget(self):
        return self._MountTarget

    @MountTarget.setter
    def MountTarget(self, MountTarget):
        self._MountTarget = MountTarget

    @property
    def DockerGraphPath(self):
        return self._DockerGraphPath

    @DockerGraphPath.setter
    def DockerGraphPath(self, DockerGraphPath):
        self._DockerGraphPath = DockerGraphPath

    @property
    def UserScript(self):
        return self._UserScript

    @UserScript.setter
    def UserScript(self, UserScript):
        self._UserScript = UserScript

    @property
    def Unschedulable(self):
        return self._Unschedulable

    @Unschedulable.setter
    def Unschedulable(self, Unschedulable):
        self._Unschedulable = Unschedulable

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def DataDisks(self):
        return self._DataDisks

    @DataDisks.setter
    def DataDisks(self, DataDisks):
        self._DataDisks = DataDisks

    @property
    def ExtraArgs(self):
        return self._ExtraArgs

    @ExtraArgs.setter
    def ExtraArgs(self, ExtraArgs):
        self._ExtraArgs = ExtraArgs


    def _deserialize(self, params):
        self._DesiredPodNumber = params.get("DesiredPodNumber")
        if params.get("GPUArgs") is not None:
            self._GPUArgs = GPUArgs()
            self._GPUArgs._deserialize(params.get("GPUArgs"))
        self._PreStartUserScript = params.get("PreStartUserScript")
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        self._MountTarget = params.get("MountTarget")
        self._DockerGraphPath = params.get("DockerGraphPath")
        self._UserScript = params.get("UserScript")
        self._Unschedulable = params.get("Unschedulable")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("DataDisks") is not None:
            self._DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self._DataDisks.append(obj)
        if params.get("ExtraArgs") is not None:
            self._ExtraArgs = InstanceExtraArgs()
            self._ExtraArgs._deserialize(params.get("ExtraArgs"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceDataDiskMountSetting(AbstractModel):
    """CVM实例数据盘挂载配置

    """

    def __init__(self):
        r"""
        :param _InstanceType: CVM实例类型
        :type InstanceType: str
        :param _DataDisks: 数据盘挂载信息
        :type DataDisks: list of DataDisk
        :param _Zone: CVM实例所属可用区
        :type Zone: str
        """
        self._InstanceType = None
        self._DataDisks = None
        self._Zone = None

    @property
    def InstanceType(self):
        return self._InstanceType

    @InstanceType.setter
    def InstanceType(self, InstanceType):
        self._InstanceType = InstanceType

    @property
    def DataDisks(self):
        return self._DataDisks

    @DataDisks.setter
    def DataDisks(self, DataDisks):
        self._DataDisks = DataDisks

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone


    def _deserialize(self, params):
        self._InstanceType = params.get("InstanceType")
        if params.get("DataDisks") is not None:
            self._DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self._DataDisks.append(obj)
        self._Zone = params.get("Zone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceExtraArgs(AbstractModel):
    """节点自定义参数

    """

    def __init__(self):
        r"""
        :param _Kubelet: kubelet自定义参数，参数格式为["k1=v1", "k1=v2"]， 例如["root-dir=/var/lib/kubelet","feature-gates=PodShareProcessNamespace=true,DynamicKubeletConfig=true"]
注意：此字段可能返回 null，表示取不到有效值。
        :type Kubelet: list of str
        """
        self._Kubelet = None

    @property
    def Kubelet(self):
        return self._Kubelet

    @Kubelet.setter
    def Kubelet(self, Kubelet):
        self._Kubelet = Kubelet


    def _deserialize(self, params):
        self._Kubelet = params.get("Kubelet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceUpgradeClusterStatus(AbstractModel):
    """节点升级过程中集群当前状态

    """

    def __init__(self):
        r"""
        :param _PodTotal: pod总数
        :type PodTotal: int
        :param _NotReadyPod: NotReady pod总数
        :type NotReadyPod: int
        """
        self._PodTotal = None
        self._NotReadyPod = None

    @property
    def PodTotal(self):
        return self._PodTotal

    @PodTotal.setter
    def PodTotal(self, PodTotal):
        self._PodTotal = PodTotal

    @property
    def NotReadyPod(self):
        return self._NotReadyPod

    @NotReadyPod.setter
    def NotReadyPod(self, NotReadyPod):
        self._NotReadyPod = NotReadyPod


    def _deserialize(self, params):
        self._PodTotal = params.get("PodTotal")
        self._NotReadyPod = params.get("NotReadyPod")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceUpgradePreCheckResult(AbstractModel):
    """某个节点升级前检查结果

    """

    def __init__(self):
        r"""
        :param _CheckPass: 检查是否通过
        :type CheckPass: bool
        :param _Items: 检查项数组
        :type Items: list of InstanceUpgradePreCheckResultItem
        :param _SinglePods: 本节点独立pod列表
        :type SinglePods: list of str
        """
        self._CheckPass = None
        self._Items = None
        self._SinglePods = None

    @property
    def CheckPass(self):
        return self._CheckPass

    @CheckPass.setter
    def CheckPass(self, CheckPass):
        self._CheckPass = CheckPass

    @property
    def Items(self):
        return self._Items

    @Items.setter
    def Items(self, Items):
        self._Items = Items

    @property
    def SinglePods(self):
        return self._SinglePods

    @SinglePods.setter
    def SinglePods(self, SinglePods):
        self._SinglePods = SinglePods


    def _deserialize(self, params):
        self._CheckPass = params.get("CheckPass")
        if params.get("Items") is not None:
            self._Items = []
            for item in params.get("Items"):
                obj = InstanceUpgradePreCheckResultItem()
                obj._deserialize(item)
                self._Items.append(obj)
        self._SinglePods = params.get("SinglePods")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceUpgradePreCheckResultItem(AbstractModel):
    """节点升级检查项结果

    """

    def __init__(self):
        r"""
        :param _Namespace: 工作负载的命名空间
        :type Namespace: str
        :param _WorkLoadKind: 工作负载类型
        :type WorkLoadKind: str
        :param _WorkLoadName: 工作负载名称
        :type WorkLoadName: str
        :param _Before: 驱逐节点前工作负载running的pod数目
        :type Before: int
        :param _After: 驱逐节点后工作负载running的pod数目
        :type After: int
        :param _Pods: 工作负载在本节点上的pod列表
        :type Pods: list of str
        """
        self._Namespace = None
        self._WorkLoadKind = None
        self._WorkLoadName = None
        self._Before = None
        self._After = None
        self._Pods = None

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def WorkLoadKind(self):
        return self._WorkLoadKind

    @WorkLoadKind.setter
    def WorkLoadKind(self, WorkLoadKind):
        self._WorkLoadKind = WorkLoadKind

    @property
    def WorkLoadName(self):
        return self._WorkLoadName

    @WorkLoadName.setter
    def WorkLoadName(self, WorkLoadName):
        self._WorkLoadName = WorkLoadName

    @property
    def Before(self):
        return self._Before

    @Before.setter
    def Before(self, Before):
        self._Before = Before

    @property
    def After(self):
        return self._After

    @After.setter
    def After(self, After):
        self._After = After

    @property
    def Pods(self):
        return self._Pods

    @Pods.setter
    def Pods(self, Pods):
        self._Pods = Pods


    def _deserialize(self, params):
        self._Namespace = params.get("Namespace")
        self._WorkLoadKind = params.get("WorkLoadKind")
        self._WorkLoadName = params.get("WorkLoadName")
        self._Before = params.get("Before")
        self._After = params.get("After")
        self._Pods = params.get("Pods")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceUpgradeProgressItem(AbstractModel):
    """某个节点的升级进度

    """

    def __init__(self):
        r"""
        :param _InstanceID: 节点instanceID
        :type InstanceID: str
        :param _LifeState: 任务生命周期
process 运行中
paused 已停止
pauing 正在停止
done  已完成
timeout 已超时
aborted 已取消
pending 还未开始
        :type LifeState: str
        :param _StartAt: 升级开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartAt: str
        :param _EndAt: 升级结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndAt: str
        :param _CheckResult: 升级前检查结果
        :type CheckResult: :class:`tencentcloud.tke.v20180525.models.InstanceUpgradePreCheckResult`
        :param _Detail: 升级步骤详情
        :type Detail: list of TaskStepInfo
        """
        self._InstanceID = None
        self._LifeState = None
        self._StartAt = None
        self._EndAt = None
        self._CheckResult = None
        self._Detail = None

    @property
    def InstanceID(self):
        return self._InstanceID

    @InstanceID.setter
    def InstanceID(self, InstanceID):
        self._InstanceID = InstanceID

    @property
    def LifeState(self):
        return self._LifeState

    @LifeState.setter
    def LifeState(self, LifeState):
        self._LifeState = LifeState

    @property
    def StartAt(self):
        return self._StartAt

    @StartAt.setter
    def StartAt(self, StartAt):
        self._StartAt = StartAt

    @property
    def EndAt(self):
        return self._EndAt

    @EndAt.setter
    def EndAt(self, EndAt):
        self._EndAt = EndAt

    @property
    def CheckResult(self):
        return self._CheckResult

    @CheckResult.setter
    def CheckResult(self, CheckResult):
        self._CheckResult = CheckResult

    @property
    def Detail(self):
        return self._Detail

    @Detail.setter
    def Detail(self, Detail):
        self._Detail = Detail


    def _deserialize(self, params):
        self._InstanceID = params.get("InstanceID")
        self._LifeState = params.get("LifeState")
        self._StartAt = params.get("StartAt")
        self._EndAt = params.get("EndAt")
        if params.get("CheckResult") is not None:
            self._CheckResult = InstanceUpgradePreCheckResult()
            self._CheckResult._deserialize(params.get("CheckResult"))
        if params.get("Detail") is not None:
            self._Detail = []
            for item in params.get("Detail"):
                obj = TaskStepInfo()
                obj._deserialize(item)
                self._Detail.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KMSConfiguration(AbstractModel):
    """kms加密参数

    """

    def __init__(self):
        r"""
        :param _KeyId: kms id
        :type KeyId: str
        :param _KmsRegion: kms 地域
        :type KmsRegion: str
        """
        self._KeyId = None
        self._KmsRegion = None

    @property
    def KeyId(self):
        return self._KeyId

    @KeyId.setter
    def KeyId(self, KeyId):
        self._KeyId = KeyId

    @property
    def KmsRegion(self):
        return self._KmsRegion

    @KmsRegion.setter
    def KmsRegion(self, KmsRegion):
        self._KmsRegion = KmsRegion


    def _deserialize(self, params):
        self._KeyId = params.get("KeyId")
        self._KmsRegion = params.get("KmsRegion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateCatalogue(AbstractModel):
    """集群巡检诊断的默认目录类型

    """

    def __init__(self):
        r"""
        :param _CatalogueLevel: 目录级别，支持参数：
first：一级目录
second：二级目录
注意：此字段可能返回 null，表示取不到有效值。
        :type CatalogueLevel: str
        :param _CatalogueName: 目录名
注意：此字段可能返回 null，表示取不到有效值。
        :type CatalogueName: str
        """
        self._CatalogueLevel = None
        self._CatalogueName = None

    @property
    def CatalogueLevel(self):
        return self._CatalogueLevel

    @CatalogueLevel.setter
    def CatalogueLevel(self, CatalogueLevel):
        self._CatalogueLevel = CatalogueLevel

    @property
    def CatalogueName(self):
        return self._CatalogueName

    @CatalogueName.setter
    def CatalogueName(self, CatalogueName):
        self._CatalogueName = CatalogueName


    def _deserialize(self, params):
        self._CatalogueLevel = params.get("CatalogueLevel")
        self._CatalogueName = params.get("CatalogueName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateDiagnostic(AbstractModel):
    """集群巡检诊断结果

    """

    def __init__(self):
        r"""
        :param _StartTime: 诊断开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param _EndTime: 诊断结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param _Catalogues: 诊断目录
注意：此字段可能返回 null，表示取不到有效值。
        :type Catalogues: list of KubeJarvisStateCatalogue
        :param _Type: 诊断类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param _Name: 诊断名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _Desc: 诊断描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Desc: str
        :param _Results: 诊断结果列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Results: list of KubeJarvisStateResultsItem
        :param _Statistics: 诊断结果统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Statistics: list of KubeJarvisStateStatistic
        """
        self._StartTime = None
        self._EndTime = None
        self._Catalogues = None
        self._Type = None
        self._Name = None
        self._Desc = None
        self._Results = None
        self._Statistics = None

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def Catalogues(self):
        return self._Catalogues

    @Catalogues.setter
    def Catalogues(self, Catalogues):
        self._Catalogues = Catalogues

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Desc(self):
        return self._Desc

    @Desc.setter
    def Desc(self, Desc):
        self._Desc = Desc

    @property
    def Results(self):
        return self._Results

    @Results.setter
    def Results(self, Results):
        self._Results = Results

    @property
    def Statistics(self):
        return self._Statistics

    @Statistics.setter
    def Statistics(self, Statistics):
        self._Statistics = Statistics


    def _deserialize(self, params):
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        if params.get("Catalogues") is not None:
            self._Catalogues = []
            for item in params.get("Catalogues"):
                obj = KubeJarvisStateCatalogue()
                obj._deserialize(item)
                self._Catalogues.append(obj)
        self._Type = params.get("Type")
        self._Name = params.get("Name")
        self._Desc = params.get("Desc")
        if params.get("Results") is not None:
            self._Results = []
            for item in params.get("Results"):
                obj = KubeJarvisStateResultsItem()
                obj._deserialize(item)
                self._Results.append(obj)
        if params.get("Statistics") is not None:
            self._Statistics = []
            for item in params.get("Statistics"):
                obj = KubeJarvisStateStatistic()
                obj._deserialize(item)
                self._Statistics.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateDiagnosticOverview(AbstractModel):
    """集群巡检诊断概览

    """

    def __init__(self):
        r"""
        :param _Catalogues: 诊断目录
注意：此字段可能返回 null，表示取不到有效值。
        :type Catalogues: list of KubeJarvisStateCatalogue
        :param _Statistics: 诊断结果统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Statistics: list of KubeJarvisStateStatistic
        """
        self._Catalogues = None
        self._Statistics = None

    @property
    def Catalogues(self):
        return self._Catalogues

    @Catalogues.setter
    def Catalogues(self, Catalogues):
        self._Catalogues = Catalogues

    @property
    def Statistics(self):
        return self._Statistics

    @Statistics.setter
    def Statistics(self, Statistics):
        self._Statistics = Statistics


    def _deserialize(self, params):
        if params.get("Catalogues") is not None:
            self._Catalogues = []
            for item in params.get("Catalogues"):
                obj = KubeJarvisStateCatalogue()
                obj._deserialize(item)
                self._Catalogues.append(obj)
        if params.get("Statistics") is not None:
            self._Statistics = []
            for item in params.get("Statistics"):
                obj = KubeJarvisStateStatistic()
                obj._deserialize(item)
                self._Statistics.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateInspectionOverview(AbstractModel):
    """集群巡检检查结果概览

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        :param _Statistics: 诊断结果统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Statistics: list of KubeJarvisStateStatistic
        :param _Diagnostics: 诊断结果详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Diagnostics: list of KubeJarvisStateDiagnosticOverview
        """
        self._ClusterId = None
        self._Statistics = None
        self._Diagnostics = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Statistics(self):
        return self._Statistics

    @Statistics.setter
    def Statistics(self, Statistics):
        self._Statistics = Statistics

    @property
    def Diagnostics(self):
        return self._Diagnostics

    @Diagnostics.setter
    def Diagnostics(self, Diagnostics):
        self._Diagnostics = Diagnostics


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("Statistics") is not None:
            self._Statistics = []
            for item in params.get("Statistics"):
                obj = KubeJarvisStateStatistic()
                obj._deserialize(item)
                self._Statistics.append(obj)
        if params.get("Diagnostics") is not None:
            self._Diagnostics = []
            for item in params.get("Diagnostics"):
                obj = KubeJarvisStateDiagnosticOverview()
                obj._deserialize(item)
                self._Diagnostics.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateInspectionResult(AbstractModel):
    """集群巡检检查结果

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        :param _StartTime: 诊断开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param _EndTime: 诊断结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param _Statistics: 诊断结果统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Statistics: list of KubeJarvisStateStatistic
        :param _Diagnostics: 诊断结果详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Diagnostics: list of KubeJarvisStateDiagnostic
        :param _Error: 查询巡检报告相关报错
注意：此字段可能返回 null，表示取不到有效值。
        :type Error: str
        """
        self._ClusterId = None
        self._StartTime = None
        self._EndTime = None
        self._Statistics = None
        self._Diagnostics = None
        self._Error = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def Statistics(self):
        return self._Statistics

    @Statistics.setter
    def Statistics(self, Statistics):
        self._Statistics = Statistics

    @property
    def Diagnostics(self):
        return self._Diagnostics

    @Diagnostics.setter
    def Diagnostics(self, Diagnostics):
        self._Diagnostics = Diagnostics

    @property
    def Error(self):
        return self._Error

    @Error.setter
    def Error(self, Error):
        self._Error = Error


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        if params.get("Statistics") is not None:
            self._Statistics = []
            for item in params.get("Statistics"):
                obj = KubeJarvisStateStatistic()
                obj._deserialize(item)
                self._Statistics.append(obj)
        if params.get("Diagnostics") is not None:
            self._Diagnostics = []
            for item in params.get("Diagnostics"):
                obj = KubeJarvisStateDiagnostic()
                obj._deserialize(item)
                self._Diagnostics.append(obj)
        self._Error = params.get("Error")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateInspectionResultsItem(AbstractModel):
    """集群巡检结果历史列表

    """

    def __init__(self):
        r"""
        :param _Name: 巡检结果名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _Statistics: 诊断结果统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Statistics: list of KubeJarvisStateStatistic
        """
        self._Name = None
        self._Statistics = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Statistics(self):
        return self._Statistics

    @Statistics.setter
    def Statistics(self, Statistics):
        self._Statistics = Statistics


    def _deserialize(self, params):
        self._Name = params.get("Name")
        if params.get("Statistics") is not None:
            self._Statistics = []
            for item in params.get("Statistics"):
                obj = KubeJarvisStateStatistic()
                obj._deserialize(item)
                self._Statistics.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateResultObjInfo(AbstractModel):
    """集群巡检诊断对象信息

    """

    def __init__(self):
        r"""
        :param _PropertyName: 对象属性名称
注意：此字段可能返回 null，表示取不到有效值。
        :type PropertyName: str
        :param _PropertyValue: 对象属性值
注意：此字段可能返回 null，表示取不到有效值。
        :type PropertyValue: str
        """
        self._PropertyName = None
        self._PropertyValue = None

    @property
    def PropertyName(self):
        return self._PropertyName

    @PropertyName.setter
    def PropertyName(self, PropertyName):
        self._PropertyName = PropertyName

    @property
    def PropertyValue(self):
        return self._PropertyValue

    @PropertyValue.setter
    def PropertyValue(self, PropertyValue):
        self._PropertyValue = PropertyValue


    def _deserialize(self, params):
        self._PropertyName = params.get("PropertyName")
        self._PropertyValue = params.get("PropertyValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateResultsItem(AbstractModel):
    """集群巡检诊断结果详情信息

    """

    def __init__(self):
        r"""
        :param _Level: 诊断结果级别
注意：此字段可能返回 null，表示取不到有效值。
        :type Level: str
        :param _ObjName: 诊断对象名
注意：此字段可能返回 null，表示取不到有效值。
        :type ObjName: str
        :param _ObjInfo: 诊断对象信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ObjInfo: list of KubeJarvisStateResultObjInfo
        :param _Title: 诊断项标题
注意：此字段可能返回 null，表示取不到有效值。
        :type Title: str
        :param _Desc: 诊断项描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Desc: str
        :param _Proposal: 诊断建议
注意：此字段可能返回 null，表示取不到有效值。
        :type Proposal: str
        :param _ProposalDocUrl: 诊断建议文档链接
注意：此字段可能返回 null，表示取不到有效值。
        :type ProposalDocUrl: str
        :param _ProposalDocName: 诊断建议文档名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ProposalDocName: str
        """
        self._Level = None
        self._ObjName = None
        self._ObjInfo = None
        self._Title = None
        self._Desc = None
        self._Proposal = None
        self._ProposalDocUrl = None
        self._ProposalDocName = None

    @property
    def Level(self):
        return self._Level

    @Level.setter
    def Level(self, Level):
        self._Level = Level

    @property
    def ObjName(self):
        return self._ObjName

    @ObjName.setter
    def ObjName(self, ObjName):
        self._ObjName = ObjName

    @property
    def ObjInfo(self):
        return self._ObjInfo

    @ObjInfo.setter
    def ObjInfo(self, ObjInfo):
        self._ObjInfo = ObjInfo

    @property
    def Title(self):
        return self._Title

    @Title.setter
    def Title(self, Title):
        self._Title = Title

    @property
    def Desc(self):
        return self._Desc

    @Desc.setter
    def Desc(self, Desc):
        self._Desc = Desc

    @property
    def Proposal(self):
        return self._Proposal

    @Proposal.setter
    def Proposal(self, Proposal):
        self._Proposal = Proposal

    @property
    def ProposalDocUrl(self):
        return self._ProposalDocUrl

    @ProposalDocUrl.setter
    def ProposalDocUrl(self, ProposalDocUrl):
        self._ProposalDocUrl = ProposalDocUrl

    @property
    def ProposalDocName(self):
        return self._ProposalDocName

    @ProposalDocName.setter
    def ProposalDocName(self, ProposalDocName):
        self._ProposalDocName = ProposalDocName


    def _deserialize(self, params):
        self._Level = params.get("Level")
        self._ObjName = params.get("ObjName")
        if params.get("ObjInfo") is not None:
            self._ObjInfo = []
            for item in params.get("ObjInfo"):
                obj = KubeJarvisStateResultObjInfo()
                obj._deserialize(item)
                self._ObjInfo.append(obj)
        self._Title = params.get("Title")
        self._Desc = params.get("Desc")
        self._Proposal = params.get("Proposal")
        self._ProposalDocUrl = params.get("ProposalDocUrl")
        self._ProposalDocName = params.get("ProposalDocName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KubeJarvisStateStatistic(AbstractModel):
    """集群巡检统计结果

    """

    def __init__(self):
        r"""
        :param _HealthyLevel: 诊断结果的健康水平
注意：此字段可能返回 null，表示取不到有效值。
        :type HealthyLevel: str
        :param _Count: 诊断结果的统计
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        """
        self._HealthyLevel = None
        self._Count = None

    @property
    def HealthyLevel(self):
        return self._HealthyLevel

    @HealthyLevel.setter
    def HealthyLevel(self, HealthyLevel):
        self._HealthyLevel = HealthyLevel

    @property
    def Count(self):
        return self._Count

    @Count.setter
    def Count(self, Count):
        self._Count = Count


    def _deserialize(self, params):
        self._HealthyLevel = params.get("HealthyLevel")
        self._Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Label(AbstractModel):
    """k8s中标签，一般以数组的方式存在

    """

    def __init__(self):
        r"""
        :param _Name: map表中的Name
        :type Name: str
        :param _Value: map表中的Value
        :type Value: str
        """
        self._Name = None
        self._Value = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, Value):
        self._Value = Value


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListClusterInspectionResultsItemsRequest(AbstractModel):
    """ListClusterInspectionResultsItems请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 目标集群ID
        :type ClusterId: str
        :param _StartTime: 查询历史结果的开始时间，Unix时间戳
        :type StartTime: str
        :param _EndTime: 查询历史结果的结束时间，默认当前距离开始时间3天，Unix时间戳
        :type EndTime: str
        """
        self._ClusterId = None
        self._StartTime = None
        self._EndTime = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListClusterInspectionResultsItemsResponse(AbstractModel):
    """ListClusterInspectionResultsItems返回参数结构体

    """

    def __init__(self):
        r"""
        :param _InspectionResultsItems: 巡检结果历史列表
注意：此字段可能返回 null，表示取不到有效值。
        :type InspectionResultsItems: list of KubeJarvisStateInspectionResultsItem
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._InspectionResultsItems = None
        self._RequestId = None

    @property
    def InspectionResultsItems(self):
        return self._InspectionResultsItems

    @InspectionResultsItems.setter
    def InspectionResultsItems(self, InspectionResultsItems):
        self._InspectionResultsItems = InspectionResultsItems

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("InspectionResultsItems") is not None:
            self._InspectionResultsItems = []
            for item in params.get("InspectionResultsItems"):
                obj = KubeJarvisStateInspectionResultsItem()
                obj._deserialize(item)
                self._InspectionResultsItems.append(obj)
        self._RequestId = params.get("RequestId")


class ListClusterInspectionResultsRequest(AbstractModel):
    """ListClusterInspectionResults请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterIds: 目标集群列表，为空查询用户所有集群

        :type ClusterIds: list of str
        :param _Hide: 隐藏的字段信息，为了减少无效的字段返回，隐藏字段不会在返回值中返回。可选值：results

        :type Hide: list of str
        :param _Name: 指定查询结果的报告名称，默认查询最新的每个集群只查询最新的一条
        :type Name: str
        """
        self._ClusterIds = None
        self._Hide = None
        self._Name = None

    @property
    def ClusterIds(self):
        return self._ClusterIds

    @ClusterIds.setter
    def ClusterIds(self, ClusterIds):
        self._ClusterIds = ClusterIds

    @property
    def Hide(self):
        return self._Hide

    @Hide.setter
    def Hide(self, Hide):
        self._Hide = Hide

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name


    def _deserialize(self, params):
        self._ClusterIds = params.get("ClusterIds")
        self._Hide = params.get("Hide")
        self._Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListClusterInspectionResultsResponse(AbstractModel):
    """ListClusterInspectionResults返回参数结构体

    """

    def __init__(self):
        r"""
        :param _InspectionResults: 集群诊断结果列表
注意：此字段可能返回 null，表示取不到有效值。
        :type InspectionResults: list of KubeJarvisStateInspectionResult
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._InspectionResults = None
        self._RequestId = None

    @property
    def InspectionResults(self):
        return self._InspectionResults

    @InspectionResults.setter
    def InspectionResults(self, InspectionResults):
        self._InspectionResults = InspectionResults

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("InspectionResults") is not None:
            self._InspectionResults = []
            for item in params.get("InspectionResults"):
                obj = KubeJarvisStateInspectionResult()
                obj._deserialize(item)
                self._InspectionResults.append(obj)
        self._RequestId = params.get("RequestId")


class LivenessOrReadinessProbe(AbstractModel):
    """健康探针

    """

    def __init__(self):
        r"""
        :param _Probe: 探针参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Probe: :class:`tencentcloud.tke.v20180525.models.Probe`
        :param _HttpGet: HttpGet检测参数
注意：此字段可能返回 null，表示取不到有效值。
        :type HttpGet: :class:`tencentcloud.tke.v20180525.models.HttpGet`
        :param _Exec: 容器内检测命令参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Exec: :class:`tencentcloud.tke.v20180525.models.Exec`
        :param _TcpSocket: TcpSocket检测的端口参数
注意：此字段可能返回 null，表示取不到有效值。
        :type TcpSocket: :class:`tencentcloud.tke.v20180525.models.TcpSocket`
        """
        self._Probe = None
        self._HttpGet = None
        self._Exec = None
        self._TcpSocket = None

    @property
    def Probe(self):
        return self._Probe

    @Probe.setter
    def Probe(self, Probe):
        self._Probe = Probe

    @property
    def HttpGet(self):
        return self._HttpGet

    @HttpGet.setter
    def HttpGet(self, HttpGet):
        self._HttpGet = HttpGet

    @property
    def Exec(self):
        return self._Exec

    @Exec.setter
    def Exec(self, Exec):
        self._Exec = Exec

    @property
    def TcpSocket(self):
        return self._TcpSocket

    @TcpSocket.setter
    def TcpSocket(self, TcpSocket):
        self._TcpSocket = TcpSocket


    def _deserialize(self, params):
        if params.get("Probe") is not None:
            self._Probe = Probe()
            self._Probe._deserialize(params.get("Probe"))
        if params.get("HttpGet") is not None:
            self._HttpGet = HttpGet()
            self._HttpGet._deserialize(params.get("HttpGet"))
        if params.get("Exec") is not None:
            self._Exec = Exec()
            self._Exec._deserialize(params.get("Exec"))
        if params.get("TcpSocket") is not None:
            self._TcpSocket = TcpSocket()
            self._TcpSocket._deserialize(params.get("TcpSocket"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LoginSettings(AbstractModel):
    """描述了实例登录相关配置与信息。

    """

    def __init__(self):
        r"""
        :param _Password: 实例登录密码。不同操作系统类型密码复杂度限制不一样，具体如下：<br><li>Linux实例密码必须8到30位，至少包括两项[a-z]，[A-Z]、[0-9] 和 [( ) \` ~ ! @ # $ % ^ & *  - + = | { } [ ] : ; ' , . ? / ]中的特殊符号。<br><li>Windows实例密码必须12到30位，至少包括三项[a-z]，[A-Z]，[0-9] 和 [( ) \` ~ ! @ # $ % ^ & * - + = | { } [ ] : ; ' , . ? /]中的特殊符号。<br><br>若不指定该参数，则由系统随机生成密码，并通过站内信方式通知到用户。
注意：此字段可能返回 null，表示取不到有效值。
        :type Password: str
        :param _KeyIds: 密钥ID列表。关联密钥后，就可以通过对应的私钥来访问实例；KeyId可通过接口[DescribeKeyPairs](https://cloud.tencent.com/document/api/213/15699)获取，密钥与密码不能同时指定，同时Windows操作系统不支持指定密钥。
注意：此字段可能返回 null，表示取不到有效值。
        :type KeyIds: list of str
        :param _KeepImageLogin: 保持镜像的原始设置。该参数与Password或KeyIds.N不能同时指定。只有使用自定义镜像、共享镜像或外部导入镜像创建实例时才能指定该参数为TRUE。取值范围：<br><li>TRUE：表示保持镜像的登录设置<br><li>FALSE：表示不保持镜像的登录设置<br><br>默认取值：FALSE。
注意：此字段可能返回 null，表示取不到有效值。
        :type KeepImageLogin: str
        """
        self._Password = None
        self._KeyIds = None
        self._KeepImageLogin = None

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def KeyIds(self):
        return self._KeyIds

    @KeyIds.setter
    def KeyIds(self, KeyIds):
        self._KeyIds = KeyIds

    @property
    def KeepImageLogin(self):
        return self._KeepImageLogin

    @KeepImageLogin.setter
    def KeepImageLogin(self, KeepImageLogin):
        self._KeepImageLogin = KeepImageLogin


    def _deserialize(self, params):
        self._Password = params.get("Password")
        self._KeyIds = params.get("KeyIds")
        self._KeepImageLogin = params.get("KeepImageLogin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ManuallyAdded(AbstractModel):
    """手动加入的节点

    """

    def __init__(self):
        r"""
        :param _Joining: 加入中的节点数量
        :type Joining: int
        :param _Initializing: 初始化中的节点数量
        :type Initializing: int
        :param _Normal: 正常的节点数量
        :type Normal: int
        :param _Total: 节点总数
        :type Total: int
        """
        self._Joining = None
        self._Initializing = None
        self._Normal = None
        self._Total = None

    @property
    def Joining(self):
        return self._Joining

    @Joining.setter
    def Joining(self, Joining):
        self._Joining = Joining

    @property
    def Initializing(self):
        return self._Initializing

    @Initializing.setter
    def Initializing(self, Initializing):
        self._Initializing = Initializing

    @property
    def Normal(self):
        return self._Normal

    @Normal.setter
    def Normal(self, Normal):
        self._Normal = Normal

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total


    def _deserialize(self, params):
        self._Joining = params.get("Joining")
        self._Initializing = params.get("Initializing")
        self._Normal = params.get("Normal")
        self._Total = params.get("Total")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterAsGroupAttributeRequest(AbstractModel):
    """ModifyClusterAsGroupAttribute请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ClusterAsGroupAttribute: 集群关联的伸缩组属性
        :type ClusterAsGroupAttribute: :class:`tencentcloud.tke.v20180525.models.ClusterAsGroupAttribute`
        """
        self._ClusterId = None
        self._ClusterAsGroupAttribute = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterAsGroupAttribute(self):
        return self._ClusterAsGroupAttribute

    @ClusterAsGroupAttribute.setter
    def ClusterAsGroupAttribute(self, ClusterAsGroupAttribute):
        self._ClusterAsGroupAttribute = ClusterAsGroupAttribute


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("ClusterAsGroupAttribute") is not None:
            self._ClusterAsGroupAttribute = ClusterAsGroupAttribute()
            self._ClusterAsGroupAttribute._deserialize(params.get("ClusterAsGroupAttribute"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterAsGroupAttributeResponse(AbstractModel):
    """ModifyClusterAsGroupAttribute返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyClusterAsGroupOptionAttributeRequest(AbstractModel):
    """ModifyClusterAsGroupOptionAttribute请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ClusterAsGroupOption: 集群弹性伸缩属性
        :type ClusterAsGroupOption: :class:`tencentcloud.tke.v20180525.models.ClusterAsGroupOption`
        """
        self._ClusterId = None
        self._ClusterAsGroupOption = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterAsGroupOption(self):
        return self._ClusterAsGroupOption

    @ClusterAsGroupOption.setter
    def ClusterAsGroupOption(self, ClusterAsGroupOption):
        self._ClusterAsGroupOption = ClusterAsGroupOption


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("ClusterAsGroupOption") is not None:
            self._ClusterAsGroupOption = ClusterAsGroupOption()
            self._ClusterAsGroupOption._deserialize(params.get("ClusterAsGroupOption"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterAsGroupOptionAttributeResponse(AbstractModel):
    """ModifyClusterAsGroupOptionAttribute返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyClusterAttributeRequest(AbstractModel):
    """ModifyClusterAttribute请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ProjectId: 集群所属项目
        :type ProjectId: int
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _ClusterDesc: 集群描述
        :type ClusterDesc: str
        :param _ClusterLevel: 集群等级
        :type ClusterLevel: str
        :param _AutoUpgradeClusterLevel: 自动变配集群等级
        :type AutoUpgradeClusterLevel: :class:`tencentcloud.tke.v20180525.models.AutoUpgradeClusterLevel`
        :param _QGPUShareEnable: 是否开启QGPU共享
        :type QGPUShareEnable: bool
        :param _ClusterProperty: 集群属性
        :type ClusterProperty: :class:`tencentcloud.tke.v20180525.models.ClusterProperty`
        """
        self._ClusterId = None
        self._ProjectId = None
        self._ClusterName = None
        self._ClusterDesc = None
        self._ClusterLevel = None
        self._AutoUpgradeClusterLevel = None
        self._QGPUShareEnable = None
        self._ClusterProperty = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel

    @property
    def QGPUShareEnable(self):
        return self._QGPUShareEnable

    @QGPUShareEnable.setter
    def QGPUShareEnable(self, QGPUShareEnable):
        self._QGPUShareEnable = QGPUShareEnable

    @property
    def ClusterProperty(self):
        return self._ClusterProperty

    @ClusterProperty.setter
    def ClusterProperty(self, ClusterProperty):
        self._ClusterProperty = ClusterProperty


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ProjectId = params.get("ProjectId")
        self._ClusterName = params.get("ClusterName")
        self._ClusterDesc = params.get("ClusterDesc")
        self._ClusterLevel = params.get("ClusterLevel")
        if params.get("AutoUpgradeClusterLevel") is not None:
            self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel()
            self._AutoUpgradeClusterLevel._deserialize(params.get("AutoUpgradeClusterLevel"))
        self._QGPUShareEnable = params.get("QGPUShareEnable")
        if params.get("ClusterProperty") is not None:
            self._ClusterProperty = ClusterProperty()
            self._ClusterProperty._deserialize(params.get("ClusterProperty"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterAttributeResponse(AbstractModel):
    """ModifyClusterAttribute返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ProjectId: 集群所属项目
注意：此字段可能返回 null，表示取不到有效值。
        :type ProjectId: int
        :param _ClusterName: 集群名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterName: str
        :param _ClusterDesc: 集群描述
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterDesc: str
        :param _ClusterLevel: 集群等级
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterLevel: str
        :param _AutoUpgradeClusterLevel: 自动变配集群等级
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoUpgradeClusterLevel: :class:`tencentcloud.tke.v20180525.models.AutoUpgradeClusterLevel`
        :param _QGPUShareEnable: 是否开启QGPU共享
注意：此字段可能返回 null，表示取不到有效值。
        :type QGPUShareEnable: bool
        :param _ClusterProperty: 集群属性
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterProperty: :class:`tencentcloud.tke.v20180525.models.ClusterProperty`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ProjectId = None
        self._ClusterName = None
        self._ClusterDesc = None
        self._ClusterLevel = None
        self._AutoUpgradeClusterLevel = None
        self._QGPUShareEnable = None
        self._ClusterProperty = None
        self._RequestId = None

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel

    @property
    def QGPUShareEnable(self):
        return self._QGPUShareEnable

    @QGPUShareEnable.setter
    def QGPUShareEnable(self, QGPUShareEnable):
        self._QGPUShareEnable = QGPUShareEnable

    @property
    def ClusterProperty(self):
        return self._ClusterProperty

    @ClusterProperty.setter
    def ClusterProperty(self, ClusterProperty):
        self._ClusterProperty = ClusterProperty

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ProjectId = params.get("ProjectId")
        self._ClusterName = params.get("ClusterName")
        self._ClusterDesc = params.get("ClusterDesc")
        self._ClusterLevel = params.get("ClusterLevel")
        if params.get("AutoUpgradeClusterLevel") is not None:
            self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel()
            self._AutoUpgradeClusterLevel._deserialize(params.get("AutoUpgradeClusterLevel"))
        self._QGPUShareEnable = params.get("QGPUShareEnable")
        if params.get("ClusterProperty") is not None:
            self._ClusterProperty = ClusterProperty()
            self._ClusterProperty._deserialize(params.get("ClusterProperty"))
        self._RequestId = params.get("RequestId")


class ModifyClusterAuthenticationOptionsRequest(AbstractModel):
    """ModifyClusterAuthenticationOptions请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ServiceAccounts: ServiceAccount认证配置
        :type ServiceAccounts: :class:`tencentcloud.tke.v20180525.models.ServiceAccountAuthenticationOptions`
        :param _OIDCConfig: OIDC认证配置
        :type OIDCConfig: :class:`tencentcloud.tke.v20180525.models.OIDCConfigAuthenticationOptions`
        """
        self._ClusterId = None
        self._ServiceAccounts = None
        self._OIDCConfig = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ServiceAccounts(self):
        return self._ServiceAccounts

    @ServiceAccounts.setter
    def ServiceAccounts(self, ServiceAccounts):
        self._ServiceAccounts = ServiceAccounts

    @property
    def OIDCConfig(self):
        return self._OIDCConfig

    @OIDCConfig.setter
    def OIDCConfig(self, OIDCConfig):
        self._OIDCConfig = OIDCConfig


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("ServiceAccounts") is not None:
            self._ServiceAccounts = ServiceAccountAuthenticationOptions()
            self._ServiceAccounts._deserialize(params.get("ServiceAccounts"))
        if params.get("OIDCConfig") is not None:
            self._OIDCConfig = OIDCConfigAuthenticationOptions()
            self._OIDCConfig._deserialize(params.get("OIDCConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterAuthenticationOptionsResponse(AbstractModel):
    """ModifyClusterAuthenticationOptions返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyClusterEndpointSPRequest(AbstractModel):
    """ModifyClusterEndpointSP请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _SecurityPolicies: 安全策略放通单个IP或CIDR(例如: "192.168.1.0/24",默认为拒绝所有)
        :type SecurityPolicies: list of str
        :param _SecurityGroup: 修改外网访问安全组
        :type SecurityGroup: str
        """
        self._ClusterId = None
        self._SecurityPolicies = None
        self._SecurityGroup = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SecurityPolicies(self):
        return self._SecurityPolicies

    @SecurityPolicies.setter
    def SecurityPolicies(self, SecurityPolicies):
        self._SecurityPolicies = SecurityPolicies

    @property
    def SecurityGroup(self):
        return self._SecurityGroup

    @SecurityGroup.setter
    def SecurityGroup(self, SecurityGroup):
        self._SecurityGroup = SecurityGroup


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._SecurityPolicies = params.get("SecurityPolicies")
        self._SecurityGroup = params.get("SecurityGroup")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterEndpointSPResponse(AbstractModel):
    """ModifyClusterEndpointSP返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyClusterNodePoolRequest(AbstractModel):
    """ModifyClusterNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodePoolId: 节点池ID
        :type NodePoolId: str
        :param _Name: 名称
        :type Name: str
        :param _MaxNodesNum: 最大节点数
        :type MaxNodesNum: int
        :param _MinNodesNum: 最小节点数
        :type MinNodesNum: int
        :param _Labels: 标签
        :type Labels: list of Label
        :param _Taints: 污点
        :type Taints: list of Taint
        :param _EnableAutoscale: 是否开启伸缩
        :type EnableAutoscale: bool
        :param _OsName: 操作系统名称
        :type OsName: str
        :param _OsCustomizeType: 镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
        :type OsCustomizeType: str
        :param _GPUArgs: GPU驱动版本，CUDA版本，cuDNN版本以及是否启用MIG特性
        :type GPUArgs: :class:`tencentcloud.tke.v20180525.models.GPUArgs`
        :param _UserScript: base64编码后的自定义脚本
        :type UserScript: str
        :param _IgnoreExistedNode: 更新label和taint时忽略存量节点
        :type IgnoreExistedNode: bool
        :param _ExtraArgs: 节点自定义参数
        :type ExtraArgs: :class:`tencentcloud.tke.v20180525.models.InstanceExtraArgs`
        :param _Tags: 资源标签
        :type Tags: list of Tag
        :param _Unschedulable: 设置加入的节点是否参与调度，默认值为0，表示参与调度；非0表示不参与调度, 待节点初始化完成之后, 可执行kubectl uncordon nodename使node加入调度.
        :type Unschedulable: int
        :param _DeletionProtection: 删除保护开关
        :type DeletionProtection: bool
        :param _DockerGraphPath: dockerd --graph 指定值, 默认为 /var/lib/docker
        :type DockerGraphPath: str
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._Name = None
        self._MaxNodesNum = None
        self._MinNodesNum = None
        self._Labels = None
        self._Taints = None
        self._EnableAutoscale = None
        self._OsName = None
        self._OsCustomizeType = None
        self._GPUArgs = None
        self._UserScript = None
        self._IgnoreExistedNode = None
        self._ExtraArgs = None
        self._Tags = None
        self._Unschedulable = None
        self._DeletionProtection = None
        self._DockerGraphPath = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def MaxNodesNum(self):
        return self._MaxNodesNum

    @MaxNodesNum.setter
    def MaxNodesNum(self, MaxNodesNum):
        self._MaxNodesNum = MaxNodesNum

    @property
    def MinNodesNum(self):
        return self._MinNodesNum

    @MinNodesNum.setter
    def MinNodesNum(self, MinNodesNum):
        self._MinNodesNum = MinNodesNum

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints

    @property
    def EnableAutoscale(self):
        return self._EnableAutoscale

    @EnableAutoscale.setter
    def EnableAutoscale(self, EnableAutoscale):
        self._EnableAutoscale = EnableAutoscale

    @property
    def OsName(self):
        return self._OsName

    @OsName.setter
    def OsName(self, OsName):
        self._OsName = OsName

    @property
    def OsCustomizeType(self):
        return self._OsCustomizeType

    @OsCustomizeType.setter
    def OsCustomizeType(self, OsCustomizeType):
        self._OsCustomizeType = OsCustomizeType

    @property
    def GPUArgs(self):
        return self._GPUArgs

    @GPUArgs.setter
    def GPUArgs(self, GPUArgs):
        self._GPUArgs = GPUArgs

    @property
    def UserScript(self):
        return self._UserScript

    @UserScript.setter
    def UserScript(self, UserScript):
        self._UserScript = UserScript

    @property
    def IgnoreExistedNode(self):
        return self._IgnoreExistedNode

    @IgnoreExistedNode.setter
    def IgnoreExistedNode(self, IgnoreExistedNode):
        self._IgnoreExistedNode = IgnoreExistedNode

    @property
    def ExtraArgs(self):
        return self._ExtraArgs

    @ExtraArgs.setter
    def ExtraArgs(self, ExtraArgs):
        self._ExtraArgs = ExtraArgs

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def Unschedulable(self):
        return self._Unschedulable

    @Unschedulable.setter
    def Unschedulable(self, Unschedulable):
        self._Unschedulable = Unschedulable

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection

    @property
    def DockerGraphPath(self):
        return self._DockerGraphPath

    @DockerGraphPath.setter
    def DockerGraphPath(self, DockerGraphPath):
        self._DockerGraphPath = DockerGraphPath


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._Name = params.get("Name")
        self._MaxNodesNum = params.get("MaxNodesNum")
        self._MinNodesNum = params.get("MinNodesNum")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        self._EnableAutoscale = params.get("EnableAutoscale")
        self._OsName = params.get("OsName")
        self._OsCustomizeType = params.get("OsCustomizeType")
        if params.get("GPUArgs") is not None:
            self._GPUArgs = GPUArgs()
            self._GPUArgs._deserialize(params.get("GPUArgs"))
        self._UserScript = params.get("UserScript")
        self._IgnoreExistedNode = params.get("IgnoreExistedNode")
        if params.get("ExtraArgs") is not None:
            self._ExtraArgs = InstanceExtraArgs()
            self._ExtraArgs._deserialize(params.get("ExtraArgs"))
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._Unschedulable = params.get("Unschedulable")
        self._DeletionProtection = params.get("DeletionProtection")
        self._DockerGraphPath = params.get("DockerGraphPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterNodePoolResponse(AbstractModel):
    """ModifyClusterNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyClusterVirtualNodePoolRequest(AbstractModel):
    """ModifyClusterVirtualNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _NodePoolId: 节点池ID
        :type NodePoolId: str
        :param _Name: 节点池名称
        :type Name: str
        :param _SecurityGroupIds: 安全组ID列表
        :type SecurityGroupIds: list of str
        :param _Labels: 虚拟节点label
        :type Labels: list of Label
        :param _Taints: 虚拟节点taint
        :type Taints: list of Taint
        :param _DeletionProtection: 删除保护开关
        :type DeletionProtection: bool
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._Name = None
        self._SecurityGroupIds = None
        self._Labels = None
        self._Taints = None
        self._DeletionProtection = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._Name = params.get("Name")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        self._DeletionProtection = params.get("DeletionProtection")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterVirtualNodePoolResponse(AbstractModel):
    """ModifyClusterVirtualNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyNodePoolDesiredCapacityAboutAsgRequest(AbstractModel):
    """ModifyNodePoolDesiredCapacityAboutAsg请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _DesiredCapacity: 节点池所关联的伸缩组的期望实例数
        :type DesiredCapacity: int
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._DesiredCapacity = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def DesiredCapacity(self):
        return self._DesiredCapacity

    @DesiredCapacity.setter
    def DesiredCapacity(self, DesiredCapacity):
        self._DesiredCapacity = DesiredCapacity


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._DesiredCapacity = params.get("DesiredCapacity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNodePoolDesiredCapacityAboutAsgResponse(AbstractModel):
    """ModifyNodePoolDesiredCapacityAboutAsg返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyNodePoolInstanceTypesRequest(AbstractModel):
    """ModifyNodePoolInstanceTypes请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _InstanceTypes: 机型列表
        :type InstanceTypes: list of str
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._InstanceTypes = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def InstanceTypes(self):
        return self._InstanceTypes

    @InstanceTypes.setter
    def InstanceTypes(self, InstanceTypes):
        self._InstanceTypes = InstanceTypes


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._InstanceTypes = params.get("InstanceTypes")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNodePoolInstanceTypesResponse(AbstractModel):
    """ModifyNodePoolInstanceTypes返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusAgentExternalLabelsRequest(AbstractModel):
    """ModifyPrometheusAgentExternalLabels请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _ExternalLabels: 新的external_labels
        :type ExternalLabels: list of Label
        """
        self._InstanceId = None
        self._ClusterId = None
        self._ExternalLabels = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ExternalLabels(self):
        return self._ExternalLabels

    @ExternalLabels.setter
    def ExternalLabels(self, ExternalLabels):
        self._ExternalLabels = ExternalLabels


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._ClusterId = params.get("ClusterId")
        if params.get("ExternalLabels") is not None:
            self._ExternalLabels = []
            for item in params.get("ExternalLabels"):
                obj = Label()
                obj._deserialize(item)
                self._ExternalLabels.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusAgentExternalLabelsResponse(AbstractModel):
    """ModifyPrometheusAgentExternalLabels返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusAlertPolicyRequest(AbstractModel):
    """ModifyPrometheusAlertPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _AlertRule: 告警配置
        :type AlertRule: :class:`tencentcloud.tke.v20180525.models.PrometheusAlertPolicyItem`
        """
        self._InstanceId = None
        self._AlertRule = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def AlertRule(self):
        return self._AlertRule

    @AlertRule.setter
    def AlertRule(self, AlertRule):
        self._AlertRule = AlertRule


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("AlertRule") is not None:
            self._AlertRule = PrometheusAlertPolicyItem()
            self._AlertRule._deserialize(params.get("AlertRule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusAlertPolicyResponse(AbstractModel):
    """ModifyPrometheusAlertPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusAlertRuleRequest(AbstractModel):
    """ModifyPrometheusAlertRule请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _AlertRule: 告警配置
        :type AlertRule: :class:`tencentcloud.tke.v20180525.models.PrometheusAlertRuleDetail`
        """
        self._InstanceId = None
        self._AlertRule = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def AlertRule(self):
        return self._AlertRule

    @AlertRule.setter
    def AlertRule(self, AlertRule):
        self._AlertRule = AlertRule


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("AlertRule") is not None:
            self._AlertRule = PrometheusAlertRuleDetail()
            self._AlertRule._deserialize(params.get("AlertRule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusAlertRuleResponse(AbstractModel):
    """ModifyPrometheusAlertRule返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusConfigRequest(AbstractModel):
    """ModifyPrometheusConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _ServiceMonitors: ServiceMonitors配置
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: PodMonitors配置
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: prometheus原生Job配置
        :type RawJobs: list of PrometheusConfigItem
        """
        self._InstanceId = None
        self._ClusterType = None
        self._ClusterId = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusConfigResponse(AbstractModel):
    """ModifyPrometheusConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusGlobalNotificationRequest(AbstractModel):
    """ModifyPrometheusGlobalNotification请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _Notification: 告警通知渠道
        :type Notification: :class:`tencentcloud.tke.v20180525.models.PrometheusNotificationItem`
        """
        self._InstanceId = None
        self._Notification = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Notification(self):
        return self._Notification

    @Notification.setter
    def Notification(self, Notification):
        self._Notification = Notification


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        if params.get("Notification") is not None:
            self._Notification = PrometheusNotificationItem()
            self._Notification._deserialize(params.get("Notification"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusGlobalNotificationResponse(AbstractModel):
    """ModifyPrometheusGlobalNotification返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusRecordRuleYamlRequest(AbstractModel):
    """ModifyPrometheusRecordRuleYaml请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Name: 聚合实例名称
        :type Name: str
        :param _Content: 新的内容
        :type Content: str
        """
        self._InstanceId = None
        self._Name = None
        self._Content = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Content(self):
        return self._Content

    @Content.setter
    def Content(self, Content):
        self._Content = Content


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Name = params.get("Name")
        self._Content = params.get("Content")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusRecordRuleYamlResponse(AbstractModel):
    """ModifyPrometheusRecordRuleYaml返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusTempRequest(AbstractModel):
    """ModifyPrometheusTemp请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        :param _Template: 修改内容
        :type Template: :class:`tencentcloud.tke.v20180525.models.PrometheusTempModify`
        """
        self._TemplateId = None
        self._Template = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        if params.get("Template") is not None:
            self._Template = PrometheusTempModify()
            self._Template._deserialize(params.get("Template"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusTempResponse(AbstractModel):
    """ModifyPrometheusTemp返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ModifyPrometheusTemplateRequest(AbstractModel):
    """ModifyPrometheusTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        :param _Template: 修改内容
        :type Template: :class:`tencentcloud.tke.v20180525.models.PrometheusTemplateModify`
        """
        self._TemplateId = None
        self._Template = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        if params.get("Template") is not None:
            self._Template = PrometheusTemplateModify()
            self._Template._deserialize(params.get("Template"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPrometheusTemplateResponse(AbstractModel):
    """ModifyPrometheusTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class NfsVolume(AbstractModel):
    """EKS Instance Nfs Volume

    """

    def __init__(self):
        r"""
        :param _Name: nfs volume 数据卷名称
        :type Name: str
        :param _Server: NFS 服务器地址
        :type Server: str
        :param _Path: NFS 数据卷路径
        :type Path: str
        :param _ReadOnly: 默认为 False
        :type ReadOnly: bool
        """
        self._Name = None
        self._Server = None
        self._Path = None
        self._ReadOnly = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Server(self):
        return self._Server

    @Server.setter
    def Server(self, Server):
        self._Server = Server

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path

    @property
    def ReadOnly(self):
        return self._ReadOnly

    @ReadOnly.setter
    def ReadOnly(self, ReadOnly):
        self._ReadOnly = ReadOnly


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Server = params.get("Server")
        self._Path = params.get("Path")
        self._ReadOnly = params.get("ReadOnly")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeCountSummary(AbstractModel):
    """节点统计列表

    """

    def __init__(self):
        r"""
        :param _ManuallyAdded: 手动管理的节点
注意：此字段可能返回 null，表示取不到有效值。
        :type ManuallyAdded: :class:`tencentcloud.tke.v20180525.models.ManuallyAdded`
        :param _AutoscalingAdded: 自动管理的节点
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoscalingAdded: :class:`tencentcloud.tke.v20180525.models.AutoscalingAdded`
        """
        self._ManuallyAdded = None
        self._AutoscalingAdded = None

    @property
    def ManuallyAdded(self):
        return self._ManuallyAdded

    @ManuallyAdded.setter
    def ManuallyAdded(self, ManuallyAdded):
        self._ManuallyAdded = ManuallyAdded

    @property
    def AutoscalingAdded(self):
        return self._AutoscalingAdded

    @AutoscalingAdded.setter
    def AutoscalingAdded(self, AutoscalingAdded):
        self._AutoscalingAdded = AutoscalingAdded


    def _deserialize(self, params):
        if params.get("ManuallyAdded") is not None:
            self._ManuallyAdded = ManuallyAdded()
            self._ManuallyAdded._deserialize(params.get("ManuallyAdded"))
        if params.get("AutoscalingAdded") is not None:
            self._AutoscalingAdded = AutoscalingAdded()
            self._AutoscalingAdded._deserialize(params.get("AutoscalingAdded"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodePool(AbstractModel):
    """节点池描述

    """

    def __init__(self):
        r"""
        :param _NodePoolId: NodePoolId 资源池id
        :type NodePoolId: str
        :param _Name: Name 资源池名称
        :type Name: str
        :param _ClusterInstanceId: ClusterInstanceId 集群实例id
        :type ClusterInstanceId: str
        :param _LifeState: LifeState 状态，当前节点池生命周期状态包括：creating，normal，updating，deleting，deleted
        :type LifeState: str
        :param _LaunchConfigurationId: LaunchConfigurationId 配置
        :type LaunchConfigurationId: str
        :param _AutoscalingGroupId: AutoscalingGroupId 分组id
        :type AutoscalingGroupId: str
        :param _Labels: Labels 标签
        :type Labels: list of Label
        :param _Taints: Taints 污点标记
        :type Taints: list of Taint
        :param _NodeCountSummary: NodeCountSummary 节点列表
        :type NodeCountSummary: :class:`tencentcloud.tke.v20180525.models.NodeCountSummary`
        :param _AutoscalingGroupStatus: 状态信息
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoscalingGroupStatus: str
        :param _MaxNodesNum: 最大节点数量
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxNodesNum: int
        :param _MinNodesNum: 最小节点数量
注意：此字段可能返回 null，表示取不到有效值。
        :type MinNodesNum: int
        :param _DesiredNodesNum: 期望的节点数量
注意：此字段可能返回 null，表示取不到有效值。
        :type DesiredNodesNum: int
        :param _NodePoolOs: 节点池osName
注意：此字段可能返回 null，表示取不到有效值。
        :type NodePoolOs: str
        :param _OsCustomizeType: 容器的镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
注意：此字段可能返回 null，表示取不到有效值。
        :type OsCustomizeType: str
        :param _ImageId: 镜像id
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageId: str
        :param _DesiredPodNum: 集群属于节点podCIDR大小自定义模式时，节点池需要带上pod数量属性
注意：此字段可能返回 null，表示取不到有效值。
        :type DesiredPodNum: int
        :param _UserScript: 用户自定义脚本
注意：此字段可能返回 null，表示取不到有效值。
        :type UserScript: str
        :param _Tags: 资源标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param _DeletionProtection: 删除保护开关
注意：此字段可能返回 null，表示取不到有效值。
        :type DeletionProtection: bool
        """
        self._NodePoolId = None
        self._Name = None
        self._ClusterInstanceId = None
        self._LifeState = None
        self._LaunchConfigurationId = None
        self._AutoscalingGroupId = None
        self._Labels = None
        self._Taints = None
        self._NodeCountSummary = None
        self._AutoscalingGroupStatus = None
        self._MaxNodesNum = None
        self._MinNodesNum = None
        self._DesiredNodesNum = None
        self._NodePoolOs = None
        self._OsCustomizeType = None
        self._ImageId = None
        self._DesiredPodNum = None
        self._UserScript = None
        self._Tags = None
        self._DeletionProtection = None

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def ClusterInstanceId(self):
        return self._ClusterInstanceId

    @ClusterInstanceId.setter
    def ClusterInstanceId(self, ClusterInstanceId):
        self._ClusterInstanceId = ClusterInstanceId

    @property
    def LifeState(self):
        return self._LifeState

    @LifeState.setter
    def LifeState(self, LifeState):
        self._LifeState = LifeState

    @property
    def LaunchConfigurationId(self):
        return self._LaunchConfigurationId

    @LaunchConfigurationId.setter
    def LaunchConfigurationId(self, LaunchConfigurationId):
        self._LaunchConfigurationId = LaunchConfigurationId

    @property
    def AutoscalingGroupId(self):
        return self._AutoscalingGroupId

    @AutoscalingGroupId.setter
    def AutoscalingGroupId(self, AutoscalingGroupId):
        self._AutoscalingGroupId = AutoscalingGroupId

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints

    @property
    def NodeCountSummary(self):
        return self._NodeCountSummary

    @NodeCountSummary.setter
    def NodeCountSummary(self, NodeCountSummary):
        self._NodeCountSummary = NodeCountSummary

    @property
    def AutoscalingGroupStatus(self):
        return self._AutoscalingGroupStatus

    @AutoscalingGroupStatus.setter
    def AutoscalingGroupStatus(self, AutoscalingGroupStatus):
        self._AutoscalingGroupStatus = AutoscalingGroupStatus

    @property
    def MaxNodesNum(self):
        return self._MaxNodesNum

    @MaxNodesNum.setter
    def MaxNodesNum(self, MaxNodesNum):
        self._MaxNodesNum = MaxNodesNum

    @property
    def MinNodesNum(self):
        return self._MinNodesNum

    @MinNodesNum.setter
    def MinNodesNum(self, MinNodesNum):
        self._MinNodesNum = MinNodesNum

    @property
    def DesiredNodesNum(self):
        return self._DesiredNodesNum

    @DesiredNodesNum.setter
    def DesiredNodesNum(self, DesiredNodesNum):
        self._DesiredNodesNum = DesiredNodesNum

    @property
    def NodePoolOs(self):
        return self._NodePoolOs

    @NodePoolOs.setter
    def NodePoolOs(self, NodePoolOs):
        self._NodePoolOs = NodePoolOs

    @property
    def OsCustomizeType(self):
        return self._OsCustomizeType

    @OsCustomizeType.setter
    def OsCustomizeType(self, OsCustomizeType):
        self._OsCustomizeType = OsCustomizeType

    @property
    def ImageId(self):
        return self._ImageId

    @ImageId.setter
    def ImageId(self, ImageId):
        self._ImageId = ImageId

    @property
    def DesiredPodNum(self):
        return self._DesiredPodNum

    @DesiredPodNum.setter
    def DesiredPodNum(self, DesiredPodNum):
        self._DesiredPodNum = DesiredPodNum

    @property
    def UserScript(self):
        return self._UserScript

    @UserScript.setter
    def UserScript(self, UserScript):
        self._UserScript = UserScript

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags

    @property
    def DeletionProtection(self):
        return self._DeletionProtection

    @DeletionProtection.setter
    def DeletionProtection(self, DeletionProtection):
        self._DeletionProtection = DeletionProtection


    def _deserialize(self, params):
        self._NodePoolId = params.get("NodePoolId")
        self._Name = params.get("Name")
        self._ClusterInstanceId = params.get("ClusterInstanceId")
        self._LifeState = params.get("LifeState")
        self._LaunchConfigurationId = params.get("LaunchConfigurationId")
        self._AutoscalingGroupId = params.get("AutoscalingGroupId")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        if params.get("NodeCountSummary") is not None:
            self._NodeCountSummary = NodeCountSummary()
            self._NodeCountSummary._deserialize(params.get("NodeCountSummary"))
        self._AutoscalingGroupStatus = params.get("AutoscalingGroupStatus")
        self._MaxNodesNum = params.get("MaxNodesNum")
        self._MinNodesNum = params.get("MinNodesNum")
        self._DesiredNodesNum = params.get("DesiredNodesNum")
        self._NodePoolOs = params.get("NodePoolOs")
        self._OsCustomizeType = params.get("OsCustomizeType")
        self._ImageId = params.get("ImageId")
        self._DesiredPodNum = params.get("DesiredPodNum")
        self._UserScript = params.get("UserScript")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self._Tags.append(obj)
        self._DeletionProtection = params.get("DeletionProtection")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodePoolOption(AbstractModel):
    """加入存量节点时的节点池选项

    """

    def __init__(self):
        r"""
        :param _AddToNodePool: 是否加入节点池
        :type AddToNodePool: bool
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _InheritConfigurationFromNodePool: 是否继承节点池相关配置
        :type InheritConfigurationFromNodePool: bool
        """
        self._AddToNodePool = None
        self._NodePoolId = None
        self._InheritConfigurationFromNodePool = None

    @property
    def AddToNodePool(self):
        return self._AddToNodePool

    @AddToNodePool.setter
    def AddToNodePool(self, AddToNodePool):
        self._AddToNodePool = AddToNodePool

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def InheritConfigurationFromNodePool(self):
        return self._InheritConfigurationFromNodePool

    @InheritConfigurationFromNodePool.setter
    def InheritConfigurationFromNodePool(self, InheritConfigurationFromNodePool):
        self._InheritConfigurationFromNodePool = InheritConfigurationFromNodePool


    def _deserialize(self, params):
        self._AddToNodePool = params.get("AddToNodePool")
        self._NodePoolId = params.get("NodePoolId")
        self._InheritConfigurationFromNodePool = params.get("InheritConfigurationFromNodePool")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OIDCConfigAuthenticationOptions(AbstractModel):
    """OIDC认证相关配置

    """

    def __init__(self):
        r"""
        :param _AutoCreateOIDCConfig: 创建身份提供商
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoCreateOIDCConfig: bool
        :param _AutoCreateClientId: 创建身份提供商的ClientId
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoCreateClientId: list of str
        :param _AutoInstallPodIdentityWebhookAddon: 创建PodIdentityWebhook组件
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoInstallPodIdentityWebhookAddon: bool
        """
        self._AutoCreateOIDCConfig = None
        self._AutoCreateClientId = None
        self._AutoInstallPodIdentityWebhookAddon = None

    @property
    def AutoCreateOIDCConfig(self):
        return self._AutoCreateOIDCConfig

    @AutoCreateOIDCConfig.setter
    def AutoCreateOIDCConfig(self, AutoCreateOIDCConfig):
        self._AutoCreateOIDCConfig = AutoCreateOIDCConfig

    @property
    def AutoCreateClientId(self):
        return self._AutoCreateClientId

    @AutoCreateClientId.setter
    def AutoCreateClientId(self, AutoCreateClientId):
        self._AutoCreateClientId = AutoCreateClientId

    @property
    def AutoInstallPodIdentityWebhookAddon(self):
        return self._AutoInstallPodIdentityWebhookAddon

    @AutoInstallPodIdentityWebhookAddon.setter
    def AutoInstallPodIdentityWebhookAddon(self, AutoInstallPodIdentityWebhookAddon):
        self._AutoInstallPodIdentityWebhookAddon = AutoInstallPodIdentityWebhookAddon


    def _deserialize(self, params):
        self._AutoCreateOIDCConfig = params.get("AutoCreateOIDCConfig")
        self._AutoCreateClientId = params.get("AutoCreateClientId")
        self._AutoInstallPodIdentityWebhookAddon = params.get("AutoInstallPodIdentityWebhookAddon")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PendingRelease(AbstractModel):
    """应用市场安装的Pending应用

    """

    def __init__(self):
        r"""
        :param _Condition: 应用状态详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Condition: str
        :param _CreatedTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreatedTime: str
        :param _ID: 应用ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ID: str
        :param _Name: 应用名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _Namespace: 应用命名空间
注意：此字段可能返回 null，表示取不到有效值。
        :type Namespace: str
        :param _Status: 应用状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _UpdatedTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedTime: str
        """
        self._Condition = None
        self._CreatedTime = None
        self._ID = None
        self._Name = None
        self._Namespace = None
        self._Status = None
        self._UpdatedTime = None

    @property
    def Condition(self):
        return self._Condition

    @Condition.setter
    def Condition(self, Condition):
        self._Condition = Condition

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def UpdatedTime(self):
        return self._UpdatedTime

    @UpdatedTime.setter
    def UpdatedTime(self, UpdatedTime):
        self._UpdatedTime = UpdatedTime


    def _deserialize(self, params):
        self._Condition = params.get("Condition")
        self._CreatedTime = params.get("CreatedTime")
        self._ID = params.get("ID")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Status = params.get("Status")
        self._UpdatedTime = params.get("UpdatedTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodLimitsByType(AbstractModel):
    """某机型可支持的最大 VPC-CNI 模式的 Pod 数量

    """

    def __init__(self):
        r"""
        :param _TKERouteENINonStaticIP: TKE共享网卡非固定IP模式可支持的Pod数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TKERouteENINonStaticIP: int
        :param _TKERouteENIStaticIP: TKE共享网卡固定IP模式可支持的Pod数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TKERouteENIStaticIP: int
        :param _TKEDirectENI: TKE独立网卡模式可支持的Pod数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TKEDirectENI: int
        """
        self._TKERouteENINonStaticIP = None
        self._TKERouteENIStaticIP = None
        self._TKEDirectENI = None

    @property
    def TKERouteENINonStaticIP(self):
        return self._TKERouteENINonStaticIP

    @TKERouteENINonStaticIP.setter
    def TKERouteENINonStaticIP(self, TKERouteENINonStaticIP):
        self._TKERouteENINonStaticIP = TKERouteENINonStaticIP

    @property
    def TKERouteENIStaticIP(self):
        return self._TKERouteENIStaticIP

    @TKERouteENIStaticIP.setter
    def TKERouteENIStaticIP(self, TKERouteENIStaticIP):
        self._TKERouteENIStaticIP = TKERouteENIStaticIP

    @property
    def TKEDirectENI(self):
        return self._TKEDirectENI

    @TKEDirectENI.setter
    def TKEDirectENI(self, TKEDirectENI):
        self._TKEDirectENI = TKEDirectENI


    def _deserialize(self, params):
        self._TKERouteENINonStaticIP = params.get("TKERouteENINonStaticIP")
        self._TKERouteENIStaticIP = params.get("TKERouteENIStaticIP")
        self._TKEDirectENI = params.get("TKEDirectENI")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodLimitsInstance(AbstractModel):
    """机型信息和其可支持的最大VPC-CNI模式Pod数量信息

    """

    def __init__(self):
        r"""
        :param _Zone: 机型所在可用区
注意：此字段可能返回 null，表示取不到有效值。
        :type Zone: str
        :param _InstanceFamily: 机型所属机型族
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceFamily: str
        :param _InstanceType: 实例机型名称
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceType: str
        :param _PodLimits: 机型可支持的最大VPC-CNI模式Pod数量信息
注意：此字段可能返回 null，表示取不到有效值。
        :type PodLimits: :class:`tencentcloud.tke.v20180525.models.PodLimitsByType`
        """
        self._Zone = None
        self._InstanceFamily = None
        self._InstanceType = None
        self._PodLimits = None

    @property
    def Zone(self):
        return self._Zone

    @Zone.setter
    def Zone(self, Zone):
        self._Zone = Zone

    @property
    def InstanceFamily(self):
        return self._InstanceFamily

    @InstanceFamily.setter
    def InstanceFamily(self, InstanceFamily):
        self._InstanceFamily = InstanceFamily

    @property
    def InstanceType(self):
        return self._InstanceType

    @InstanceType.setter
    def InstanceType(self, InstanceType):
        self._InstanceType = InstanceType

    @property
    def PodLimits(self):
        return self._PodLimits

    @PodLimits.setter
    def PodLimits(self, PodLimits):
        self._PodLimits = PodLimits


    def _deserialize(self, params):
        self._Zone = params.get("Zone")
        self._InstanceFamily = params.get("InstanceFamily")
        self._InstanceType = params.get("InstanceType")
        if params.get("PodLimits") is not None:
            self._PodLimits = PodLimitsByType()
            self._PodLimits._deserialize(params.get("PodLimits"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Probe(AbstractModel):
    """健康检查探测参数

    """

    def __init__(self):
        r"""
        :param _InitialDelaySeconds: Number of seconds after the container has started before liveness probes are initiated.
注意：此字段可能返回 null，表示取不到有效值。
        :type InitialDelaySeconds: int
        :param _TimeoutSeconds: Number of seconds after which the probe times out.
Defaults to 1 second. Minimum value is 1.
注意：此字段可能返回 null，表示取不到有效值。
        :type TimeoutSeconds: int
        :param _PeriodSeconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1.
注意：此字段可能返回 null，表示取不到有效值。
        :type PeriodSeconds: int
        :param _SuccessThreshold: Minimum consecutive successes for the probe to be considered successful after having failed.Defaults to 1. Must be 1 for liveness. Minimum value is 1.
注意：此字段可能返回 null，表示取不到有效值。
        :type SuccessThreshold: int
        :param _FailureThreshold: Minimum consecutive failures for the probe to be considered failed after having succeeded.Defaults to 3. Minimum value is 1.
注意：此字段可能返回 null，表示取不到有效值。
        :type FailureThreshold: int
        """
        self._InitialDelaySeconds = None
        self._TimeoutSeconds = None
        self._PeriodSeconds = None
        self._SuccessThreshold = None
        self._FailureThreshold = None

    @property
    def InitialDelaySeconds(self):
        return self._InitialDelaySeconds

    @InitialDelaySeconds.setter
    def InitialDelaySeconds(self, InitialDelaySeconds):
        self._InitialDelaySeconds = InitialDelaySeconds

    @property
    def TimeoutSeconds(self):
        return self._TimeoutSeconds

    @TimeoutSeconds.setter
    def TimeoutSeconds(self, TimeoutSeconds):
        self._TimeoutSeconds = TimeoutSeconds

    @property
    def PeriodSeconds(self):
        return self._PeriodSeconds

    @PeriodSeconds.setter
    def PeriodSeconds(self, PeriodSeconds):
        self._PeriodSeconds = PeriodSeconds

    @property
    def SuccessThreshold(self):
        return self._SuccessThreshold

    @SuccessThreshold.setter
    def SuccessThreshold(self, SuccessThreshold):
        self._SuccessThreshold = SuccessThreshold

    @property
    def FailureThreshold(self):
        return self._FailureThreshold

    @FailureThreshold.setter
    def FailureThreshold(self, FailureThreshold):
        self._FailureThreshold = FailureThreshold


    def _deserialize(self, params):
        self._InitialDelaySeconds = params.get("InitialDelaySeconds")
        self._TimeoutSeconds = params.get("TimeoutSeconds")
        self._PeriodSeconds = params.get("PeriodSeconds")
        self._SuccessThreshold = params.get("SuccessThreshold")
        self._FailureThreshold = params.get("FailureThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAgentInfo(AbstractModel):
    """托管Prometheus agent信息

    """

    def __init__(self):
        r"""
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _Describe: 备注
        :type Describe: str
        """
        self._ClusterType = None
        self._ClusterId = None
        self._Describe = None

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe


    def _deserialize(self, params):
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        self._Describe = params.get("Describe")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAgentOverview(AbstractModel):
    """托管prometheus agent概览

    """

    def __init__(self):
        r"""
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _Status: agent状态
normal = 正常
abnormal = 异常
        :type Status: str
        :param _ClusterName: 集群名称
        :type ClusterName: str
        :param _ExternalLabels: 额外labels
本集群的所有指标都会带上这几个label
注意：此字段可能返回 null，表示取不到有效值。
        :type ExternalLabels: list of Label
        :param _Region: 集群所在地域
注意：此字段可能返回 null，表示取不到有效值。
        :type Region: str
        :param _VpcId: 集群所在VPC ID
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param _FailedReason: 记录关联等操作的失败信息
注意：此字段可能返回 null，表示取不到有效值。
        :type FailedReason: str
        """
        self._ClusterType = None
        self._ClusterId = None
        self._Status = None
        self._ClusterName = None
        self._ExternalLabels = None
        self._Region = None
        self._VpcId = None
        self._FailedReason = None

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ExternalLabels(self):
        return self._ExternalLabels

    @ExternalLabels.setter
    def ExternalLabels(self, ExternalLabels):
        self._ExternalLabels = ExternalLabels

    @property
    def Region(self):
        return self._Region

    @Region.setter
    def Region(self, Region):
        self._Region = Region

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def FailedReason(self):
        return self._FailedReason

    @FailedReason.setter
    def FailedReason(self, FailedReason):
        self._FailedReason = FailedReason


    def _deserialize(self, params):
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        self._Status = params.get("Status")
        self._ClusterName = params.get("ClusterName")
        if params.get("ExternalLabels") is not None:
            self._ExternalLabels = []
            for item in params.get("ExternalLabels"):
                obj = Label()
                obj._deserialize(item)
                self._ExternalLabels.append(obj)
        self._Region = params.get("Region")
        self._VpcId = params.get("VpcId")
        self._FailedReason = params.get("FailedReason")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAlertHistoryItem(AbstractModel):
    """prometheus告警历史

    """

    def __init__(self):
        r"""
        :param _RuleName: 告警名称
        :type RuleName: str
        :param _StartTime: 告警开始时间
        :type StartTime: str
        :param _Content: 告警内容
        :type Content: str
        :param _State: 告警状态
注意：此字段可能返回 null，表示取不到有效值。
        :type State: str
        :param _RuleItem: 触发的规则名称
注意：此字段可能返回 null，表示取不到有效值。
        :type RuleItem: str
        :param _TopicId: 告警渠道的id
注意：此字段可能返回 null，表示取不到有效值。
        :type TopicId: str
        :param _TopicName: 告警渠道的名称
注意：此字段可能返回 null，表示取不到有效值。
        :type TopicName: str
        """
        self._RuleName = None
        self._StartTime = None
        self._Content = None
        self._State = None
        self._RuleItem = None
        self._TopicId = None
        self._TopicName = None

    @property
    def RuleName(self):
        return self._RuleName

    @RuleName.setter
    def RuleName(self, RuleName):
        self._RuleName = RuleName

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def Content(self):
        return self._Content

    @Content.setter
    def Content(self, Content):
        self._Content = Content

    @property
    def State(self):
        return self._State

    @State.setter
    def State(self, State):
        self._State = State

    @property
    def RuleItem(self):
        return self._RuleItem

    @RuleItem.setter
    def RuleItem(self, RuleItem):
        self._RuleItem = RuleItem

    @property
    def TopicId(self):
        return self._TopicId

    @TopicId.setter
    def TopicId(self, TopicId):
        self._TopicId = TopicId

    @property
    def TopicName(self):
        return self._TopicName

    @TopicName.setter
    def TopicName(self, TopicName):
        self._TopicName = TopicName


    def _deserialize(self, params):
        self._RuleName = params.get("RuleName")
        self._StartTime = params.get("StartTime")
        self._Content = params.get("Content")
        self._State = params.get("State")
        self._RuleItem = params.get("RuleItem")
        self._TopicId = params.get("TopicId")
        self._TopicName = params.get("TopicName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAlertManagerConfig(AbstractModel):
    """告警渠道使用自建alertmanager的配置

    """

    def __init__(self):
        r"""
        :param _Url: alertmanager url
        :type Url: str
        :param _ClusterType: alertmanager部署所在集群类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterType: str
        :param _ClusterId: alertmanager部署所在集群ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        """
        self._Url = None
        self._ClusterType = None
        self._ClusterId = None

    @property
    def Url(self):
        return self._Url

    @Url.setter
    def Url(self, Url):
        self._Url = Url

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._Url = params.get("Url")
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAlertPolicyItem(AbstractModel):
    """托管prometheus告警策略实例

    """

    def __init__(self):
        r"""
        :param _Name: 策略名称
        :type Name: str
        :param _Rules: 规则列表
        :type Rules: list of PrometheusAlertRule
        :param _Id: 告警策略 id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: str
        :param _TemplateId: 如果该告警来自模板下发，则TemplateId为模板id
注意：此字段可能返回 null，表示取不到有效值。
        :type TemplateId: str
        :param _Notification: 告警渠道，模板中使用可能返回null
注意：此字段可能返回 null，表示取不到有效值。
        :type Notification: :class:`tencentcloud.tke.v20180525.models.PrometheusNotificationItem`
        :param _UpdatedAt: 最后修改时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedAt: str
        :param _ClusterId: 如果告警策略来源于用户集群CRD资源定义，则ClusterId为所属集群ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        """
        self._Name = None
        self._Rules = None
        self._Id = None
        self._TemplateId = None
        self._Notification = None
        self._UpdatedAt = None
        self._ClusterId = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Rules(self):
        return self._Rules

    @Rules.setter
    def Rules(self, Rules):
        self._Rules = Rules

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Notification(self):
        return self._Notification

    @Notification.setter
    def Notification(self, Notification):
        self._Notification = Notification

    @property
    def UpdatedAt(self):
        return self._UpdatedAt

    @UpdatedAt.setter
    def UpdatedAt(self, UpdatedAt):
        self._UpdatedAt = UpdatedAt

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._Name = params.get("Name")
        if params.get("Rules") is not None:
            self._Rules = []
            for item in params.get("Rules"):
                obj = PrometheusAlertRule()
                obj._deserialize(item)
                self._Rules.append(obj)
        self._Id = params.get("Id")
        self._TemplateId = params.get("TemplateId")
        if params.get("Notification") is not None:
            self._Notification = PrometheusNotificationItem()
            self._Notification._deserialize(params.get("Notification"))
        self._UpdatedAt = params.get("UpdatedAt")
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAlertRule(AbstractModel):
    """Prometheus告警规则

    """

    def __init__(self):
        r"""
        :param _Name: 规则名称
        :type Name: str
        :param _Rule: prometheus语句
        :type Rule: str
        :param _Labels: 额外标签
        :type Labels: list of Label
        :param _Template: 告警发送模板
        :type Template: str
        :param _For: 持续时间
        :type For: str
        :param _Describe: 该条规则的描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param _Annotations: 参考prometheus rule中的annotations
注意：此字段可能返回 null，表示取不到有效值。
        :type Annotations: list of Label
        :param _RuleState: 告警规则状态
注意：此字段可能返回 null，表示取不到有效值。
        :type RuleState: int
        """
        self._Name = None
        self._Rule = None
        self._Labels = None
        self._Template = None
        self._For = None
        self._Describe = None
        self._Annotations = None
        self._RuleState = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Rule(self):
        return self._Rule

    @Rule.setter
    def Rule(self, Rule):
        self._Rule = Rule

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template

    @property
    def For(self):
        return self._For

    @For.setter
    def For(self, For):
        self._For = For

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe

    @property
    def Annotations(self):
        return self._Annotations

    @Annotations.setter
    def Annotations(self, Annotations):
        self._Annotations = Annotations

    @property
    def RuleState(self):
        return self._RuleState

    @RuleState.setter
    def RuleState(self, RuleState):
        self._RuleState = RuleState


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Rule = params.get("Rule")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        self._Template = params.get("Template")
        self._For = params.get("For")
        self._Describe = params.get("Describe")
        if params.get("Annotations") is not None:
            self._Annotations = []
            for item in params.get("Annotations"):
                obj = Label()
                obj._deserialize(item)
                self._Annotations.append(obj)
        self._RuleState = params.get("RuleState")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusAlertRuleDetail(AbstractModel):
    """托管prometheus告警配置实例

    """

    def __init__(self):
        r"""
        :param _Name: 规则名称
        :type Name: str
        :param _Rules: 规则列表
        :type Rules: list of PrometheusAlertRule
        :param _UpdatedAt: 最后修改时间
        :type UpdatedAt: str
        :param _Notification: 告警渠道
        :type Notification: :class:`tencentcloud.tke.v20180525.models.PrometheusNotification`
        :param _Id: 告警 id
        :type Id: str
        :param _TemplateId: 如果该告警来至模板下发，则TemplateId为模板id
注意：此字段可能返回 null，表示取不到有效值。
        :type TemplateId: str
        :param _Interval: 计算周期
注意：此字段可能返回 null，表示取不到有效值。
        :type Interval: str
        """
        self._Name = None
        self._Rules = None
        self._UpdatedAt = None
        self._Notification = None
        self._Id = None
        self._TemplateId = None
        self._Interval = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Rules(self):
        return self._Rules

    @Rules.setter
    def Rules(self, Rules):
        self._Rules = Rules

    @property
    def UpdatedAt(self):
        return self._UpdatedAt

    @UpdatedAt.setter
    def UpdatedAt(self, UpdatedAt):
        self._UpdatedAt = UpdatedAt

    @property
    def Notification(self):
        return self._Notification

    @Notification.setter
    def Notification(self, Notification):
        self._Notification = Notification

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Interval(self):
        return self._Interval

    @Interval.setter
    def Interval(self, Interval):
        self._Interval = Interval


    def _deserialize(self, params):
        self._Name = params.get("Name")
        if params.get("Rules") is not None:
            self._Rules = []
            for item in params.get("Rules"):
                obj = PrometheusAlertRule()
                obj._deserialize(item)
                self._Rules.append(obj)
        self._UpdatedAt = params.get("UpdatedAt")
        if params.get("Notification") is not None:
            self._Notification = PrometheusNotification()
            self._Notification._deserialize(params.get("Notification"))
        self._Id = params.get("Id")
        self._TemplateId = params.get("TemplateId")
        self._Interval = params.get("Interval")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusClusterAgentBasic(AbstractModel):
    """与云监控融合托管prometheus实例，关联集群基础信息

    """

    def __init__(self):
        r"""
        :param _Region: 集群ID
        :type Region: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _EnableExternal: 是否开启公网CLB
        :type EnableExternal: bool
        :param _InClusterPodConfig: 集群内部署组件的pod配置
        :type InClusterPodConfig: :class:`tencentcloud.tke.v20180525.models.PrometheusClusterAgentPodConfig`
        :param _ExternalLabels: 该集群采集的所有指标都会带上这些labels
        :type ExternalLabels: list of Label
        :param _NotInstallBasicScrape: 是否安装默认采集配置
        :type NotInstallBasicScrape: bool
        :param _NotScrape: 是否采集指标，true代表drop所有指标，false代表采集默认指标
        :type NotScrape: bool
        """
        self._Region = None
        self._ClusterType = None
        self._ClusterId = None
        self._EnableExternal = None
        self._InClusterPodConfig = None
        self._ExternalLabels = None
        self._NotInstallBasicScrape = None
        self._NotScrape = None

    @property
    def Region(self):
        return self._Region

    @Region.setter
    def Region(self, Region):
        self._Region = Region

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def EnableExternal(self):
        return self._EnableExternal

    @EnableExternal.setter
    def EnableExternal(self, EnableExternal):
        self._EnableExternal = EnableExternal

    @property
    def InClusterPodConfig(self):
        return self._InClusterPodConfig

    @InClusterPodConfig.setter
    def InClusterPodConfig(self, InClusterPodConfig):
        self._InClusterPodConfig = InClusterPodConfig

    @property
    def ExternalLabels(self):
        return self._ExternalLabels

    @ExternalLabels.setter
    def ExternalLabels(self, ExternalLabels):
        self._ExternalLabels = ExternalLabels

    @property
    def NotInstallBasicScrape(self):
        return self._NotInstallBasicScrape

    @NotInstallBasicScrape.setter
    def NotInstallBasicScrape(self, NotInstallBasicScrape):
        self._NotInstallBasicScrape = NotInstallBasicScrape

    @property
    def NotScrape(self):
        return self._NotScrape

    @NotScrape.setter
    def NotScrape(self, NotScrape):
        self._NotScrape = NotScrape


    def _deserialize(self, params):
        self._Region = params.get("Region")
        self._ClusterType = params.get("ClusterType")
        self._ClusterId = params.get("ClusterId")
        self._EnableExternal = params.get("EnableExternal")
        if params.get("InClusterPodConfig") is not None:
            self._InClusterPodConfig = PrometheusClusterAgentPodConfig()
            self._InClusterPodConfig._deserialize(params.get("InClusterPodConfig"))
        if params.get("ExternalLabels") is not None:
            self._ExternalLabels = []
            for item in params.get("ExternalLabels"):
                obj = Label()
                obj._deserialize(item)
                self._ExternalLabels.append(obj)
        self._NotInstallBasicScrape = params.get("NotInstallBasicScrape")
        self._NotScrape = params.get("NotScrape")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusClusterAgentPodConfig(AbstractModel):
    """关联集群时在集群内部署组件的pod额外配置

    """

    def __init__(self):
        r"""
        :param _HostNet: 是否使用HostNetWork
        :type HostNet: bool
        :param _NodeSelector: 指定pod运行节点
        :type NodeSelector: list of Label
        :param _Tolerations: 容忍污点
        :type Tolerations: list of Toleration
        """
        self._HostNet = None
        self._NodeSelector = None
        self._Tolerations = None

    @property
    def HostNet(self):
        return self._HostNet

    @HostNet.setter
    def HostNet(self, HostNet):
        self._HostNet = HostNet

    @property
    def NodeSelector(self):
        return self._NodeSelector

    @NodeSelector.setter
    def NodeSelector(self, NodeSelector):
        self._NodeSelector = NodeSelector

    @property
    def Tolerations(self):
        return self._Tolerations

    @Tolerations.setter
    def Tolerations(self, Tolerations):
        self._Tolerations = Tolerations


    def _deserialize(self, params):
        self._HostNet = params.get("HostNet")
        if params.get("NodeSelector") is not None:
            self._NodeSelector = []
            for item in params.get("NodeSelector"):
                obj = Label()
                obj._deserialize(item)
                self._NodeSelector.append(obj)
        if params.get("Tolerations") is not None:
            self._Tolerations = []
            for item in params.get("Tolerations"):
                obj = Toleration()
                obj._deserialize(item)
                self._Tolerations.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusConfigItem(AbstractModel):
    """prometheus配置

    """

    def __init__(self):
        r"""
        :param _Name: 名称
        :type Name: str
        :param _Config: 配置内容
        :type Config: str
        :param _TemplateId: 用于出参，如果该配置来至模板，则为模板id
注意：此字段可能返回 null，表示取不到有效值。
        :type TemplateId: str
        """
        self._Name = None
        self._Config = None
        self._TemplateId = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Config(self):
        return self._Config

    @Config.setter
    def Config(self, Config):
        self._Config = Config

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Config = params.get("Config")
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusGrafanaInfo(AbstractModel):
    """托管prometheus中grafana的信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否启用
        :type Enabled: bool
        :param _Domain: 域名，只有开启外网访问才有效果
        :type Domain: str
        :param _Address: 内网地址，或者外网地址
        :type Address: str
        :param _Internet: 是否开启了外网访问
close = 未开启外网访问
opening = 正在开启外网访问
open  = 已开启外网访问
        :type Internet: str
        :param _AdminUser: grafana管理员用户名
        :type AdminUser: str
        """
        self._Enabled = None
        self._Domain = None
        self._Address = None
        self._Internet = None
        self._AdminUser = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def Address(self):
        return self._Address

    @Address.setter
    def Address(self, Address):
        self._Address = Address

    @property
    def Internet(self):
        return self._Internet

    @Internet.setter
    def Internet(self, Internet):
        self._Internet = Internet

    @property
    def AdminUser(self):
        return self._AdminUser

    @AdminUser.setter
    def AdminUser(self, AdminUser):
        self._AdminUser = AdminUser


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._Domain = params.get("Domain")
        self._Address = params.get("Address")
        self._Internet = params.get("Internet")
        self._AdminUser = params.get("AdminUser")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusInstanceOverview(AbstractModel):
    """托管prometheus实例概览

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例id
        :type InstanceId: str
        :param _Name: 实例名称
        :type Name: str
        :param _VpcId: 实例vpcId
        :type VpcId: str
        :param _SubnetId: 实例子网Id
        :type SubnetId: str
        :param _Status: 实例当前的状态
prepare_env = 初始化环境
install_suit = 安装组件
running = 运行中
        :type Status: str
        :param _COSBucket: COS桶存储
        :type COSBucket: str
        :param _GrafanaURL: grafana默认地址，如果开启外网访问得为域名，否则为内网地址
注意：此字段可能返回 null，表示取不到有效值。
        :type GrafanaURL: str
        :param _BoundTotal: 关联集群总数
注意：此字段可能返回 null，表示取不到有效值。
        :type BoundTotal: int
        :param _BoundNormal: 运行正常的集群数
注意：此字段可能返回 null，表示取不到有效值。
        :type BoundNormal: int
        """
        self._InstanceId = None
        self._Name = None
        self._VpcId = None
        self._SubnetId = None
        self._Status = None
        self._COSBucket = None
        self._GrafanaURL = None
        self._BoundTotal = None
        self._BoundNormal = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def COSBucket(self):
        return self._COSBucket

    @COSBucket.setter
    def COSBucket(self, COSBucket):
        self._COSBucket = COSBucket

    @property
    def GrafanaURL(self):
        return self._GrafanaURL

    @GrafanaURL.setter
    def GrafanaURL(self, GrafanaURL):
        self._GrafanaURL = GrafanaURL

    @property
    def BoundTotal(self):
        return self._BoundTotal

    @BoundTotal.setter
    def BoundTotal(self, BoundTotal):
        self._BoundTotal = BoundTotal

    @property
    def BoundNormal(self):
        return self._BoundNormal

    @BoundNormal.setter
    def BoundNormal(self, BoundNormal):
        self._BoundNormal = BoundNormal


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Name = params.get("Name")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._Status = params.get("Status")
        self._COSBucket = params.get("COSBucket")
        self._GrafanaURL = params.get("GrafanaURL")
        self._BoundTotal = params.get("BoundTotal")
        self._BoundNormal = params.get("BoundNormal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusInstancesOverview(AbstractModel):
    """托管prometheusV2实例概览

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _InstanceName: 实例名
        :type InstanceName: str
        :param _VpcId: VPC ID
        :type VpcId: str
        :param _SubnetId: 子网ID
        :type SubnetId: str
        :param _InstanceStatus: 运行状态（1:正在创建；2:运行中；3:异常；4:重启中；5:销毁中； 6:已停机； 7: 已删除）
        :type InstanceStatus: int
        :param _ChargeStatus: 计费状态（1:正常；2:过期; 3:销毁; 4:分配中; 5:分配失败）
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeStatus: int
        :param _EnableGrafana: 是否开启 Grafana（0:不开启，1:开启）
        :type EnableGrafana: int
        :param _GrafanaURL: Grafana 面板 URL
注意：此字段可能返回 null，表示取不到有效值。
        :type GrafanaURL: str
        :param _InstanceChargeType: 实例付费类型（1:试用版；2:预付费）
        :type InstanceChargeType: int
        :param _SpecName: 规格名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SpecName: str
        :param _DataRetentionTime: 存储周期
注意：此字段可能返回 null，表示取不到有效值。
        :type DataRetentionTime: int
        :param _ExpireTime: 购买的实例过期时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpireTime: str
        :param _AutoRenewFlag: 自动续费标记(0:不自动续费；1:开启自动续费；2:禁止自动续费；-1:无效)
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoRenewFlag: int
        :param _BoundTotal: 绑定集群总数
        :type BoundTotal: int
        :param _BoundNormal: 绑定集群正常状态总数
        :type BoundNormal: int
        """
        self._InstanceId = None
        self._InstanceName = None
        self._VpcId = None
        self._SubnetId = None
        self._InstanceStatus = None
        self._ChargeStatus = None
        self._EnableGrafana = None
        self._GrafanaURL = None
        self._InstanceChargeType = None
        self._SpecName = None
        self._DataRetentionTime = None
        self._ExpireTime = None
        self._AutoRenewFlag = None
        self._BoundTotal = None
        self._BoundNormal = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def InstanceStatus(self):
        return self._InstanceStatus

    @InstanceStatus.setter
    def InstanceStatus(self, InstanceStatus):
        self._InstanceStatus = InstanceStatus

    @property
    def ChargeStatus(self):
        return self._ChargeStatus

    @ChargeStatus.setter
    def ChargeStatus(self, ChargeStatus):
        self._ChargeStatus = ChargeStatus

    @property
    def EnableGrafana(self):
        return self._EnableGrafana

    @EnableGrafana.setter
    def EnableGrafana(self, EnableGrafana):
        self._EnableGrafana = EnableGrafana

    @property
    def GrafanaURL(self):
        return self._GrafanaURL

    @GrafanaURL.setter
    def GrafanaURL(self, GrafanaURL):
        self._GrafanaURL = GrafanaURL

    @property
    def InstanceChargeType(self):
        return self._InstanceChargeType

    @InstanceChargeType.setter
    def InstanceChargeType(self, InstanceChargeType):
        self._InstanceChargeType = InstanceChargeType

    @property
    def SpecName(self):
        return self._SpecName

    @SpecName.setter
    def SpecName(self, SpecName):
        self._SpecName = SpecName

    @property
    def DataRetentionTime(self):
        return self._DataRetentionTime

    @DataRetentionTime.setter
    def DataRetentionTime(self, DataRetentionTime):
        self._DataRetentionTime = DataRetentionTime

    @property
    def ExpireTime(self):
        return self._ExpireTime

    @ExpireTime.setter
    def ExpireTime(self, ExpireTime):
        self._ExpireTime = ExpireTime

    @property
    def AutoRenewFlag(self):
        return self._AutoRenewFlag

    @AutoRenewFlag.setter
    def AutoRenewFlag(self, AutoRenewFlag):
        self._AutoRenewFlag = AutoRenewFlag

    @property
    def BoundTotal(self):
        return self._BoundTotal

    @BoundTotal.setter
    def BoundTotal(self, BoundTotal):
        self._BoundTotal = BoundTotal

    @property
    def BoundNormal(self):
        return self._BoundNormal

    @BoundNormal.setter
    def BoundNormal(self, BoundNormal):
        self._BoundNormal = BoundNormal


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._InstanceName = params.get("InstanceName")
        self._VpcId = params.get("VpcId")
        self._SubnetId = params.get("SubnetId")
        self._InstanceStatus = params.get("InstanceStatus")
        self._ChargeStatus = params.get("ChargeStatus")
        self._EnableGrafana = params.get("EnableGrafana")
        self._GrafanaURL = params.get("GrafanaURL")
        self._InstanceChargeType = params.get("InstanceChargeType")
        self._SpecName = params.get("SpecName")
        self._DataRetentionTime = params.get("DataRetentionTime")
        self._ExpireTime = params.get("ExpireTime")
        self._AutoRenewFlag = params.get("AutoRenewFlag")
        self._BoundTotal = params.get("BoundTotal")
        self._BoundNormal = params.get("BoundNormal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusJobTargets(AbstractModel):
    """prometheus一个job的targets

    """

    def __init__(self):
        r"""
        :param _Targets: 该Job的targets列表
        :type Targets: list of PrometheusTarget
        :param _JobName: job的名称
        :type JobName: str
        :param _Total: targets总数
        :type Total: int
        :param _Up: 健康的target总数
        :type Up: int
        """
        self._Targets = None
        self._JobName = None
        self._Total = None
        self._Up = None

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets

    @property
    def JobName(self):
        return self._JobName

    @JobName.setter
    def JobName(self, JobName):
        self._JobName = JobName

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def Up(self):
        return self._Up

    @Up.setter
    def Up(self, Up):
        self._Up = Up


    def _deserialize(self, params):
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        self._JobName = params.get("JobName")
        self._Total = params.get("Total")
        self._Up = params.get("Up")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusNotification(AbstractModel):
    """amp告警渠道配置

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否启用
        :type Enabled: bool
        :param _RepeatInterval: 收敛时间
        :type RepeatInterval: str
        :param _TimeRangeStart: 生效起始时间
        :type TimeRangeStart: str
        :param _TimeRangeEnd: 生效结束时间
        :type TimeRangeEnd: str
        :param _NotifyWay: 告警通知方式。目前有SMS、EMAIL、CALL、WECHAT方式。
分别代表：短信、邮件、电话、微信
注意：此字段可能返回 null，表示取不到有效值。
        :type NotifyWay: list of str
        :param _ReceiverGroups: 告警接收组（用户组）
注意：此字段可能返回 null，表示取不到有效值。
        :type ReceiverGroups: list of int non-negative
        :param _PhoneNotifyOrder: 电话告警顺序。
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneNotifyOrder: list of int non-negative
        :param _PhoneCircleTimes: 电话告警次数。
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneCircleTimes: int
        :param _PhoneInnerInterval: 电话告警轮内间隔。单位：秒
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneInnerInterval: int
        :param _PhoneCircleInterval: 电话告警轮外间隔。单位：秒
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneCircleInterval: int
        :param _PhoneArriveNotice: 电话告警触达通知
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneArriveNotice: bool
        :param _Type: 通道类型，默认为amp，支持以下
amp
webhook
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param _WebHook: 如果Type为webhook, 则该字段为必填项
注意：此字段可能返回 null，表示取不到有效值。
        :type WebHook: str
        """
        self._Enabled = None
        self._RepeatInterval = None
        self._TimeRangeStart = None
        self._TimeRangeEnd = None
        self._NotifyWay = None
        self._ReceiverGroups = None
        self._PhoneNotifyOrder = None
        self._PhoneCircleTimes = None
        self._PhoneInnerInterval = None
        self._PhoneCircleInterval = None
        self._PhoneArriveNotice = None
        self._Type = None
        self._WebHook = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def RepeatInterval(self):
        return self._RepeatInterval

    @RepeatInterval.setter
    def RepeatInterval(self, RepeatInterval):
        self._RepeatInterval = RepeatInterval

    @property
    def TimeRangeStart(self):
        return self._TimeRangeStart

    @TimeRangeStart.setter
    def TimeRangeStart(self, TimeRangeStart):
        self._TimeRangeStart = TimeRangeStart

    @property
    def TimeRangeEnd(self):
        return self._TimeRangeEnd

    @TimeRangeEnd.setter
    def TimeRangeEnd(self, TimeRangeEnd):
        self._TimeRangeEnd = TimeRangeEnd

    @property
    def NotifyWay(self):
        return self._NotifyWay

    @NotifyWay.setter
    def NotifyWay(self, NotifyWay):
        self._NotifyWay = NotifyWay

    @property
    def ReceiverGroups(self):
        return self._ReceiverGroups

    @ReceiverGroups.setter
    def ReceiverGroups(self, ReceiverGroups):
        self._ReceiverGroups = ReceiverGroups

    @property
    def PhoneNotifyOrder(self):
        return self._PhoneNotifyOrder

    @PhoneNotifyOrder.setter
    def PhoneNotifyOrder(self, PhoneNotifyOrder):
        self._PhoneNotifyOrder = PhoneNotifyOrder

    @property
    def PhoneCircleTimes(self):
        return self._PhoneCircleTimes

    @PhoneCircleTimes.setter
    def PhoneCircleTimes(self, PhoneCircleTimes):
        self._PhoneCircleTimes = PhoneCircleTimes

    @property
    def PhoneInnerInterval(self):
        return self._PhoneInnerInterval

    @PhoneInnerInterval.setter
    def PhoneInnerInterval(self, PhoneInnerInterval):
        self._PhoneInnerInterval = PhoneInnerInterval

    @property
    def PhoneCircleInterval(self):
        return self._PhoneCircleInterval

    @PhoneCircleInterval.setter
    def PhoneCircleInterval(self, PhoneCircleInterval):
        self._PhoneCircleInterval = PhoneCircleInterval

    @property
    def PhoneArriveNotice(self):
        return self._PhoneArriveNotice

    @PhoneArriveNotice.setter
    def PhoneArriveNotice(self, PhoneArriveNotice):
        self._PhoneArriveNotice = PhoneArriveNotice

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def WebHook(self):
        return self._WebHook

    @WebHook.setter
    def WebHook(self, WebHook):
        self._WebHook = WebHook


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._RepeatInterval = params.get("RepeatInterval")
        self._TimeRangeStart = params.get("TimeRangeStart")
        self._TimeRangeEnd = params.get("TimeRangeEnd")
        self._NotifyWay = params.get("NotifyWay")
        self._ReceiverGroups = params.get("ReceiverGroups")
        self._PhoneNotifyOrder = params.get("PhoneNotifyOrder")
        self._PhoneCircleTimes = params.get("PhoneCircleTimes")
        self._PhoneInnerInterval = params.get("PhoneInnerInterval")
        self._PhoneCircleInterval = params.get("PhoneCircleInterval")
        self._PhoneArriveNotice = params.get("PhoneArriveNotice")
        self._Type = params.get("Type")
        self._WebHook = params.get("WebHook")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusNotificationItem(AbstractModel):
    """告警通知渠道配置

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否启用
        :type Enabled: bool
        :param _Type: 通道类型，默认为amp，支持以下
amp
webhook
alertmanager
        :type Type: str
        :param _WebHook: 如果Type为webhook, 则该字段为必填项
注意：此字段可能返回 null，表示取不到有效值。
        :type WebHook: str
        :param _AlertManager: 如果Type为alertmanager, 则该字段为必填项
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertManager: :class:`tencentcloud.tke.v20180525.models.PrometheusAlertManagerConfig`
        :param _RepeatInterval: 收敛时间
        :type RepeatInterval: str
        :param _TimeRangeStart: 生效起始时间
        :type TimeRangeStart: str
        :param _TimeRangeEnd: 生效结束时间
        :type TimeRangeEnd: str
        :param _NotifyWay: 告警通知方式。目前有SMS、EMAIL、CALL、WECHAT方式。
注意：此字段可能返回 null，表示取不到有效值。
        :type NotifyWay: list of str
        :param _ReceiverGroups: 告警接收组（用户组）
注意：此字段可能返回 null，表示取不到有效值。
        :type ReceiverGroups: list of str
        :param _PhoneNotifyOrder: 电话告警顺序。
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneNotifyOrder: list of int non-negative
        :param _PhoneCircleTimes: 电话告警次数。
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneCircleTimes: int
        :param _PhoneInnerInterval: 电话告警轮内间隔。单位：秒
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneInnerInterval: int
        :param _PhoneCircleInterval: 电话告警轮外间隔。单位：秒
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneCircleInterval: int
        :param _PhoneArriveNotice: 电话告警触达通知
注：NotifyWay选择CALL，采用该参数。
注意：此字段可能返回 null，表示取不到有效值。
        :type PhoneArriveNotice: bool
        """
        self._Enabled = None
        self._Type = None
        self._WebHook = None
        self._AlertManager = None
        self._RepeatInterval = None
        self._TimeRangeStart = None
        self._TimeRangeEnd = None
        self._NotifyWay = None
        self._ReceiverGroups = None
        self._PhoneNotifyOrder = None
        self._PhoneCircleTimes = None
        self._PhoneInnerInterval = None
        self._PhoneCircleInterval = None
        self._PhoneArriveNotice = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def WebHook(self):
        return self._WebHook

    @WebHook.setter
    def WebHook(self, WebHook):
        self._WebHook = WebHook

    @property
    def AlertManager(self):
        return self._AlertManager

    @AlertManager.setter
    def AlertManager(self, AlertManager):
        self._AlertManager = AlertManager

    @property
    def RepeatInterval(self):
        return self._RepeatInterval

    @RepeatInterval.setter
    def RepeatInterval(self, RepeatInterval):
        self._RepeatInterval = RepeatInterval

    @property
    def TimeRangeStart(self):
        return self._TimeRangeStart

    @TimeRangeStart.setter
    def TimeRangeStart(self, TimeRangeStart):
        self._TimeRangeStart = TimeRangeStart

    @property
    def TimeRangeEnd(self):
        return self._TimeRangeEnd

    @TimeRangeEnd.setter
    def TimeRangeEnd(self, TimeRangeEnd):
        self._TimeRangeEnd = TimeRangeEnd

    @property
    def NotifyWay(self):
        return self._NotifyWay

    @NotifyWay.setter
    def NotifyWay(self, NotifyWay):
        self._NotifyWay = NotifyWay

    @property
    def ReceiverGroups(self):
        return self._ReceiverGroups

    @ReceiverGroups.setter
    def ReceiverGroups(self, ReceiverGroups):
        self._ReceiverGroups = ReceiverGroups

    @property
    def PhoneNotifyOrder(self):
        return self._PhoneNotifyOrder

    @PhoneNotifyOrder.setter
    def PhoneNotifyOrder(self, PhoneNotifyOrder):
        self._PhoneNotifyOrder = PhoneNotifyOrder

    @property
    def PhoneCircleTimes(self):
        return self._PhoneCircleTimes

    @PhoneCircleTimes.setter
    def PhoneCircleTimes(self, PhoneCircleTimes):
        self._PhoneCircleTimes = PhoneCircleTimes

    @property
    def PhoneInnerInterval(self):
        return self._PhoneInnerInterval

    @PhoneInnerInterval.setter
    def PhoneInnerInterval(self, PhoneInnerInterval):
        self._PhoneInnerInterval = PhoneInnerInterval

    @property
    def PhoneCircleInterval(self):
        return self._PhoneCircleInterval

    @PhoneCircleInterval.setter
    def PhoneCircleInterval(self, PhoneCircleInterval):
        self._PhoneCircleInterval = PhoneCircleInterval

    @property
    def PhoneArriveNotice(self):
        return self._PhoneArriveNotice

    @PhoneArriveNotice.setter
    def PhoneArriveNotice(self, PhoneArriveNotice):
        self._PhoneArriveNotice = PhoneArriveNotice


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        self._Type = params.get("Type")
        self._WebHook = params.get("WebHook")
        if params.get("AlertManager") is not None:
            self._AlertManager = PrometheusAlertManagerConfig()
            self._AlertManager._deserialize(params.get("AlertManager"))
        self._RepeatInterval = params.get("RepeatInterval")
        self._TimeRangeStart = params.get("TimeRangeStart")
        self._TimeRangeEnd = params.get("TimeRangeEnd")
        self._NotifyWay = params.get("NotifyWay")
        self._ReceiverGroups = params.get("ReceiverGroups")
        self._PhoneNotifyOrder = params.get("PhoneNotifyOrder")
        self._PhoneCircleTimes = params.get("PhoneCircleTimes")
        self._PhoneInnerInterval = params.get("PhoneInnerInterval")
        self._PhoneCircleInterval = params.get("PhoneCircleInterval")
        self._PhoneArriveNotice = params.get("PhoneArriveNotice")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusRecordRuleYamlItem(AbstractModel):
    """prometheus聚合规则实例详情，包含所属集群ID

    """

    def __init__(self):
        r"""
        :param _Name: 实例名称
        :type Name: str
        :param _UpdateTime: 最近更新时间
        :type UpdateTime: str
        :param _TemplateId: Yaml内容
        :type TemplateId: str
        :param _Content: 如果该聚合规则来至模板，则TemplateId为模板id
注意：此字段可能返回 null，表示取不到有效值。
        :type Content: str
        :param _ClusterId: 该聚合规则如果来源于用户集群crd资源定义，则ClusterId为所属集群ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        """
        self._Name = None
        self._UpdateTime = None
        self._TemplateId = None
        self._Content = None
        self._ClusterId = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def UpdateTime(self):
        return self._UpdateTime

    @UpdateTime.setter
    def UpdateTime(self, UpdateTime):
        self._UpdateTime = UpdateTime

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Content(self):
        return self._Content

    @Content.setter
    def Content(self, Content):
        self._Content = Content

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._UpdateTime = params.get("UpdateTime")
        self._TemplateId = params.get("TemplateId")
        self._Content = params.get("Content")
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusTarget(AbstractModel):
    """prometheus一个抓取目标的信息

    """

    def __init__(self):
        r"""
        :param _Url: 抓取目标的URL
        :type Url: str
        :param _State: target当前状态,当前支持
up = 健康
down = 不健康
unknown = 未知
        :type State: str
        :param _Labels: target的元label
        :type Labels: list of Label
        :param _LastScrape: 上一次抓取的时间
        :type LastScrape: str
        :param _ScrapeDuration: 上一次抓取的耗时，单位是s
        :type ScrapeDuration: float
        :param _Error: 上一次抓取如果错误，该字段存储错误信息
        :type Error: str
        """
        self._Url = None
        self._State = None
        self._Labels = None
        self._LastScrape = None
        self._ScrapeDuration = None
        self._Error = None

    @property
    def Url(self):
        return self._Url

    @Url.setter
    def Url(self, Url):
        self._Url = Url

    @property
    def State(self):
        return self._State

    @State.setter
    def State(self, State):
        self._State = State

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def LastScrape(self):
        return self._LastScrape

    @LastScrape.setter
    def LastScrape(self, LastScrape):
        self._LastScrape = LastScrape

    @property
    def ScrapeDuration(self):
        return self._ScrapeDuration

    @ScrapeDuration.setter
    def ScrapeDuration(self, ScrapeDuration):
        self._ScrapeDuration = ScrapeDuration

    @property
    def Error(self):
        return self._Error

    @Error.setter
    def Error(self, Error):
        self._Error = Error


    def _deserialize(self, params):
        self._Url = params.get("Url")
        self._State = params.get("State")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        self._LastScrape = params.get("LastScrape")
        self._ScrapeDuration = params.get("ScrapeDuration")
        self._Error = params.get("Error")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusTemp(AbstractModel):
    """模板实例

    """

    def __init__(self):
        r"""
        :param _Name: 模板名称
        :type Name: str
        :param _Level: 模板维度，支持以下类型
instance 实例级别
cluster 集群级别
        :type Level: str
        :param _Describe: 模板描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param _RecordRules: 当Level为instance时有效，
模板中的聚合规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordRules: list of PrometheusConfigItem
        :param _ServiceMonitors: 当Level为cluster时有效，
模板中的ServiceMonitor规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: 当Level为cluster时有效，
模板中的PodMonitors规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: 当Level为cluster时有效，
模板中的RawJobs规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RawJobs: list of PrometheusConfigItem
        :param _TemplateId: 模板的ID, 用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type TemplateId: str
        :param _UpdateTime: 最近更新时间，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param _Version: 当前版本，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param _IsDefault: 是否系统提供的默认模板，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type IsDefault: bool
        :param _AlertDetailRules: 当Level为instance时有效，
模板中的告警配置列表
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertDetailRules: list of PrometheusAlertPolicyItem
        :param _TargetsTotal: 关联实例数目
注意：此字段可能返回 null，表示取不到有效值。
        :type TargetsTotal: int
        """
        self._Name = None
        self._Level = None
        self._Describe = None
        self._RecordRules = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None
        self._TemplateId = None
        self._UpdateTime = None
        self._Version = None
        self._IsDefault = None
        self._AlertDetailRules = None
        self._TargetsTotal = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Level(self):
        return self._Level

    @Level.setter
    def Level(self, Level):
        self._Level = Level

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe

    @property
    def RecordRules(self):
        return self._RecordRules

    @RecordRules.setter
    def RecordRules(self, RecordRules):
        self._RecordRules = RecordRules

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def UpdateTime(self):
        return self._UpdateTime

    @UpdateTime.setter
    def UpdateTime(self, UpdateTime):
        self._UpdateTime = UpdateTime

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def IsDefault(self):
        return self._IsDefault

    @IsDefault.setter
    def IsDefault(self, IsDefault):
        self._IsDefault = IsDefault

    @property
    def AlertDetailRules(self):
        return self._AlertDetailRules

    @AlertDetailRules.setter
    def AlertDetailRules(self, AlertDetailRules):
        self._AlertDetailRules = AlertDetailRules

    @property
    def TargetsTotal(self):
        return self._TargetsTotal

    @TargetsTotal.setter
    def TargetsTotal(self, TargetsTotal):
        self._TargetsTotal = TargetsTotal


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Level = params.get("Level")
        self._Describe = params.get("Describe")
        if params.get("RecordRules") is not None:
            self._RecordRules = []
            for item in params.get("RecordRules"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RecordRules.append(obj)
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        self._TemplateId = params.get("TemplateId")
        self._UpdateTime = params.get("UpdateTime")
        self._Version = params.get("Version")
        self._IsDefault = params.get("IsDefault")
        if params.get("AlertDetailRules") is not None:
            self._AlertDetailRules = []
            for item in params.get("AlertDetailRules"):
                obj = PrometheusAlertPolicyItem()
                obj._deserialize(item)
                self._AlertDetailRules.append(obj)
        self._TargetsTotal = params.get("TargetsTotal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusTempModify(AbstractModel):
    """云原生Prometheus模板可修改项

    """

    def __init__(self):
        r"""
        :param _Name: 修改名称
        :type Name: str
        :param _Describe: 修改描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param _ServiceMonitors: 当Level为cluster时有效，
模板中的ServiceMonitor规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: 当Level为cluster时有效，
模板中的PodMonitors规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: 当Level为cluster时有效，
模板中的RawJobs规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RawJobs: list of PrometheusConfigItem
        :param _RecordRules: 当Level为instance时有效，
模板中的聚合规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordRules: list of PrometheusConfigItem
        :param _AlertDetailRules: 修改内容，只有当模板类型是Alert时生效
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertDetailRules: list of PrometheusAlertPolicyItem
        """
        self._Name = None
        self._Describe = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None
        self._RecordRules = None
        self._AlertDetailRules = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs

    @property
    def RecordRules(self):
        return self._RecordRules

    @RecordRules.setter
    def RecordRules(self, RecordRules):
        self._RecordRules = RecordRules

    @property
    def AlertDetailRules(self):
        return self._AlertDetailRules

    @AlertDetailRules.setter
    def AlertDetailRules(self, AlertDetailRules):
        self._AlertDetailRules = AlertDetailRules


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Describe = params.get("Describe")
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        if params.get("RecordRules") is not None:
            self._RecordRules = []
            for item in params.get("RecordRules"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RecordRules.append(obj)
        if params.get("AlertDetailRules") is not None:
            self._AlertDetailRules = []
            for item in params.get("AlertDetailRules"):
                obj = PrometheusAlertPolicyItem()
                obj._deserialize(item)
                self._AlertDetailRules.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusTemplate(AbstractModel):
    """模板实例

    """

    def __init__(self):
        r"""
        :param _Name: 模板名称
        :type Name: str
        :param _Level: 模板维度，支持以下类型
instance 实例级别
cluster 集群级别
        :type Level: str
        :param _Describe: 模板描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param _AlertRules: 当Level为instance时有效，
模板中的告警配置列表
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertRules: list of PrometheusAlertRule
        :param _RecordRules: 当Level为instance时有效，
模板中的聚合规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordRules: list of PrometheusConfigItem
        :param _ServiceMonitors: 当Level为cluster时有效，
模板中的ServiceMonitor规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: 当Level为cluster时有效，
模板中的PodMonitors规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: 当Level为cluster时有效，
模板中的RawJobs规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RawJobs: list of PrometheusConfigItem
        :param _TemplateId: 模板的ID, 用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type TemplateId: str
        :param _UpdateTime: 最近更新时间，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param _Version: 当前版本，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param _IsDefault: 是否系统提供的默认模板，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type IsDefault: bool
        :param _AlertDetailRules: 当Level为instance时有效，
模板中的告警配置列表
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertDetailRules: list of PrometheusAlertRuleDetail
        """
        self._Name = None
        self._Level = None
        self._Describe = None
        self._AlertRules = None
        self._RecordRules = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None
        self._TemplateId = None
        self._UpdateTime = None
        self._Version = None
        self._IsDefault = None
        self._AlertDetailRules = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Level(self):
        return self._Level

    @Level.setter
    def Level(self, Level):
        self._Level = Level

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe

    @property
    def AlertRules(self):
        return self._AlertRules

    @AlertRules.setter
    def AlertRules(self, AlertRules):
        self._AlertRules = AlertRules

    @property
    def RecordRules(self):
        return self._RecordRules

    @RecordRules.setter
    def RecordRules(self, RecordRules):
        self._RecordRules = RecordRules

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def UpdateTime(self):
        return self._UpdateTime

    @UpdateTime.setter
    def UpdateTime(self, UpdateTime):
        self._UpdateTime = UpdateTime

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def IsDefault(self):
        return self._IsDefault

    @IsDefault.setter
    def IsDefault(self, IsDefault):
        self._IsDefault = IsDefault

    @property
    def AlertDetailRules(self):
        return self._AlertDetailRules

    @AlertDetailRules.setter
    def AlertDetailRules(self, AlertDetailRules):
        self._AlertDetailRules = AlertDetailRules


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Level = params.get("Level")
        self._Describe = params.get("Describe")
        if params.get("AlertRules") is not None:
            self._AlertRules = []
            for item in params.get("AlertRules"):
                obj = PrometheusAlertRule()
                obj._deserialize(item)
                self._AlertRules.append(obj)
        if params.get("RecordRules") is not None:
            self._RecordRules = []
            for item in params.get("RecordRules"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RecordRules.append(obj)
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        self._TemplateId = params.get("TemplateId")
        self._UpdateTime = params.get("UpdateTime")
        self._Version = params.get("Version")
        self._IsDefault = params.get("IsDefault")
        if params.get("AlertDetailRules") is not None:
            self._AlertDetailRules = []
            for item in params.get("AlertDetailRules"):
                obj = PrometheusAlertRuleDetail()
                obj._deserialize(item)
                self._AlertDetailRules.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusTemplateModify(AbstractModel):
    """云原生Prometheus模板可修改项

    """

    def __init__(self):
        r"""
        :param _Name: 修改名称
        :type Name: str
        :param _Describe: 修改描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param _AlertRules: 修改内容，只有当模板类型是Alert时生效
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertRules: list of PrometheusAlertRule
        :param _RecordRules: 当Level为instance时有效，
模板中的聚合规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordRules: list of PrometheusConfigItem
        :param _ServiceMonitors: 当Level为cluster时有效，
模板中的ServiceMonitor规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceMonitors: list of PrometheusConfigItem
        :param _PodMonitors: 当Level为cluster时有效，
模板中的PodMonitors规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type PodMonitors: list of PrometheusConfigItem
        :param _RawJobs: 当Level为cluster时有效，
模板中的RawJobs规则列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RawJobs: list of PrometheusConfigItem
        :param _AlertDetailRules: 修改内容，只有当模板类型是Alert时生效
注意：此字段可能返回 null，表示取不到有效值。
        :type AlertDetailRules: list of PrometheusAlertRuleDetail
        """
        self._Name = None
        self._Describe = None
        self._AlertRules = None
        self._RecordRules = None
        self._ServiceMonitors = None
        self._PodMonitors = None
        self._RawJobs = None
        self._AlertDetailRules = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe

    @property
    def AlertRules(self):
        return self._AlertRules

    @AlertRules.setter
    def AlertRules(self, AlertRules):
        self._AlertRules = AlertRules

    @property
    def RecordRules(self):
        return self._RecordRules

    @RecordRules.setter
    def RecordRules(self, RecordRules):
        self._RecordRules = RecordRules

    @property
    def ServiceMonitors(self):
        return self._ServiceMonitors

    @ServiceMonitors.setter
    def ServiceMonitors(self, ServiceMonitors):
        self._ServiceMonitors = ServiceMonitors

    @property
    def PodMonitors(self):
        return self._PodMonitors

    @PodMonitors.setter
    def PodMonitors(self, PodMonitors):
        self._PodMonitors = PodMonitors

    @property
    def RawJobs(self):
        return self._RawJobs

    @RawJobs.setter
    def RawJobs(self, RawJobs):
        self._RawJobs = RawJobs

    @property
    def AlertDetailRules(self):
        return self._AlertDetailRules

    @AlertDetailRules.setter
    def AlertDetailRules(self, AlertDetailRules):
        self._AlertDetailRules = AlertDetailRules


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Describe = params.get("Describe")
        if params.get("AlertRules") is not None:
            self._AlertRules = []
            for item in params.get("AlertRules"):
                obj = PrometheusAlertRule()
                obj._deserialize(item)
                self._AlertRules.append(obj)
        if params.get("RecordRules") is not None:
            self._RecordRules = []
            for item in params.get("RecordRules"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RecordRules.append(obj)
        if params.get("ServiceMonitors") is not None:
            self._ServiceMonitors = []
            for item in params.get("ServiceMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._ServiceMonitors.append(obj)
        if params.get("PodMonitors") is not None:
            self._PodMonitors = []
            for item in params.get("PodMonitors"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._PodMonitors.append(obj)
        if params.get("RawJobs") is not None:
            self._RawJobs = []
            for item in params.get("RawJobs"):
                obj = PrometheusConfigItem()
                obj._deserialize(item)
                self._RawJobs.append(obj)
        if params.get("AlertDetailRules") is not None:
            self._AlertDetailRules = []
            for item in params.get("AlertDetailRules"):
                obj = PrometheusAlertRuleDetail()
                obj._deserialize(item)
                self._AlertDetailRules.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrometheusTemplateSyncTarget(AbstractModel):
    """云原生Prometheus模板同步目标

    """

    def __init__(self):
        r"""
        :param _Region: 目标所在地域
        :type Region: str
        :param _InstanceId: 目标实例
        :type InstanceId: str
        :param _ClusterId: 集群id，只有当采集模板的Level为cluster的时候需要
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        :param _SyncTime: 最后一次同步时间， 用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type SyncTime: str
        :param _Version: 当前使用的模板版本，用于出参
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param _ClusterType: 集群类型，只有当采集模板的Level为cluster的时候需要
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterType: str
        :param _InstanceName: 用于出参，实例名称
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        :param _ClusterName: 用于出参，集群名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterName: str
        """
        self._Region = None
        self._InstanceId = None
        self._ClusterId = None
        self._SyncTime = None
        self._Version = None
        self._ClusterType = None
        self._InstanceName = None
        self._ClusterName = None

    @property
    def Region(self):
        return self._Region

    @Region.setter
    def Region(self, Region):
        self._Region = Region

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SyncTime(self):
        return self._SyncTime

    @SyncTime.setter
    def SyncTime(self, SyncTime):
        self._SyncTime = SyncTime

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType

    @property
    def InstanceName(self):
        return self._InstanceName

    @InstanceName.setter
    def InstanceName(self, InstanceName):
        self._InstanceName = InstanceName

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName


    def _deserialize(self, params):
        self._Region = params.get("Region")
        self._InstanceId = params.get("InstanceId")
        self._ClusterId = params.get("ClusterId")
        self._SyncTime = params.get("SyncTime")
        self._Version = params.get("Version")
        self._ClusterType = params.get("ClusterType")
        self._InstanceName = params.get("InstanceName")
        self._ClusterName = params.get("ClusterName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RegionInstance(AbstractModel):
    """地域属性信息

    """

    def __init__(self):
        r"""
        :param _RegionName: 地域名称
注意：此字段可能返回 null，表示取不到有效值。
        :type RegionName: str
        :param _RegionId: 地域ID
注意：此字段可能返回 null，表示取不到有效值。
        :type RegionId: int
        :param _Status: 地域状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _FeatureGates: 地域特性开关(按照JSON的形式返回所有属性)
注意：此字段可能返回 null，表示取不到有效值。
        :type FeatureGates: str
        :param _Alias: 地域简称
注意：此字段可能返回 null，表示取不到有效值。
        :type Alias: str
        :param _Remark: 地域白名单
注意：此字段可能返回 null，表示取不到有效值。
        :type Remark: str
        """
        self._RegionName = None
        self._RegionId = None
        self._Status = None
        self._FeatureGates = None
        self._Alias = None
        self._Remark = None

    @property
    def RegionName(self):
        return self._RegionName

    @RegionName.setter
    def RegionName(self, RegionName):
        self._RegionName = RegionName

    @property
    def RegionId(self):
        return self._RegionId

    @RegionId.setter
    def RegionId(self, RegionId):
        self._RegionId = RegionId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def FeatureGates(self):
        return self._FeatureGates

    @FeatureGates.setter
    def FeatureGates(self, FeatureGates):
        self._FeatureGates = FeatureGates

    @property
    def Alias(self):
        return self._Alias

    @Alias.setter
    def Alias(self, Alias):
        self._Alias = Alias

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark


    def _deserialize(self, params):
        self._RegionName = params.get("RegionName")
        self._RegionId = params.get("RegionId")
        self._Status = params.get("Status")
        self._FeatureGates = params.get("FeatureGates")
        self._Alias = params.get("Alias")
        self._Remark = params.get("Remark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Release(AbstractModel):
    """应用市场部署的应用结构

    """

    def __init__(self):
        r"""
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用命名空间
        :type Namespace: str
        :param _Revision: 应用当前版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Revision: str
        :param _Status: 应用状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _ChartName: 制品名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ChartName: str
        :param _ChartVersion: 制品版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ChartVersion: str
        :param _AppVersion: 制品应用版本
注意：此字段可能返回 null，表示取不到有效值。
        :type AppVersion: str
        :param _UpdatedTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedTime: str
        :param _Description: 应用描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        """
        self._Name = None
        self._Namespace = None
        self._Revision = None
        self._Status = None
        self._ChartName = None
        self._ChartVersion = None
        self._AppVersion = None
        self._UpdatedTime = None
        self._Description = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Revision(self):
        return self._Revision

    @Revision.setter
    def Revision(self, Revision):
        self._Revision = Revision

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def ChartName(self):
        return self._ChartName

    @ChartName.setter
    def ChartName(self, ChartName):
        self._ChartName = ChartName

    @property
    def ChartVersion(self):
        return self._ChartVersion

    @ChartVersion.setter
    def ChartVersion(self, ChartVersion):
        self._ChartVersion = ChartVersion

    @property
    def AppVersion(self):
        return self._AppVersion

    @AppVersion.setter
    def AppVersion(self, AppVersion):
        self._AppVersion = AppVersion

    @property
    def UpdatedTime(self):
        return self._UpdatedTime

    @UpdatedTime.setter
    def UpdatedTime(self, UpdatedTime):
        self._UpdatedTime = UpdatedTime

    @property
    def Description(self):
        return self._Description

    @Description.setter
    def Description(self, Description):
        self._Description = Description


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Revision = params.get("Revision")
        self._Status = params.get("Status")
        self._ChartName = params.get("ChartName")
        self._ChartVersion = params.get("ChartVersion")
        self._AppVersion = params.get("AppVersion")
        self._UpdatedTime = params.get("UpdatedTime")
        self._Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReleaseDetails(AbstractModel):
    """应用市场的安装应用详情

    """

    def __init__(self):
        r"""
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用所在命名空间
        :type Namespace: str
        :param _Version: 应用当前版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: int
        :param _Status: 应用状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _Description: 应用描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param _Notes: 应用提示
注意：此字段可能返回 null，表示取不到有效值。
        :type Notes: str
        :param _Config: 用户自定义参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Config: str
        :param _Manifest: 应用资源详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Manifest: str
        :param _ChartVersion: 应用制品版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ChartVersion: str
        :param _ChartName: 应用制品名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ChartName: str
        :param _ChartDescription: 应用制品描述
注意：此字段可能返回 null，表示取不到有效值。
        :type ChartDescription: str
        :param _AppVersion: 应用制品app版本
注意：此字段可能返回 null，表示取不到有效值。
        :type AppVersion: str
        :param _FirstDeployedTime: 应用首次部署时间
注意：此字段可能返回 null，表示取不到有效值。
        :type FirstDeployedTime: str
        :param _LastDeployedTime: 应用最近部署时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastDeployedTime: str
        :param _ComputedValues: 应用参数
注意：此字段可能返回 null，表示取不到有效值。
        :type ComputedValues: str
        """
        self._Name = None
        self._Namespace = None
        self._Version = None
        self._Status = None
        self._Description = None
        self._Notes = None
        self._Config = None
        self._Manifest = None
        self._ChartVersion = None
        self._ChartName = None
        self._ChartDescription = None
        self._AppVersion = None
        self._FirstDeployedTime = None
        self._LastDeployedTime = None
        self._ComputedValues = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Description(self):
        return self._Description

    @Description.setter
    def Description(self, Description):
        self._Description = Description

    @property
    def Notes(self):
        return self._Notes

    @Notes.setter
    def Notes(self, Notes):
        self._Notes = Notes

    @property
    def Config(self):
        return self._Config

    @Config.setter
    def Config(self, Config):
        self._Config = Config

    @property
    def Manifest(self):
        return self._Manifest

    @Manifest.setter
    def Manifest(self, Manifest):
        self._Manifest = Manifest

    @property
    def ChartVersion(self):
        return self._ChartVersion

    @ChartVersion.setter
    def ChartVersion(self, ChartVersion):
        self._ChartVersion = ChartVersion

    @property
    def ChartName(self):
        return self._ChartName

    @ChartName.setter
    def ChartName(self, ChartName):
        self._ChartName = ChartName

    @property
    def ChartDescription(self):
        return self._ChartDescription

    @ChartDescription.setter
    def ChartDescription(self, ChartDescription):
        self._ChartDescription = ChartDescription

    @property
    def AppVersion(self):
        return self._AppVersion

    @AppVersion.setter
    def AppVersion(self, AppVersion):
        self._AppVersion = AppVersion

    @property
    def FirstDeployedTime(self):
        return self._FirstDeployedTime

    @FirstDeployedTime.setter
    def FirstDeployedTime(self, FirstDeployedTime):
        self._FirstDeployedTime = FirstDeployedTime

    @property
    def LastDeployedTime(self):
        return self._LastDeployedTime

    @LastDeployedTime.setter
    def LastDeployedTime(self, LastDeployedTime):
        self._LastDeployedTime = LastDeployedTime

    @property
    def ComputedValues(self):
        return self._ComputedValues

    @ComputedValues.setter
    def ComputedValues(self, ComputedValues):
        self._ComputedValues = ComputedValues


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Version = params.get("Version")
        self._Status = params.get("Status")
        self._Description = params.get("Description")
        self._Notes = params.get("Notes")
        self._Config = params.get("Config")
        self._Manifest = params.get("Manifest")
        self._ChartVersion = params.get("ChartVersion")
        self._ChartName = params.get("ChartName")
        self._ChartDescription = params.get("ChartDescription")
        self._AppVersion = params.get("AppVersion")
        self._FirstDeployedTime = params.get("FirstDeployedTime")
        self._LastDeployedTime = params.get("LastDeployedTime")
        self._ComputedValues = params.get("ComputedValues")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReleaseHistory(AbstractModel):
    """应用市场中部署的应用版本历史

    """

    def __init__(self):
        r"""
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用命名空间
        :type Namespace: str
        :param _Revision: 应用版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Revision: int
        :param _Status: 应用状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param _Chart: 应用制品名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Chart: str
        :param _AppVersion: 应用制品版本
注意：此字段可能返回 null，表示取不到有效值。
        :type AppVersion: str
        :param _UpdatedTime: 应用更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedTime: str
        :param _Description: 应用描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        """
        self._Name = None
        self._Namespace = None
        self._Revision = None
        self._Status = None
        self._Chart = None
        self._AppVersion = None
        self._UpdatedTime = None
        self._Description = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Revision(self):
        return self._Revision

    @Revision.setter
    def Revision(self, Revision):
        self._Revision = Revision

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Chart(self):
        return self._Chart

    @Chart.setter
    def Chart(self, Chart):
        self._Chart = Chart

    @property
    def AppVersion(self):
        return self._AppVersion

    @AppVersion.setter
    def AppVersion(self, AppVersion):
        self._AppVersion = AppVersion

    @property
    def UpdatedTime(self):
        return self._UpdatedTime

    @UpdatedTime.setter
    def UpdatedTime(self, UpdatedTime):
        self._UpdatedTime = UpdatedTime

    @property
    def Description(self):
        return self._Description

    @Description.setter
    def Description(self, Description):
        self._Description = Description


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Revision = params.get("Revision")
        self._Status = params.get("Status")
        self._Chart = params.get("Chart")
        self._AppVersion = params.get("AppVersion")
        self._UpdatedTime = params.get("UpdatedTime")
        self._Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReleaseValues(AbstractModel):
    """应用市场自定义参数

    """

    def __init__(self):
        r"""
        :param _RawOriginal: 自定义参数原始值
        :type RawOriginal: str
        :param _ValuesType: 自定义参数值类型
        :type ValuesType: str
        """
        self._RawOriginal = None
        self._ValuesType = None

    @property
    def RawOriginal(self):
        return self._RawOriginal

    @RawOriginal.setter
    def RawOriginal(self, RawOriginal):
        self._RawOriginal = RawOriginal

    @property
    def ValuesType(self):
        return self._ValuesType

    @ValuesType.setter
    def ValuesType(self, ValuesType):
        self._ValuesType = ValuesType


    def _deserialize(self, params):
        self._RawOriginal = params.get("RawOriginal")
        self._ValuesType = params.get("ValuesType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveNodeFromNodePoolRequest(AbstractModel):
    """RemoveNodeFromNodePool请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _InstanceIds: 节点id列表，一次最多支持100台
        :type InstanceIds: list of str
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._InstanceIds = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveNodeFromNodePoolResponse(AbstractModel):
    """RemoveNodeFromNodePool返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ResourceDeleteOption(AbstractModel):
    """资源删除选项

    """

    def __init__(self):
        r"""
        :param _ResourceType: 资源类型，例如CBS
        :type ResourceType: str
        :param _DeleteMode: 集群删除时资源的删除模式：terminate（销毁），retain （保留）
        :type DeleteMode: str
        """
        self._ResourceType = None
        self._DeleteMode = None

    @property
    def ResourceType(self):
        return self._ResourceType

    @ResourceType.setter
    def ResourceType(self, ResourceType):
        self._ResourceType = ResourceType

    @property
    def DeleteMode(self):
        return self._DeleteMode

    @DeleteMode.setter
    def DeleteMode(self, DeleteMode):
        self._DeleteMode = DeleteMode


    def _deserialize(self, params):
        self._ResourceType = params.get("ResourceType")
        self._DeleteMode = params.get("DeleteMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResourceUsage(AbstractModel):
    """集群资源使用量

    """

    def __init__(self):
        r"""
        :param _Name: 资源类型
        :type Name: str
        :param _Usage: 资源使用量
        :type Usage: int
        :param _Details: 资源使用详情
        :type Details: list of ResourceUsageDetail
        """
        self._Name = None
        self._Usage = None
        self._Details = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Usage(self):
        return self._Usage

    @Usage.setter
    def Usage(self, Usage):
        self._Usage = Usage

    @property
    def Details(self):
        return self._Details

    @Details.setter
    def Details(self, Details):
        self._Details = Details


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Usage = params.get("Usage")
        if params.get("Details") is not None:
            self._Details = []
            for item in params.get("Details"):
                obj = ResourceUsageDetail()
                obj._deserialize(item)
                self._Details.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResourceUsageDetail(AbstractModel):
    """资源使用明细

    """

    def __init__(self):
        r"""
        :param _Name: 资源名称
        :type Name: str
        :param _Usage: 资源使用量
        :type Usage: int
        """
        self._Name = None
        self._Usage = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Usage(self):
        return self._Usage

    @Usage.setter
    def Usage(self, Usage):
        self._Usage = Usage


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Usage = params.get("Usage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartEKSContainerInstancesRequest(AbstractModel):
    """RestartEKSContainerInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiIds: EKS instance ids
        :type EksCiIds: list of str
        """
        self._EksCiIds = None

    @property
    def EksCiIds(self):
        return self._EksCiIds

    @EksCiIds.setter
    def EksCiIds(self, EksCiIds):
        self._EksCiIds = EksCiIds


    def _deserialize(self, params):
        self._EksCiIds = params.get("EksCiIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartEKSContainerInstancesResponse(AbstractModel):
    """RestartEKSContainerInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class RollbackClusterReleaseRequest(AbstractModel):
    """RollbackClusterRelease请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用命名空间
        :type Namespace: str
        :param _Revision: 回滚版本号
        :type Revision: int
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Name = None
        self._Namespace = None
        self._Revision = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Revision(self):
        return self._Revision

    @Revision.setter
    def Revision(self, Revision):
        self._Revision = Revision

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Revision = params.get("Revision")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RollbackClusterReleaseResponse(AbstractModel):
    """RollbackClusterRelease返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Release: 应用详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Release: :class:`tencentcloud.tke.v20180525.models.PendingRelease`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Release = None
        self._RequestId = None

    @property
    def Release(self):
        return self._Release

    @Release.setter
    def Release(self, Release):
        self._Release = Release

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Release") is not None:
            self._Release = PendingRelease()
            self._Release._deserialize(params.get("Release"))
        self._RequestId = params.get("RequestId")


class RouteInfo(AbstractModel):
    """集群路由对象

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param _DestinationCidrBlock: 目的端CIDR。
        :type DestinationCidrBlock: str
        :param _GatewayIp: 下一跳地址。
        :type GatewayIp: str
        """
        self._RouteTableName = None
        self._DestinationCidrBlock = None
        self._GatewayIp = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def DestinationCidrBlock(self):
        return self._DestinationCidrBlock

    @DestinationCidrBlock.setter
    def DestinationCidrBlock(self, DestinationCidrBlock):
        self._DestinationCidrBlock = DestinationCidrBlock

    @property
    def GatewayIp(self):
        return self._GatewayIp

    @GatewayIp.setter
    def GatewayIp(self, GatewayIp):
        self._GatewayIp = GatewayIp


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        self._DestinationCidrBlock = params.get("DestinationCidrBlock")
        self._GatewayIp = params.get("GatewayIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RouteTableConflict(AbstractModel):
    """路由表冲突对象

    """

    def __init__(self):
        r"""
        :param _RouteTableType: 路由表类型。
        :type RouteTableType: str
        :param _RouteTableCidrBlock: 路由表CIDR。
注意：此字段可能返回 null，表示取不到有效值。
        :type RouteTableCidrBlock: str
        :param _RouteTableName: 路由表名称。
注意：此字段可能返回 null，表示取不到有效值。
        :type RouteTableName: str
        :param _RouteTableId: 路由表ID。
注意：此字段可能返回 null，表示取不到有效值。
        :type RouteTableId: str
        """
        self._RouteTableType = None
        self._RouteTableCidrBlock = None
        self._RouteTableName = None
        self._RouteTableId = None

    @property
    def RouteTableType(self):
        return self._RouteTableType

    @RouteTableType.setter
    def RouteTableType(self, RouteTableType):
        self._RouteTableType = RouteTableType

    @property
    def RouteTableCidrBlock(self):
        return self._RouteTableCidrBlock

    @RouteTableCidrBlock.setter
    def RouteTableCidrBlock(self, RouteTableCidrBlock):
        self._RouteTableCidrBlock = RouteTableCidrBlock

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def RouteTableId(self):
        return self._RouteTableId

    @RouteTableId.setter
    def RouteTableId(self, RouteTableId):
        self._RouteTableId = RouteTableId


    def _deserialize(self, params):
        self._RouteTableType = params.get("RouteTableType")
        self._RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self._RouteTableName = params.get("RouteTableName")
        self._RouteTableId = params.get("RouteTableId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RouteTableInfo(AbstractModel):
    """集群路由表对象

    """

    def __init__(self):
        r"""
        :param _RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param _RouteTableCidrBlock: 路由表CIDR。
        :type RouteTableCidrBlock: str
        :param _VpcId: VPC实例ID。
        :type VpcId: str
        """
        self._RouteTableName = None
        self._RouteTableCidrBlock = None
        self._VpcId = None

    @property
    def RouteTableName(self):
        return self._RouteTableName

    @RouteTableName.setter
    def RouteTableName(self, RouteTableName):
        self._RouteTableName = RouteTableName

    @property
    def RouteTableCidrBlock(self):
        return self._RouteTableCidrBlock

    @RouteTableCidrBlock.setter
    def RouteTableCidrBlock(self, RouteTableCidrBlock):
        self._RouteTableCidrBlock = RouteTableCidrBlock

    @property
    def VpcId(self):
        return self._VpcId

    @VpcId.setter
    def VpcId(self, VpcId):
        self._VpcId = VpcId


    def _deserialize(self, params):
        self._RouteTableName = params.get("RouteTableName")
        self._RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self._VpcId = params.get("VpcId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunAutomationServiceEnabled(AbstractModel):
    """描述了 “云自动化助手” 服务相关的信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启云自动化助手。取值范围：<br><li>TRUE：表示开启云自动化助手服务<br><li>FALSE：表示不开启云自动化助手服务<br><br>默认取值：FALSE。
        :type Enabled: bool
        """
        self._Enabled = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunInstancesForNode(AbstractModel):
    """不同角色的节点配置参数

    """

    def __init__(self):
        r"""
        :param _NodeRole: 节点角色，取值:MASTER_ETCD, WORKER。MASTER_ETCD只有在创建 INDEPENDENT_CLUSTER 独立集群时需要指定。MASTER_ETCD节点数量为3～7，建议为奇数。MASTER_ETCD节点最小配置为4C8G。
        :type NodeRole: str
        :param _RunInstancesPara: CVM创建透传参数，json化字符串格式，详见[CVM创建实例](https://cloud.tencent.com/document/product/213/15730)接口，传入公共参数外的其他参数即可，其中ImageId会替换为TKE集群OS对应的镜像。
        :type RunInstancesPara: list of str
        :param _InstanceAdvancedSettingsOverrides: 节点高级设置，该参数会覆盖集群级别设置的InstanceAdvancedSettings，和上边的RunInstancesPara按照顺序一一对应（当前只对节点自定义参数ExtraArgs生效）。
        :type InstanceAdvancedSettingsOverrides: list of InstanceAdvancedSettings
        """
        self._NodeRole = None
        self._RunInstancesPara = None
        self._InstanceAdvancedSettingsOverrides = None

    @property
    def NodeRole(self):
        return self._NodeRole

    @NodeRole.setter
    def NodeRole(self, NodeRole):
        self._NodeRole = NodeRole

    @property
    def RunInstancesPara(self):
        return self._RunInstancesPara

    @RunInstancesPara.setter
    def RunInstancesPara(self, RunInstancesPara):
        self._RunInstancesPara = RunInstancesPara

    @property
    def InstanceAdvancedSettingsOverrides(self):
        return self._InstanceAdvancedSettingsOverrides

    @InstanceAdvancedSettingsOverrides.setter
    def InstanceAdvancedSettingsOverrides(self, InstanceAdvancedSettingsOverrides):
        self._InstanceAdvancedSettingsOverrides = InstanceAdvancedSettingsOverrides


    def _deserialize(self, params):
        self._NodeRole = params.get("NodeRole")
        self._RunInstancesPara = params.get("RunInstancesPara")
        if params.get("InstanceAdvancedSettingsOverrides") is not None:
            self._InstanceAdvancedSettingsOverrides = []
            for item in params.get("InstanceAdvancedSettingsOverrides"):
                obj = InstanceAdvancedSettings()
                obj._deserialize(item)
                self._InstanceAdvancedSettingsOverrides.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunMonitorServiceEnabled(AbstractModel):
    """描述了 “云监控” 服务相关的信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启[云监控](/document/product/248)服务。取值范围：<br><li>TRUE：表示开启云监控服务<br><li>FALSE：表示不开启云监控服务<br><br>默认取值：TRUE。
        :type Enabled: bool
        """
        self._Enabled = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunPrometheusInstanceRequest(AbstractModel):
    """RunPrometheusInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _SubnetId: 子网ID，默认使用实例所用子网初始化，也可通过该参数传递新的子网ID初始化
        :type SubnetId: str
        """
        self._InstanceId = None
        self._SubnetId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunPrometheusInstanceResponse(AbstractModel):
    """RunPrometheusInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class RunSecurityServiceEnabled(AbstractModel):
    """描述了 “云安全” 服务相关的信息

    """

    def __init__(self):
        r"""
        :param _Enabled: 是否开启[云安全](/document/product/296)服务。取值范围：<br><li>TRUE：表示开启云安全服务<br><li>FALSE：表示不开启云安全服务<br><br>默认取值：TRUE。
        :type Enabled: bool
        """
        self._Enabled = None

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, Enabled):
        self._Enabled = Enabled


    def _deserialize(self, params):
        self._Enabled = params.get("Enabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleInClusterMasterRequest(AbstractModel):
    """ScaleInClusterMaster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群实例ID
        :type ClusterId: str
        :param _ScaleInMasters: master缩容选项
        :type ScaleInMasters: list of ScaleInMaster
        """
        self._ClusterId = None
        self._ScaleInMasters = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ScaleInMasters(self):
        return self._ScaleInMasters

    @ScaleInMasters.setter
    def ScaleInMasters(self, ScaleInMasters):
        self._ScaleInMasters = ScaleInMasters


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("ScaleInMasters") is not None:
            self._ScaleInMasters = []
            for item in params.get("ScaleInMasters"):
                obj = ScaleInMaster()
                obj._deserialize(item)
                self._ScaleInMasters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleInClusterMasterResponse(AbstractModel):
    """ScaleInClusterMaster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class ScaleInMaster(AbstractModel):
    """master节点缩容参数

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
        :type InstanceId: str
        :param _NodeRole: 缩容的实例角色：MASTER,ETCD,MASTER_ETCD
        :type NodeRole: str
        :param _InstanceDeleteMode: 实例的保留模式
        :type InstanceDeleteMode: str
        """
        self._InstanceId = None
        self._NodeRole = None
        self._InstanceDeleteMode = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def NodeRole(self):
        return self._NodeRole

    @NodeRole.setter
    def NodeRole(self, NodeRole):
        self._NodeRole = NodeRole

    @property
    def InstanceDeleteMode(self):
        return self._InstanceDeleteMode

    @InstanceDeleteMode.setter
    def InstanceDeleteMode(self, InstanceDeleteMode):
        self._InstanceDeleteMode = InstanceDeleteMode


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._NodeRole = params.get("NodeRole")
        self._InstanceDeleteMode = params.get("InstanceDeleteMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleOutClusterMasterRequest(AbstractModel):
    """ScaleOutClusterMaster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群实例ID
        :type ClusterId: str
        :param _RunInstancesForNode: 新建节点参数
        :type RunInstancesForNode: list of RunInstancesForNode
        :param _ExistedInstancesForNode: 添加已有节点相关参数
        :type ExistedInstancesForNode: list of ExistedInstancesForNode
        :param _InstanceAdvancedSettings: 实例高级设置
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _ExtraArgs: 集群master组件自定义参数
        :type ExtraArgs: :class:`tencentcloud.tke.v20180525.models.ClusterExtraArgs`
        """
        self._ClusterId = None
        self._RunInstancesForNode = None
        self._ExistedInstancesForNode = None
        self._InstanceAdvancedSettings = None
        self._ExtraArgs = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def RunInstancesForNode(self):
        return self._RunInstancesForNode

    @RunInstancesForNode.setter
    def RunInstancesForNode(self, RunInstancesForNode):
        self._RunInstancesForNode = RunInstancesForNode

    @property
    def ExistedInstancesForNode(self):
        return self._ExistedInstancesForNode

    @ExistedInstancesForNode.setter
    def ExistedInstancesForNode(self, ExistedInstancesForNode):
        self._ExistedInstancesForNode = ExistedInstancesForNode

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def ExtraArgs(self):
        return self._ExtraArgs

    @ExtraArgs.setter
    def ExtraArgs(self, ExtraArgs):
        self._ExtraArgs = ExtraArgs


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        if params.get("RunInstancesForNode") is not None:
            self._RunInstancesForNode = []
            for item in params.get("RunInstancesForNode"):
                obj = RunInstancesForNode()
                obj._deserialize(item)
                self._RunInstancesForNode.append(obj)
        if params.get("ExistedInstancesForNode") is not None:
            self._ExistedInstancesForNode = []
            for item in params.get("ExistedInstancesForNode"):
                obj = ExistedInstancesForNode()
                obj._deserialize(item)
                self._ExistedInstancesForNode.append(obj)
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("ExtraArgs") is not None:
            self._ExtraArgs = ClusterExtraArgs()
            self._ExtraArgs._deserialize(params.get("ExtraArgs"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleOutClusterMasterResponse(AbstractModel):
    """ScaleOutClusterMaster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class SecurityContext(AbstractModel):
    """cloudrun安全特性

    """

    def __init__(self):
        r"""
        :param _Capabilities: 安全能力清单
注意：此字段可能返回 null，表示取不到有效值。
        :type Capabilities: :class:`tencentcloud.tke.v20180525.models.Capabilities`
        """
        self._Capabilities = None

    @property
    def Capabilities(self):
        return self._Capabilities

    @Capabilities.setter
    def Capabilities(self, Capabilities):
        self._Capabilities = Capabilities


    def _deserialize(self, params):
        if params.get("Capabilities") is not None:
            self._Capabilities = Capabilities()
            self._Capabilities._deserialize(params.get("Capabilities"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceAccountAuthenticationOptions(AbstractModel):
    """ServiceAccount认证相关配置

    """

    def __init__(self):
        r"""
        :param _UseTKEDefault: 使用TKE默认issuer和jwksuri
注意：此字段可能返回 null，表示取不到有效值。
        :type UseTKEDefault: bool
        :param _Issuer: service-account-issuer
注意：此字段可能返回 null，表示取不到有效值。
        :type Issuer: str
        :param _JWKSURI: service-account-jwks-uri
注意：此字段可能返回 null，表示取不到有效值。
        :type JWKSURI: str
        :param _AutoCreateDiscoveryAnonymousAuth: 如果为true，则会自动创建允许匿名用户访问'/.well-known/openid-configuration'和/openid/v1/jwks的rbac规则
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoCreateDiscoveryAnonymousAuth: bool
        """
        self._UseTKEDefault = None
        self._Issuer = None
        self._JWKSURI = None
        self._AutoCreateDiscoveryAnonymousAuth = None

    @property
    def UseTKEDefault(self):
        return self._UseTKEDefault

    @UseTKEDefault.setter
    def UseTKEDefault(self, UseTKEDefault):
        self._UseTKEDefault = UseTKEDefault

    @property
    def Issuer(self):
        return self._Issuer

    @Issuer.setter
    def Issuer(self, Issuer):
        self._Issuer = Issuer

    @property
    def JWKSURI(self):
        return self._JWKSURI

    @JWKSURI.setter
    def JWKSURI(self, JWKSURI):
        self._JWKSURI = JWKSURI

    @property
    def AutoCreateDiscoveryAnonymousAuth(self):
        return self._AutoCreateDiscoveryAnonymousAuth

    @AutoCreateDiscoveryAnonymousAuth.setter
    def AutoCreateDiscoveryAnonymousAuth(self, AutoCreateDiscoveryAnonymousAuth):
        self._AutoCreateDiscoveryAnonymousAuth = AutoCreateDiscoveryAnonymousAuth


    def _deserialize(self, params):
        self._UseTKEDefault = params.get("UseTKEDefault")
        self._Issuer = params.get("Issuer")
        self._JWKSURI = params.get("JWKSURI")
        self._AutoCreateDiscoveryAnonymousAuth = params.get("AutoCreateDiscoveryAnonymousAuth")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetNodePoolNodeProtectionRequest(AbstractModel):
    """SetNodePoolNodeProtection请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群id
        :type ClusterId: str
        :param _NodePoolId: 节点池id
        :type NodePoolId: str
        :param _InstanceIds: 节点id
        :type InstanceIds: list of str
        :param _ProtectedFromScaleIn: 节点是否需要移出保护
        :type ProtectedFromScaleIn: bool
        """
        self._ClusterId = None
        self._NodePoolId = None
        self._InstanceIds = None
        self._ProtectedFromScaleIn = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def ProtectedFromScaleIn(self):
        return self._ProtectedFromScaleIn

    @ProtectedFromScaleIn.setter
    def ProtectedFromScaleIn(self, ProtectedFromScaleIn):
        self._ProtectedFromScaleIn = ProtectedFromScaleIn


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._NodePoolId = params.get("NodePoolId")
        self._InstanceIds = params.get("InstanceIds")
        self._ProtectedFromScaleIn = params.get("ProtectedFromScaleIn")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetNodePoolNodeProtectionResponse(AbstractModel):
    """SetNodePoolNodeProtection返回参数结构体

    """

    def __init__(self):
        r"""
        :param _SucceedInstanceIds: 成功设置的节点id
注意：此字段可能返回 null，表示取不到有效值。
        :type SucceedInstanceIds: list of str
        :param _FailedInstanceIds: 没有成功设置的节点id
注意：此字段可能返回 null，表示取不到有效值。
        :type FailedInstanceIds: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._SucceedInstanceIds = None
        self._FailedInstanceIds = None
        self._RequestId = None

    @property
    def SucceedInstanceIds(self):
        return self._SucceedInstanceIds

    @SucceedInstanceIds.setter
    def SucceedInstanceIds(self, SucceedInstanceIds):
        self._SucceedInstanceIds = SucceedInstanceIds

    @property
    def FailedInstanceIds(self):
        return self._FailedInstanceIds

    @FailedInstanceIds.setter
    def FailedInstanceIds(self, FailedInstanceIds):
        self._FailedInstanceIds = FailedInstanceIds

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._SucceedInstanceIds = params.get("SucceedInstanceIds")
        self._FailedInstanceIds = params.get("FailedInstanceIds")
        self._RequestId = params.get("RequestId")


class SubnetInfos(AbstractModel):
    """子网信息

    """

    def __init__(self):
        r"""
        :param _SubnetId: 子网id
        :type SubnetId: str
        :param _Name: 子网节点名称
        :type Name: str
        :param _SecurityGroups: 安全组id
        :type SecurityGroups: list of str
        :param _Os: 系统
        :type Os: str
        :param _Arch: 硬件架构
        :type Arch: str
        """
        self._SubnetId = None
        self._Name = None
        self._SecurityGroups = None
        self._Os = None
        self._Arch = None

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def SecurityGroups(self):
        return self._SecurityGroups

    @SecurityGroups.setter
    def SecurityGroups(self, SecurityGroups):
        self._SecurityGroups = SecurityGroups

    @property
    def Os(self):
        return self._Os

    @Os.setter
    def Os(self, Os):
        self._Os = Os

    @property
    def Arch(self):
        return self._Arch

    @Arch.setter
    def Arch(self, Arch):
        self._Arch = Arch


    def _deserialize(self, params):
        self._SubnetId = params.get("SubnetId")
        self._Name = params.get("Name")
        self._SecurityGroups = params.get("SecurityGroups")
        self._Os = params.get("Os")
        self._Arch = params.get("Arch")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SyncPrometheusTempRequest(AbstractModel):
    """SyncPrometheusTemp请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 实例id
        :type TemplateId: str
        :param _Targets: 同步目标
        :type Targets: list of PrometheusTemplateSyncTarget
        """
        self._TemplateId = None
        self._Targets = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTemplateSyncTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SyncPrometheusTempResponse(AbstractModel):
    """SyncPrometheusTemp返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class SyncPrometheusTemplateRequest(AbstractModel):
    """SyncPrometheusTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 实例id
        :type TemplateId: str
        :param _Targets: 同步目标
        :type Targets: list of PrometheusTemplateSyncTarget
        """
        self._TemplateId = None
        self._Targets = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Targets(self):
        return self._Targets

    @Targets.setter
    def Targets(self, Targets):
        self._Targets = Targets


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        if params.get("Targets") is not None:
            self._Targets = []
            for item in params.get("Targets"):
                obj = PrometheusTemplateSyncTarget()
                obj._deserialize(item)
                self._Targets.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SyncPrometheusTemplateResponse(AbstractModel):
    """SyncPrometheusTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class Tag(AbstractModel):
    """标签绑定的资源类型，当前支持类型："cluster"

    """

    def __init__(self):
        r"""
        :param _Key: 标签键
        :type Key: str
        :param _Value: 标签值
        :type Value: str
        """
        self._Key = None
        self._Value = None

    @property
    def Key(self):
        return self._Key

    @Key.setter
    def Key(self, Key):
        self._Key = Key

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, Value):
        self._Value = Value


    def _deserialize(self, params):
        self._Key = params.get("Key")
        self._Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TagSpecification(AbstractModel):
    """标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到云主机实例。

    """

    def __init__(self):
        r"""
        :param _ResourceType: 标签绑定的资源类型，当前支持类型："cluster"
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceType: str
        :param _Tags: 标签对列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        """
        self._ResourceType = None
        self._Tags = None

    @property
    def ResourceType(self):
        return self._ResourceType

    @ResourceType.setter
    def ResourceType(self, ResourceType):
        self._ResourceType = ResourceType

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags


    def _deserialize(self, params):
        self._ResourceType = params.get("ResourceType")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self._Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Taint(AbstractModel):
    """kubernetes Taint

    """

    def __init__(self):
        r"""
        :param _Key: Key
        :type Key: str
        :param _Value: Value
        :type Value: str
        :param _Effect: Effect
        :type Effect: str
        """
        self._Key = None
        self._Value = None
        self._Effect = None

    @property
    def Key(self):
        return self._Key

    @Key.setter
    def Key(self, Key):
        self._Key = Key

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, Value):
        self._Value = Value

    @property
    def Effect(self):
        return self._Effect

    @Effect.setter
    def Effect(self, Effect):
        self._Effect = Effect


    def _deserialize(self, params):
        self._Key = params.get("Key")
        self._Value = params.get("Value")
        self._Effect = params.get("Effect")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TaskStepInfo(AbstractModel):
    """任务步骤信息

    """

    def __init__(self):
        r"""
        :param _Step: 步骤名称
        :type Step: str
        :param _LifeState: 生命周期
pending : 步骤未开始
running: 步骤执行中
success: 步骤成功完成
failed: 步骤失败
        :type LifeState: str
        :param _StartAt: 步骤开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartAt: str
        :param _EndAt: 步骤结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndAt: str
        :param _FailedMsg: 若步骤生命周期为failed,则此字段显示错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type FailedMsg: str
        """
        self._Step = None
        self._LifeState = None
        self._StartAt = None
        self._EndAt = None
        self._FailedMsg = None

    @property
    def Step(self):
        return self._Step

    @Step.setter
    def Step(self, Step):
        self._Step = Step

    @property
    def LifeState(self):
        return self._LifeState

    @LifeState.setter
    def LifeState(self, LifeState):
        self._LifeState = LifeState

    @property
    def StartAt(self):
        return self._StartAt

    @StartAt.setter
    def StartAt(self, StartAt):
        self._StartAt = StartAt

    @property
    def EndAt(self):
        return self._EndAt

    @EndAt.setter
    def EndAt(self, EndAt):
        self._EndAt = EndAt

    @property
    def FailedMsg(self):
        return self._FailedMsg

    @FailedMsg.setter
    def FailedMsg(self, FailedMsg):
        self._FailedMsg = FailedMsg


    def _deserialize(self, params):
        self._Step = params.get("Step")
        self._LifeState = params.get("LifeState")
        self._StartAt = params.get("StartAt")
        self._EndAt = params.get("EndAt")
        self._FailedMsg = params.get("FailedMsg")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TcpSocket(AbstractModel):
    """探针使用TcpSocket检测容器

    """

    def __init__(self):
        r"""
        :param _Port: TcpSocket检测的端口
注意：此字段可能返回 null，表示取不到有效值。
        :type Port: int
        """
        self._Port = None

    @property
    def Port(self):
        return self._Port

    @Port.setter
    def Port(self, Port):
        self._Port = Port


    def _deserialize(self, params):
        self._Port = params.get("Port")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Toleration(AbstractModel):
    """kubernetes Taint

    """

    def __init__(self):
        r"""
        :param _Key: 容忍应用到的 taint key
        :type Key: str
        :param _Operator: 键与值的关系
        :type Operator: str
        :param _Effect: 要匹配的污点效果
        :type Effect: str
        """
        self._Key = None
        self._Operator = None
        self._Effect = None

    @property
    def Key(self):
        return self._Key

    @Key.setter
    def Key(self, Key):
        self._Key = Key

    @property
    def Operator(self):
        return self._Operator

    @Operator.setter
    def Operator(self, Operator):
        self._Operator = Operator

    @property
    def Effect(self):
        return self._Effect

    @Effect.setter
    def Effect(self, Effect):
        self._Effect = Effect


    def _deserialize(self, params):
        self._Key = params.get("Key")
        self._Operator = params.get("Operator")
        self._Effect = params.get("Effect")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnavailableReason(AbstractModel):
    """不可用原因

    """

    def __init__(self):
        r"""
        :param _InstanceId: 实例ID
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceId: str
        :param _Reason: 原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        """
        self._InstanceId = None
        self._Reason = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Reason = params.get("Reason")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UninstallClusterReleaseRequest(AbstractModel):
    """UninstallClusterRelease请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Name: 应用名称
        :type Name: str
        :param _Namespace: 应用命名空间
        :type Namespace: str
        :param _ClusterType: 集群类型
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Name = None
        self._Namespace = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UninstallClusterReleaseResponse(AbstractModel):
    """UninstallClusterRelease返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Release: 应用详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Release: :class:`tencentcloud.tke.v20180525.models.PendingRelease`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Release = None
        self._RequestId = None

    @property
    def Release(self):
        return self._Release

    @Release.setter
    def Release(self, Release):
        self._Release = Release

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Release") is not None:
            self._Release = PendingRelease()
            self._Release._deserialize(params.get("Release"))
        self._RequestId = params.get("RequestId")


class UninstallEdgeLogAgentRequest(AbstractModel):
    """UninstallEdgeLogAgent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UninstallEdgeLogAgentResponse(AbstractModel):
    """UninstallEdgeLogAgent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UninstallLogAgentRequest(AbstractModel):
    """UninstallLogAgent请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        """
        self._ClusterId = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UninstallLogAgentResponse(AbstractModel):
    """UninstallLogAgent返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateAddonRequest(AbstractModel):
    """UpdateAddon请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _AddonName: addon名称
        :type AddonName: str
        :param _AddonVersion: addon版本（不传默认不更新）
        :type AddonVersion: str
        :param _RawValues: addon的参数，是一个json格式的base64转码后的字符串（addon参数由DescribeAddonValues获取）
        :type RawValues: str
        """
        self._ClusterId = None
        self._AddonName = None
        self._AddonVersion = None
        self._RawValues = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def AddonName(self):
        return self._AddonName

    @AddonName.setter
    def AddonName(self, AddonName):
        self._AddonName = AddonName

    @property
    def AddonVersion(self):
        return self._AddonVersion

    @AddonVersion.setter
    def AddonVersion(self, AddonVersion):
        self._AddonVersion = AddonVersion

    @property
    def RawValues(self):
        return self._RawValues

    @RawValues.setter
    def RawValues(self, RawValues):
        self._RawValues = RawValues


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._AddonName = params.get("AddonName")
        self._AddonVersion = params.get("AddonVersion")
        self._RawValues = params.get("RawValues")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateAddonResponse(AbstractModel):
    """UpdateAddon返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateClusterKubeconfigRequest(AbstractModel):
    """UpdateClusterKubeconfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _SubAccounts: 子账户Uin列表，传空默认为调用此接口的SubUin
        :type SubAccounts: list of str
        """
        self._ClusterId = None
        self._SubAccounts = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def SubAccounts(self):
        return self._SubAccounts

    @SubAccounts.setter
    def SubAccounts(self, SubAccounts):
        self._SubAccounts = SubAccounts


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._SubAccounts = params.get("SubAccounts")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateClusterKubeconfigResponse(AbstractModel):
    """UpdateClusterKubeconfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param _UpdatedSubAccounts: 已更新的子账户Uin列表
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedSubAccounts: list of str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._UpdatedSubAccounts = None
        self._RequestId = None

    @property
    def UpdatedSubAccounts(self):
        return self._UpdatedSubAccounts

    @UpdatedSubAccounts.setter
    def UpdatedSubAccounts(self, UpdatedSubAccounts):
        self._UpdatedSubAccounts = UpdatedSubAccounts

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._UpdatedSubAccounts = params.get("UpdatedSubAccounts")
        self._RequestId = params.get("RequestId")


class UpdateClusterVersionRequest(AbstractModel):
    """UpdateClusterVersion请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群 Id
        :type ClusterId: str
        :param _DstVersion: 需要升级到的版本
        :type DstVersion: str
        :param _ExtraArgs: 集群自定义参数
        :type ExtraArgs: :class:`tencentcloud.tke.v20180525.models.ClusterExtraArgs`
        :param _MaxNotReadyPercent: 可容忍的最大不可用pod数目
        :type MaxNotReadyPercent: float
        :param _SkipPreCheck: 是否跳过预检查阶段
        :type SkipPreCheck: bool
        """
        self._ClusterId = None
        self._DstVersion = None
        self._ExtraArgs = None
        self._MaxNotReadyPercent = None
        self._SkipPreCheck = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def DstVersion(self):
        return self._DstVersion

    @DstVersion.setter
    def DstVersion(self, DstVersion):
        self._DstVersion = DstVersion

    @property
    def ExtraArgs(self):
        return self._ExtraArgs

    @ExtraArgs.setter
    def ExtraArgs(self, ExtraArgs):
        self._ExtraArgs = ExtraArgs

    @property
    def MaxNotReadyPercent(self):
        return self._MaxNotReadyPercent

    @MaxNotReadyPercent.setter
    def MaxNotReadyPercent(self, MaxNotReadyPercent):
        self._MaxNotReadyPercent = MaxNotReadyPercent

    @property
    def SkipPreCheck(self):
        return self._SkipPreCheck

    @SkipPreCheck.setter
    def SkipPreCheck(self, SkipPreCheck):
        self._SkipPreCheck = SkipPreCheck


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._DstVersion = params.get("DstVersion")
        if params.get("ExtraArgs") is not None:
            self._ExtraArgs = ClusterExtraArgs()
            self._ExtraArgs._deserialize(params.get("ExtraArgs"))
        self._MaxNotReadyPercent = params.get("MaxNotReadyPercent")
        self._SkipPreCheck = params.get("SkipPreCheck")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateClusterVersionResponse(AbstractModel):
    """UpdateClusterVersion返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateEKSClusterRequest(AbstractModel):
    """UpdateEKSCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 弹性集群Id
        :type ClusterId: str
        :param _ClusterName: 弹性集群名称
        :type ClusterName: str
        :param _ClusterDesc: 弹性集群描述信息
        :type ClusterDesc: str
        :param _SubnetIds: 子网Id 列表
        :type SubnetIds: list of str
        :param _PublicLB: 弹性容器集群公网访问LB信息
        :type PublicLB: :class:`tencentcloud.tke.v20180525.models.ClusterPublicLB`
        :param _InternalLB: 弹性容器集群内网访问LB信息
        :type InternalLB: :class:`tencentcloud.tke.v20180525.models.ClusterInternalLB`
        :param _ServiceSubnetId: Service 子网Id
        :type ServiceSubnetId: str
        :param _DnsServers: 集群自定义的dns 服务器信息
        :type DnsServers: list of DnsServerConf
        :param _ClearDnsServer: 是否清空自定义dns 服务器设置。为1 表示 是。其他表示 否。
        :type ClearDnsServer: str
        :param _NeedDeleteCbs: 将来删除集群时是否要删除cbs。默认为 FALSE
        :type NeedDeleteCbs: bool
        :param _ProxyLB: 标记是否是新的内外网。默认为false
        :type ProxyLB: bool
        :param _ExtraParam: 扩展参数。须是map[string]string 的json 格式。
        :type ExtraParam: str
        """
        self._ClusterId = None
        self._ClusterName = None
        self._ClusterDesc = None
        self._SubnetIds = None
        self._PublicLB = None
        self._InternalLB = None
        self._ServiceSubnetId = None
        self._DnsServers = None
        self._ClearDnsServer = None
        self._NeedDeleteCbs = None
        self._ProxyLB = None
        self._ExtraParam = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def PublicLB(self):
        return self._PublicLB

    @PublicLB.setter
    def PublicLB(self, PublicLB):
        self._PublicLB = PublicLB

    @property
    def InternalLB(self):
        return self._InternalLB

    @InternalLB.setter
    def InternalLB(self, InternalLB):
        self._InternalLB = InternalLB

    @property
    def ServiceSubnetId(self):
        return self._ServiceSubnetId

    @ServiceSubnetId.setter
    def ServiceSubnetId(self, ServiceSubnetId):
        self._ServiceSubnetId = ServiceSubnetId

    @property
    def DnsServers(self):
        return self._DnsServers

    @DnsServers.setter
    def DnsServers(self, DnsServers):
        self._DnsServers = DnsServers

    @property
    def ClearDnsServer(self):
        return self._ClearDnsServer

    @ClearDnsServer.setter
    def ClearDnsServer(self, ClearDnsServer):
        self._ClearDnsServer = ClearDnsServer

    @property
    def NeedDeleteCbs(self):
        return self._NeedDeleteCbs

    @NeedDeleteCbs.setter
    def NeedDeleteCbs(self, NeedDeleteCbs):
        self._NeedDeleteCbs = NeedDeleteCbs

    @property
    def ProxyLB(self):
        return self._ProxyLB

    @ProxyLB.setter
    def ProxyLB(self, ProxyLB):
        self._ProxyLB = ProxyLB

    @property
    def ExtraParam(self):
        return self._ExtraParam

    @ExtraParam.setter
    def ExtraParam(self, ExtraParam):
        self._ExtraParam = ExtraParam


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterName = params.get("ClusterName")
        self._ClusterDesc = params.get("ClusterDesc")
        self._SubnetIds = params.get("SubnetIds")
        if params.get("PublicLB") is not None:
            self._PublicLB = ClusterPublicLB()
            self._PublicLB._deserialize(params.get("PublicLB"))
        if params.get("InternalLB") is not None:
            self._InternalLB = ClusterInternalLB()
            self._InternalLB._deserialize(params.get("InternalLB"))
        self._ServiceSubnetId = params.get("ServiceSubnetId")
        if params.get("DnsServers") is not None:
            self._DnsServers = []
            for item in params.get("DnsServers"):
                obj = DnsServerConf()
                obj._deserialize(item)
                self._DnsServers.append(obj)
        self._ClearDnsServer = params.get("ClearDnsServer")
        self._NeedDeleteCbs = params.get("NeedDeleteCbs")
        self._ProxyLB = params.get("ProxyLB")
        self._ExtraParam = params.get("ExtraParam")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateEKSClusterResponse(AbstractModel):
    """UpdateEKSCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateEKSContainerInstanceRequest(AbstractModel):
    """UpdateEKSContainerInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiId: 容器实例 ID
        :type EksCiId: str
        :param _RestartPolicy: 实例重启策略： Always(总是重启)、Never(从不重启)、OnFailure(失败时重启)
        :type RestartPolicy: str
        :param _EksCiVolume: 数据卷，包含NfsVolume数组和CbsVolume数组
        :type EksCiVolume: :class:`tencentcloud.tke.v20180525.models.EksCiVolume`
        :param _Containers: 容器组
        :type Containers: list of Container
        :param _InitContainers: Init 容器组
        :type InitContainers: list of Container
        :param _Name: 容器实例名称
        :type Name: str
        :param _ImageRegistryCredentials: 镜像仓库凭证数组
        :type ImageRegistryCredentials: list of ImageRegistryCredential
        """
        self._EksCiId = None
        self._RestartPolicy = None
        self._EksCiVolume = None
        self._Containers = None
        self._InitContainers = None
        self._Name = None
        self._ImageRegistryCredentials = None

    @property
    def EksCiId(self):
        return self._EksCiId

    @EksCiId.setter
    def EksCiId(self, EksCiId):
        self._EksCiId = EksCiId

    @property
    def RestartPolicy(self):
        return self._RestartPolicy

    @RestartPolicy.setter
    def RestartPolicy(self, RestartPolicy):
        self._RestartPolicy = RestartPolicy

    @property
    def EksCiVolume(self):
        return self._EksCiVolume

    @EksCiVolume.setter
    def EksCiVolume(self, EksCiVolume):
        self._EksCiVolume = EksCiVolume

    @property
    def Containers(self):
        return self._Containers

    @Containers.setter
    def Containers(self, Containers):
        self._Containers = Containers

    @property
    def InitContainers(self):
        return self._InitContainers

    @InitContainers.setter
    def InitContainers(self, InitContainers):
        self._InitContainers = InitContainers

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def ImageRegistryCredentials(self):
        return self._ImageRegistryCredentials

    @ImageRegistryCredentials.setter
    def ImageRegistryCredentials(self, ImageRegistryCredentials):
        self._ImageRegistryCredentials = ImageRegistryCredentials


    def _deserialize(self, params):
        self._EksCiId = params.get("EksCiId")
        self._RestartPolicy = params.get("RestartPolicy")
        if params.get("EksCiVolume") is not None:
            self._EksCiVolume = EksCiVolume()
            self._EksCiVolume._deserialize(params.get("EksCiVolume"))
        if params.get("Containers") is not None:
            self._Containers = []
            for item in params.get("Containers"):
                obj = Container()
                obj._deserialize(item)
                self._Containers.append(obj)
        if params.get("InitContainers") is not None:
            self._InitContainers = []
            for item in params.get("InitContainers"):
                obj = Container()
                obj._deserialize(item)
                self._InitContainers.append(obj)
        self._Name = params.get("Name")
        if params.get("ImageRegistryCredentials") is not None:
            self._ImageRegistryCredentials = []
            for item in params.get("ImageRegistryCredentials"):
                obj = ImageRegistryCredential()
                obj._deserialize(item)
                self._ImageRegistryCredentials.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateEKSContainerInstanceResponse(AbstractModel):
    """UpdateEKSContainerInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param _EksCiId: 容器实例 ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EksCiId: str
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._EksCiId = None
        self._RequestId = None

    @property
    def EksCiId(self):
        return self._EksCiId

    @EksCiId.setter
    def EksCiId(self, EksCiId):
        self._EksCiId = EksCiId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._EksCiId = params.get("EksCiId")
        self._RequestId = params.get("RequestId")


class UpdateEdgeClusterVersionRequest(AbstractModel):
    """UpdateEdgeClusterVersion请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群 Id
        :type ClusterId: str
        :param _EdgeVersion: 需要升级到的版本
        :type EdgeVersion: str
        :param _RegistryPrefix: 自定义边缘组件镜像仓库前缀
        :type RegistryPrefix: str
        :param _SkipPreCheck: 是否跳过预检查阶段
        :type SkipPreCheck: bool
        """
        self._ClusterId = None
        self._EdgeVersion = None
        self._RegistryPrefix = None
        self._SkipPreCheck = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def EdgeVersion(self):
        return self._EdgeVersion

    @EdgeVersion.setter
    def EdgeVersion(self, EdgeVersion):
        self._EdgeVersion = EdgeVersion

    @property
    def RegistryPrefix(self):
        return self._RegistryPrefix

    @RegistryPrefix.setter
    def RegistryPrefix(self, RegistryPrefix):
        self._RegistryPrefix = RegistryPrefix

    @property
    def SkipPreCheck(self):
        return self._SkipPreCheck

    @SkipPreCheck.setter
    def SkipPreCheck(self, SkipPreCheck):
        self._SkipPreCheck = SkipPreCheck


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._EdgeVersion = params.get("EdgeVersion")
        self._RegistryPrefix = params.get("RegistryPrefix")
        self._SkipPreCheck = params.get("SkipPreCheck")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateEdgeClusterVersionResponse(AbstractModel):
    """UpdateEdgeClusterVersion返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateImageCacheRequest(AbstractModel):
    """UpdateImageCache请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ImageCacheId: 镜像缓存Id
        :type ImageCacheId: str
        :param _ImageCacheName: 镜像缓存名称
        :type ImageCacheName: str
        :param _ImageRegistryCredentials: 镜像仓库凭证数组
        :type ImageRegistryCredentials: list of ImageRegistryCredential
        :param _Images: 用于制作镜像缓存的容器镜像列表
        :type Images: list of str
        :param _ImageCacheSize: 镜像缓存的大小。默认为20 GiB。取值范围参考[云硬盘类型](https://cloud.tencent.com/document/product/362/2353)中的高性能云盘类型的大小限制。
        :type ImageCacheSize: int
        :param _RetentionDays: 镜像缓存保留时间天数，过期将会自动清理，默认为0，永不过期。
        :type RetentionDays: int
        :param _SecurityGroupIds: 安全组Id
        :type SecurityGroupIds: list of str
        """
        self._ImageCacheId = None
        self._ImageCacheName = None
        self._ImageRegistryCredentials = None
        self._Images = None
        self._ImageCacheSize = None
        self._RetentionDays = None
        self._SecurityGroupIds = None

    @property
    def ImageCacheId(self):
        return self._ImageCacheId

    @ImageCacheId.setter
    def ImageCacheId(self, ImageCacheId):
        self._ImageCacheId = ImageCacheId

    @property
    def ImageCacheName(self):
        return self._ImageCacheName

    @ImageCacheName.setter
    def ImageCacheName(self, ImageCacheName):
        self._ImageCacheName = ImageCacheName

    @property
    def ImageRegistryCredentials(self):
        return self._ImageRegistryCredentials

    @ImageRegistryCredentials.setter
    def ImageRegistryCredentials(self, ImageRegistryCredentials):
        self._ImageRegistryCredentials = ImageRegistryCredentials

    @property
    def Images(self):
        return self._Images

    @Images.setter
    def Images(self, Images):
        self._Images = Images

    @property
    def ImageCacheSize(self):
        return self._ImageCacheSize

    @ImageCacheSize.setter
    def ImageCacheSize(self, ImageCacheSize):
        self._ImageCacheSize = ImageCacheSize

    @property
    def RetentionDays(self):
        return self._RetentionDays

    @RetentionDays.setter
    def RetentionDays(self, RetentionDays):
        self._RetentionDays = RetentionDays

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds


    def _deserialize(self, params):
        self._ImageCacheId = params.get("ImageCacheId")
        self._ImageCacheName = params.get("ImageCacheName")
        if params.get("ImageRegistryCredentials") is not None:
            self._ImageRegistryCredentials = []
            for item in params.get("ImageRegistryCredentials"):
                obj = ImageRegistryCredential()
                obj._deserialize(item)
                self._ImageRegistryCredentials.append(obj)
        self._Images = params.get("Images")
        self._ImageCacheSize = params.get("ImageCacheSize")
        self._RetentionDays = params.get("RetentionDays")
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateImageCacheResponse(AbstractModel):
    """UpdateImageCache返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateTKEEdgeClusterRequest(AbstractModel):
    """UpdateTKEEdgeCluster请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 边缘计算集群ID
        :type ClusterId: str
        :param _ClusterName: 边缘计算集群名称
        :type ClusterName: str
        :param _ClusterDesc: 边缘计算集群描述信息
        :type ClusterDesc: str
        :param _PodCIDR: 边缘计算集群的pod cidr
        :type PodCIDR: str
        :param _ServiceCIDR: 边缘计算集群的service cidr
        :type ServiceCIDR: str
        :param _PublicLB: 边缘计算集群公网访问LB信息
        :type PublicLB: :class:`tencentcloud.tke.v20180525.models.EdgeClusterPublicLB`
        :param _InternalLB: 边缘计算集群内网访问LB信息
        :type InternalLB: :class:`tencentcloud.tke.v20180525.models.EdgeClusterInternalLB`
        :param _CoreDns: 边缘计算集群的CoreDns部署信息
        :type CoreDns: str
        :param _HealthRegion: 边缘计算集群的健康检查多地域部署信息
        :type HealthRegion: str
        :param _Health: 边缘计算集群的健康检查部署信息
        :type Health: str
        :param _GridDaemon: 边缘计算集群的GridDaemon部署信息
        :type GridDaemon: str
        :param _AutoUpgradeClusterLevel: 边缘集群开启自动升配
        :type AutoUpgradeClusterLevel: bool
        :param _ClusterLevel: 边缘集群的集群规模
        :type ClusterLevel: str
        """
        self._ClusterId = None
        self._ClusterName = None
        self._ClusterDesc = None
        self._PodCIDR = None
        self._ServiceCIDR = None
        self._PublicLB = None
        self._InternalLB = None
        self._CoreDns = None
        self._HealthRegion = None
        self._Health = None
        self._GridDaemon = None
        self._AutoUpgradeClusterLevel = None
        self._ClusterLevel = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def ClusterName(self):
        return self._ClusterName

    @ClusterName.setter
    def ClusterName(self, ClusterName):
        self._ClusterName = ClusterName

    @property
    def ClusterDesc(self):
        return self._ClusterDesc

    @ClusterDesc.setter
    def ClusterDesc(self, ClusterDesc):
        self._ClusterDesc = ClusterDesc

    @property
    def PodCIDR(self):
        return self._PodCIDR

    @PodCIDR.setter
    def PodCIDR(self, PodCIDR):
        self._PodCIDR = PodCIDR

    @property
    def ServiceCIDR(self):
        return self._ServiceCIDR

    @ServiceCIDR.setter
    def ServiceCIDR(self, ServiceCIDR):
        self._ServiceCIDR = ServiceCIDR

    @property
    def PublicLB(self):
        return self._PublicLB

    @PublicLB.setter
    def PublicLB(self, PublicLB):
        self._PublicLB = PublicLB

    @property
    def InternalLB(self):
        return self._InternalLB

    @InternalLB.setter
    def InternalLB(self, InternalLB):
        self._InternalLB = InternalLB

    @property
    def CoreDns(self):
        return self._CoreDns

    @CoreDns.setter
    def CoreDns(self, CoreDns):
        self._CoreDns = CoreDns

    @property
    def HealthRegion(self):
        return self._HealthRegion

    @HealthRegion.setter
    def HealthRegion(self, HealthRegion):
        self._HealthRegion = HealthRegion

    @property
    def Health(self):
        return self._Health

    @Health.setter
    def Health(self, Health):
        self._Health = Health

    @property
    def GridDaemon(self):
        return self._GridDaemon

    @GridDaemon.setter
    def GridDaemon(self, GridDaemon):
        self._GridDaemon = GridDaemon

    @property
    def AutoUpgradeClusterLevel(self):
        return self._AutoUpgradeClusterLevel

    @AutoUpgradeClusterLevel.setter
    def AutoUpgradeClusterLevel(self, AutoUpgradeClusterLevel):
        self._AutoUpgradeClusterLevel = AutoUpgradeClusterLevel

    @property
    def ClusterLevel(self):
        return self._ClusterLevel

    @ClusterLevel.setter
    def ClusterLevel(self, ClusterLevel):
        self._ClusterLevel = ClusterLevel


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._ClusterName = params.get("ClusterName")
        self._ClusterDesc = params.get("ClusterDesc")
        self._PodCIDR = params.get("PodCIDR")
        self._ServiceCIDR = params.get("ServiceCIDR")
        if params.get("PublicLB") is not None:
            self._PublicLB = EdgeClusterPublicLB()
            self._PublicLB._deserialize(params.get("PublicLB"))
        if params.get("InternalLB") is not None:
            self._InternalLB = EdgeClusterInternalLB()
            self._InternalLB._deserialize(params.get("InternalLB"))
        self._CoreDns = params.get("CoreDns")
        self._HealthRegion = params.get("HealthRegion")
        self._Health = params.get("Health")
        self._GridDaemon = params.get("GridDaemon")
        self._AutoUpgradeClusterLevel = params.get("AutoUpgradeClusterLevel")
        self._ClusterLevel = params.get("ClusterLevel")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateTKEEdgeClusterResponse(AbstractModel):
    """UpdateTKEEdgeCluster返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpgradeAbleInstancesItem(AbstractModel):
    """可升级节点信息

    """

    def __init__(self):
        r"""
        :param _InstanceId: 节点Id
        :type InstanceId: str
        :param _Version: 节点的当前版本
        :type Version: str
        :param _LatestVersion: 当前版本的最新小版本
注意：此字段可能返回 null，表示取不到有效值。
        :type LatestVersion: str
        :param _RuntimeVersion: RuntimeVersion
        :type RuntimeVersion: str
        :param _RuntimeLatestVersion: RuntimeLatestVersion
        :type RuntimeLatestVersion: str
        """
        self._InstanceId = None
        self._Version = None
        self._LatestVersion = None
        self._RuntimeVersion = None
        self._RuntimeLatestVersion = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, InstanceId):
        self._InstanceId = InstanceId

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def LatestVersion(self):
        return self._LatestVersion

    @LatestVersion.setter
    def LatestVersion(self, LatestVersion):
        self._LatestVersion = LatestVersion

    @property
    def RuntimeVersion(self):
        return self._RuntimeVersion

    @RuntimeVersion.setter
    def RuntimeVersion(self, RuntimeVersion):
        self._RuntimeVersion = RuntimeVersion

    @property
    def RuntimeLatestVersion(self):
        return self._RuntimeLatestVersion

    @RuntimeLatestVersion.setter
    def RuntimeLatestVersion(self, RuntimeLatestVersion):
        self._RuntimeLatestVersion = RuntimeLatestVersion


    def _deserialize(self, params):
        self._InstanceId = params.get("InstanceId")
        self._Version = params.get("Version")
        self._LatestVersion = params.get("LatestVersion")
        self._RuntimeVersion = params.get("RuntimeVersion")
        self._RuntimeLatestVersion = params.get("RuntimeLatestVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeClusterInstancesRequest(AbstractModel):
    """UpgradeClusterInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Operation: create 表示开始一次升级任务
pause 表示停止任务
resume表示继续任务
abort表示终止任务
        :type Operation: str
        :param _UpgradeType: 升级类型，只有Operation是create需要设置
reset 大版本重装升级
hot 小版本热升级
major 大版本原地升级
        :type UpgradeType: str
        :param _InstanceIds: 需要升级的节点列表
        :type InstanceIds: list of str
        :param _ResetParam: 当节点重新加入集群时候所使用的参数，参考添加已有节点接口
        :type ResetParam: :class:`tencentcloud.tke.v20180525.models.UpgradeNodeResetParam`
        :param _SkipPreCheck: 是否忽略节点升级前检查
        :type SkipPreCheck: bool
        :param _MaxNotReadyPercent: 最大可容忍的不可用Pod比例
        :type MaxNotReadyPercent: float
        :param _UpgradeRunTime: 是否升级节点运行时，默认false不升级
        :type UpgradeRunTime: bool
        """
        self._ClusterId = None
        self._Operation = None
        self._UpgradeType = None
        self._InstanceIds = None
        self._ResetParam = None
        self._SkipPreCheck = None
        self._MaxNotReadyPercent = None
        self._UpgradeRunTime = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Operation(self):
        return self._Operation

    @Operation.setter
    def Operation(self, Operation):
        self._Operation = Operation

    @property
    def UpgradeType(self):
        return self._UpgradeType

    @UpgradeType.setter
    def UpgradeType(self, UpgradeType):
        self._UpgradeType = UpgradeType

    @property
    def InstanceIds(self):
        return self._InstanceIds

    @InstanceIds.setter
    def InstanceIds(self, InstanceIds):
        self._InstanceIds = InstanceIds

    @property
    def ResetParam(self):
        return self._ResetParam

    @ResetParam.setter
    def ResetParam(self, ResetParam):
        self._ResetParam = ResetParam

    @property
    def SkipPreCheck(self):
        return self._SkipPreCheck

    @SkipPreCheck.setter
    def SkipPreCheck(self, SkipPreCheck):
        self._SkipPreCheck = SkipPreCheck

    @property
    def MaxNotReadyPercent(self):
        return self._MaxNotReadyPercent

    @MaxNotReadyPercent.setter
    def MaxNotReadyPercent(self, MaxNotReadyPercent):
        self._MaxNotReadyPercent = MaxNotReadyPercent

    @property
    def UpgradeRunTime(self):
        return self._UpgradeRunTime

    @UpgradeRunTime.setter
    def UpgradeRunTime(self, UpgradeRunTime):
        self._UpgradeRunTime = UpgradeRunTime


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Operation = params.get("Operation")
        self._UpgradeType = params.get("UpgradeType")
        self._InstanceIds = params.get("InstanceIds")
        if params.get("ResetParam") is not None:
            self._ResetParam = UpgradeNodeResetParam()
            self._ResetParam._deserialize(params.get("ResetParam"))
        self._SkipPreCheck = params.get("SkipPreCheck")
        self._MaxNotReadyPercent = params.get("MaxNotReadyPercent")
        self._UpgradeRunTime = params.get("UpgradeRunTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeClusterInstancesResponse(AbstractModel):
    """UpgradeClusterInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpgradeClusterReleaseRequest(AbstractModel):
    """UpgradeClusterRelease请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ClusterId: 集群ID
        :type ClusterId: str
        :param _Name: 自定义的应用名称
        :type Name: str
        :param _Namespace: 应用命名空间
        :type Namespace: str
        :param _Chart: 制品名称或从第三方repo 安装chart时，制品压缩包下载地址, 不支持重定向类型chart 地址，结尾为*.tgz
        :type Chart: str
        :param _Values: 自定义参数，覆盖chart 中values.yaml 中的参数
        :type Values: :class:`tencentcloud.tke.v20180525.models.ReleaseValues`
        :param _ChartFrom: 制品来源，范围：tke-market 或 other
        :type ChartFrom: str
        :param _ChartVersion: 制品版本( 从第三安装时，不传这个参数）
        :type ChartVersion: str
        :param _ChartRepoURL: 制品仓库URL地址
        :type ChartRepoURL: str
        :param _Username: 制品访问用户名
        :type Username: str
        :param _Password: 制品访问密码
        :type Password: str
        :param _ChartNamespace: 制品命名空间
        :type ChartNamespace: str
        :param _ClusterType: 集群类型，支持传 tke, eks, tkeedge, exernal(注册集群）
        :type ClusterType: str
        """
        self._ClusterId = None
        self._Name = None
        self._Namespace = None
        self._Chart = None
        self._Values = None
        self._ChartFrom = None
        self._ChartVersion = None
        self._ChartRepoURL = None
        self._Username = None
        self._Password = None
        self._ChartNamespace = None
        self._ClusterType = None

    @property
    def ClusterId(self):
        return self._ClusterId

    @ClusterId.setter
    def ClusterId(self, ClusterId):
        self._ClusterId = ClusterId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Namespace(self):
        return self._Namespace

    @Namespace.setter
    def Namespace(self, Namespace):
        self._Namespace = Namespace

    @property
    def Chart(self):
        return self._Chart

    @Chart.setter
    def Chart(self, Chart):
        self._Chart = Chart

    @property
    def Values(self):
        return self._Values

    @Values.setter
    def Values(self, Values):
        self._Values = Values

    @property
    def ChartFrom(self):
        return self._ChartFrom

    @ChartFrom.setter
    def ChartFrom(self, ChartFrom):
        self._ChartFrom = ChartFrom

    @property
    def ChartVersion(self):
        return self._ChartVersion

    @ChartVersion.setter
    def ChartVersion(self, ChartVersion):
        self._ChartVersion = ChartVersion

    @property
    def ChartRepoURL(self):
        return self._ChartRepoURL

    @ChartRepoURL.setter
    def ChartRepoURL(self, ChartRepoURL):
        self._ChartRepoURL = ChartRepoURL

    @property
    def Username(self):
        return self._Username

    @Username.setter
    def Username(self, Username):
        self._Username = Username

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def ChartNamespace(self):
        return self._ChartNamespace

    @ChartNamespace.setter
    def ChartNamespace(self, ChartNamespace):
        self._ChartNamespace = ChartNamespace

    @property
    def ClusterType(self):
        return self._ClusterType

    @ClusterType.setter
    def ClusterType(self, ClusterType):
        self._ClusterType = ClusterType


    def _deserialize(self, params):
        self._ClusterId = params.get("ClusterId")
        self._Name = params.get("Name")
        self._Namespace = params.get("Namespace")
        self._Chart = params.get("Chart")
        if params.get("Values") is not None:
            self._Values = ReleaseValues()
            self._Values._deserialize(params.get("Values"))
        self._ChartFrom = params.get("ChartFrom")
        self._ChartVersion = params.get("ChartVersion")
        self._ChartRepoURL = params.get("ChartRepoURL")
        self._Username = params.get("Username")
        self._Password = params.get("Password")
        self._ChartNamespace = params.get("ChartNamespace")
        self._ClusterType = params.get("ClusterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeClusterReleaseResponse(AbstractModel):
    """UpgradeClusterRelease返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Release: 应用详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Release: :class:`tencentcloud.tke.v20180525.models.PendingRelease`
        :param _RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Release = None
        self._RequestId = None

    @property
    def Release(self):
        return self._Release

    @Release.setter
    def Release(self, Release):
        self._Release = Release

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Release") is not None:
            self._Release = PendingRelease()
            self._Release._deserialize(params.get("Release"))
        self._RequestId = params.get("RequestId")


class UpgradeNodeResetParam(AbstractModel):
    """节点升级重装参数

    """

    def __init__(self):
        r"""
        :param _InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tencentcloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param _EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tencentcloud.tke.v20180525.models.EnhancedService`
        :param _LoginSettings: 节点登录信息（目前仅支持使用Password或者单个KeyIds）
        :type LoginSettings: :class:`tencentcloud.tke.v20180525.models.LoginSettings`
        :param _SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则绑定默认安全组。（目前仅支持设置单个sgId）
        :type SecurityGroupIds: list of str
        """
        self._InstanceAdvancedSettings = None
        self._EnhancedService = None
        self._LoginSettings = None
        self._SecurityGroupIds = None

    @property
    def InstanceAdvancedSettings(self):
        return self._InstanceAdvancedSettings

    @InstanceAdvancedSettings.setter
    def InstanceAdvancedSettings(self, InstanceAdvancedSettings):
        self._InstanceAdvancedSettings = InstanceAdvancedSettings

    @property
    def EnhancedService(self):
        return self._EnhancedService

    @EnhancedService.setter
    def EnhancedService(self, EnhancedService):
        self._EnhancedService = EnhancedService

    @property
    def LoginSettings(self):
        return self._LoginSettings

    @LoginSettings.setter
    def LoginSettings(self, LoginSettings):
        self._LoginSettings = LoginSettings

    @property
    def SecurityGroupIds(self):
        return self._SecurityGroupIds

    @SecurityGroupIds.setter
    def SecurityGroupIds(self, SecurityGroupIds):
        self._SecurityGroupIds = SecurityGroupIds


    def _deserialize(self, params):
        if params.get("InstanceAdvancedSettings") is not None:
            self._InstanceAdvancedSettings = InstanceAdvancedSettings()
            self._InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("EnhancedService") is not None:
            self._EnhancedService = EnhancedService()
            self._EnhancedService._deserialize(params.get("EnhancedService"))
        if params.get("LoginSettings") is not None:
            self._LoginSettings = LoginSettings()
            self._LoginSettings._deserialize(params.get("LoginSettings"))
        self._SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VersionInstance(AbstractModel):
    """版本信息

    """

    def __init__(self):
        r"""
        :param _Name: 版本名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _Version: 版本信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param _Remark: Remark
注意：此字段可能返回 null，表示取不到有效值。
        :type Remark: str
        """
        self._Name = None
        self._Version = None
        self._Remark = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Version(self):
        return self._Version

    @Version.setter
    def Version(self, Version):
        self._Version = Version

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._Version = params.get("Version")
        self._Remark = params.get("Remark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VirtualNode(AbstractModel):
    """虚拟节点

    """

    def __init__(self):
        r"""
        :param _Name: 虚拟节点名称
        :type Name: str
        :param _SubnetId: 虚拟节点所属子网
        :type SubnetId: str
        :param _Phase: 虚拟节点状态
        :type Phase: str
        :param _CreatedTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreatedTime: str
        """
        self._Name = None
        self._SubnetId = None
        self._Phase = None
        self._CreatedTime = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Phase(self):
        return self._Phase

    @Phase.setter
    def Phase(self, Phase):
        self._Phase = Phase

    @property
    def CreatedTime(self):
        return self._CreatedTime

    @CreatedTime.setter
    def CreatedTime(self, CreatedTime):
        self._CreatedTime = CreatedTime


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._SubnetId = params.get("SubnetId")
        self._Phase = params.get("Phase")
        self._CreatedTime = params.get("CreatedTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VirtualNodePool(AbstractModel):
    """虚拟节点池

    """

    def __init__(self):
        r"""
        :param _NodePoolId: 节点池ID
        :type NodePoolId: str
        :param _SubnetIds: 子网列表
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetIds: list of str
        :param _Name: 节点池名称
        :type Name: str
        :param _LifeState: 节点池生命周期
        :type LifeState: str
        :param _Labels: 虚拟节点label
注意：此字段可能返回 null，表示取不到有效值。
        :type Labels: list of Label
        :param _Taints: 虚拟节点taint
注意：此字段可能返回 null，表示取不到有效值。
        :type Taints: list of Taint
        """
        self._NodePoolId = None
        self._SubnetIds = None
        self._Name = None
        self._LifeState = None
        self._Labels = None
        self._Taints = None

    @property
    def NodePoolId(self):
        return self._NodePoolId

    @NodePoolId.setter
    def NodePoolId(self, NodePoolId):
        self._NodePoolId = NodePoolId

    @property
    def SubnetIds(self):
        return self._SubnetIds

    @SubnetIds.setter
    def SubnetIds(self, SubnetIds):
        self._SubnetIds = SubnetIds

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def LifeState(self):
        return self._LifeState

    @LifeState.setter
    def LifeState(self, LifeState):
        self._LifeState = LifeState

    @property
    def Labels(self):
        return self._Labels

    @Labels.setter
    def Labels(self, Labels):
        self._Labels = Labels

    @property
    def Taints(self):
        return self._Taints

    @Taints.setter
    def Taints(self, Taints):
        self._Taints = Taints


    def _deserialize(self, params):
        self._NodePoolId = params.get("NodePoolId")
        self._SubnetIds = params.get("SubnetIds")
        self._Name = params.get("Name")
        self._LifeState = params.get("LifeState")
        if params.get("Labels") is not None:
            self._Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self._Labels.append(obj)
        if params.get("Taints") is not None:
            self._Taints = []
            for item in params.get("Taints"):
                obj = Taint()
                obj._deserialize(item)
                self._Taints.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VirtualNodeSpec(AbstractModel):
    """虚拟节点

    """

    def __init__(self):
        r"""
        :param _DisplayName: 节点展示名称
        :type DisplayName: str
        :param _SubnetId: 子网ID
        :type SubnetId: str
        :param _Tags: 腾讯云标签
        :type Tags: list of Tag
        """
        self._DisplayName = None
        self._SubnetId = None
        self._Tags = None

    @property
    def DisplayName(self):
        return self._DisplayName

    @DisplayName.setter
    def DisplayName(self, DisplayName):
        self._DisplayName = DisplayName

    @property
    def SubnetId(self):
        return self._SubnetId

    @SubnetId.setter
    def SubnetId(self, SubnetId):
        self._SubnetId = SubnetId

    @property
    def Tags(self):
        return self._Tags

    @Tags.setter
    def Tags(self, Tags):
        self._Tags = Tags


    def _deserialize(self, params):
        self._DisplayName = params.get("DisplayName")
        self._SubnetId = params.get("SubnetId")
        if params.get("Tags") is not None:
            self._Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self._Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VolumeMount(AbstractModel):
    """数据卷挂载路径信息

    """

    def __init__(self):
        r"""
        :param _Name: volume名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param _MountPath: 挂载路径
注意：此字段可能返回 null，表示取不到有效值。
        :type MountPath: str
        :param _ReadOnly: 是否只读
注意：此字段可能返回 null，表示取不到有效值。
        :type ReadOnly: bool
        :param _SubPath: 子路径
注意：此字段可能返回 null，表示取不到有效值。
        :type SubPath: str
        :param _MountPropagation: 传播挂载方式
注意：此字段可能返回 null，表示取不到有效值。
        :type MountPropagation: str
        :param _SubPathExpr: 子路径表达式
注意：此字段可能返回 null，表示取不到有效值。
        :type SubPathExpr: str
        """
        self._Name = None
        self._MountPath = None
        self._ReadOnly = None
        self._SubPath = None
        self._MountPropagation = None
        self._SubPathExpr = None

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def MountPath(self):
        return self._MountPath

    @MountPath.setter
    def MountPath(self, MountPath):
        self._MountPath = MountPath

    @property
    def ReadOnly(self):
        return self._ReadOnly

    @ReadOnly.setter
    def ReadOnly(self, ReadOnly):
        self._ReadOnly = ReadOnly

    @property
    def SubPath(self):
        return self._SubPath

    @SubPath.setter
    def SubPath(self, SubPath):
        self._SubPath = SubPath

    @property
    def MountPropagation(self):
        return self._MountPropagation

    @MountPropagation.setter
    def MountPropagation(self, MountPropagation):
        self._MountPropagation = MountPropagation

    @property
    def SubPathExpr(self):
        return self._SubPathExpr

    @SubPathExpr.setter
    def SubPathExpr(self, SubPathExpr):
        self._SubPathExpr = SubPathExpr


    def _deserialize(self, params):
        self._Name = params.get("Name")
        self._MountPath = params.get("MountPath")
        self._ReadOnly = params.get("ReadOnly")
        self._SubPath = params.get("SubPath")
        self._MountPropagation = params.get("MountPropagation")
        self._SubPathExpr = params.get("SubPathExpr")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        