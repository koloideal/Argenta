from argenta.app.presentation.renderers import RichRenderer, PlainRenderer
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router


class TestRichRenderer:
    def test_render_prompt(self):
        result = RichRenderer.render_prompt("Enter command")
        assert result == "<gray><b>Enter command</b></gray>"

    def test_render_text_for_description_message_generator(self):
        result = RichRenderer.render_text_for_description_message_generator("test", "Test command")
        assert "[bold red]<test>[/bold red]" in result
        assert "[bold yellow italic]Test command[/bold yellow italic]" in result

    def test_render_text_for_incorrect_input_syntax_handler(self):
        result = RichRenderer.render_text_for_incorrect_input_syntax_handler("bad --flag")
        assert result == "[red bold]Incorrect flag syntax: bad --flag[/red bold]"

    def test_render_text_for_repeated_input_flags_handler(self):
        result = RichRenderer.render_text_for_repeated_input_flags_handler("cmd --flag --flag")
        assert result == "[red bold]Repeated input flags: cmd --flag --flag[/red bold]"

    def test_render_text_for_empty_input_command_handler(self):
        result = RichRenderer.render_text_for_empty_input_command_handler()
        assert result == "[red bold]Empty input command[/red bold]"

    def test_render_text_for_unknown_command_handler_without_similar(self):
        result = RichRenderer.render_text_for_unknown_command_handler("unknown", None)
        assert "[red]Unknown command:[/red]" in result
        assert "[blue]unknown[/blue]" in result
        assert "most similar" not in result

    def test_render_text_for_unknown_command_handler_with_similar(self):
        result = RichRenderer.render_text_for_unknown_command_handler("unknwn", "unknown")
        assert "[red]Unknown command:[/red]" in result
        assert "[blue]unknwn[/blue]" in result
        assert "[red], most similar:[/red]" in result
        assert "[blue]unknown[/blue]" in result

    def test_render_messages_on_startup(self):
        messages = ["Message 1", "Message 2"]
        result = RichRenderer.render_messages_on_startup(messages)
        assert result == "\nMessage 1\nMessage 2"

    def test_render_command_groups_description(self):
        router = Router(title="Test Router")
        
        @router.command(Command("test", description="Test command"))
        def handler(_: Response):
            pass
        
        registered_routers = RegisteredRouters()
        registered_routers.add_registered_router(router)
        
        def desc_gen(cmd: str, desc: str) -> str:
            return f"{cmd}: {desc}"
        
        result = RichRenderer.render_command_groups_description(desc_gen, registered_routers)
        assert "Test Router" in result
        assert "test: Test command" in result


class TestPlainRenderer:
    def test_render_prompt(self):
        result = PlainRenderer.render_prompt("Enter command")
        assert result == "Enter command"

    def test_render_initial_message(self):
        result = PlainRenderer.render_initial_message("Welcome")
        assert result == "Welcome"

    def test_render_farewell_message(self):
        result = PlainRenderer.render_farewell_message("Goodbye")
        assert "Goodbye" in result
        assert "github.com/koloideal/Argenta" in result
        assert "made by kolo" in result

    def test_render_text_for_description_message_generator(self):
        result = PlainRenderer.render_text_for_description_message_generator("test", "Test command")
        assert result == "test *=*=* Test command"

    def test_render_text_for_incorrect_input_syntax_handler(self):
        result = PlainRenderer.render_text_for_incorrect_input_syntax_handler("bad --flag")
        assert result == "Incorrect flag syntax: bad --flag"

    def test_render_text_for_repeated_input_flags_handler(self):
        result = PlainRenderer.render_text_for_repeated_input_flags_handler("cmd --flag --flag")
        assert result == "Repeated input flags: cmd --flag --flag"

    def test_render_text_for_empty_input_command_handler(self):
        result = PlainRenderer.render_text_for_empty_input_command_handler()
        assert result == "Empty input command"

    def test_render_text_for_unknown_command_handler_without_similar(self):
        result = PlainRenderer.render_text_for_unknown_command_handler("unknown", None)
        assert result == "Unknown command: unknown"

    def test_render_text_for_unknown_command_handler_with_similar(self):
        result = PlainRenderer.render_text_for_unknown_command_handler("unknwn", "unknown")
        assert result == "Unknown command: unknwn, most similar: unknown"

    def test_render_messages_on_startup(self):
        renderer = PlainRenderer()
        messages = ["Message 1", "Message 2"]
        result = renderer.render_messages_on_startup(messages)
        assert result == "\nMessage 1\nMessage 2"

    def test_render_command_groups_description(self):
        router = Router(title="Test Router")
        
        @router.command(Command("test", description="Test command"))
        def handler(_: Response):
            pass
        
        registered_routers = RegisteredRouters()
        registered_routers.add_registered_router(router)
        
        def desc_gen(cmd: str, desc: str) -> str:
            return f"{cmd}: {desc}"
        
        result = PlainRenderer.render_command_groups_description(desc_gen, registered_routers)
        assert "Test Router" in result
        assert "test: Test command" in result
