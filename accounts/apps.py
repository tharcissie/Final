from django.apps import AppConfig
class AccountsConfig(AppConfig):
    name = 'accounts'

#####################     triggering the signals      ######################

    def ready(self):
        import accounts.signals
