# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict, Any


class ActiveConfigRulesRequest(TeaModel):
    def __init__(
        self,
        config_rule_ids: str = None,
    ):
        # The IDs of the rules. Separate multiple rule IDs with commas (,). You can specify a maximum of 20 rule IDs at a time.
        self.config_rule_ids = config_rule_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_ids is not None:
            result['ConfigRuleIds'] = self.config_rule_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleIds') is not None:
            self.config_rule_ids = m.get('ConfigRuleIds')
        return self


class ActiveConfigRulesResponseBodyOperateRuleResultOperateRuleItemList(TeaModel):
    def __init__(
        self,
        config_rule_id: str = None,
        error_code: str = None,
        success: bool = None,
    ):
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The error code.
        # 
        # *   If the rule is enabled, no error code is returned.
        # *   If you fail to enable the rule, an error code is returned. For more information, visit the [API Error Center](https://error-center.alibabacloud.com/status/product/Config).
        self.error_code = error_code
        # Indicates whether the rule is enabled. Valid values:
        # 
        # *   true
        # *   false
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ActiveConfigRulesResponseBodyOperateRuleResult(TeaModel):
    def __init__(
        self,
        operate_rule_item_list: List[ActiveConfigRulesResponseBodyOperateRuleResultOperateRuleItemList] = None,
    ):
        # The result information about each rule.
        self.operate_rule_item_list = operate_rule_item_list

    def validate(self):
        if self.operate_rule_item_list:
            for k in self.operate_rule_item_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['OperateRuleItemList'] = []
        if self.operate_rule_item_list is not None:
            for k in self.operate_rule_item_list:
                result['OperateRuleItemList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.operate_rule_item_list = []
        if m.get('OperateRuleItemList') is not None:
            for k in m.get('OperateRuleItemList'):
                temp_model = ActiveConfigRulesResponseBodyOperateRuleResultOperateRuleItemList()
                self.operate_rule_item_list.append(temp_model.from_map(k))
        return self


class ActiveConfigRulesResponseBody(TeaModel):
    def __init__(
        self,
        operate_rule_result: ActiveConfigRulesResponseBodyOperateRuleResult = None,
        request_id: str = None,
    ):
        # The result information about the operation.
        self.operate_rule_result = operate_rule_result
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.operate_rule_result:
            self.operate_rule_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operate_rule_result is not None:
            result['OperateRuleResult'] = self.operate_rule_result.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperateRuleResult') is not None:
            temp_model = ActiveConfigRulesResponseBodyOperateRuleResult()
            self.operate_rule_result = temp_model.from_map(m['OperateRuleResult'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ActiveConfigRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ActiveConfigRulesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ActiveConfigRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteConfigRulesRequest(TeaModel):
    def __init__(
        self,
        config_rule_ids: str = None,
    ):
        # The IDs of the rules. Separate multiple rule IDs with commas (,). You can specify a maximum of 20 rule IDs at a time.
        self.config_rule_ids = config_rule_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_ids is not None:
            result['ConfigRuleIds'] = self.config_rule_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleIds') is not None:
            self.config_rule_ids = m.get('ConfigRuleIds')
        return self


class DeleteConfigRulesResponseBodyOperateRuleResultOperateRuleItemList(TeaModel):
    def __init__(
        self,
        config_rule_id: str = None,
        error_code: str = None,
        success: bool = None,
    ):
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The error code.
        # 
        # *   If the rule is deleted, no error code is returned.
        # *   If you fail to delete the rule, an error code is returned. For more information, visit the [API Error Center](https://error-center.alibabacloud.com/status/product/Config).
        self.error_code = error_code
        # Indicates whether the rule is deleted. Valid values:
        # 
        # *   true
        # *   false
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteConfigRulesResponseBodyOperateRuleResult(TeaModel):
    def __init__(
        self,
        operate_rule_item_list: List[DeleteConfigRulesResponseBodyOperateRuleResultOperateRuleItemList] = None,
    ):
        # The result information about each rule.
        self.operate_rule_item_list = operate_rule_item_list

    def validate(self):
        if self.operate_rule_item_list:
            for k in self.operate_rule_item_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['OperateRuleItemList'] = []
        if self.operate_rule_item_list is not None:
            for k in self.operate_rule_item_list:
                result['OperateRuleItemList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.operate_rule_item_list = []
        if m.get('OperateRuleItemList') is not None:
            for k in m.get('OperateRuleItemList'):
                temp_model = DeleteConfigRulesResponseBodyOperateRuleResultOperateRuleItemList()
                self.operate_rule_item_list.append(temp_model.from_map(k))
        return self


class DeleteConfigRulesResponseBody(TeaModel):
    def __init__(
        self,
        operate_rule_result: DeleteConfigRulesResponseBodyOperateRuleResult = None,
        request_id: str = None,
    ):
        # The result information about the operation.
        self.operate_rule_result = operate_rule_result
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.operate_rule_result:
            self.operate_rule_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operate_rule_result is not None:
            result['OperateRuleResult'] = self.operate_rule_result.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperateRuleResult') is not None:
            temp_model = DeleteConfigRulesResponseBodyOperateRuleResult()
            self.operate_rule_result = temp_model.from_map(m['OperateRuleResult'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteConfigRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteConfigRulesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteConfigRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeComplianceRequest(TeaModel):
    def __init__(
        self,
        compliance_type: str = None,
        config_rule_id: str = None,
        member_id: int = None,
        multi_account: bool = None,
        resource_id: str = None,
        resource_type: str = None,
    ):
        # The compliance evaluation result of the resource. Valid values:
        # 
        # *   COMPLIANT: The resource is evaluated to be compliant.
        # *   NON_COMPLIANT: The resource is evaluated to be non-compliant.
        # *   NOT_APPLICABLE: The rule does not apply to the resource.
        # *   INSUFFICIENT_DATA: The resource data is insufficient.
        self.compliance_type = compliance_type
        # The ID of the rule.
        # 
        # If you query compliance evaluation results by resource, you must specify the ConfigRuleId, ResourceType, and ResourceId parameters. Otherwise, the ConfigRuleId parameter becomes invalid.
        self.config_rule_id = config_rule_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account
        # The ID of the resource.
        # 
        # If you query compliance evaluation results by resource, you must specify the ResourceType and ResourceId parameters.
        self.resource_id = resource_id
        # The type of the resource.
        # 
        # If you query compliance evaluation results by resource, you must specify the ResourceType and ResourceId parameters.
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_type is not None:
            result['ComplianceType'] = self.compliance_type
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceType') is not None:
            self.compliance_type = m.get('ComplianceType')
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class DescribeComplianceResponseBodyComplianceResultCompliances(TeaModel):
    def __init__(
        self,
        compliance_type: str = None,
        count: int = None,
    ):
        # The compliance evaluation result of the resource. Valid values:
        # 
        # *   COMPLIANT: The resource is evaluated to be compliant.
        # *   NON_COMPLIANT: The resource is evaluated to be non-compliant.
        # *   NOT_APPLICABLE: The rule does not apply to the resource.
        # *   INSUFFICIENT_DATA: The resource data is insufficient.
        self.compliance_type = compliance_type
        # The number of compliance evaluations with the corresponding result.
        # 
        # *   This parameter returns the total number of evaluated resources if you set the ResourceId parameter in the request.
        # *   This parameter returns the total number of triggered rules if you set the ConfigRuleId parameter in the request.
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_type is not None:
            result['ComplianceType'] = self.compliance_type
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceType') is not None:
            self.compliance_type = m.get('ComplianceType')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeComplianceResponseBodyComplianceResult(TeaModel):
    def __init__(
        self,
        compliances: List[DescribeComplianceResponseBodyComplianceResultCompliances] = None,
        total_count: int = None,
    ):
        # The compliance evaluation results based on compliance types.
        self.compliances = compliances
        # The total number of compliance evaluations.
        # 
        # *   This parameter returns the total number of evaluated resources if you set the ResourceId parameter in the request.
        # *   This parameter returns the total number of triggered rules if you set the ConfigRuleId parameter in the request.
        self.total_count = total_count

    def validate(self):
        if self.compliances:
            for k in self.compliances:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Compliances'] = []
        if self.compliances is not None:
            for k in self.compliances:
                result['Compliances'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.compliances = []
        if m.get('Compliances') is not None:
            for k in m.get('Compliances'):
                temp_model = DescribeComplianceResponseBodyComplianceResultCompliances()
                self.compliances.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class DescribeComplianceResponseBody(TeaModel):
    def __init__(
        self,
        compliance_result: DescribeComplianceResponseBodyComplianceResult = None,
        request_id: str = None,
    ):
        # The statistics of compliance evaluations.
        self.compliance_result = compliance_result
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.compliance_result:
            self.compliance_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_result is not None:
            result['ComplianceResult'] = self.compliance_result.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceResult') is not None:
            temp_model = DescribeComplianceResponseBodyComplianceResult()
            self.compliance_result = temp_model.from_map(m['ComplianceResult'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeComplianceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeComplianceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeComplianceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeComplianceSummaryRequest(TeaModel):
    def __init__(
        self,
        member_id: int = None,
        multi_account: bool = None,
    ):
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        return self


class DescribeComplianceSummaryResponseBodyComplianceSummaryComplianceSummaryByConfigRule(TeaModel):
    def __init__(
        self,
        compliance_summary_timestamp: int = None,
        compliant_count: int = None,
        non_compliant_count: int = None,
        total_count: int = None,
    ):
        # The timestamp when the summary was recorded.
        self.compliance_summary_timestamp = compliance_summary_timestamp
        # The number of rules whose evaluation results are compliant.
        self.compliant_count = compliant_count
        # The number of rules whose evaluation results are non-compliant.
        self.non_compliant_count = non_compliant_count
        # The total number of rules.
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_summary_timestamp is not None:
            result['ComplianceSummaryTimestamp'] = self.compliance_summary_timestamp
        if self.compliant_count is not None:
            result['CompliantCount'] = self.compliant_count
        if self.non_compliant_count is not None:
            result['NonCompliantCount'] = self.non_compliant_count
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceSummaryTimestamp') is not None:
            self.compliance_summary_timestamp = m.get('ComplianceSummaryTimestamp')
        if m.get('CompliantCount') is not None:
            self.compliant_count = m.get('CompliantCount')
        if m.get('NonCompliantCount') is not None:
            self.non_compliant_count = m.get('NonCompliantCount')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class DescribeComplianceSummaryResponseBodyComplianceSummaryComplianceSummaryByResource(TeaModel):
    def __init__(
        self,
        compliance_summary_timestamp: int = None,
        compliant_count: int = None,
        non_compliant_count: int = None,
        total_count: int = None,
    ):
        # The timestamp when the summary was recorded.
        self.compliance_summary_timestamp = compliance_summary_timestamp
        # The number of resources evaluated as compliant.
        self.compliant_count = compliant_count
        # The number of resources evaluated as non-compliant.
        self.non_compliant_count = non_compliant_count
        # The total number of resources.
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_summary_timestamp is not None:
            result['ComplianceSummaryTimestamp'] = self.compliance_summary_timestamp
        if self.compliant_count is not None:
            result['CompliantCount'] = self.compliant_count
        if self.non_compliant_count is not None:
            result['NonCompliantCount'] = self.non_compliant_count
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceSummaryTimestamp') is not None:
            self.compliance_summary_timestamp = m.get('ComplianceSummaryTimestamp')
        if m.get('CompliantCount') is not None:
            self.compliant_count = m.get('CompliantCount')
        if m.get('NonCompliantCount') is not None:
            self.non_compliant_count = m.get('NonCompliantCount')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class DescribeComplianceSummaryResponseBodyComplianceSummary(TeaModel):
    def __init__(
        self,
        compliance_summary_by_config_rule: DescribeComplianceSummaryResponseBodyComplianceSummaryComplianceSummaryByConfigRule = None,
        compliance_summary_by_resource: DescribeComplianceSummaryResponseBodyComplianceSummaryComplianceSummaryByResource = None,
    ):
        # The summary of compliance evaluations from the rule dimension.
        self.compliance_summary_by_config_rule = compliance_summary_by_config_rule
        # The summary of compliance evaluations from the resource dimension.
        self.compliance_summary_by_resource = compliance_summary_by_resource

    def validate(self):
        if self.compliance_summary_by_config_rule:
            self.compliance_summary_by_config_rule.validate()
        if self.compliance_summary_by_resource:
            self.compliance_summary_by_resource.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_summary_by_config_rule is not None:
            result['ComplianceSummaryByConfigRule'] = self.compliance_summary_by_config_rule.to_map()
        if self.compliance_summary_by_resource is not None:
            result['ComplianceSummaryByResource'] = self.compliance_summary_by_resource.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceSummaryByConfigRule') is not None:
            temp_model = DescribeComplianceSummaryResponseBodyComplianceSummaryComplianceSummaryByConfigRule()
            self.compliance_summary_by_config_rule = temp_model.from_map(m['ComplianceSummaryByConfigRule'])
        if m.get('ComplianceSummaryByResource') is not None:
            temp_model = DescribeComplianceSummaryResponseBodyComplianceSummaryComplianceSummaryByResource()
            self.compliance_summary_by_resource = temp_model.from_map(m['ComplianceSummaryByResource'])
        return self


class DescribeComplianceSummaryResponseBody(TeaModel):
    def __init__(
        self,
        compliance_summary: DescribeComplianceSummaryResponseBodyComplianceSummary = None,
        request_id: str = None,
    ):
        # The summary of compliance evaluations.
        self.compliance_summary = compliance_summary
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.compliance_summary:
            self.compliance_summary.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_summary is not None:
            result['ComplianceSummary'] = self.compliance_summary.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceSummary') is not None:
            temp_model = DescribeComplianceSummaryResponseBodyComplianceSummary()
            self.compliance_summary = temp_model.from_map(m['ComplianceSummary'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeComplianceSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeComplianceSummaryResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeComplianceSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeConfigRuleRequest(TeaModel):
    def __init__(
        self,
        config_rule_id: str = None,
        member_id: int = None,
        multi_account: bool = None,
    ):
        # The ID of the rule. You can call the [ListConfigRules](~~169607~~) operation to obtain the rule ID.
        self.config_rule_id = config_rule_id
        # This parameter is unavailable since 00:00:00 on June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00 on May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00 on May 30, 2021. For information about account groups, see [Overview](~~211534~~).
        self.member_id = member_id
        # This parameter is unavailable since 00:00:00 on June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00 on May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00 on May 30, 2021. For information about account groups, see [Overview](~~211534~~).
        self.multi_account = multi_account

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        return self


class DescribeConfigRuleResponseBodyConfigRuleConfigRuleEvaluationStatus(TeaModel):
    def __init__(
        self,
        first_activated_timestamp: int = None,
        first_evaluation_started: bool = None,
        last_error_code: str = None,
        last_error_message: str = None,
        last_failed_evaluation_timestamp: int = None,
        last_failed_invocation_timestamp: int = None,
        last_successful_evaluation_timestamp: int = None,
        last_successful_invocation_timestamp: int = None,
    ):
        # The timestamp when the rule was first triggered.
        self.first_activated_timestamp = first_activated_timestamp
        # Indicates whether resources were evaluated based on the rule. Valid values:
        # 
        # *   true
        # *   false
        self.first_evaluation_started = first_evaluation_started
        # The error code returned for the last failed compliance evaluation.
        self.last_error_code = last_error_code
        # The error message returned for the last failed compliance evaluation.
        self.last_error_message = last_error_message
        # The timestamp when the last failed compliance evaluation of the rule ended.
        self.last_failed_evaluation_timestamp = last_failed_evaluation_timestamp
        # The timestamp when the last failed compliance evaluation of the rule started.
        self.last_failed_invocation_timestamp = last_failed_invocation_timestamp
        # The timestamp when the last successful compliance evaluation of the rule ended.
        self.last_successful_evaluation_timestamp = last_successful_evaluation_timestamp
        # The timestamp when the last successful compliance evaluation of the rule started.
        self.last_successful_invocation_timestamp = last_successful_invocation_timestamp

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.first_activated_timestamp is not None:
            result['FirstActivatedTimestamp'] = self.first_activated_timestamp
        if self.first_evaluation_started is not None:
            result['FirstEvaluationStarted'] = self.first_evaluation_started
        if self.last_error_code is not None:
            result['LastErrorCode'] = self.last_error_code
        if self.last_error_message is not None:
            result['LastErrorMessage'] = self.last_error_message
        if self.last_failed_evaluation_timestamp is not None:
            result['LastFailedEvaluationTimestamp'] = self.last_failed_evaluation_timestamp
        if self.last_failed_invocation_timestamp is not None:
            result['LastFailedInvocationTimestamp'] = self.last_failed_invocation_timestamp
        if self.last_successful_evaluation_timestamp is not None:
            result['LastSuccessfulEvaluationTimestamp'] = self.last_successful_evaluation_timestamp
        if self.last_successful_invocation_timestamp is not None:
            result['LastSuccessfulInvocationTimestamp'] = self.last_successful_invocation_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FirstActivatedTimestamp') is not None:
            self.first_activated_timestamp = m.get('FirstActivatedTimestamp')
        if m.get('FirstEvaluationStarted') is not None:
            self.first_evaluation_started = m.get('FirstEvaluationStarted')
        if m.get('LastErrorCode') is not None:
            self.last_error_code = m.get('LastErrorCode')
        if m.get('LastErrorMessage') is not None:
            self.last_error_message = m.get('LastErrorMessage')
        if m.get('LastFailedEvaluationTimestamp') is not None:
            self.last_failed_evaluation_timestamp = m.get('LastFailedEvaluationTimestamp')
        if m.get('LastFailedInvocationTimestamp') is not None:
            self.last_failed_invocation_timestamp = m.get('LastFailedInvocationTimestamp')
        if m.get('LastSuccessfulEvaluationTimestamp') is not None:
            self.last_successful_evaluation_timestamp = m.get('LastSuccessfulEvaluationTimestamp')
        if m.get('LastSuccessfulInvocationTimestamp') is not None:
            self.last_successful_invocation_timestamp = m.get('LastSuccessfulInvocationTimestamp')
        return self


class DescribeConfigRuleResponseBodyConfigRuleManagedRuleSourceDetails(TeaModel):
    def __init__(
        self,
        event_source: str = None,
        maximum_execution_frequency: str = None,
        message_type: str = None,
    ):
        # The event source of the managed rule.
        # 
        # >  Only events related to Cloud Config are supported. The value is fixed to aliyun.config.
        self.event_source = event_source
        # The intervals at which the managed rule is triggered. Valid values:
        # 
        # *   One_Hour: 1 hour.
        # *   Three_Hours: 3 hours.
        # *   Six_Hours: 6 hours.
        # *   Twelve_Hours: 12 hours.
        # *   TwentyFour_Hours: 24 hours.
        self.maximum_execution_frequency = maximum_execution_frequency
        # The trigger type of the managed rule. Valid values:
        # 
        # *   ConfigurationItemChangeNotification: The managed rule is triggered by configuration changes.
        # *   ScheduledNotification: The managed rule is triggered as scheduled.
        self.message_type = message_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.event_source is not None:
            result['EventSource'] = self.event_source
        if self.maximum_execution_frequency is not None:
            result['MaximumExecutionFrequency'] = self.maximum_execution_frequency
        if self.message_type is not None:
            result['MessageType'] = self.message_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventSource') is not None:
            self.event_source = m.get('EventSource')
        if m.get('MaximumExecutionFrequency') is not None:
            self.maximum_execution_frequency = m.get('MaximumExecutionFrequency')
        if m.get('MessageType') is not None:
            self.message_type = m.get('MessageType')
        return self


class DescribeConfigRuleResponseBodyConfigRuleManagedRule(TeaModel):
    def __init__(
        self,
        compulsory_input_parameter_details: Dict[str, Any] = None,
        description: str = None,
        identifier: str = None,
        labels: List[str] = None,
        managed_rule_name: str = None,
        optional_input_parameter_details: Dict[str, Any] = None,
        source_details: List[DescribeConfigRuleResponseBodyConfigRuleManagedRuleSourceDetails] = None,
    ):
        # The settings of the required input parameters for the managed rule.
        self.compulsory_input_parameter_details = compulsory_input_parameter_details
        # The description of the managed rule.
        self.description = description
        # The identifier of the managed rule.
        self.identifier = identifier
        # The labels.
        self.labels = labels
        # The name of the managed rule.
        self.managed_rule_name = managed_rule_name
        # The settings of the optional input parameters for the managed rule.
        self.optional_input_parameter_details = optional_input_parameter_details
        # The intervals at which the rule is triggered. Valid values:
        # 
        # *   One_Hour: 1 hour
        # *   Three_Hours: 3 hours
        # *   Six_Hours: 6 hours
        # *   Twelve_Hours: 12 hours.
        # *   TwentyFour_Hours: 24 hours.
        self.source_details = source_details

    def validate(self):
        if self.source_details:
            for k in self.source_details:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compulsory_input_parameter_details is not None:
            result['CompulsoryInputParameterDetails'] = self.compulsory_input_parameter_details
        if self.description is not None:
            result['Description'] = self.description
        if self.identifier is not None:
            result['Identifier'] = self.identifier
        if self.labels is not None:
            result['Labels'] = self.labels
        if self.managed_rule_name is not None:
            result['ManagedRuleName'] = self.managed_rule_name
        if self.optional_input_parameter_details is not None:
            result['OptionalInputParameterDetails'] = self.optional_input_parameter_details
        result['SourceDetails'] = []
        if self.source_details is not None:
            for k in self.source_details:
                result['SourceDetails'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CompulsoryInputParameterDetails') is not None:
            self.compulsory_input_parameter_details = m.get('CompulsoryInputParameterDetails')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Identifier') is not None:
            self.identifier = m.get('Identifier')
        if m.get('Labels') is not None:
            self.labels = m.get('Labels')
        if m.get('ManagedRuleName') is not None:
            self.managed_rule_name = m.get('ManagedRuleName')
        if m.get('OptionalInputParameterDetails') is not None:
            self.optional_input_parameter_details = m.get('OptionalInputParameterDetails')
        self.source_details = []
        if m.get('SourceDetails') is not None:
            for k in m.get('SourceDetails'):
                temp_model = DescribeConfigRuleResponseBodyConfigRuleManagedRuleSourceDetails()
                self.source_details.append(temp_model.from_map(k))
        return self


class DescribeConfigRuleResponseBodyConfigRuleScope(TeaModel):
    def __init__(
        self,
        compliance_resource_id: str = None,
        compliance_resource_types: List[str] = None,
    ):
        # The ID of the resource to be evaluated.
        self.compliance_resource_id = compliance_resource_id
        # The types of the resources to be evaluated.
        self.compliance_resource_types = compliance_resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_resource_id is not None:
            result['ComplianceResourceId'] = self.compliance_resource_id
        if self.compliance_resource_types is not None:
            result['ComplianceResourceTypes'] = self.compliance_resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceResourceId') is not None:
            self.compliance_resource_id = m.get('ComplianceResourceId')
        if m.get('ComplianceResourceTypes') is not None:
            self.compliance_resource_types = m.get('ComplianceResourceTypes')
        return self


class DescribeConfigRuleResponseBodyConfigRuleSourceSourceConditions(TeaModel):
    def __init__(
        self,
        desired_value: str = None,
        name: str = None,
        operator: str = None,
        tips: str = None,
    ):
        # The expected value of the input parameter.
        self.desired_value = desired_value
        # The name of the input parameter for the rule.
        self.name = name
        # The operator used to compare the actual value against the expected value of the input parameter. The operator varies based on the type of data returned for the SelectPath parameter.
        # 
        # *   Valid values for the String data type:
        # 
        #     *   StringEquals: The actual value is equal to the expected value.
        #     *   NotStringEquals: The actual value is not equal to the expected value.
        #     *   StringIn: The actual value exists in the expected value.
        #     *   NotStringIn: The actual value does not exist in the expected value.
        #     *   StringContains: The actual value contains the expected value.
        #     *   NotStringContains: The actual value does not contain the expected value.
        # 
        # *   Valid values for the Number data type:
        # 
        #     *   Equals: The actual value is equal to the expected value.
        #     *   NotEquals: The actual value is not equal to the expected value.
        #     *   Less: The actual value is less than the expected value.
        #     *   LessOrEquals: The actual value is less than or equal to the expected value.
        #     *   Greater: The actual value is greater than the expected value.
        #     *   GreaterOrEquals: The actual value is greater than or equal to the expected value.
        # 
        # *   Valid values for the Base64String data type that indicates a Base64-encoded string:
        # 
        #     *   Base64Contains: The actual value contains the expected value.
        #     *   NotBase64Contains: The actual value does not contain the expected value.
        #     *   Base64ContainsAll: The actual value contains all characters in the expected value.
        #     *   Base64ExcludeAll: The actual value excludes all characters in the expected value.
        # 
        # *   Valid values for the Array data type:
        # 
        #     *   Contains: The actual value contains the expected value.
        #     *   NotContains: The actual value does not contain the expected value.
        #     *   In: The actual value exists in the expected value.
        #     *   NotIn: The actual value does not exist in the expected value.
        #     *   ContainsAll: The actual value contains all elements of the expected value.
        #     *   ExcludeAll: The actual value excludes all elements of the expected value.
        #     *   IsEmpty: The actual value is null.
        self.operator = operator
        # The description of the input parameter.
        self.tips = tips

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.desired_value is not None:
            result['DesiredValue'] = self.desired_value
        if self.name is not None:
            result['Name'] = self.name
        if self.operator is not None:
            result['Operator'] = self.operator
        if self.tips is not None:
            result['Tips'] = self.tips
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DesiredValue') is not None:
            self.desired_value = m.get('DesiredValue')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Operator') is not None:
            self.operator = m.get('Operator')
        if m.get('Tips') is not None:
            self.tips = m.get('Tips')
        return self


class DescribeConfigRuleResponseBodyConfigRuleSourceSourceDetails(TeaModel):
    def __init__(
        self,
        event_source: str = None,
        maximum_execution_frequency: str = None,
        message_type: str = None,
    ):
        # The event source of the rule.
        # 
        # >  Only events related to Cloud Config are supported. The value is fixed to aliyun.config.
        self.event_source = event_source
        # The intervals at which the rule is triggered. Valid values:
        # 
        # *   One_Hour: 1 hour.
        # *   Three_Hours: 3 hours.
        # *   Six_Hours: 6 hours.
        # *   Twelve_Hours: 12 hours.
        # *   TwentyFour_Hours: 24 hours.
        self.maximum_execution_frequency = maximum_execution_frequency
        # The trigger type of the rule. Valid values:
        # 
        # *   ConfigurationItemChangeNotification: The rule is triggered by configuration changes.
        # *   ScheduledNotification: The rule is triggered as scheduled.
        self.message_type = message_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.event_source is not None:
            result['EventSource'] = self.event_source
        if self.maximum_execution_frequency is not None:
            result['MaximumExecutionFrequency'] = self.maximum_execution_frequency
        if self.message_type is not None:
            result['MessageType'] = self.message_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventSource') is not None:
            self.event_source = m.get('EventSource')
        if m.get('MaximumExecutionFrequency') is not None:
            self.maximum_execution_frequency = m.get('MaximumExecutionFrequency')
        if m.get('MessageType') is not None:
            self.message_type = m.get('MessageType')
        return self


class DescribeConfigRuleResponseBodyConfigRuleSource(TeaModel):
    def __init__(
        self,
        identifier: str = None,
        owner: str = None,
        source_conditions: List[DescribeConfigRuleResponseBodyConfigRuleSourceSourceConditions] = None,
        source_details: List[DescribeConfigRuleResponseBodyConfigRuleSourceSourceDetails] = None,
    ):
        # The identifier of the rule.
        # 
        # *   If the rule was created based on a managed rule, the value of this parameter is the name of the managed rule.
        # *   If the rule is a custom rule, the value of this parameter is the Alibaba Cloud Resource Name (ARN) of the relevant function in Function Compute.
        self.identifier = identifier
        # The way in which the rule was created. Valid values:
        # 
        # *   CUSTOM_FC: The rule is a custom rule.
        # *   ALIYUN: The rule was created based on a managed rule of Alibaba Cloud.
        self.owner = owner
        # The name of the input parameter for the rule.
        self.source_conditions = source_conditions
        # The intervals at which the rule is triggered. Valid values:
        # 
        # *   One_Hour: 1 hour
        # *   Three_Hours: 3 hours
        # *   Six_Hours: 6 hours
        # *   Twelve_Hours: 12 hours.
        # *   TwentyFour_Hours: 24 hours.
        self.source_details = source_details

    def validate(self):
        if self.source_conditions:
            for k in self.source_conditions:
                if k:
                    k.validate()
        if self.source_details:
            for k in self.source_details:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.identifier is not None:
            result['Identifier'] = self.identifier
        if self.owner is not None:
            result['Owner'] = self.owner
        result['SourceConditions'] = []
        if self.source_conditions is not None:
            for k in self.source_conditions:
                result['SourceConditions'].append(k.to_map() if k else None)
        result['SourceDetails'] = []
        if self.source_details is not None:
            for k in self.source_details:
                result['SourceDetails'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Identifier') is not None:
            self.identifier = m.get('Identifier')
        if m.get('Owner') is not None:
            self.owner = m.get('Owner')
        self.source_conditions = []
        if m.get('SourceConditions') is not None:
            for k in m.get('SourceConditions'):
                temp_model = DescribeConfigRuleResponseBodyConfigRuleSourceSourceConditions()
                self.source_conditions.append(temp_model.from_map(k))
        self.source_details = []
        if m.get('SourceDetails') is not None:
            for k in m.get('SourceDetails'):
                temp_model = DescribeConfigRuleResponseBodyConfigRuleSourceSourceDetails()
                self.source_details.append(temp_model.from_map(k))
        return self


class DescribeConfigRuleResponseBodyConfigRule(TeaModel):
    def __init__(
        self,
        config_rule_arn: str = None,
        config_rule_evaluation_status: DescribeConfigRuleResponseBodyConfigRuleConfigRuleEvaluationStatus = None,
        config_rule_id: str = None,
        config_rule_name: str = None,
        config_rule_state: str = None,
        create_timestamp: int = None,
        description: str = None,
        input_parameters: Dict[str, Any] = None,
        managed_rule: DescribeConfigRuleResponseBodyConfigRuleManagedRule = None,
        maximum_execution_frequency: str = None,
        modified_timestamp: int = None,
        risk_level: int = None,
        scope: DescribeConfigRuleResponseBodyConfigRuleScope = None,
        source: DescribeConfigRuleResponseBodyConfigRuleSource = None,
    ):
        # The Alibaba Cloud Resource Name (ARN) of the rule.
        self.config_rule_arn = config_rule_arn
        # The information about compliance evaluations performed by the rule.
        self.config_rule_evaluation_status = config_rule_evaluation_status
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The name of the evaluation rule.
        self.config_rule_name = config_rule_name
        # The status of the rule. Valid values:
        # 
        # *   ACTIVE: The rule is enabled.
        # *   EVALUATING: The rule was triggered and is being used to monitor resource configurations.
        # *   INACTIVE: The rule was disabled.
        self.config_rule_state = config_rule_state
        # The timestamp when the rule was created.
        self.create_timestamp = create_timestamp
        # The description of the system defense rule.
        self.description = description
        # The input parameters of the rule.
        self.input_parameters = input_parameters
        # The details of the managed rule.
        self.managed_rule = managed_rule
        # The intervals at which the rule is triggered. Valid values:
        # 
        # *   One_Hour: 1 hour
        # *   Three_Hours: 3 hours
        # *   Six_Hours: 6 hours
        # *   Twelve_Hours: 12 hours.
        # *   TwentyFour_Hours: 24 hours.
        self.maximum_execution_frequency = maximum_execution_frequency
        # The timestamp when the rule was last modified.
        self.modified_timestamp = modified_timestamp
        # The risk level of the resources that are not compliant with the rule. Valid values:
        # 
        # *   1: high
        # *   2: medium
        # *   3: low
        self.risk_level = risk_level
        # The monitoring scope of the rule.
        self.scope = scope
        # The information about the trigger of the rule.
        self.source = source

    def validate(self):
        if self.config_rule_evaluation_status:
            self.config_rule_evaluation_status.validate()
        if self.managed_rule:
            self.managed_rule.validate()
        if self.scope:
            self.scope.validate()
        if self.source:
            self.source.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_arn is not None:
            result['ConfigRuleArn'] = self.config_rule_arn
        if self.config_rule_evaluation_status is not None:
            result['ConfigRuleEvaluationStatus'] = self.config_rule_evaluation_status.to_map()
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.config_rule_name is not None:
            result['ConfigRuleName'] = self.config_rule_name
        if self.config_rule_state is not None:
            result['ConfigRuleState'] = self.config_rule_state
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.description is not None:
            result['Description'] = self.description
        if self.input_parameters is not None:
            result['InputParameters'] = self.input_parameters
        if self.managed_rule is not None:
            result['ManagedRule'] = self.managed_rule.to_map()
        if self.maximum_execution_frequency is not None:
            result['MaximumExecutionFrequency'] = self.maximum_execution_frequency
        if self.modified_timestamp is not None:
            result['ModifiedTimestamp'] = self.modified_timestamp
        if self.risk_level is not None:
            result['RiskLevel'] = self.risk_level
        if self.scope is not None:
            result['Scope'] = self.scope.to_map()
        if self.source is not None:
            result['Source'] = self.source.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleArn') is not None:
            self.config_rule_arn = m.get('ConfigRuleArn')
        if m.get('ConfigRuleEvaluationStatus') is not None:
            temp_model = DescribeConfigRuleResponseBodyConfigRuleConfigRuleEvaluationStatus()
            self.config_rule_evaluation_status = temp_model.from_map(m['ConfigRuleEvaluationStatus'])
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ConfigRuleName') is not None:
            self.config_rule_name = m.get('ConfigRuleName')
        if m.get('ConfigRuleState') is not None:
            self.config_rule_state = m.get('ConfigRuleState')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('InputParameters') is not None:
            self.input_parameters = m.get('InputParameters')
        if m.get('ManagedRule') is not None:
            temp_model = DescribeConfigRuleResponseBodyConfigRuleManagedRule()
            self.managed_rule = temp_model.from_map(m['ManagedRule'])
        if m.get('MaximumExecutionFrequency') is not None:
            self.maximum_execution_frequency = m.get('MaximumExecutionFrequency')
        if m.get('ModifiedTimestamp') is not None:
            self.modified_timestamp = m.get('ModifiedTimestamp')
        if m.get('RiskLevel') is not None:
            self.risk_level = m.get('RiskLevel')
        if m.get('Scope') is not None:
            temp_model = DescribeConfigRuleResponseBodyConfigRuleScope()
            self.scope = temp_model.from_map(m['Scope'])
        if m.get('Source') is not None:
            temp_model = DescribeConfigRuleResponseBodyConfigRuleSource()
            self.source = temp_model.from_map(m['Source'])
        return self


class DescribeConfigRuleResponseBody(TeaModel):
    def __init__(
        self,
        config_rule: DescribeConfigRuleResponseBodyConfigRule = None,
        request_id: str = None,
    ):
        # The details of the rule.
        self.config_rule = config_rule
        # The request ID.
        self.request_id = request_id

    def validate(self):
        if self.config_rule:
            self.config_rule.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule is not None:
            result['ConfigRule'] = self.config_rule.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRule') is not None:
            temp_model = DescribeConfigRuleResponseBodyConfigRule()
            self.config_rule = temp_model.from_map(m['ConfigRule'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeConfigRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeConfigRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeConfigRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeConfigurationRecorderResponseBodyConfigurationRecorder(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        configuration_recorder_status: str = None,
        organization_enable_status: str = None,
        organization_master_id: int = None,
        resource_types: List[str] = None,
    ):
        # The ID of your Alibaba Cloud account.
        self.account_id = account_id
        # The status of the configuration recorder. Valid values:
        # 
        # *   REGISTRABLE: The configuration recorder has not been registered.
        # *   BUILDING: The configuration recorder is being deployed.
        # *   REGISTERED: The configuration recorder has been registered.
        # *   REBUILDING: The configuration recorder is being redeployed.
        self.configuration_recorder_status = configuration_recorder_status
        # Indicates whether Cloud Config is upgraded to Cloud Config for Enterprise. Valid values:
        # 
        # *   REGISTRABLE: Cloud Config is not upgraded to Cloud Config for Enterprise.
        # *   BUILDING: Cloud Config is being upgraded to Cloud Config for Enterprise.
        # *   REGISTERED: Cloud Config is upgraded to Cloud Config for Enterprise.
        self.organization_enable_status = organization_enable_status
        # The ID of the management account.
        # 
        # >  This parameter is returned only when the operation is called by a management account.
        self.organization_master_id = organization_master_id
        # The types of resources that are monitored by Cloud Config.
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.configuration_recorder_status is not None:
            result['ConfigurationRecorderStatus'] = self.configuration_recorder_status
        if self.organization_enable_status is not None:
            result['OrganizationEnableStatus'] = self.organization_enable_status
        if self.organization_master_id is not None:
            result['OrganizationMasterId'] = self.organization_master_id
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('ConfigurationRecorderStatus') is not None:
            self.configuration_recorder_status = m.get('ConfigurationRecorderStatus')
        if m.get('OrganizationEnableStatus') is not None:
            self.organization_enable_status = m.get('OrganizationEnableStatus')
        if m.get('OrganizationMasterId') is not None:
            self.organization_master_id = m.get('OrganizationMasterId')
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class DescribeConfigurationRecorderResponseBody(TeaModel):
    def __init__(
        self,
        configuration_recorder: DescribeConfigurationRecorderResponseBodyConfigurationRecorder = None,
        request_id: str = None,
    ):
        # The details of the configuration recorder that monitors resources.
        self.configuration_recorder = configuration_recorder
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.configuration_recorder:
            self.configuration_recorder.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.configuration_recorder is not None:
            result['ConfigurationRecorder'] = self.configuration_recorder.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigurationRecorder') is not None:
            temp_model = DescribeConfigurationRecorderResponseBodyConfigurationRecorder()
            self.configuration_recorder = temp_model.from_map(m['ConfigurationRecorder'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeConfigurationRecorderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeConfigurationRecorderResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeConfigurationRecorderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDeliveryChannelsRequest(TeaModel):
    def __init__(
        self,
        delivery_channel_ids: str = None,
    ):
        # The ID of the delivery channel. Separate multiple IDs with commas (,).
        # 
        # For more information about how to obtain the ID of a delivery channel, see [PutDeliveryChannel](~~174253~~).
        self.delivery_channel_ids = delivery_channel_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delivery_channel_ids is not None:
            result['DeliveryChannelIds'] = self.delivery_channel_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeliveryChannelIds') is not None:
            self.delivery_channel_ids = m.get('DeliveryChannelIds')
        return self


class DescribeDeliveryChannelsResponseBodyDeliveryChannels(TeaModel):
    def __init__(
        self,
        configuration_item_change_notification: bool = None,
        configuration_snapshot: bool = None,
        delivery_channel_assume_role_arn: str = None,
        delivery_channel_condition: str = None,
        delivery_channel_id: str = None,
        delivery_channel_name: str = None,
        delivery_channel_target_arn: str = None,
        delivery_channel_type: str = None,
        description: str = None,
        non_compliant_notification: bool = None,
        oversized_data_osstarget_arn: str = None,
        status: int = None,
    ):
        # Indicates whether the resource change logs are received by the specified destination. If you set this parameter to true, Cloud Config delivers the resource change logs to OSS, Log Service, or MNS when the configurations of the resources change. Valid values:
        # 
        # *   true: The resource change logs are received by the specified destination.
        # *   false: The resource change logs are not received by the specified destination.
        self.configuration_item_change_notification = configuration_item_change_notification
        # Indicates whether the scheduled resource snapshots are received by the OSS bucket. If you set this parameter to true, Cloud Config delivers the scheduled resource snapshots to the specified OSS bucket at 00:00:00 and 12:00:00 every day. Valid values:
        # 
        # *   true: The scheduled resource snapshots are received by the specified OSS bucket.
        # *   false: The scheduled resource snapshots are not received by the specified OSS bucket.
        self.configuration_snapshot = configuration_snapshot
        # The Alibaba Cloud Resource Name (ARN) of the role assumed by the delivery channel.
        self.delivery_channel_assume_role_arn = delivery_channel_assume_role_arn
        # The rule attached to the delivery channel. This parameter is applicable only to delivery channels of the MNS type.
        # 
        # This parameter indicates the lowest risk level for the events to subscribe to and the resource types for which you subscribe to events.
        # 
        # *   The setting of the lowest risk level for the events to subscribe to is in the following format: `{"filterType":"RuleRiskLevel","value":"1","multiple":false}`.
        # 
        #     The value field indicates the lowest risk level. Valid values: 1, 2, and 3. A value of 1 indicates the high risk level. A value of 2 indicates the medium risk level. A value of 3 indicates the low risk level.
        # 
        # *   The setting of the resource types for which you subscribe to events is in the following format: `{"filterType":"ResourceType","values":["ACS::ACK::Cluster","ACS::ActionTrail::Trail","ACS::CBWP::CommonBandwidthPackage"],"multiple":true}`.
        # 
        #     The values field indicates the resource types for which you subscribe to events. Its value is a JSON array.
        # 
        #     Example: `[{"filterType":"ResourceType","values":["ACS::ActionTrail::Trail","ACS::CBWP::CommonBandwidthPackage","ACS::CDN::Domain","ACS::CEN::CenBandwidthPackage","ACS::CEN::CenInstance","ACS::CEN::Flowlog","ACS::DdosCoo::Instance"],"multiple":true}]`
        self.delivery_channel_condition = delivery_channel_condition
        # The ID of the delivery channel.
        self.delivery_channel_id = delivery_channel_id
        # The name of the delivery channel.
        self.delivery_channel_name = delivery_channel_name
        # The ARN of the delivery destination.
        # 
        # *   If the DeliveryChannelType parameter is set to OSS, the value of this parameter is the ARN of the destination OSS bucket.
        # *   If the DeliveryChannelType parameter is set to MNS, the value of this parameter is the ARN of the destination MNS topic.
        # *   If the DeliveryChannelType parameter is set to SLS, the value is the ARN of the destination Log Service Logstore.
        self.delivery_channel_target_arn = delivery_channel_target_arn
        # The type of the delivery channel. Valid values:
        # 
        # *   OSS: Object Storage Service (OSS)
        # *   MNS: Message Service (MNS)
        # *   SLS: Log Service
        self.delivery_channel_type = delivery_channel_type
        # The description of the delivery channel.
        self.description = description
        # Indicates whether the resource non-compliance events are received by the specified destination. If you set this parameter to true, Cloud Config delivers resource non-compliance events to Log Service or MNS when resources are evaluated as non-compliant. Valid values:
        # 
        # *   true: The resource non-compliance events are received by the specified destination.
        # *   false: The resource non-compliance events are not received by the specified destination.
        self.non_compliant_notification = non_compliant_notification
        # The ARN of the OSS bucket to which the delivered data is transferred when the size of the data exceeds the specified upper limit of the delivery channel.
        self.oversized_data_osstarget_arn = oversized_data_osstarget_arn
        # The status of the delivery channel. Valid values:
        # 
        # *   0: The delivery channel is disabled.
        # *   1: The delivery channel is enabled.
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.configuration_item_change_notification is not None:
            result['ConfigurationItemChangeNotification'] = self.configuration_item_change_notification
        if self.configuration_snapshot is not None:
            result['ConfigurationSnapshot'] = self.configuration_snapshot
        if self.delivery_channel_assume_role_arn is not None:
            result['DeliveryChannelAssumeRoleArn'] = self.delivery_channel_assume_role_arn
        if self.delivery_channel_condition is not None:
            result['DeliveryChannelCondition'] = self.delivery_channel_condition
        if self.delivery_channel_id is not None:
            result['DeliveryChannelId'] = self.delivery_channel_id
        if self.delivery_channel_name is not None:
            result['DeliveryChannelName'] = self.delivery_channel_name
        if self.delivery_channel_target_arn is not None:
            result['DeliveryChannelTargetArn'] = self.delivery_channel_target_arn
        if self.delivery_channel_type is not None:
            result['DeliveryChannelType'] = self.delivery_channel_type
        if self.description is not None:
            result['Description'] = self.description
        if self.non_compliant_notification is not None:
            result['NonCompliantNotification'] = self.non_compliant_notification
        if self.oversized_data_osstarget_arn is not None:
            result['OversizedDataOSSTargetArn'] = self.oversized_data_osstarget_arn
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigurationItemChangeNotification') is not None:
            self.configuration_item_change_notification = m.get('ConfigurationItemChangeNotification')
        if m.get('ConfigurationSnapshot') is not None:
            self.configuration_snapshot = m.get('ConfigurationSnapshot')
        if m.get('DeliveryChannelAssumeRoleArn') is not None:
            self.delivery_channel_assume_role_arn = m.get('DeliveryChannelAssumeRoleArn')
        if m.get('DeliveryChannelCondition') is not None:
            self.delivery_channel_condition = m.get('DeliveryChannelCondition')
        if m.get('DeliveryChannelId') is not None:
            self.delivery_channel_id = m.get('DeliveryChannelId')
        if m.get('DeliveryChannelName') is not None:
            self.delivery_channel_name = m.get('DeliveryChannelName')
        if m.get('DeliveryChannelTargetArn') is not None:
            self.delivery_channel_target_arn = m.get('DeliveryChannelTargetArn')
        if m.get('DeliveryChannelType') is not None:
            self.delivery_channel_type = m.get('DeliveryChannelType')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('NonCompliantNotification') is not None:
            self.non_compliant_notification = m.get('NonCompliantNotification')
        if m.get('OversizedDataOSSTargetArn') is not None:
            self.oversized_data_osstarget_arn = m.get('OversizedDataOSSTargetArn')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeDeliveryChannelsResponseBody(TeaModel):
    def __init__(
        self,
        delivery_channels: List[DescribeDeliveryChannelsResponseBodyDeliveryChannels] = None,
        request_id: str = None,
    ):
        # The information about the delivery channel.
        self.delivery_channels = delivery_channels
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.delivery_channels:
            for k in self.delivery_channels:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DeliveryChannels'] = []
        if self.delivery_channels is not None:
            for k in self.delivery_channels:
                result['DeliveryChannels'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.delivery_channels = []
        if m.get('DeliveryChannels') is not None:
            for k in m.get('DeliveryChannels'):
                temp_model = DescribeDeliveryChannelsResponseBodyDeliveryChannels()
                self.delivery_channels.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeDeliveryChannelsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeDeliveryChannelsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeDeliveryChannelsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDiscoveredResourceRequest(TeaModel):
    def __init__(
        self,
        member_id: int = None,
        multi_account: bool = None,
        region: str = None,
        resource_id: str = None,
        resource_type: str = None,
    ):
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account
        # The ID of the region.
        self.region = region
        # The ID of the resource.
        self.resource_id = resource_id
        # The type of the resource.
        # 
        # >  You can call the GetSupportedResourceTypes operation to query the resource types supported by Cloud Config. For more information, see [GetSupportedResourceTypes](~~169618~~).
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class DescribeDiscoveredResourceResponseBodyDiscoveredResourceDetail(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        availability_zone: str = None,
        configuration: str = None,
        region: str = None,
        resource_creation_time: int = None,
        resource_deleted: int = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_status: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        # The ID of your Alibaba Cloud account.
        self.account_id = account_id
        # The zone where the resource resides.
        self.availability_zone = availability_zone
        # The configuration of the resource.
        self.configuration = configuration
        # The ID of the region.
        self.region = region
        # The timestamp when the resource was created.
        self.resource_creation_time = resource_creation_time
        # Indicates whether the resource is deleted. Valid values:
        # 
        # *   1: The resource is not deleted.
        # *   0: The resource is deleted.
        self.resource_deleted = resource_deleted
        # The ID of the resource.
        self.resource_id = resource_id
        # The name of the resource.
        self.resource_name = resource_name
        # The status of the resource. The parameter value varies with the resource type and may be left empty. Examples:
        # 
        # *   If ResourceType is set to ACS::ECS::Instance, the resource is an Elastic Compute Service (ECS) instance which has a specific state. In this case, valid values of this parameter include Running and Stopped.
        # *   If ResourceType is set to ACS::OSS::Bucket, the resource is an Object Storage Service (OSS) bucket which does not have a specific state. In this case, this parameter is left empty.
        self.resource_status = resource_status
        # The type of the resource.
        self.resource_type = resource_type
        # The tags of the resource.
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.availability_zone is not None:
            result['AvailabilityZone'] = self.availability_zone
        if self.configuration is not None:
            result['Configuration'] = self.configuration
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_creation_time is not None:
            result['ResourceCreationTime'] = self.resource_creation_time
        if self.resource_deleted is not None:
            result['ResourceDeleted'] = self.resource_deleted
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_status is not None:
            result['ResourceStatus'] = self.resource_status
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('AvailabilityZone') is not None:
            self.availability_zone = m.get('AvailabilityZone')
        if m.get('Configuration') is not None:
            self.configuration = m.get('Configuration')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceCreationTime') is not None:
            self.resource_creation_time = m.get('ResourceCreationTime')
        if m.get('ResourceDeleted') is not None:
            self.resource_deleted = m.get('ResourceDeleted')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceStatus') is not None:
            self.resource_status = m.get('ResourceStatus')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class DescribeDiscoveredResourceResponseBody(TeaModel):
    def __init__(
        self,
        discovered_resource_detail: DescribeDiscoveredResourceResponseBodyDiscoveredResourceDetail = None,
        request_id: str = None,
    ):
        # The information about the resource.
        self.discovered_resource_detail = discovered_resource_detail
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.discovered_resource_detail:
            self.discovered_resource_detail.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.discovered_resource_detail is not None:
            result['DiscoveredResourceDetail'] = self.discovered_resource_detail.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DiscoveredResourceDetail') is not None:
            temp_model = DescribeDiscoveredResourceResponseBodyDiscoveredResourceDetail()
            self.discovered_resource_detail = temp_model.from_map(m['DiscoveredResourceDetail'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeDiscoveredResourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeDiscoveredResourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeDiscoveredResourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeEvaluationResultsRequest(TeaModel):
    def __init__(
        self,
        compliance_type: str = None,
        config_rule_id: str = None,
        member_id: int = None,
        multi_account: bool = None,
        page_number: int = None,
        page_size: int = None,
        resource_id: str = None,
        resource_type: str = None,
    ):
        # The compliance evaluation result. Valid values:
        # 
        # *   COMPLIANT: The resources are evaluated as compliant.
        # *   NON_COMPLIANT: The resources are evaluated as non-compliant.
        # *   NOT_APPLICABLE: The rule does not apply to the resources.
        # *   INSUFFICIENT_DATA: The resource data is insufficient.
        self.compliance_type = compliance_type
        # The rule ID. If you query the compliance evaluation results of resources by rule, you must specify this parameter.
        # 
        # > You must specify the ResourceType or ConfigRuleId parameter.
        self.config_rule_id = config_rule_id
        # This parameter is unavailable since 00:00:00 on June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00 on May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00 on May 30, 2021. For information about account groups, see [Overview](~~211534~~).
        self.member_id = member_id
        # This parameter is unavailable since 00:00:00 on June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00 on May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00 on May 30, 2021. For information about account groups, see [Overview](~~211534~~).
        self.multi_account = multi_account
        # The number of the page to return. Pages start from page 1.
        self.page_number = page_number
        # The number of entries to return per page. Valid values: 1 to 100.
        self.page_size = page_size
        # The resource ID. If you query the compliance evaluation results of resources by resource type, you must specify this parameter.
        self.resource_id = resource_id
        # The type of resource. If you query the compliance evaluation results of resources by resource type, you must specify this parameter.
        # 
        # You can call the GetSupportedResourceTypes operation to query the resource types supported by Cloud Config. For more information, see [GetSupportedResourceTypes](~~169618~~).
        # 
        # > You must specify the ResourceType or ConfigRuleId parameter.
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_type is not None:
            result['ComplianceType'] = self.compliance_type
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceType') is not None:
            self.compliance_type = m.get('ComplianceType')
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultListEvaluationResultIdentifierEvaluationResultQualifier(TeaModel):
    def __init__(
        self,
        config_rule_arn: str = None,
        config_rule_id: str = None,
        config_rule_name: str = None,
        region_id: str = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_type: str = None,
    ):
        # The Alibaba Cloud Resource Name (ARN) of the rule.
        self.config_rule_arn = config_rule_arn
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The name of the rule.
        self.config_rule_name = config_rule_name
        # The ID of the region.
        self.region_id = region_id
        # The ID of the evaluated resource.
        self.resource_id = resource_id
        # The type of the evaluated resource.
        self.resource_name = resource_name
        # The type of the evaluated resource.
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_arn is not None:
            result['ConfigRuleArn'] = self.config_rule_arn
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.config_rule_name is not None:
            result['ConfigRuleName'] = self.config_rule_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleArn') is not None:
            self.config_rule_arn = m.get('ConfigRuleArn')
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ConfigRuleName') is not None:
            self.config_rule_name = m.get('ConfigRuleName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultListEvaluationResultIdentifier(TeaModel):
    def __init__(
        self,
        evaluation_result_qualifier: DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultListEvaluationResultIdentifierEvaluationResultQualifier = None,
        ordering_timestamp: int = None,
    ):
        # The information of the rule and the evaluated resource.
        self.evaluation_result_qualifier = evaluation_result_qualifier
        # The timestamp that was generated when the compliance evaluation was performed.
        self.ordering_timestamp = ordering_timestamp

    def validate(self):
        if self.evaluation_result_qualifier:
            self.evaluation_result_qualifier.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.evaluation_result_qualifier is not None:
            result['EvaluationResultQualifier'] = self.evaluation_result_qualifier.to_map()
        if self.ordering_timestamp is not None:
            result['OrderingTimestamp'] = self.ordering_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EvaluationResultQualifier') is not None:
            temp_model = DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultListEvaluationResultIdentifierEvaluationResultQualifier()
            self.evaluation_result_qualifier = temp_model.from_map(m['EvaluationResultQualifier'])
        if m.get('OrderingTimestamp') is not None:
            self.ordering_timestamp = m.get('OrderingTimestamp')
        return self


class DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultList(TeaModel):
    def __init__(
        self,
        annotation: str = None,
        compliance_type: str = None,
        config_rule_invoked_timestamp: int = None,
        evaluation_result_identifier: DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultListEvaluationResultIdentifier = None,
        invoking_event_message_type: str = None,
        remediation_enabled: bool = None,
        result_recorded_timestamp: int = None,
        risk_level: int = None,
    ):
        # The annotation to the resource that is evaluated to be non-compliant.
        self.annotation = annotation
        # The compliance evaluation result of the resource. Valid values:
        # 
        # *   COMPLIANT: The resource is evaluated to be compliant.
        # *   NON_COMPLIANT: The resource is evaluated to be non-compliant.
        # *   NOT_APPLICABLE: The rule does not apply to the resource.
        # *   INSUFFICIENT_DATA: The resource data is insufficient.
        self.compliance_type = compliance_type
        # The timestamp that was generated when the rule was triggered.
        self.config_rule_invoked_timestamp = config_rule_invoked_timestamp
        # The identifier of the compliance evaluation result.
        self.evaluation_result_identifier = evaluation_result_identifier
        # The trigger type of the rule. Valid values:
        # 
        # *   ConfigurationItemChangeNotification: The rule is triggered by configuration changes.
        # *   ScheduledNotification: The rule is triggered as scheduled.
        self.invoking_event_message_type = invoking_event_message_type
        # Specifies whether to enable the remediation template. Valid values:
        # 
        # * **true**\
        # * **false**\
        self.remediation_enabled = remediation_enabled
        # The timestamp that was generated when the compliance evaluation result was recorded.
        self.result_recorded_timestamp = result_recorded_timestamp
        # The risk level of the non-compliant resource. Valid values:
        # 
        # *   1: high risk
        # *   2: medium risk
        # *   3: low risk
        self.risk_level = risk_level

    def validate(self):
        if self.evaluation_result_identifier:
            self.evaluation_result_identifier.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.annotation is not None:
            result['Annotation'] = self.annotation
        if self.compliance_type is not None:
            result['ComplianceType'] = self.compliance_type
        if self.config_rule_invoked_timestamp is not None:
            result['ConfigRuleInvokedTimestamp'] = self.config_rule_invoked_timestamp
        if self.evaluation_result_identifier is not None:
            result['EvaluationResultIdentifier'] = self.evaluation_result_identifier.to_map()
        if self.invoking_event_message_type is not None:
            result['InvokingEventMessageType'] = self.invoking_event_message_type
        if self.remediation_enabled is not None:
            result['RemediationEnabled'] = self.remediation_enabled
        if self.result_recorded_timestamp is not None:
            result['ResultRecordedTimestamp'] = self.result_recorded_timestamp
        if self.risk_level is not None:
            result['RiskLevel'] = self.risk_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Annotation') is not None:
            self.annotation = m.get('Annotation')
        if m.get('ComplianceType') is not None:
            self.compliance_type = m.get('ComplianceType')
        if m.get('ConfigRuleInvokedTimestamp') is not None:
            self.config_rule_invoked_timestamp = m.get('ConfigRuleInvokedTimestamp')
        if m.get('EvaluationResultIdentifier') is not None:
            temp_model = DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultListEvaluationResultIdentifier()
            self.evaluation_result_identifier = temp_model.from_map(m['EvaluationResultIdentifier'])
        if m.get('InvokingEventMessageType') is not None:
            self.invoking_event_message_type = m.get('InvokingEventMessageType')
        if m.get('RemediationEnabled') is not None:
            self.remediation_enabled = m.get('RemediationEnabled')
        if m.get('ResultRecordedTimestamp') is not None:
            self.result_recorded_timestamp = m.get('ResultRecordedTimestamp')
        if m.get('RiskLevel') is not None:
            self.risk_level = m.get('RiskLevel')
        return self


class DescribeEvaluationResultsResponseBodyEvaluationResults(TeaModel):
    def __init__(
        self,
        evaluation_result_list: List[DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultList] = None,
        page_number: int = None,
        page_size: int = None,
        total_count: int = None,
    ):
        # Indicates whether remediation is enabled. Valid values:
        # 
        # *   true
        # *   false
        self.evaluation_result_list = evaluation_result_list
        # The page number of the returned page. Pages start from page 1.
        self.page_number = page_number
        # The number of entries returned per page. Valid values: 1 to 100.
        self.page_size = page_size
        # The total number of compliance evaluation results.
        self.total_count = total_count

    def validate(self):
        if self.evaluation_result_list:
            for k in self.evaluation_result_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['EvaluationResultList'] = []
        if self.evaluation_result_list is not None:
            for k in self.evaluation_result_list:
                result['EvaluationResultList'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.evaluation_result_list = []
        if m.get('EvaluationResultList') is not None:
            for k in m.get('EvaluationResultList'):
                temp_model = DescribeEvaluationResultsResponseBodyEvaluationResultsEvaluationResultList()
                self.evaluation_result_list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class DescribeEvaluationResultsResponseBody(TeaModel):
    def __init__(
        self,
        evaluation_results: DescribeEvaluationResultsResponseBodyEvaluationResults = None,
        request_id: str = None,
    ):
        # The information about the compliance evaluation results returned.
        self.evaluation_results = evaluation_results
        # The request ID.
        self.request_id = request_id

    def validate(self):
        if self.evaluation_results:
            self.evaluation_results.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.evaluation_results is not None:
            result['EvaluationResults'] = self.evaluation_results.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EvaluationResults') is not None:
            temp_model = DescribeEvaluationResultsResponseBodyEvaluationResults()
            self.evaluation_results = temp_model.from_map(m['EvaluationResults'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeEvaluationResultsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DescribeEvaluationResultsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeEvaluationResultsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAggregateDiscoveredResourceRequest(TeaModel):
    def __init__(
        self,
        aggregator_id: str = None,
        region: str = None,
        resource_id: str = None,
        resource_owner_id: int = None,
        resource_type: str = None,
    ):
        # The ID of the account group.
        # 
        # For more information about how to obtain the ID of an account group, see [ListAggregators](~~255797~~).
        self.aggregator_id = aggregator_id
        # The ID of the region where the resource resides.
        # 
        # For more information about how to obtain the region ID of a resource, see [ListAggregateDiscoveredResources](~~265983~~).
        self.region = region
        # The ID of the resource.
        # 
        # For more information about how to obtain the ID of a resource, see [ListAggregateDiscoveredResources](~~265983~~).
        self.resource_id = resource_id
        self.resource_owner_id = resource_owner_id
        # The type of the resource.
        # 
        # For more information about how to obtain the type of a resource, see [ListAggregateDiscoveredResources](~~265983~~).
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aggregator_id is not None:
            result['AggregatorId'] = self.aggregator_id
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AggregatorId') is not None:
            self.aggregator_id = m.get('AggregatorId')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class GetAggregateDiscoveredResourceResponseBodyDiscoveredResourceDetail(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        availability_zone: str = None,
        configuration: str = None,
        region: str = None,
        resource_creation_time: int = None,
        resource_deleted: int = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_status: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        # The ID of the Alibaba Cloud account to which the resource belongs.
        self.account_id = account_id
        # The zone where the resource resides.
        self.availability_zone = availability_zone
        # The configuration of the resource.
        self.configuration = configuration
        # The ID of the region where the resource resides.
        self.region = region
        # The timestamp when the resource was created.
        self.resource_creation_time = resource_creation_time
        # Indicates whether the resource is deleted. Valid values:
        # 
        # *   1: The resource is retained.
        # *   0: The resource is deleted.
        self.resource_deleted = resource_deleted
        # The ID of the resource.
        self.resource_id = resource_id
        # The name of the resource.
        self.resource_name = resource_name
        # The status of the resource. The parameter value varies with the resource type and may be left empty. Examples:
        # 
        # *   If the ResourceType parameter is set to ACS::ECS::Instance, the resource is an Elastic Compute Service (ECS) instance that has a specific state. In this case, valid values of this parameter include Running and Stopped.
        # *   If the ResourceType parameter is set to ACS::OSS::Bucket, the resource is an Object Storage Service (OSS) bucket that does not have a specific state. In this case, this parameter is left empty.
        self.resource_status = resource_status
        # The type of the resource.
        self.resource_type = resource_type
        # The tags of the resource.
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.availability_zone is not None:
            result['AvailabilityZone'] = self.availability_zone
        if self.configuration is not None:
            result['Configuration'] = self.configuration
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_creation_time is not None:
            result['ResourceCreationTime'] = self.resource_creation_time
        if self.resource_deleted is not None:
            result['ResourceDeleted'] = self.resource_deleted
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_status is not None:
            result['ResourceStatus'] = self.resource_status
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('AvailabilityZone') is not None:
            self.availability_zone = m.get('AvailabilityZone')
        if m.get('Configuration') is not None:
            self.configuration = m.get('Configuration')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceCreationTime') is not None:
            self.resource_creation_time = m.get('ResourceCreationTime')
        if m.get('ResourceDeleted') is not None:
            self.resource_deleted = m.get('ResourceDeleted')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceStatus') is not None:
            self.resource_status = m.get('ResourceStatus')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class GetAggregateDiscoveredResourceResponseBody(TeaModel):
    def __init__(
        self,
        discovered_resource_detail: GetAggregateDiscoveredResourceResponseBodyDiscoveredResourceDetail = None,
        request_id: str = None,
    ):
        # The information about the resource.
        self.discovered_resource_detail = discovered_resource_detail
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.discovered_resource_detail:
            self.discovered_resource_detail.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.discovered_resource_detail is not None:
            result['DiscoveredResourceDetail'] = self.discovered_resource_detail.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DiscoveredResourceDetail') is not None:
            temp_model = GetAggregateDiscoveredResourceResponseBodyDiscoveredResourceDetail()
            self.discovered_resource_detail = temp_model.from_map(m['DiscoveredResourceDetail'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetAggregateDiscoveredResourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAggregateDiscoveredResourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetAggregateDiscoveredResourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetDiscoveredResourceCountsRequest(TeaModel):
    def __init__(
        self,
        group_by_key: str = None,
        member_id: int = None,
        multi_account: bool = None,
    ):
        # The dimension by which resources are grouped. Valid values:
        # 
        # *   ResourceType: specifies that resources are grouped by type.
        # *   Region: specifies that resources are grouped by region.
        self.group_by_key = group_by_key
        # This parameter has been removed from 00:00:00, June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00, May 30, 2021. For more information about account groups, see [Overview](~~211534~~).
        self.member_id = member_id
        # This parameter has been removed from 00:00:00, June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00, May 30, 2021. For more information about account groups, see [Overview](~~211534~~).
        self.multi_account = multi_account

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.group_by_key is not None:
            result['GroupByKey'] = self.group_by_key
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupByKey') is not None:
            self.group_by_key = m.get('GroupByKey')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        return self


class GetDiscoveredResourceCountsResponseBodyGroupedResourceCountsGroupedResourceCountList(TeaModel):
    def __init__(
        self,
        group_name: str = None,
        resource_count: int = None,
    ):
        # The name of the resource group.
        self.group_name = group_name
        # The number of resources in the group.
        self.resource_count = resource_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.resource_count is not None:
            result['ResourceCount'] = self.resource_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('ResourceCount') is not None:
            self.resource_count = m.get('ResourceCount')
        return self


class GetDiscoveredResourceCountsResponseBodyGroupedResourceCounts(TeaModel):
    def __init__(
        self,
        group_by_key: str = None,
        grouped_resource_count_list: List[GetDiscoveredResourceCountsResponseBodyGroupedResourceCountsGroupedResourceCountList] = None,
    ):
        # The dimension by which resources are grouped.
        self.group_by_key = group_by_key
        # The information about resources in a specific group.
        self.grouped_resource_count_list = grouped_resource_count_list

    def validate(self):
        if self.grouped_resource_count_list:
            for k in self.grouped_resource_count_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.group_by_key is not None:
            result['GroupByKey'] = self.group_by_key
        result['GroupedResourceCountList'] = []
        if self.grouped_resource_count_list is not None:
            for k in self.grouped_resource_count_list:
                result['GroupedResourceCountList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupByKey') is not None:
            self.group_by_key = m.get('GroupByKey')
        self.grouped_resource_count_list = []
        if m.get('GroupedResourceCountList') is not None:
            for k in m.get('GroupedResourceCountList'):
                temp_model = GetDiscoveredResourceCountsResponseBodyGroupedResourceCountsGroupedResourceCountList()
                self.grouped_resource_count_list.append(temp_model.from_map(k))
        return self


class GetDiscoveredResourceCountsResponseBody(TeaModel):
    def __init__(
        self,
        grouped_resource_counts: GetDiscoveredResourceCountsResponseBodyGroupedResourceCounts = None,
        request_id: str = None,
    ):
        # The returned information about resources.
        self.grouped_resource_counts = grouped_resource_counts
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.grouped_resource_counts:
            self.grouped_resource_counts.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.grouped_resource_counts is not None:
            result['GroupedResourceCounts'] = self.grouped_resource_counts.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupedResourceCounts') is not None:
            temp_model = GetDiscoveredResourceCountsResponseBodyGroupedResourceCounts()
            self.grouped_resource_counts = temp_model.from_map(m['GroupedResourceCounts'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetDiscoveredResourceCountsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetDiscoveredResourceCountsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetDiscoveredResourceCountsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetDiscoveredResourceSummaryRequest(TeaModel):
    def __init__(
        self,
        member_id: int = None,
        multi_account: bool = None,
    ):
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        return self


class GetDiscoveredResourceSummaryResponseBodyDiscoveredResourceSummary(TeaModel):
    def __init__(
        self,
        region_count: int = None,
        resource_count: int = None,
        resource_type_count: int = None,
    ):
        # The number of the regions involved in the monitoring.
        self.region_count = region_count
        # The number of the resources monitored by Cloud Config.
        self.resource_count = resource_count
        # The number of the resource types monitored by Cloud Config.
        self.resource_type_count = resource_type_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_count is not None:
            result['RegionCount'] = self.region_count
        if self.resource_count is not None:
            result['ResourceCount'] = self.resource_count
        if self.resource_type_count is not None:
            result['ResourceTypeCount'] = self.resource_type_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionCount') is not None:
            self.region_count = m.get('RegionCount')
        if m.get('ResourceCount') is not None:
            self.resource_count = m.get('ResourceCount')
        if m.get('ResourceTypeCount') is not None:
            self.resource_type_count = m.get('ResourceTypeCount')
        return self


class GetDiscoveredResourceSummaryResponseBody(TeaModel):
    def __init__(
        self,
        discovered_resource_summary: GetDiscoveredResourceSummaryResponseBodyDiscoveredResourceSummary = None,
        request_id: str = None,
    ):
        # The statistics of the resources monitored by Cloud Config.
        self.discovered_resource_summary = discovered_resource_summary
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.discovered_resource_summary:
            self.discovered_resource_summary.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.discovered_resource_summary is not None:
            result['DiscoveredResourceSummary'] = self.discovered_resource_summary.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DiscoveredResourceSummary') is not None:
            temp_model = GetDiscoveredResourceSummaryResponseBodyDiscoveredResourceSummary()
            self.discovered_resource_summary = temp_model.from_map(m['DiscoveredResourceSummary'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetDiscoveredResourceSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetDiscoveredResourceSummaryResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetDiscoveredResourceSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceComplianceTimelineRequest(TeaModel):
    def __init__(
        self,
        end_time: int = None,
        limit: int = None,
        member_id: str = None,
        multi_account: bool = None,
        next_token: str = None,
        region: str = None,
        resource_id: str = None,
        resource_type: str = None,
        start_time: int = None,
    ):
        # The timestamp that specifies the end of the time range to query. By default, the value is the time when the GetResourceConfigurationTimeline operation is called.
        self.end_time = end_time
        # The number of entries to return on each page. Valid values: 1 to 100. Default value: 10.
        self.limit = limit
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account
        # The token that is used to start the next query.
        self.next_token = next_token
        # The ID of the region.
        self.region = region
        # The ID of the resource.
        self.resource_id = resource_id
        # The type of the resource.
        self.resource_type = resource_type
        # The timestamp that specifies the beginning of the time range to query. By default, Cloud Config retrieves the configuration changes in the last 30 days for the specified resource.
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.limit is not None:
            result['Limit'] = self.limit
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Limit') is not None:
            self.limit = m.get('Limit')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetResourceComplianceTimelineResponseBodyResourceComplianceTimelineComplianceList(TeaModel):
    def __init__(
        self,
        account_id: str = None,
        availability_zone: str = None,
        capture_time: int = None,
        configuration: str = None,
        configuration_diff: str = None,
        region: str = None,
        resource_create_time: int = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_status: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        # The ID of your Alibaba Cloud account.
        self.account_id = account_id
        # The ID of the zone.
        self.availability_zone = availability_zone
        # The timestamp when the compliance evaluation occurred.
        self.capture_time = capture_time
        # The information about the rules triggered for the resource and the compliance evaluation results.
        self.configuration = configuration
        # The information about the changes to the compliance evaluation results, including the information about the triggered rules.
        self.configuration_diff = configuration_diff
        # The ID of the region.
        self.region = region
        # The timestamp when the resource was created.
        self.resource_create_time = resource_create_time
        # The ID of the resource.
        self.resource_id = resource_id
        # The name of the resource.
        self.resource_name = resource_name
        # The status of the resource. The parameter value varies with the resource type and may be left empty. Examples:
        # 
        # *   If ResourceType is set to ACS::ECS::Instance, the resource is an Elastic Compute Service (ECS) instance which has a specific state. In this case, valid values of this parameter include Running and Stopped.
        # *   If ResourceType is set to ACS::OSS::Bucket, the resource is an Object Storage Service (OSS) bucket which does not have a specific state. In this case, this parameter is left empty.
        self.resource_status = resource_status
        # The type of the resource.
        self.resource_type = resource_type
        # The tags of the resource.
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.availability_zone is not None:
            result['AvailabilityZone'] = self.availability_zone
        if self.capture_time is not None:
            result['CaptureTime'] = self.capture_time
        if self.configuration is not None:
            result['Configuration'] = self.configuration
        if self.configuration_diff is not None:
            result['ConfigurationDiff'] = self.configuration_diff
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_create_time is not None:
            result['ResourceCreateTime'] = self.resource_create_time
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_status is not None:
            result['ResourceStatus'] = self.resource_status
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('AvailabilityZone') is not None:
            self.availability_zone = m.get('AvailabilityZone')
        if m.get('CaptureTime') is not None:
            self.capture_time = m.get('CaptureTime')
        if m.get('Configuration') is not None:
            self.configuration = m.get('Configuration')
        if m.get('ConfigurationDiff') is not None:
            self.configuration_diff = m.get('ConfigurationDiff')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceCreateTime') is not None:
            self.resource_create_time = m.get('ResourceCreateTime')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceStatus') is not None:
            self.resource_status = m.get('ResourceStatus')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class GetResourceComplianceTimelineResponseBodyResourceComplianceTimeline(TeaModel):
    def __init__(
        self,
        compliance_list: List[GetResourceComplianceTimelineResponseBodyResourceComplianceTimelineComplianceList] = None,
        limit: int = None,
        next_token: str = None,
        total_count: int = None,
    ):
        # The compliance evaluations in the compliance timeline.
        self.compliance_list = compliance_list
        # The number of entries returned on each page. Valid values: 1 to 100.
        self.limit = limit
        # The token that was returned for the next query.
        self.next_token = next_token
        # The total number of the compliance evaluations for the specified resource.
        self.total_count = total_count

    def validate(self):
        if self.compliance_list:
            for k in self.compliance_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ComplianceList'] = []
        if self.compliance_list is not None:
            for k in self.compliance_list:
                result['ComplianceList'].append(k.to_map() if k else None)
        if self.limit is not None:
            result['Limit'] = self.limit
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.compliance_list = []
        if m.get('ComplianceList') is not None:
            for k in m.get('ComplianceList'):
                temp_model = GetResourceComplianceTimelineResponseBodyResourceComplianceTimelineComplianceList()
                self.compliance_list.append(temp_model.from_map(k))
        if m.get('Limit') is not None:
            self.limit = m.get('Limit')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetResourceComplianceTimelineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_compliance_timeline: GetResourceComplianceTimelineResponseBodyResourceComplianceTimeline = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The information about the compliance timeline.
        self.resource_compliance_timeline = resource_compliance_timeline

    def validate(self):
        if self.resource_compliance_timeline:
            self.resource_compliance_timeline.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_compliance_timeline is not None:
            result['ResourceComplianceTimeline'] = self.resource_compliance_timeline.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceComplianceTimeline') is not None:
            temp_model = GetResourceComplianceTimelineResponseBodyResourceComplianceTimeline()
            self.resource_compliance_timeline = temp_model.from_map(m['ResourceComplianceTimeline'])
        return self


class GetResourceComplianceTimelineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceComplianceTimelineResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetResourceComplianceTimelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceConfigurationTimelineRequest(TeaModel):
    def __init__(
        self,
        end_time: int = None,
        limit: int = None,
        member_id: int = None,
        multi_account: bool = None,
        next_token: str = None,
        region: str = None,
        resource_id: str = None,
        resource_type: str = None,
        start_time: int = None,
    ):
        # The timestamp that specifies the end of the time range to query. By default, the value is the time when the GetResourceConfigurationTimeline operation is called.
        self.end_time = end_time
        # The number of entries to return on each page. Valid values: 1 to 100. Default value: 10.
        self.limit = limit
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account
        # The token that is used to start the next query.
        self.next_token = next_token
        # The ID of the region.
        self.region = region
        # The ID of the resource.
        self.resource_id = resource_id
        # The type of the resource.
        self.resource_type = resource_type
        # The timestamp that specifies the beginning of the time range to query. By default, Cloud Config retrieves the configuration changes in the last 30 days for the specified resource.
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.limit is not None:
            result['Limit'] = self.limit
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Limit') is not None:
            self.limit = m.get('Limit')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class GetResourceConfigurationTimelineResponseBodyResourceConfigurationTimelineConfigurationList(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        availability_zone: str = None,
        capture_time: str = None,
        configuration_diff: str = None,
        region: str = None,
        resource_create_time: str = None,
        resource_event_type: str = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        # The ID of your Alibaba Cloud account.
        self.account_id = account_id
        # The ID of the zone.
        self.availability_zone = availability_zone
        # The timestamp when the configuration change occurred.
        self.capture_time = capture_time
        # The information of the changes to the configuration of the resource.
        self.configuration_diff = configuration_diff
        # The ID of the region.
        self.region = region
        # The time when the resource was created.
        self.resource_create_time = resource_create_time
        # The type of the resource change event. Valid values:
        # 
        # *   DISCOVERED: A resource was created.
        # *   MODIFY: A resource was modified.
        # *   REMOVE: A resource is deleted.
        self.resource_event_type = resource_event_type
        # The ID of the resource.
        self.resource_id = resource_id
        # The name of the resource.
        self.resource_name = resource_name
        # The type of the resource.
        self.resource_type = resource_type
        # The tags of the resource.
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.availability_zone is not None:
            result['AvailabilityZone'] = self.availability_zone
        if self.capture_time is not None:
            result['CaptureTime'] = self.capture_time
        if self.configuration_diff is not None:
            result['ConfigurationDiff'] = self.configuration_diff
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_create_time is not None:
            result['ResourceCreateTime'] = self.resource_create_time
        if self.resource_event_type is not None:
            result['ResourceEventType'] = self.resource_event_type
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('AvailabilityZone') is not None:
            self.availability_zone = m.get('AvailabilityZone')
        if m.get('CaptureTime') is not None:
            self.capture_time = m.get('CaptureTime')
        if m.get('ConfigurationDiff') is not None:
            self.configuration_diff = m.get('ConfigurationDiff')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceCreateTime') is not None:
            self.resource_create_time = m.get('ResourceCreateTime')
        if m.get('ResourceEventType') is not None:
            self.resource_event_type = m.get('ResourceEventType')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class GetResourceConfigurationTimelineResponseBodyResourceConfigurationTimeline(TeaModel):
    def __init__(
        self,
        configuration_list: List[GetResourceConfigurationTimelineResponseBodyResourceConfigurationTimelineConfigurationList] = None,
        limit: int = None,
        next_token: str = None,
        total_count: int = None,
    ):
        # The configuration changes of the configuration timeline.
        self.configuration_list = configuration_list
        # The number of entries returned on each page. Valid values: 1 to 100.
        self.limit = limit
        # The token that was returned for the next query.
        self.next_token = next_token
        # The total number of configuration changes for the specified resource.
        self.total_count = total_count

    def validate(self):
        if self.configuration_list:
            for k in self.configuration_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ConfigurationList'] = []
        if self.configuration_list is not None:
            for k in self.configuration_list:
                result['ConfigurationList'].append(k.to_map() if k else None)
        if self.limit is not None:
            result['Limit'] = self.limit
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.configuration_list = []
        if m.get('ConfigurationList') is not None:
            for k in m.get('ConfigurationList'):
                temp_model = GetResourceConfigurationTimelineResponseBodyResourceConfigurationTimelineConfigurationList()
                self.configuration_list.append(temp_model.from_map(k))
        if m.get('Limit') is not None:
            self.limit = m.get('Limit')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class GetResourceConfigurationTimelineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_configuration_timeline: GetResourceConfigurationTimelineResponseBodyResourceConfigurationTimeline = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The information of the configuration timeline.
        self.resource_configuration_timeline = resource_configuration_timeline

    def validate(self):
        if self.resource_configuration_timeline:
            self.resource_configuration_timeline.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_configuration_timeline is not None:
            result['ResourceConfigurationTimeline'] = self.resource_configuration_timeline.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceConfigurationTimeline') is not None:
            temp_model = GetResourceConfigurationTimelineResponseBodyResourceConfigurationTimeline()
            self.resource_configuration_timeline = temp_model.from_map(m['ResourceConfigurationTimeline'])
        return self


class GetResourceConfigurationTimelineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceConfigurationTimelineResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetResourceConfigurationTimelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSupportedResourceTypesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        resource_types: List[str] = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # The types of resources that are supported by Cloud Config.
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class GetSupportedResourceTypesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetSupportedResourceTypesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetSupportedResourceTypesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAggregateDiscoveredResourcesRequest(TeaModel):
    def __init__(
        self,
        aggregator_id: str = None,
        page_number: int = None,
        page_size: int = None,
        regions: str = None,
        resource_deleted: int = None,
        resource_id: str = None,
        resource_owner_id: int = None,
        resource_types: str = None,
    ):
        # The ID of the account group.
        # 
        # For more information about how to obtain the ID of an account group, see [ListAggregators](~~255797~~).
        self.aggregator_id = aggregator_id
        # The number of the page to return.
        # 
        # Pages start from page 1. Default value: 1.
        self.page_number = page_number
        # The number of entries to return on each page.
        # 
        # Valid values: 1 to 100. A minimum of 1 entry can be returned on each page. Default value: 10.
        self.page_size = page_size
        # The ID of the region in which the resource resides. Separate multiple region IDs with commas (,).
        # 
        # For more information about how to obtain the region ID of a resource, see [ListAggregateDiscoveredResources](~~265983~~).
        self.regions = regions
        # The status of the resource. Valid values:
        # 
        # *   0: The resource is deleted.
        # *   1: The resource is retained. This is the default value.
        self.resource_deleted = resource_deleted
        # The ID of the resource.
        self.resource_id = resource_id
        self.resource_owner_id = resource_owner_id
        # The type of the resource. Separate multiple resource types with commas (,).
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aggregator_id is not None:
            result['AggregatorId'] = self.aggregator_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.regions is not None:
            result['Regions'] = self.regions
        if self.resource_deleted is not None:
            result['ResourceDeleted'] = self.resource_deleted
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AggregatorId') is not None:
            self.aggregator_id = m.get('AggregatorId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Regions') is not None:
            self.regions = m.get('Regions')
        if m.get('ResourceDeleted') is not None:
            self.resource_deleted = m.get('ResourceDeleted')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class ListAggregateDiscoveredResourcesResponseBodyDiscoveredResourceProfilesDiscoveredResourceProfileList(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        region: str = None,
        resource_creation_time: int = None,
        resource_deleted: int = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_owner_id: int = None,
        resource_status: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        # The ID of the Alibaba Cloud account to which the resource belongs.
        self.account_id = account_id
        # The ID of the region.
        self.region = region
        # The timestamp when the resource was created. Unit: milliseconds.
        self.resource_creation_time = resource_creation_time
        # Indicates whether the resource is deleted. Valid values:
        # 
        # *   0: The resource is deleted.
        # *   1: The resource is retained.
        self.resource_deleted = resource_deleted
        # The ID of the resource.
        self.resource_id = resource_id
        # The name of the resource.
        self.resource_name = resource_name
        # The ID of the Alibaba Cloud account to which the resource belongs.
        self.resource_owner_id = resource_owner_id
        # The status of the resource. The parameter value varies based on the resource type and may be left empty. Examples:
        # 
        # *   If the value of the ResourceType parameter is ACS::ECS::Instance, the resource is an Elastic Compute Service (ECS) instance that has a specific state. In this case, the valid values of this parameter are Running and Stopped.
        # *   If the value of the ResourceType parameter is ACS::OSS::Bucket, the resource is an Object Storage Service (OSS) bucket that does not have a specific state. In this case, this parameter is left empty.
        self.resource_status = resource_status
        # The type of the resource.
        self.resource_type = resource_type
        # The tags of the resource.
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_creation_time is not None:
            result['ResourceCreationTime'] = self.resource_creation_time
        if self.resource_deleted is not None:
            result['ResourceDeleted'] = self.resource_deleted
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id
        if self.resource_status is not None:
            result['ResourceStatus'] = self.resource_status
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceCreationTime') is not None:
            self.resource_creation_time = m.get('ResourceCreationTime')
        if m.get('ResourceDeleted') is not None:
            self.resource_deleted = m.get('ResourceDeleted')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')
        if m.get('ResourceStatus') is not None:
            self.resource_status = m.get('ResourceStatus')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class ListAggregateDiscoveredResourcesResponseBodyDiscoveredResourceProfiles(TeaModel):
    def __init__(
        self,
        discovered_resource_profile_list: List[ListAggregateDiscoveredResourcesResponseBodyDiscoveredResourceProfilesDiscoveredResourceProfileList] = None,
        page_number: int = None,
        page_size: int = None,
        total_count: int = None,
    ):
        # The information about the resource.
        self.discovered_resource_profile_list = discovered_resource_profile_list
        # The page number of the returned page. Pages start from page 1.
        self.page_number = page_number
        # The number of entries returned per page. Valid values: 1 to 100.
        self.page_size = page_size
        # The total number of resources.
        self.total_count = total_count

    def validate(self):
        if self.discovered_resource_profile_list:
            for k in self.discovered_resource_profile_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DiscoveredResourceProfileList'] = []
        if self.discovered_resource_profile_list is not None:
            for k in self.discovered_resource_profile_list:
                result['DiscoveredResourceProfileList'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.discovered_resource_profile_list = []
        if m.get('DiscoveredResourceProfileList') is not None:
            for k in m.get('DiscoveredResourceProfileList'):
                temp_model = ListAggregateDiscoveredResourcesResponseBodyDiscoveredResourceProfilesDiscoveredResourceProfileList()
                self.discovered_resource_profile_list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListAggregateDiscoveredResourcesResponseBody(TeaModel):
    def __init__(
        self,
        discovered_resource_profiles: ListAggregateDiscoveredResourcesResponseBodyDiscoveredResourceProfiles = None,
        request_id: str = None,
    ):
        # The information about the returned resources.
        self.discovered_resource_profiles = discovered_resource_profiles
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.discovered_resource_profiles:
            self.discovered_resource_profiles.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.discovered_resource_profiles is not None:
            result['DiscoveredResourceProfiles'] = self.discovered_resource_profiles.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DiscoveredResourceProfiles') is not None:
            temp_model = ListAggregateDiscoveredResourcesResponseBodyDiscoveredResourceProfiles()
            self.discovered_resource_profiles = temp_model.from_map(m['DiscoveredResourceProfiles'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListAggregateDiscoveredResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAggregateDiscoveredResourcesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListAggregateDiscoveredResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListConfigRulesRequest(TeaModel):
    def __init__(
        self,
        compliance_pack_id: str = None,
        compliance_type: str = None,
        config_rule_name: str = None,
        config_rule_state: str = None,
        member_id: int = None,
        multi_account: bool = None,
        page_number: int = None,
        page_size: int = None,
        risk_level: int = None,
    ):
        # The ID of the compliance package to which the rule belongs.
        self.compliance_pack_id = compliance_pack_id
        # The compliance evaluation result of the resources. Valid values:
        # 
        # *   COMPLIANT: The resources are evaluated as compliant.
        # *   NON_COMPLIANT: The resources are evaluated as non-compliant.
        # *   NOT_APPLICABLE: The rule does not apply to the resources.
        # *   INSUFFICIENT_DATA: The resource data is insufficient.
        self.compliance_type = compliance_type
        # The name of the monitoring rule.
        self.config_rule_name = config_rule_name
        # The status of the rule. Valid values:
        # 
        # *   ACTIVE: The rule is enabled.
        # *   EVALUATING: The rule is triggered and is being used to monitor resource configurations.
        # *   INACTIVE: The rule is disabled.
        self.config_rule_state = config_rule_state
        # This parameter is unavailable since 00:00:00 on June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00 on May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00 on May 30, 2021. For information about account groups, see [Overview](~~211534~~).
        self.member_id = member_id
        # This parameter is unavailable since 00:00:00 on June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00 on May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00 on May 30, 2021. For information about account groups, see [Overview](~~211534~~).
        self.multi_account = multi_account
        # The page number of the returned page. A minimum of one entry can be returned on each page.
        self.page_number = page_number
        # The number of entries per page. Valid values: 1 to 100.
        self.page_size = page_size
        # The risk level of the resources that are not compliant with the rule. Valid values:
        # 
        # *   1: high
        # *   2: medium
        # *   3: low
        self.risk_level = risk_level

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_pack_id is not None:
            result['CompliancePackId'] = self.compliance_pack_id
        if self.compliance_type is not None:
            result['ComplianceType'] = self.compliance_type
        if self.config_rule_name is not None:
            result['ConfigRuleName'] = self.config_rule_name
        if self.config_rule_state is not None:
            result['ConfigRuleState'] = self.config_rule_state
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.risk_level is not None:
            result['RiskLevel'] = self.risk_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CompliancePackId') is not None:
            self.compliance_pack_id = m.get('CompliancePackId')
        if m.get('ComplianceType') is not None:
            self.compliance_type = m.get('ComplianceType')
        if m.get('ConfigRuleName') is not None:
            self.config_rule_name = m.get('ConfigRuleName')
        if m.get('ConfigRuleState') is not None:
            self.config_rule_state = m.get('ConfigRuleState')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RiskLevel') is not None:
            self.risk_level = m.get('RiskLevel')
        return self


class ListConfigRulesResponseBodyConfigRulesConfigRuleListCompliance(TeaModel):
    def __init__(
        self,
        compliance_type: str = None,
        count: int = None,
    ):
        # The compliance evaluation result of the resources. Valid values:
        # 
        # *   COMPLIANT: The resources are evaluated as compliant.
        # *   NON_COMPLIANT: The resources are evaluated as non-compliant.
        # *   NOT_APPLICABLE: The rule does not apply to the resources.
        # *   INSUFFICIENT_DATA: The resource data is insufficient.
        self.compliance_type = compliance_type
        # The number of resources with the specified compliance evaluation result.
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_type is not None:
            result['ComplianceType'] = self.compliance_type
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ComplianceType') is not None:
            self.compliance_type = m.get('ComplianceType')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class ListConfigRulesResponseBodyConfigRulesConfigRuleListCreateBy(TeaModel):
    def __init__(
        self,
        compliance_pack_id: str = None,
        compliance_pack_name: str = None,
    ):
        # The ID of the compliance package.
        self.compliance_pack_id = compliance_pack_id
        # The name of the compliance package.
        self.compliance_pack_name = compliance_pack_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_pack_id is not None:
            result['CompliancePackId'] = self.compliance_pack_id
        if self.compliance_pack_name is not None:
            result['CompliancePackName'] = self.compliance_pack_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CompliancePackId') is not None:
            self.compliance_pack_id = m.get('CompliancePackId')
        if m.get('CompliancePackName') is not None:
            self.compliance_pack_name = m.get('CompliancePackName')
        return self


class ListConfigRulesResponseBodyConfigRulesConfigRuleListTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        # The key of the tag.
        self.key = key
        # The value of the tag.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListConfigRulesResponseBodyConfigRulesConfigRuleList(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        automation_type: str = None,
        compliance: ListConfigRulesResponseBodyConfigRulesConfigRuleListCompliance = None,
        compliance_pack_id: str = None,
        config_rule_arn: str = None,
        config_rule_id: str = None,
        config_rule_name: str = None,
        config_rule_state: str = None,
        create_by: ListConfigRulesResponseBodyConfigRulesConfigRuleListCreateBy = None,
        description: str = None,
        risk_level: int = None,
        source_identifier: str = None,
        source_owner: str = None,
        tags: List[ListConfigRulesResponseBodyConfigRulesConfigRuleListTags] = None,
    ):
        # The ID of the Alibaba Cloud account that owns the rule.
        self.account_id = account_id
        # The type of the remediation template. The value is fixed to LC.
        # 
        # >  LC stands for Logic Composer.
        self.automation_type = automation_type
        # The statistics about the compliance evaluation results based on the rule.
        self.compliance = compliance
        # The ID of the compliance package to which the rule belongs.
        self.compliance_pack_id = compliance_pack_id
        # The ARN of the rule.
        self.config_rule_arn = config_rule_arn
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The name of the rule.
        self.config_rule_name = config_rule_name
        # The status of the rule. Valid values:
        # 
        # *   ACTIVE: The rule is enabled.
        # *   EVALUATING: The rule is triggered and is being used to monitor resource configurations.
        # *   INACTIVE: The rule is disabled.
        self.config_rule_state = config_rule_state
        # The information about how the rule is created.
        self.create_by = create_by
        # The description of the rule.
        self.description = description
        # The risk level of the resources that are not compliant with the rule. Valid values:
        # 
        # *   1: high risk level
        # *   2: medium risk level
        # *   3: low risk level
        self.risk_level = risk_level
        # The identifier of the rule.
        # 
        # *   If the rule was created based on a managed rule, the value of this parameter is the name of the managed rule.
        # *   If the rule is a custom rule, the value of this parameter is the Alibaba Cloud Resource Name (ARN) of the relevant function in Function Compute.
        self.source_identifier = source_identifier
        # The method that is used to create the rule. Valid values:
        # 
        # *   CUSTOM_FC: The rule is a custom rule.
        # *   ALIYUN: The rule is created based on a managed rule of Alibaba Cloud.
        self.source_owner = source_owner
        # The tags.
        self.tags = tags

    def validate(self):
        if self.compliance:
            self.compliance.validate()
        if self.create_by:
            self.create_by.validate()
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.automation_type is not None:
            result['AutomationType'] = self.automation_type
        if self.compliance is not None:
            result['Compliance'] = self.compliance.to_map()
        if self.compliance_pack_id is not None:
            result['CompliancePackId'] = self.compliance_pack_id
        if self.config_rule_arn is not None:
            result['ConfigRuleArn'] = self.config_rule_arn
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.config_rule_name is not None:
            result['ConfigRuleName'] = self.config_rule_name
        if self.config_rule_state is not None:
            result['ConfigRuleState'] = self.config_rule_state
        if self.create_by is not None:
            result['CreateBy'] = self.create_by.to_map()
        if self.description is not None:
            result['Description'] = self.description
        if self.risk_level is not None:
            result['RiskLevel'] = self.risk_level
        if self.source_identifier is not None:
            result['SourceIdentifier'] = self.source_identifier
        if self.source_owner is not None:
            result['SourceOwner'] = self.source_owner
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('AutomationType') is not None:
            self.automation_type = m.get('AutomationType')
        if m.get('Compliance') is not None:
            temp_model = ListConfigRulesResponseBodyConfigRulesConfigRuleListCompliance()
            self.compliance = temp_model.from_map(m['Compliance'])
        if m.get('CompliancePackId') is not None:
            self.compliance_pack_id = m.get('CompliancePackId')
        if m.get('ConfigRuleArn') is not None:
            self.config_rule_arn = m.get('ConfigRuleArn')
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ConfigRuleName') is not None:
            self.config_rule_name = m.get('ConfigRuleName')
        if m.get('ConfigRuleState') is not None:
            self.config_rule_state = m.get('ConfigRuleState')
        if m.get('CreateBy') is not None:
            temp_model = ListConfigRulesResponseBodyConfigRulesConfigRuleListCreateBy()
            self.create_by = temp_model.from_map(m['CreateBy'])
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RiskLevel') is not None:
            self.risk_level = m.get('RiskLevel')
        if m.get('SourceIdentifier') is not None:
            self.source_identifier = m.get('SourceIdentifier')
        if m.get('SourceOwner') is not None:
            self.source_owner = m.get('SourceOwner')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = ListConfigRulesResponseBodyConfigRulesConfigRuleListTags()
                self.tags.append(temp_model.from_map(k))
        return self


class ListConfigRulesResponseBodyConfigRules(TeaModel):
    def __init__(
        self,
        config_rule_list: List[ListConfigRulesResponseBodyConfigRulesConfigRuleList] = None,
        page_number: int = None,
        page_size: int = None,
        total_count: int = None,
    ):
        # The tag key of the ENI.
        self.config_rule_list = config_rule_list
        # The page number of the returned page. A minimum of one entry can be returned on each page.
        self.page_number = page_number
        # The number of entries per page. Valid values: 1 to 100.
        self.page_size = page_size
        # The total number of cluster defense rules.
        self.total_count = total_count

    def validate(self):
        if self.config_rule_list:
            for k in self.config_rule_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ConfigRuleList'] = []
        if self.config_rule_list is not None:
            for k in self.config_rule_list:
                result['ConfigRuleList'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.config_rule_list = []
        if m.get('ConfigRuleList') is not None:
            for k in m.get('ConfigRuleList'):
                temp_model = ListConfigRulesResponseBodyConfigRulesConfigRuleList()
                self.config_rule_list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListConfigRulesResponseBody(TeaModel):
    def __init__(
        self,
        config_rules: ListConfigRulesResponseBodyConfigRules = None,
        request_id: str = None,
    ):
        # The rules.
        self.config_rules = config_rules
        # The request ID.
        self.request_id = request_id

    def validate(self):
        if self.config_rules:
            self.config_rules.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rules is not None:
            result['ConfigRules'] = self.config_rules.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRules') is not None:
            temp_model = ListConfigRulesResponseBodyConfigRules()
            self.config_rules = temp_model.from_map(m['ConfigRules'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListConfigRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListConfigRulesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListConfigRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDiscoveredResourcesRequest(TeaModel):
    def __init__(
        self,
        member_id: int = None,
        multi_account: bool = None,
        page_number: int = None,
        page_size: int = None,
        regions: str = None,
        resource_deleted: int = None,
        resource_id: str = None,
        resource_types: str = None,
    ):
        # This parameter has been removed from 00:00:00, June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00, May 30, 2021. For more information about account groups, see [Overview](~~211534~~).
        self.member_id = member_id
        # This parameter has been removed from 00:00:00, June 30, 2021. Account group-related operations are provided as an alternative after 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related operations after 00:00:00, May 30, 2021. For more information about account groups, see [Overview](~~211534~~).
        self.multi_account = multi_account
        # The number of the page to return. Pages start from page 1.
        self.page_number = page_number
        # The number of entries to return on each page. Valid values: 1 to 100.
        self.page_size = page_size
        # The ID of the region in which the resource resides. Separate multiple regions IDs with commas (,).
        self.regions = regions
        # The status of the resource. Valid values:
        # 
        # *   0: The resource is deleted.
        # *   1: The resource is retained. This is the default value.
        self.resource_deleted = resource_deleted
        # The ID of the resource.
        self.resource_id = resource_id
        # The type of the resource. Separate multiple resource types with commas (,).
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.regions is not None:
            result['Regions'] = self.regions
        if self.resource_deleted is not None:
            result['ResourceDeleted'] = self.resource_deleted
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Regions') is not None:
            self.regions = m.get('Regions')
        if m.get('ResourceDeleted') is not None:
            self.resource_deleted = m.get('ResourceDeleted')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class ListDiscoveredResourcesResponseBodyDiscoveredResourceProfilesDiscoveredResourceProfileList(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        region: str = None,
        resource_creation_time: int = None,
        resource_deleted: int = None,
        resource_id: str = None,
        resource_name: str = None,
        resource_status: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        # The ID of the Alibaba Cloud account to which the resource belongs.
        self.account_id = account_id
        # The ID of the region.
        self.region = region
        # The timestamp when the resource was created.
        self.resource_creation_time = resource_creation_time
        # Indicates whether the resource is deleted. Valid values:
        # 
        # *   1: The resource is retained.
        # *   0: The resource is deleted.
        self.resource_deleted = resource_deleted
        # The ID of the resource.
        self.resource_id = resource_id
        # The name of the resource.
        self.resource_name = resource_name
        # The status of the resource. The parameter value varies based on the resource type and may be left empty.
        # 
        # Examples:
        # 
        # *   If the value of the ResourceType parameter is ACS::ECS::Instance, the resource is an Elastic Compute Service (ECS) instance that has a specific state. In this case, the valid values of this parameter are Running and Stopped.
        # *   If the value of the ResourceType parameter is ACS::OSS::Bucket, the resource is an Object Storage Service (OSS) bucket that does not have a specific state. In this case, this parameter is left empty.
        self.resource_status = resource_status
        # The type of the resource.
        self.resource_type = resource_type
        # The tags of the resource.
        self.tags = tags

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.region is not None:
            result['Region'] = self.region
        if self.resource_creation_time is not None:
            result['ResourceCreationTime'] = self.resource_creation_time
        if self.resource_deleted is not None:
            result['ResourceDeleted'] = self.resource_deleted
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_name is not None:
            result['ResourceName'] = self.resource_name
        if self.resource_status is not None:
            result['ResourceStatus'] = self.resource_status
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tags is not None:
            result['Tags'] = self.tags
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('Region') is not None:
            self.region = m.get('Region')
        if m.get('ResourceCreationTime') is not None:
            self.resource_creation_time = m.get('ResourceCreationTime')
        if m.get('ResourceDeleted') is not None:
            self.resource_deleted = m.get('ResourceDeleted')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceName') is not None:
            self.resource_name = m.get('ResourceName')
        if m.get('ResourceStatus') is not None:
            self.resource_status = m.get('ResourceStatus')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Tags') is not None:
            self.tags = m.get('Tags')
        return self


class ListDiscoveredResourcesResponseBodyDiscoveredResourceProfiles(TeaModel):
    def __init__(
        self,
        discovered_resource_profile_list: List[ListDiscoveredResourcesResponseBodyDiscoveredResourceProfilesDiscoveredResourceProfileList] = None,
        page_number: int = None,
        page_size: int = None,
        total_count: int = None,
    ):
        # The information about the resource.
        self.discovered_resource_profile_list = discovered_resource_profile_list
        # The page number of the returned page. Pages start from page 1.
        self.page_number = page_number
        # The number of entries returned per page. Valid values: 1 to 100.
        self.page_size = page_size
        # The total number of resources.
        self.total_count = total_count

    def validate(self):
        if self.discovered_resource_profile_list:
            for k in self.discovered_resource_profile_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DiscoveredResourceProfileList'] = []
        if self.discovered_resource_profile_list is not None:
            for k in self.discovered_resource_profile_list:
                result['DiscoveredResourceProfileList'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.discovered_resource_profile_list = []
        if m.get('DiscoveredResourceProfileList') is not None:
            for k in m.get('DiscoveredResourceProfileList'):
                temp_model = ListDiscoveredResourcesResponseBodyDiscoveredResourceProfilesDiscoveredResourceProfileList()
                self.discovered_resource_profile_list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class ListDiscoveredResourcesResponseBody(TeaModel):
    def __init__(
        self,
        discovered_resource_profiles: ListDiscoveredResourcesResponseBodyDiscoveredResourceProfiles = None,
        request_id: str = None,
    ):
        # The information about the returned resources.
        self.discovered_resource_profiles = discovered_resource_profiles
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.discovered_resource_profiles:
            self.discovered_resource_profiles.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.discovered_resource_profiles is not None:
            result['DiscoveredResourceProfiles'] = self.discovered_resource_profiles.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DiscoveredResourceProfiles') is not None:
            temp_model = ListDiscoveredResourcesResponseBodyDiscoveredResourceProfiles()
            self.discovered_resource_profiles = temp_model.from_map(m['DiscoveredResourceProfiles'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListDiscoveredResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDiscoveredResourcesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDiscoveredResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRemediationTemplatesRequest(TeaModel):
    def __init__(
        self,
        managed_rule_identifier: str = None,
        remediation_type: str = None,
    ):
        # The identifier of the managed rule.
        self.managed_rule_identifier = managed_rule_identifier
        # The type of the remediation template. Valid value: OOS, which stands for Operation Orchestration Service.
        self.remediation_type = remediation_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.managed_rule_identifier is not None:
            result['ManagedRuleIdentifier'] = self.managed_rule_identifier
        if self.remediation_type is not None:
            result['RemediationType'] = self.remediation_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ManagedRuleIdentifier') is not None:
            self.managed_rule_identifier = m.get('ManagedRuleIdentifier')
        if m.get('RemediationType') is not None:
            self.remediation_type = m.get('RemediationType')
        return self


class ListRemediationTemplatesResponseBodyRemediationTemplates(TeaModel):
    def __init__(
        self,
        remediation_type: str = None,
        template_definition: str = None,
        template_identifier: str = None,
        template_name: str = None,
    ):
        # The type of the remediation template. Valid value: OOS, which stands for Operation Orchestration Service.
        self.remediation_type = remediation_type
        # The configuration of the remediation template.
        self.template_definition = template_definition
        # The ID of the remediation template.
        self.template_identifier = template_identifier
        # The name of the remediation template.
        self.template_name = template_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.remediation_type is not None:
            result['RemediationType'] = self.remediation_type
        if self.template_definition is not None:
            result['TemplateDefinition'] = self.template_definition
        if self.template_identifier is not None:
            result['TemplateIdentifier'] = self.template_identifier
        if self.template_name is not None:
            result['TemplateName'] = self.template_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RemediationType') is not None:
            self.remediation_type = m.get('RemediationType')
        if m.get('TemplateDefinition') is not None:
            self.template_definition = m.get('TemplateDefinition')
        if m.get('TemplateIdentifier') is not None:
            self.template_identifier = m.get('TemplateIdentifier')
        if m.get('TemplateName') is not None:
            self.template_name = m.get('TemplateName')
        return self


class ListRemediationTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        remediation_templates: List[ListRemediationTemplatesResponseBodyRemediationTemplates] = None,
        request_id: str = None,
    ):
        # The information about the remediation template.
        self.remediation_templates = remediation_templates
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.remediation_templates:
            for k in self.remediation_templates:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['RemediationTemplates'] = []
        if self.remediation_templates is not None:
            for k in self.remediation_templates:
                result['RemediationTemplates'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.remediation_templates = []
        if m.get('RemediationTemplates') is not None:
            for k in m.get('RemediationTemplates'):
                temp_model = ListRemediationTemplatesResponseBodyRemediationTemplates()
                self.remediation_templates.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListRemediationTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListRemediationTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListRemediationTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutConfigRuleRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        config_rule_id: str = None,
        config_rule_name: str = None,
        description: str = None,
        input_parameters: str = None,
        member_id: int = None,
        multi_account: bool = None,
        risk_level: int = None,
        scope_compliance_resource_id: str = None,
        scope_compliance_resource_types: str = None,
        source_detail_message_type: str = None,
        source_identifier: str = None,
        source_maximum_execution_frequency: str = None,
        source_owner: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You can use the client to generate the value, but you must ensure that it is unique among different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The name of the rule.
        self.config_rule_name = config_rule_name
        # The description of the rule.
        self.description = description
        # The settings of the input parameters for the rule.
        self.input_parameters = input_parameters
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.member_id = member_id
        # This parameter is scheduled to be removed before 00:00:00, June 30, 2021. Account group-related APIs will be provided as an alternative before 00:00:00, May 30, 2021. If you are using this parameter, we recommend that you switch to account group-related APIs after 00:00:00, May 30, 2021. For more information, see [Account groups](~~211534~~).
        self.multi_account = multi_account
        # The risk level of the non-compliant resource. Valid values:
        # 
        # *   1: high risk
        # *   2: medium risk
        # *   3: low risk
        self.risk_level = risk_level
        # The ID of the resource to be evaluated.
        # 
        # *   If you do not set this parameter, the rule evaluates resources of all the types specified by ScopeComplianceResourceTypes.
        # *   If you specify a resource ID, the rule evaluates the resource identified by the ID.
        self.scope_compliance_resource_id = scope_compliance_resource_id
        # The types of the resources to be evaluated.
        self.scope_compliance_resource_types = scope_compliance_resource_types
        # The trigger type of the rule. Valid values:
        # 
        # *   ConfigurationItemChangeNotification: The rule is triggered by configuration changes.
        # *   ScheduledNotification: The rule is triggered as scheduled.
        self.source_detail_message_type = source_detail_message_type
        # The identifier of the rule.
        # 
        # *   For a managed rule, the value is the name of the managed rule.
        # *   For a custom rule, the value is the Alibaba Cloud Resource Name (ARN) of the custom rule.
        self.source_identifier = source_identifier
        # The frequency at which the rule is executed. Valid values:
        # 
        # *   One_Hour: 1 hour
        # *   Three_Hours: 3 hours
        # *   Six_Hours: 6 hours
        # *   Twelve_Hours: 12 hours
        # *   TwentyFour_Hours: 24 hours
        self.source_maximum_execution_frequency = source_maximum_execution_frequency
        # Indicates whether you or Alibaba Cloud owns and manages the rule. Valid values:
        # 
        # *   CUSTOM_FC: The rule is a custom rule that you own.
        # *   ALIYUN: The rule is a managed rule of Alibaba Cloud.
        self.source_owner = source_owner

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.config_rule_name is not None:
            result['ConfigRuleName'] = self.config_rule_name
        if self.description is not None:
            result['Description'] = self.description
        if self.input_parameters is not None:
            result['InputParameters'] = self.input_parameters
        if self.member_id is not None:
            result['MemberId'] = self.member_id
        if self.multi_account is not None:
            result['MultiAccount'] = self.multi_account
        if self.risk_level is not None:
            result['RiskLevel'] = self.risk_level
        if self.scope_compliance_resource_id is not None:
            result['ScopeComplianceResourceId'] = self.scope_compliance_resource_id
        if self.scope_compliance_resource_types is not None:
            result['ScopeComplianceResourceTypes'] = self.scope_compliance_resource_types
        if self.source_detail_message_type is not None:
            result['SourceDetailMessageType'] = self.source_detail_message_type
        if self.source_identifier is not None:
            result['SourceIdentifier'] = self.source_identifier
        if self.source_maximum_execution_frequency is not None:
            result['SourceMaximumExecutionFrequency'] = self.source_maximum_execution_frequency
        if self.source_owner is not None:
            result['SourceOwner'] = self.source_owner
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ConfigRuleName') is not None:
            self.config_rule_name = m.get('ConfigRuleName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('InputParameters') is not None:
            self.input_parameters = m.get('InputParameters')
        if m.get('MemberId') is not None:
            self.member_id = m.get('MemberId')
        if m.get('MultiAccount') is not None:
            self.multi_account = m.get('MultiAccount')
        if m.get('RiskLevel') is not None:
            self.risk_level = m.get('RiskLevel')
        if m.get('ScopeComplianceResourceId') is not None:
            self.scope_compliance_resource_id = m.get('ScopeComplianceResourceId')
        if m.get('ScopeComplianceResourceTypes') is not None:
            self.scope_compliance_resource_types = m.get('ScopeComplianceResourceTypes')
        if m.get('SourceDetailMessageType') is not None:
            self.source_detail_message_type = m.get('SourceDetailMessageType')
        if m.get('SourceIdentifier') is not None:
            self.source_identifier = m.get('SourceIdentifier')
        if m.get('SourceMaximumExecutionFrequency') is not None:
            self.source_maximum_execution_frequency = m.get('SourceMaximumExecutionFrequency')
        if m.get('SourceOwner') is not None:
            self.source_owner = m.get('SourceOwner')
        return self


class PutConfigRuleResponseBody(TeaModel):
    def __init__(
        self,
        config_rule_id: str = None,
        request_id: str = None,
    ):
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class PutConfigRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PutConfigRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PutConfigRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutConfigurationRecorderRequest(TeaModel):
    def __init__(
        self,
        resource_types: str = None,
    ):
        # The types of the resources that you want Cloud Config to monitor. Separate multiple resource types with commas (,).
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class PutConfigurationRecorderResponseBodyConfigurationRecorder(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        configuration_recorder_status: str = None,
        resource_types: List[str] = None,
    ):
        # The ID of your Alibaba Cloud account.
        self.account_id = account_id
        # The status of the configuration recorder. Valid values:
        # 
        # *   REGISTRABLE: The configuration recorder has not been registered.
        # *   BUILDING: The configuration recorder is being deployed.
        # *   REGISTERED: The configuration recorder has been registered.
        # *   REBUILDING: The configuration recorder is being redeployed.
        self.configuration_recorder_status = configuration_recorder_status
        # The types of resources that are monitored by Cloud Config.
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.configuration_recorder_status is not None:
            result['ConfigurationRecorderStatus'] = self.configuration_recorder_status
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('ConfigurationRecorderStatus') is not None:
            self.configuration_recorder_status = m.get('ConfigurationRecorderStatus')
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class PutConfigurationRecorderResponseBody(TeaModel):
    def __init__(
        self,
        configuration_recorder: PutConfigurationRecorderResponseBodyConfigurationRecorder = None,
        request_id: str = None,
    ):
        # The details of the configuration recorder that monitors resources.
        self.configuration_recorder = configuration_recorder
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.configuration_recorder:
            self.configuration_recorder.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.configuration_recorder is not None:
            result['ConfigurationRecorder'] = self.configuration_recorder.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigurationRecorder') is not None:
            temp_model = PutConfigurationRecorderResponseBodyConfigurationRecorder()
            self.configuration_recorder = temp_model.from_map(m['ConfigurationRecorder'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class PutConfigurationRecorderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PutConfigurationRecorderResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PutConfigurationRecorderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutDeliveryChannelRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        delivery_channel_assume_role_arn: str = None,
        delivery_channel_condition: str = None,
        delivery_channel_id: str = None,
        delivery_channel_name: str = None,
        delivery_channel_target_arn: str = None,
        delivery_channel_type: str = None,
        description: str = None,
        status: int = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You can use the client to generate a token, but you must make sure that it is unique among different requests. The token cannot exceed 64 characters in length and can only contain ASCII characters.
        self.client_token = client_token
        # The Alibaba Cloud Resource Name (ARN) of the role to be assumed by the delivery method. This parameter is required when you create a delivery method.
        # 
        # >  If the delivery method assumes the service linked role for Cloud Config, you can specify the ARN in the format of the provided example and replace the account ID with the ID of your Alibaba Cloud account.
        self.delivery_channel_assume_role_arn = delivery_channel_assume_role_arn
        # The rule attached to the delivery method. This parameter is applicable only to delivery methods of the MNS type.
        # 
        # This parameter allows you to specify the lowest risk level for the events to subscribe to and the resource types for which you want to subscribe to events.
        # 
        # *   To specify the lowest risk level for the events to subscribe to, use the following format:`{"filterType":"RuleRiskLevel","value":"1","multiple":false}.`
        # 
        #     The value field indicates the lowest risk level and can be set to 1, 2, or 3, which indicates the high risk level, the medium risk level, and the low risk level, respectively.
        # 
        # *   To specify the resource types for which you want to subscribe to events, use the following format:`{"filterType":"ResourceType","values":["ACS::ACK::Cluster","ACS::ActionTrail::Trail","ACS::CBWP::CommonBandwidthPackage"],"multiple":true}.`
        # 
        #     The values field indicates the resource types. Its value is a JSON array.
        # 
        #     Example: `[{"filterType":"ResourceType","values":["ACS::ActionTrail::Trail","ACS::CBWP::CommonBandwidthPackage","ACS::CDN::Domain","ACS::CEN::CenBandwidthPackage","ACS::CEN::CenInstance","ACS::CEN::Flowlog","ACS::DdosCoo::Instance"],"multiple":true}]`
        self.delivery_channel_condition = delivery_channel_condition
        # The ID of the delivery method. This parameter is required when you modify a delivery method.
        self.delivery_channel_id = delivery_channel_id
        # The name of the delivery method.
        self.delivery_channel_name = delivery_channel_name
        # The ARN of the delivery destination. This parameter is required when you create a delivery method. The value must be in one of the following formats:
        # 
        # *   `acs:oss:{RegionId}:{Aliuid}:{bucketName}` if your delivery destination is an Object Storage Service (OSS) bucket.
        # *   `acs:mns:{RegionId}:{Aliuid}:/topics/{topicName}` if your delivery destination is a Message Service (MNS) topic.
        # *   `acs:log:{RegionId}:{Aliuid}:project/{projectName}/logstore/{logstoreName}` if your delivery destination is a Log Service Logstore.
        self.delivery_channel_target_arn = delivery_channel_target_arn
        # The type of the delivery method. This parameter is required when you create a delivery method. Valid values:
        # 
        # *   OSS
        # *   MNS
        # *   SLS
        self.delivery_channel_type = delivery_channel_type
        # The description of the delivery method.
        self.description = description
        # The status of the delivery method. Valid values:
        # 
        # *   0: The delivery method is disabled.
        # *   1: The delivery destination is enabled. This is the default value.
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.delivery_channel_assume_role_arn is not None:
            result['DeliveryChannelAssumeRoleArn'] = self.delivery_channel_assume_role_arn
        if self.delivery_channel_condition is not None:
            result['DeliveryChannelCondition'] = self.delivery_channel_condition
        if self.delivery_channel_id is not None:
            result['DeliveryChannelId'] = self.delivery_channel_id
        if self.delivery_channel_name is not None:
            result['DeliveryChannelName'] = self.delivery_channel_name
        if self.delivery_channel_target_arn is not None:
            result['DeliveryChannelTargetArn'] = self.delivery_channel_target_arn
        if self.delivery_channel_type is not None:
            result['DeliveryChannelType'] = self.delivery_channel_type
        if self.description is not None:
            result['Description'] = self.description
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('DeliveryChannelAssumeRoleArn') is not None:
            self.delivery_channel_assume_role_arn = m.get('DeliveryChannelAssumeRoleArn')
        if m.get('DeliveryChannelCondition') is not None:
            self.delivery_channel_condition = m.get('DeliveryChannelCondition')
        if m.get('DeliveryChannelId') is not None:
            self.delivery_channel_id = m.get('DeliveryChannelId')
        if m.get('DeliveryChannelName') is not None:
            self.delivery_channel_name = m.get('DeliveryChannelName')
        if m.get('DeliveryChannelTargetArn') is not None:
            self.delivery_channel_target_arn = m.get('DeliveryChannelTargetArn')
        if m.get('DeliveryChannelType') is not None:
            self.delivery_channel_type = m.get('DeliveryChannelType')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class PutDeliveryChannelResponseBody(TeaModel):
    def __init__(
        self,
        delivery_channel_id: str = None,
        request_id: str = None,
    ):
        # The ID of the delivery method that you created or the updated ID of the delivery method that you modified.
        self.delivery_channel_id = delivery_channel_id
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delivery_channel_id is not None:
            result['DeliveryChannelId'] = self.delivery_channel_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeliveryChannelId') is not None:
            self.delivery_channel_id = m.get('DeliveryChannelId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class PutDeliveryChannelResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PutDeliveryChannelResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PutDeliveryChannelResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutEvaluationsRequest(TeaModel):
    def __init__(
        self,
        evaluations: str = None,
        result_token: str = None,
    ):
        # The compliance evaluation results.
        self.evaluations = evaluations
        # The token used to return the response.
        self.result_token = result_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.evaluations is not None:
            result['Evaluations'] = self.evaluations
        if self.result_token is not None:
            result['ResultToken'] = self.result_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Evaluations') is not None:
            self.evaluations = m.get('Evaluations')
        if m.get('ResultToken') is not None:
            self.result_token = m.get('ResultToken')
        return self


class PutEvaluationsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # Indicates whether the operation was successful. Valid values:
        # 
        # *   true: The operation was successful.
        # *   false: The operation failed.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        return self


class PutEvaluationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PutEvaluationsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PutEvaluationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartConfigRuleEvaluationRequest(TeaModel):
    def __init__(
        self,
        compliance_pack_id: str = None,
        config_rule_id: str = None,
        revert_evaluation: bool = None,
    ):
        # The ID of the compliance package.
        # 
        # For more information about how to obtain the ID of a compliance package, see [ListCompliancePacks](~~263332~~).
        # 
        # >  You must set one of the `CompliancePackId` and `ConfigRuleId` parameters.
        self.compliance_pack_id = compliance_pack_id
        # The ID of the rule.
        # 
        # For more information about how to obtain the ID of a rule, see [ListConfigRules](~~169607~~).
        self.config_rule_id = config_rule_id
        # Specifies whether to reevaluate a non-compliant resource that is ignored. Valid values:
        # 
        # *   true: reevaluates a non-compliant resource that is ignored.
        # *   false: continues to ignore a non-compliant resource.
        self.revert_evaluation = revert_evaluation

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.compliance_pack_id is not None:
            result['CompliancePackId'] = self.compliance_pack_id
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.revert_evaluation is not None:
            result['RevertEvaluation'] = self.revert_evaluation
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CompliancePackId') is not None:
            self.compliance_pack_id = m.get('CompliancePackId')
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('RevertEvaluation') is not None:
            self.revert_evaluation = m.get('RevertEvaluation')
        return self


class StartConfigRuleEvaluationResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
    ):
        # The ID of the request.
        self.request_id = request_id
        # Indicates whether the operation is successful. Valid values:
        # 
        # *   true: The operation is successful.
        # *   false: The operation fails.
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        return self


class StartConfigRuleEvaluationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StartConfigRuleEvaluationResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StartConfigRuleEvaluationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartConfigurationRecorderRequest(TeaModel):
    def __init__(
        self,
        enterprise_edition: bool = None,
    ):
        # Specifies whether to upgrade Cloud Config for Enterprise. Default value: false. Valid values:
        # 
        # *   true
        # *   false
        # 
        # >  Cloud Config for Enterprise is upgraded to the account group feature. For more information, see [Announcement: Enterprise Edition Cloud Config Upgrade to Account Group](~~213433~~).
        self.enterprise_edition = enterprise_edition

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enterprise_edition is not None:
            result['EnterpriseEdition'] = self.enterprise_edition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EnterpriseEdition') is not None:
            self.enterprise_edition = m.get('EnterpriseEdition')
        return self


class StartConfigurationRecorderResponseBodyConfigurationRecorder(TeaModel):
    def __init__(
        self,
        account_id: int = None,
        configuration_recorder_status: str = None,
        organization_enable_status: str = None,
        organization_master_id: int = None,
        resource_types: List[str] = None,
    ):
        # The ID of your Alibaba Cloud account.
        # 
        # >  This parameter is returned only when the operation was called by an ordinary account.
        self.account_id = account_id
        # The status of the configuration recorder. Valid values:
        # 
        # *   REGISTRABLE: The configuration recorder has not been registered.
        # *   BUILDING: The configuration recorder is being deployed.
        # *   REGISTERED: The configuration recorder has been registered.
        # *   REBUILDING: The configuration recorder is being redeployed.
        self.configuration_recorder_status = configuration_recorder_status
        # The upgrade status of Cloud Config for Enterprise. Valid values:
        # 
        # *   REGISTRABLE: Cloud Config for Enterprise is not upgraded.
        # *   BUILDING: Cloud Config for Enterprise is being upgraded.
        # *   REGISTERED: Cloud Config for Enterprise is upgraded.
        self.organization_enable_status = organization_enable_status
        # The ID of the management account.
        # 
        # >  This parameter is returned only when the operation was called by a management account.
        self.organization_master_id = organization_master_id
        # The types of resources that are monitored by Cloud Config.
        # 
        # >  By default, Cloud Config returns all resource types. In the following sample responses, `ACS::ECS::Instance` and `ACS::ECS::NetworkInterface` are returned.
        self.resource_types = resource_types

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.configuration_recorder_status is not None:
            result['ConfigurationRecorderStatus'] = self.configuration_recorder_status
        if self.organization_enable_status is not None:
            result['OrganizationEnableStatus'] = self.organization_enable_status
        if self.organization_master_id is not None:
            result['OrganizationMasterId'] = self.organization_master_id
        if self.resource_types is not None:
            result['ResourceTypes'] = self.resource_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('ConfigurationRecorderStatus') is not None:
            self.configuration_recorder_status = m.get('ConfigurationRecorderStatus')
        if m.get('OrganizationEnableStatus') is not None:
            self.organization_enable_status = m.get('OrganizationEnableStatus')
        if m.get('OrganizationMasterId') is not None:
            self.organization_master_id = m.get('OrganizationMasterId')
        if m.get('ResourceTypes') is not None:
            self.resource_types = m.get('ResourceTypes')
        return self


class StartConfigurationRecorderResponseBody(TeaModel):
    def __init__(
        self,
        configuration_recorder: StartConfigurationRecorderResponseBodyConfigurationRecorder = None,
        request_id: str = None,
    ):
        # The details of the configuration recorder that monitors resources.
        self.configuration_recorder = configuration_recorder
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.configuration_recorder:
            self.configuration_recorder.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.configuration_recorder is not None:
            result['ConfigurationRecorder'] = self.configuration_recorder.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigurationRecorder') is not None:
            temp_model = StartConfigurationRecorderResponseBodyConfigurationRecorder()
            self.configuration_recorder = temp_model.from_map(m['ConfigurationRecorder'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartConfigurationRecorderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StartConfigurationRecorderResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StartConfigurationRecorderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopConfigRulesRequest(TeaModel):
    def __init__(
        self,
        config_rule_ids: str = None,
    ):
        # The IDs of the rules. Separate multiple rule IDs with commas (,). You can specify a maximum of 20 rule IDs at a time.
        self.config_rule_ids = config_rule_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_ids is not None:
            result['ConfigRuleIds'] = self.config_rule_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleIds') is not None:
            self.config_rule_ids = m.get('ConfigRuleIds')
        return self


class StopConfigRulesResponseBodyOperateRuleResultOperateRuleItemList(TeaModel):
    def __init__(
        self,
        config_rule_id: str = None,
        error_code: str = None,
        success: bool = None,
    ):
        # The ID of the rule.
        self.config_rule_id = config_rule_id
        # The error code.
        # 
        # *   If the rule is disabled, no error code is returned.
        # *   If you fail to disable the rule, an error code is returned. For more information, visit the [API Error Center](https://error-center.alibabacloud.com/status/product/Config).
        self.error_code = error_code
        # Indicates whether the rule is disabled. Valid values:
        # 
        # *   true
        # *   false
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_rule_id is not None:
            result['ConfigRuleId'] = self.config_rule_id
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigRuleId') is not None:
            self.config_rule_id = m.get('ConfigRuleId')
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class StopConfigRulesResponseBodyOperateRuleResult(TeaModel):
    def __init__(
        self,
        operate_rule_item_list: List[StopConfigRulesResponseBodyOperateRuleResultOperateRuleItemList] = None,
    ):
        # The result information about each rule.
        self.operate_rule_item_list = operate_rule_item_list

    def validate(self):
        if self.operate_rule_item_list:
            for k in self.operate_rule_item_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['OperateRuleItemList'] = []
        if self.operate_rule_item_list is not None:
            for k in self.operate_rule_item_list:
                result['OperateRuleItemList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.operate_rule_item_list = []
        if m.get('OperateRuleItemList') is not None:
            for k in m.get('OperateRuleItemList'):
                temp_model = StopConfigRulesResponseBodyOperateRuleResultOperateRuleItemList()
                self.operate_rule_item_list.append(temp_model.from_map(k))
        return self


class StopConfigRulesResponseBody(TeaModel):
    def __init__(
        self,
        operate_rule_result: StopConfigRulesResponseBodyOperateRuleResult = None,
        request_id: str = None,
    ):
        # The result information about the operation.
        self.operate_rule_result = operate_rule_result
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.operate_rule_result:
            self.operate_rule_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.operate_rule_result is not None:
            result['OperateRuleResult'] = self.operate_rule_result.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OperateRuleResult') is not None:
            temp_model = StopConfigRulesResponseBodyOperateRuleResult()
            self.operate_rule_result = temp_model.from_map(m['OperateRuleResult'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopConfigRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: StopConfigRulesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = StopConfigRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


