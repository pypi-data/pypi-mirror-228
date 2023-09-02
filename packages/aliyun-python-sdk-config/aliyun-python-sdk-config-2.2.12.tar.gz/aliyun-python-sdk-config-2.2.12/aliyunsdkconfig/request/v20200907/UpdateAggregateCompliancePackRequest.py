# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkconfig.endpoint import endpoint_data
import json

class UpdateAggregateCompliancePackRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Config', '2020-09-07', 'UpdateAggregateCompliancePack')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_TagKeyScope(self): # String
		return self.get_body_params().get('TagKeyScope')

	def set_TagKeyScope(self, TagKeyScope):  # String
		self.add_body_params('TagKeyScope', TagKeyScope)
	def get_CompliancePackName(self): # String
		return self.get_body_params().get('CompliancePackName')

	def set_CompliancePackName(self, CompliancePackName):  # String
		self.add_body_params('CompliancePackName', CompliancePackName)
	def get_ClientToken(self): # String
		return self.get_body_params().get('ClientToken')

	def set_ClientToken(self, ClientToken):  # String
		self.add_body_params('ClientToken', ClientToken)
	def get_Description(self): # String
		return self.get_body_params().get('Description')

	def set_Description(self, Description):  # String
		self.add_body_params('Description', Description)
	def get_AggregatorId(self): # String
		return self.get_body_params().get('AggregatorId')

	def set_AggregatorId(self, AggregatorId):  # String
		self.add_body_params('AggregatorId', AggregatorId)
	def get_TagValueScope(self): # String
		return self.get_body_params().get('TagValueScope')

	def set_TagValueScope(self, TagValueScope):  # String
		self.add_body_params('TagValueScope', TagValueScope)
	def get_RegionIdsScope(self): # String
		return self.get_body_params().get('RegionIdsScope')

	def set_RegionIdsScope(self, RegionIdsScope):  # String
		self.add_body_params('RegionIdsScope', RegionIdsScope)
	def get_CompliancePackId(self): # String
		return self.get_body_params().get('CompliancePackId')

	def set_CompliancePackId(self, CompliancePackId):  # String
		self.add_body_params('CompliancePackId', CompliancePackId)
	def get_ConfigRules(self): # Array
		return self.get_body_params().get('ConfigRules')

	def set_ConfigRules(self, ConfigRules):  # Array
		self.add_body_params("ConfigRules", json.dumps(ConfigRules))
	def get_RiskLevel(self): # Integer
		return self.get_body_params().get('RiskLevel')

	def set_RiskLevel(self, RiskLevel):  # Integer
		self.add_body_params('RiskLevel', RiskLevel)
	def get_ResourceGroupIdsScope(self): # String
		return self.get_body_params().get('ResourceGroupIdsScope')

	def set_ResourceGroupIdsScope(self, ResourceGroupIdsScope):  # String
		self.add_body_params('ResourceGroupIdsScope', ResourceGroupIdsScope)
	def get_ExcludeResourceIdsScope(self): # String
		return self.get_body_params().get('ExcludeResourceIdsScope')

	def set_ExcludeResourceIdsScope(self, ExcludeResourceIdsScope):  # String
		self.add_body_params('ExcludeResourceIdsScope', ExcludeResourceIdsScope)
