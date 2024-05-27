from django.apps import AppConfig


class AppForAnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_analysis'

    def ready(self):
        try:
            import app_analysis.signals
        except ImportError:
            pass
