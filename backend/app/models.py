from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class NodeModel(BaseModel):
    id: str
    label: str
    type: str  # 'person', 'phone', 'vehicle', 'account', 'location', 'cctv', 'organization'
    risk_score: float = 0.0  # 0 to 100
    syndicate: Optional[str] = "Independent"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EdgeModel(BaseModel):
    id: str
    source: str
    target: str
    type: str  # 'calls', 'transfers_to', 'owns_vehicle', 'spotted_at', 'co_accused', 'member_of', 'captured_by'
    weight: float = 1.0
    frequency: int = 1
    evidence_count: int = 1
    label: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GraphData(BaseModel):
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    summary: Dict[str, Any] = Field(default_factory=dict)

class LinkPredictionExplanation(BaseModel):
    source: str
    target: str
    source_name: str
    target_name: str
    predicted_relation: str
    confidence: float
    reasons: List[str]
    evidence_trail: List[str]

class CrossCaseCorrelation(BaseModel):
    fir_primary: str
    fir_secondary: str
    correlation_score: float
    shared_entities: List[Dict[str, Any]]
    modus_operandi_match: str
    recommended_action: str

class IngestionRequest(BaseModel):
    source_type: str  # 'fir', 'cdr', 'bank_statement', 'cctv_log'
    raw_text: Optional[str] = None
    file_name: Optional[str] = None
    records: Optional[List[Dict[str, Any]]] = None

class CopilotQuery(BaseModel):
    question: str
    case_context: Optional[str] = None
