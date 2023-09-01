# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from aliyunsdkess.request.v20140828.ScaleWithAdjustmentRequest import ScaleWithAdjustmentRequest
from aliyunsdkess.request.v20140828.RemoveInstancesRequest import RemoveInstancesRequest
from aliyunsdkess.request.v20140828.DescribeScalingInstancesRequest import DescribeScalingInstancesRequest
from aliyunsdkess.request.v20140828.DescribeScalingGroupsRequest import DescribeScalingGroupsRequest
from .utils import get_setting, Api

A = lambda c: get_setting('ESS', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')
GROUP_ID = A('GROUP_ID')
AP = A('AP') or "cn-shenzhen"


class EssApi(Api):

    def __init__(self, group_id=GROUP_ID, **kwargs):
        self.group_id = group_id
        self.default_query_params = dict(
            ScalingGroupId=self.group_id
        )
        d = dict(region_id=AP)
        d.update(kwargs)
        return super(EssApi, self).__init__(category='ESS', **d)

    def get_kwargs(self, kwargs):
        d = {}
        d.update(self.default_query_params)
        d.update(kwargs)
        return d

    def scale(self, AdjustmentType='QuantityChangeInCapacity', AdjustmentValue=1, **kwargs):
        return self.call(
            ScaleWithAdjustmentRequest,
            AdjustmentType=AdjustmentType,
            AdjustmentValue=AdjustmentValue,
            **self.get_kwargs(kwargs)
        )

    def remove_instances(self, instances, **kwargs):
        return self.call(RemoveInstancesRequest, InstanceIds=instances, **self.get_kwargs(kwargs))

    def list_instances(self, **kwargs):
        return self.call(DescribeScalingInstancesRequest, 'ScalingInstances.ScalingInstance', **self.get_kwargs(kwargs))

    def list_groups(self, **kwargs):
        return self.call(DescribeScalingGroupsRequest, 'ScalingGroups.ScalingGroup', **kwargs)
