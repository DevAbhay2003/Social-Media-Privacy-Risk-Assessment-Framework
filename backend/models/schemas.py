"""
Social Media Privacy Risk Assessment Framework
Data Models and Data Contracts
===================================================
Defines explicit contracts for requests, responses, and assessment entities.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class CategoryScoreDTO:
    category_code: str
    category_name: str
    score: int
    weight: float
    risk_level: str
    description: str

@dataclass
class FindingDTO:
    category_code: str
    category_name: str
    finding_type: str
    severity: str
    title: str
    description: str
    question_id: Optional[str] = None
    user_response: Optional[str] = None

@dataclass
class RecommendationDTO:
    category_code: str
    category_name: str
    priority: str
    title: str
    action_steps: str
    impact_estimate: str
    question_id: Optional[str] = None

@dataclass
class AssessmentDTO:
    assessment_id: str
    overall_score: int
    risk_level: str
    platform: str
    source_type: str
    created_at: str
    category_scores: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
