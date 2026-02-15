from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime

@dataclass
class Action:
    type: str
    content: str
    target: str

@dataclass
class ConnectionEdge:
    connection_id: str
    strength: float  # 0.0-1.0
    influence_score: float
    interaction_history: List[Any] = field(default_factory=list)

@dataclass
class BehavioralEvent:
    timestamp: datetime
    action_type: str
    content_id: str
    outcome: Any

@dataclass
class InfluenceProfile:
    reach: float
    authority: float
    expertise_domains: List[str]
    follower_to_following_ratio: float
    engagement_rate: float

@dataclass
class Content:
    text: str
    content_type: str  # article, video, poll, etc.
    topics: List[str]
    length: int
    tone: str
    author_name: Optional[str] = None
    author_title: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    images: List[str] = field(default_factory=list)
    video_url: Optional[str] = None
    external_links: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Reaction:
    reaction_type: str  # like, love, insightful, celebrate
    comment: Optional[str] = None
    will_share: bool = False
    virality_coefficient: float = 0.0

@dataclass
class Interaction:
    content_id: str
    action_type: str
    outcome: Any
    timestamp: datetime = field(default_factory=datetime.now)
