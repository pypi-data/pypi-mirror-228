"""
App config
"""

# Django
from django.apps import AppConfig

from . import __version__


class TemplateConfig(AppConfig):
    """
    Template config
    """

    name = "sev3rance_auth_templates"
    label = "sev3rance_auth_templates"
    verbose_name = f"Sev3rance Alliance Auth Templates v{__version__}"
