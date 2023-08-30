# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2022 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from ansible_risk_insight.models import (
    AnsibleRunContext,
    RunTargetType,
    DefaultRiskType as RiskType,
    AnnotationCondition,
    Rule,
    Severity,
    RuleTag as Tag,
    RuleResult,
)


@dataclass
class PkgInstallRuleResult(RuleResult):
    pass


@dataclass
class PkgInstallRule(Rule):
    rule_id: str = "R113"
    description: str = "A parameterized pkg installation is found"
    enabled: bool = True
    name: str = "PkgInstall"
    version: str = "v0.0.1"
    severity: Severity = Severity.MEDIUM
    tags: tuple = Tag.PACKAGE
    result_type: type = PkgInstallRuleResult

    def match(self, ctx: AnsibleRunContext) -> bool:
        return ctx.current.type == RunTargetType.Task

    def process(self, ctx: AnsibleRunContext):
        task = ctx.current

        ac = AnnotationCondition().risk_type(RiskType.PACKAGE_INSTALL).attr("is_mutable_pkg", True)
        verdict = task.has_annotation_by_condition(ac)

        detail = {}
        if verdict:
            anno = task.get_annotation_by_condition(ac)
            if anno:
                detail["pkg"] = anno.pkg

        return RuleResult(verdict=verdict, detail=detail, file=task.file_info(), rule=self.get_metadata())
