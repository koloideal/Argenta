import dishka

from argenta.a2ui.models import A2UIConfig


class A2UIProvider(dishka.Provider):
    """
    Public. Provides the A2UI configuration from the container context
    """

    a2ui_config = dishka.from_context(provides=A2UIConfig, scope=dishka.Scope.APP)
