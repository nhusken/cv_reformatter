"""
Template management and field mapping functionality.
"""
from typing import Dict, Any
from backend.models.template_fields import CVTemplateData, KompetenzField, TemplateField, TemplateSection, TemplateStructure
from backend.utils.constants import TemplateFields
from backend.services.docx_reader import DocxReader
import logging
import re

logger = logging.getLogger(__name__)

class TemplateManager:
    def __init__(self):
        self.reader = DocxReader()
        self.template_structure = self._create_default_structure()

    def _create_default_structure(self) -> TemplateStructure:
        """Create the default template structure with the five specific fields."""
        sections = {
            "personal": TemplateSection(
                name="Personal Information",
                fields={
                    "field1": TemplateField(
                        name="Field 1",
                        placeholder="[Field 1 Content]"
                    )
                },
                order=1
            ),
            # Add other sections for your specific fields
        }
        
        return TemplateStructure(
            sections=sections,
            metadata={"version": "1.0"}
        )

    def extract_days_from_text(self, text: str) -> int:
        """
        Extract number of days from text.
        
        Examples:
            "120 Tage in Python" -> 120
            "Etwa 50 Personentage" -> 50
            "PT: 30" -> 30
            "20 PT in Java" -> 20
        
        Args:
            text: Text to extract days from
            
        Returns:
            Number of days as integer, 0 if no valid number found
        """
        if not text:
            return 0

        # Convert text to lowercase for easier matching
        text = text.lower()
        
        # Look for specific patterns
        patterns = [
            r'(\d+)\s*(?:tage?|pt|personentage?)',  # matches: 120 Tage, 50 PT, 30 Personentage
            r'(?:tage?|pt|personentage?)\s*:\s*(\d+)',  # matches: Tage: 120, PT: 50
            r'(\d+)\s*(?=\s|$)',  # fallback: just look for numbers
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    return int(match.group(1))
                except (IndexError, ValueError):
                    continue
        
        # If no patterns matched, try to find any number
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0

    def process_cv_content(self, cv_content: Dict[str, Any]) -> CVTemplateData:
        """
        Process the CV content and extract relevant information for the template fields.
        
        Args:
            cv_content: Dictionary containing paragraphs and tables from the CV
            
        Returns:
            CVTemplateData object with extracted information
        """
        template_data = CVTemplateData()
        paragraphs = cv_content.get("paragraphs", [])
        tables = cv_content.get("tables", [])

        # Process competency fields
        for field in TemplateFields.get_all_fields():
            content = self.reader.find_field_content(field)
            if content:
                if field == TemplateFields.TAETIGKEIT:
                    template_data.taetigkeit = content
                else:
                    # For competency fields, extract days and description
                    days = self.extract_days_from_text(content)
                    if field == TemplateFields.KOMPETENZ_1:
                        template_data.kompetenz_1 = KompetenzField(days, content)
                    elif field == TemplateFields.KOMPETENZ_2:
                        template_data.kompetenz_2 = KompetenzField(days, content)
                    elif field == TemplateFields.KOMPETENZ_3:
                        template_data.kompetenz_3 = KompetenzField(days, content)
                    elif field == TemplateFields.KOMPETENZ_4:
                        template_data.kompetenz_4 = KompetenzField(days, content)

        return template_data

    def load_and_process_template(self, template_file) -> None:
        """
        Load and process the template file.
        
        Args:
            template_file: The template file to process
        """
        try:
            self.reader.load_document(template_file)
            logger.info("Template file loaded successfully")
        except Exception as e:
            logger.error(f"Error loading template file: {str(e)}")
            raise

    def validate_template(self) -> bool:
        """
        Validate that the template contains all required fields.
        
        Returns:
            bool: True if template is valid, False otherwise
        """
        if not self.reader.document:
            raise ValueError("No template loaded")

        missing_fields = []
        for field in TemplateFields.get_all_fields():
            if not self.reader.find_field_content(field):
                missing_fields.append(field)

        if missing_fields:
            logger.warning(f"Missing fields in template: {missing_fields}")
            return False

        return True

    def map_cv_to_template(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map CV data to template fields."""
        mapped_data = {}
        for section_name, section in self.template_structure.sections.items():
            mapped_data[section_name] = {}
            for field_name, field in section.fields.items():
                # Implement your mapping logic here
                mapped_data[section_name][field_name] = cv_data.get(field_name, "")
        
        return mapped_data
