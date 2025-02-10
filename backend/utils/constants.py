"""
Constants used throughout the application.
"""

# Template field names
class TemplateFields:
    KOMPETENZ_1 = "Personentage Kompetenz 1:"
    KOMPETENZ_2 = "Personentage Kompetenz 2:"
    KOMPETENZ_3 = "Personentage Kompetenz 3:"
    KOMPETENZ_4 = "Personentage Kompetenz 4:"
    TAETIGKEIT = "Tätigkeitsbeschreibung:"

    @classmethod
    def get_all_fields(cls) -> list[str]:
        """Return all field names."""
        return [
            cls.KOMPETENZ_1,
            cls.KOMPETENZ_2,
            cls.KOMPETENZ_3,
            cls.KOMPETENZ_4,
            cls.TAETIGKEIT
        ]
