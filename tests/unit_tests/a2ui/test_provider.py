from dishka import make_container

from argenta.a2ui.config import A2UIConfig
from argenta.a2ui.provider import A2UIProvider


def test_a2ui_config_resolved_from_context() -> None:
    config = A2UIConfig(surface_id="custom")
    container = make_container(A2UIProvider(), context={A2UIConfig: config})

    with container:
        assert container.get(A2UIConfig) is config
