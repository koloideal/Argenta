import pytest
from unittest.mock import Mock

from argenta.app.presentation.viewers import Viewer
from argenta.app.presentation.renderers import PlainRenderer
from argenta.app.dividing_line.models import StaticDividingLine, DynamicDividingLine
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router


@pytest.fixture
def mock_printer() -> Mock:
    return Mock()


@pytest.fixture
def mock_output_generator() -> Mock:
    return Mock()


class TestViewer:
    def test_viewer_initialization(self, mock_printer: Mock):
        renderer = PlainRenderer()
        dividing_line = StaticDividingLine()
        
        viewer = Viewer(mock_printer, renderer, dividing_line, False)
        
        assert viewer._printer == mock_printer
        assert viewer._renderer == renderer
        assert viewer._dividing_line == dividing_line
        assert viewer._override_system_messages is False

    def test_view_initial_message(self, mock_printer: Mock):
        renderer = PlainRenderer()
        viewer = Viewer(mock_printer, renderer, None, False)
        
        viewer.view_initial_message("Welcome")
        
        mock_printer.assert_called_once_with("Welcome")

    def test_view_messages_on_startup(self, mock_printer: Mock):
        renderer = PlainRenderer()
        viewer = Viewer(mock_printer, renderer, None, False)
        
        messages = ["Message 1", "Message 2"]
        viewer.view_messages_on_startup(messages)
        
        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Message 1" in call_arg
        assert "Message 2" in call_arg

    def test_view_command_groups_description(self, mock_printer: Mock):
        renderer = PlainRenderer()
        viewer = Viewer(mock_printer, renderer, None, False)
        
        router = Router(title="Test Router")
        
        @router.command(Command("test", description="Test command"))
        def handler(_: Response):
            pass
        
        registered_routers = RegisteredRouters()
        registered_routers.add_registered_router(router)
        
        def desc_gen(cmd: str, desc: str) -> str:
            return f"{cmd}: {desc}"
        
        viewer.view_command_groups_description(desc_gen, registered_routers)
        
        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Test Router" in call_arg
        assert "test: Test command" in call_arg

    def test_view_framed_text_with_no_dividing_line(self, mock_printer: Mock, mock_output_generator: Mock):
        renderer = PlainRenderer()
        viewer = Viewer(mock_printer, renderer, None, False)
        
        viewer.view_framed_text_from_generator(mock_output_generator)
        
        mock_output_generator.assert_called_once()

    def test_view_framed_text_with_static_dividing_line(self, mock_printer: Mock, mock_output_generator: Mock):
        renderer = PlainRenderer()
        dividing_line = StaticDividingLine("=")
        viewer = Viewer(mock_printer, renderer, dividing_line, False)
        
        viewer.view_framed_text_from_generator(mock_output_generator)
        
        mock_output_generator.assert_called_once()
        assert mock_printer.call_count >= 2

    def test_capture_stdout(self, mock_printer: Mock):
        renderer = PlainRenderer()
        viewer = Viewer(mock_printer, renderer, None, False)
        
        def test_func():
            print("test output")
        
        result = viewer._capture_stdout(test_func)
        assert "test output" in result

    def test_capture_stdout_reuses_buffer(self, mock_printer: Mock):
        renderer = PlainRenderer()
        viewer = Viewer(mock_printer, renderer, None, False)
        
        def test_func1():
            print("output 1")
        
        def test_func2():
            print("output 2")
        
        result1 = viewer._capture_stdout(test_func1)
        result2 = viewer._capture_stdout(test_func2)
        
        assert "output 1" in result1
        assert "output 1" not in result2
        assert "output 2" in result2

    def test_view_framed_text_with_dynamic_dividing_line(self, mock_printer: Mock):
        renderer = PlainRenderer()
        dividing_line = DynamicDividingLine("=")
        viewer = Viewer(mock_printer, renderer, dividing_line, False)
        
        def output_generator():
            print("test output")
        
        viewer.view_framed_text_from_generator(output_generator)
        
        assert mock_printer.call_count >= 2

    def test_view_framed_text_with_router_stdout_redirect(self, mock_printer: Mock, mock_output_generator: Mock):
        renderer = PlainRenderer()
        dividing_line = DynamicDividingLine("=")
        viewer = Viewer(mock_printer, renderer, dividing_line, False)
        
        viewer.view_framed_text_from_generator(mock_output_generator, is_stdout_redirected_by_router=True)
        
        mock_output_generator.assert_called_once()
        assert mock_printer.call_count >= 2

    def test_view_framed_text_with_unimplemented_dividing_line(self, mock_printer: Mock, mock_output_generator: Mock):
        class NotImplementedDividingLine:
            pass

        renderer = PlainRenderer()
        dividing_line = NotImplementedDividingLine()
        viewer = Viewer(mock_printer, renderer, dividing_line, False)
        
        with pytest.raises(NotImplementedError):
            viewer.view_framed_text_from_generator(mock_output_generator, is_stdout_redirected_by_router=True)
        
