from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class PhoneRecord:
    phone_type: str = ""
    phone_value: str = ""
    is_primary: bool = False
    is_email: bool = False

@dataclass
class EmploymentRecord:
    organization: str = "Columbia College"
    position: str = ""
    profession: str = ""
    from_date: str = ""
    to_date: str = ""
    industry: str = ""
    is_employer: bool = True
    is_primary: bool = False
    relationship: str = "Employer"
    reciprocal: str = "Employee"

@dataclass
class MajorRecord:
    major: str = ""
    import_id: str = ""

@dataclass
class MinorRecord:
    minor: str = ""
    import_id: str = ""

@dataclass
class AttributeRecord:
    category: str = ""
    description: str = ""
    import_id: str = ""

@dataclass
class DegreeRecord:
    school_name: str = ""
    entry_date: str = ""
    left_date: str = ""
    graduation_date: str = ""
    class_of: str = ""
    degree: str = ""
    campus: str = ""
    primary_alumni: str = ""
    majors: List[MajorRecord] = field(default_factory=list)
    minors: List[MinorRecord] = field(default_factory=list)
    attributes: List[AttributeRecord] = field(default_factory=list)

@dataclass
class MilitaryRecord:
    organization: str = "United States Military"
    service_type: str = ""
    branch: str = ""
    is_employer: bool = True
    is_primary: bool = False
    relationship: str = "Employer"
    reciprocal: str = "Employee"

@dataclass
class RelationshipRecord:
    related_lookup_id: str = ""
    relationship: str = ""
    reciprocal: str = ""

@dataclass
class Constituent:
    lookup_id: str
    sky_id: Optional[int] = None
    cons_import_id: Optional[str] = None
    record_status: str = "NEW"
    core: Dict[str, Any] = field(default_factory=dict)
    phones: List[PhoneRecord] = field(default_factory=list)
    employment: List[EmploymentRecord] = field(default_factory=list)
    education: List[DegreeRecord] = field(default_factory=list)
    military: List[MilitaryRecord] = field(default_factory=list)
    relationships: List[RelationshipRecord] = field(default_factory=list)
    update_flags: dict = field(default_factory=dict)
    update_actions: List[str] = field(default_factory=list)