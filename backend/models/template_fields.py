"""
Data models for template fields and mapping.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
from backend.utils.constants import TemplateFields

@dataclass
class TemplateField:
    name: str
    placeholder: str
    required: bool = True
    max_length: Optional[int] = None
    field_type: str = "text"  # text, list, table, etc.

@dataclass
class KompetenzField:
    """Represents a competency field in the template."""
    days: int
    description: str

@dataclass
class CVTemplateData:
    """Represents the data structure for the CV template."""
    kompetenz_1: Optional[KompetenzField] = None
    kompetenz_2: Optional[KompetenzField] = None
    kompetenz_3: Optional[KompetenzField] = None
    kompetenz_4: Optional[KompetenzField] = None
    taetigkeit: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the template data to a dictionary."""
        return {
            TemplateFields.KOMPETENZ_1: self.kompetenz_1.days if self.kompetenz_1 else "",
            TemplateFields.KOMPETENZ_2: self.kompetenz_2.days if self.kompetenz_2 else "",
            TemplateFields.KOMPETENZ_3: self.kompetenz_3.days if self.kompetenz_3 else "",
            TemplateFields.KOMPETENZ_4: self.kompetenz_4.days if self.kompetenz_4 else "",
            TemplateFields.TAETIGKEIT: self.taetigkeit if self.taetigkeit else "",
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CVTemplateData':
        """Create a CVTemplateData instance from a dictionary."""
        return cls(
            kompetenz_1=KompetenzField(data.get('kompetenz_1_days', 0), data.get('kompetenz_1_description', '')),
            kompetenz_2=KompetenzField(data.get('kompetenz_2_days', 0), data.get('kompetenz_2_description', '')),
            kompetenz_3=KompetenzField(data.get('kompetenz_3_days', 0), data.get('kompetenz_3_description', '')),
            kompetenz_4=KompetenzField(data.get('kompetenz_4_days', 0), data.get('kompetenz_4_description', '')),
            taetigkeit=data.get('taetigkeit', '')
        )

@dataclass
class TemplateSection:
    name: str
    fields: Dict[str, TemplateField]
    order: int

@dataclass
class TemplateStructure:
    sections: Dict[str, TemplateSection]
    metadata: Dict[str, Any]
