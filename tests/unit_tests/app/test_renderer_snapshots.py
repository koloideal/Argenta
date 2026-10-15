import pytest
from syrupy import SnapshotAssertion

from argenta.app.presentation.ascii_art import BundledFont, FigletFontLoader
from argenta.app.presentation.renderers import PlainRenderer, Renderer, RichRenderer
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.models import Command
from argenta.router import Router

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def registered_routers() -> RegisteredRouters:
    admin = Router(title="Admin")
    user = Router(title="User")

    @admin.command(Command("restart", description="Restart the service"))
    def restart_handler(response):
        pass

    @admin.command(Command("logs", description=""))
    def logs_handler(response):
        pass

    @user.command(Command("profile", description="Show user profile"))
    def profile_handler(response):
        pass

    routers = RegisteredRouters()
    routers.add_registered_router(admin)
    routers.add_registered_router(user)
    return routers


# ============================================================================
# Snapshot tests — parametrized over both renderers
# ============================================================================


_font_loader = FigletFontLoader()
_rich_renderer = RichRenderer(
    initial_message_font=_font_loader.load_bundled(BundledFont.TARTY1),
    farewell_message_font=_font_loader.load_bundled(BundledFont.CHUNKY),
)


@pytest.mark.parametrize("renderer", [_rich_renderer, PlainRenderer()], ids=["rich", "plain"])
class TestRendererSnapshots:
    def test_render_prompt(self, renderer: Renderer, snapshot: SnapshotAssertion) -> None:
        assert renderer.render_prompt("Enter command") == snapshot

    def test_render_initial_message(self, renderer: Renderer, snapshot: SnapshotAssertion) -> None:
        assert renderer.render_initial_message("Welcome!") == snapshot

    def test_render_farewell_message(self, renderer: Renderer, snapshot: SnapshotAssertion) -> None:
        assert renderer.render_farewell_message("Bye!") == snapshot

    def test_render_messages_on_startup(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        result = renderer.render_messages_on_startup(["First", "Second", "Third"])
        assert result == snapshot

    def test_render_text_for_description_message_generator(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        result = renderer.render_text_for_description_message_generator("deploy", "Deploy the app")
        assert result == snapshot

    def test_render_command_groups_description(
        self,
        renderer: Renderer,
        registered_routers: RegisteredRouters,
        snapshot: SnapshotAssertion,
    ) -> None:
        result = renderer.render_command_groups_description(
            lambda command, description: f"{command} — {description}",
            registered_routers,
        )
        assert result == snapshot

    def test_render_text_for_incorrect_input_syntax_handler(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        assert renderer.render_text_for_incorrect_input_syntax_handler("cmd --") == snapshot

    def test_render_text_for_repeated_input_flags_handler(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        result = renderer.render_text_for_repeated_input_flags_handler("cmd -a -a")
        assert result == snapshot

    def test_render_text_for_empty_input_command_handler(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        assert renderer.render_text_for_empty_input_command_handler() == snapshot

    def test_render_text_for_unknown_command_handler_no_similar(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        result = renderer.render_text_for_unknown_command_handler("whetever", None)
        assert result == snapshot

    def test_render_text_for_unknown_command_handler_with_similar(
        self, renderer: Renderer, snapshot: SnapshotAssertion
    ) -> None:
        result = renderer.render_text_for_unknown_command_handler("whetever", "whatever")
        assert result == snapshot
