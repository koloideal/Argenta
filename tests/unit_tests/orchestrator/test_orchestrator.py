import pytest
from dishka import Provider
from pytest_mock import MockerFixture

from argenta import App, Router
from argenta.a2ui import A2UIConfig, StdioTransport
from argenta.command import Command
from argenta.orchestrator import Orchestrator, RunnerConfig
from argenta.orchestrator.argparser import ArgParser
from argenta.response import Response

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_argparser(mocker: MockerFixture) -> ArgParser:
    """Create a mock ArgParser that doesn't actually parse sys.argv"""
    argparser = ArgParser(processed_args=[])
    mocker.patch.object(argparser, "_parse_args")
    return argparser


@pytest.fixture
def sample_app() -> App:
    """Create a sample App for testing"""
    return App(override_system_messages=True)


@pytest.fixture
def sample_router() -> Router:
    """Create a sample Router with a test command"""
    router = Router()

    @router.command(Command("test"))
    def handler(_res: Response) -> None:
        print("test command executed")

    return router


# ============================================================================
# Tests for Orchestrator initialization
# ============================================================================


def test_orchestrator_initializes_with_no_argparser(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with no ArgParser"""
    mocker.patch("sys.argv", ["test_program"])
    orchestrator = Orchestrator()
    assert orchestrator._arg_parser is None


def test_orchestrator_initializes_with_custom_argparser(mock_argparser: ArgParser) -> None:
    """Test Orchestrator initialization with custom ArgParser"""
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    assert orchestrator._arg_parser is mock_argparser


def test_orchestrator_initializes_with_custom_providers(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with custom providers"""
    mocker.patch("sys.argv", ["test_program"])
    custom_provider = Provider()
    orchestrator = Orchestrator(custom_providers=[custom_provider])
    assert custom_provider in orchestrator._custom_providers


def test_orchestrator_initializes_with_auto_inject_disabled(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with auto_inject_handlers disabled"""
    mocker.patch("sys.argv", ["test_program"])
    orchestrator = Orchestrator(auto_inject_handlers=False)
    assert orchestrator._auto_inject_handlers is False


def test_orchestrator_initializes_with_auto_inject_enabled(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with auto_inject_handlers enabled (default)"""
    mocker.patch("sys.argv", ["test_program"])
    orchestrator = Orchestrator()
    assert orchestrator._auto_inject_handlers is True


def test_orchestrator_parses_args_on_initialization(
    mocker: MockerFixture, mock_argparser: ArgParser
) -> None:
    """Test that Orchestrator calls _parse_args on initialization"""
    parse_spy = mocker.spy(mock_argparser, "_parse_args")
    Orchestrator(arg_parser=mock_argparser)
    parse_spy.assert_called_once()


# ============================================================================
# Tests for run_repl method
# ============================================================================


def test_run_repl_creates_dishka_container(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl creates a dishka container"""
    mock_make_container = mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)

    mock_make_container.assert_called_once()
    assert mock_make_container.call_args[1]["context"] == {ArgParser: mock_argparser}


def test_run_repl_calls_setup_dishka_with_auto_inject_enabled(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl calls setup_dishka with auto_inject=True"""
    mock_container = mocker.MagicMock()
    mocker.patch("argenta.orchestrator.entity.make_container", return_value=mock_container)
    mock_setup_dishka = mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser, auto_inject_handlers=True)
    orchestrator.run_repl(sample_app)

    mock_setup_dishka.assert_called_once_with(sample_app, mock_container, auto_inject=True)


def test_run_repl_calls_setup_dishka_with_auto_inject_disabled(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl calls setup_dishka with auto_inject=False"""
    mock_container = mocker.MagicMock()
    mocker.patch("argenta.orchestrator.entity.make_container", return_value=mock_container)
    mock_setup_dishka = mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser, auto_inject_handlers=False)
    orchestrator.run_repl(sample_app)

    mock_setup_dishka.assert_called_once_with(sample_app, mock_container, auto_inject=False)


def test_run_repl_calls_app_run_repl(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl calls app.run_polling()"""
    mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mock_runtime_cls = mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)

    mock_runtime_cls.return_value.run.assert_called_once()


def test_run_repl_includes_custom_providers_in_container(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl includes custom providers in container"""
    custom_provider = Provider()
    mock_make_container = mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser, custom_providers=[custom_provider])
    orchestrator.run_repl(sample_app)

    # Check that custom_provider was passed to make_container
    call_args = mock_make_container.call_args[0]
    assert custom_provider in call_args


def test_run_repl_delegates_to_run_agent_in_a2ui_mode(
    mocker: MockerFixture,
    mock_argparser: ArgParser,
    sample_app: App,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that run_repl delegates to run_agent when ARGENTA_RUN_MODE=a2ui"""
    monkeypatch.setenv("ARGENTA_RUN_MODE", "a2ui")
    mock_run_agent = mocker.patch.object(Orchestrator, "run_agent")
    mock_repl_runtime = mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)

    mock_run_agent.assert_called_once()
    called_app, called_transport = mock_run_agent.call_args.args
    assert called_app is sample_app
    assert isinstance(called_transport, StdioTransport)
    mock_repl_runtime.assert_not_called()


def test_run_repl_delegates_with_custom_runner_config(
    mocker: MockerFixture,
    mock_argparser: ArgParser,
    sample_app: App,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a custom RunnerConfig changes the mode env var read"""
    monkeypatch.setenv("CUSTOM_RUN_MODE", "a2ui")
    mock_run_agent = mocker.patch.object(Orchestrator, "run_agent")

    orchestrator = Orchestrator(
        arg_parser=mock_argparser,
        runner_config=RunnerConfig(mode_env_var="CUSTOM_RUN_MODE"),
    )
    orchestrator.run_repl(sample_app)

    mock_run_agent.assert_called_once()


# ============================================================================
# Tests for run_agent method
# ============================================================================


def test_run_agent_creates_dishka_container(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_agent creates a dishka container"""
    mock_make_container = mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.AgentRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_agent(sample_app, mocker.MagicMock())

    mock_make_container.assert_called_once()


def test_run_agent_calls_setup_dishka(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_agent calls setup_dishka"""
    mock_container = mocker.MagicMock()
    mocker.patch("argenta.orchestrator.entity.make_container", return_value=mock_container)
    mock_setup_dishka = mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.AgentRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_agent(sample_app, mocker.MagicMock())

    mock_setup_dishka.assert_called_once_with(sample_app, mock_container, auto_inject=True)


def test_run_agent_runs_agent_runtime(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_agent instantiates and runs AgentRuntime"""
    mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mock_runtime_cls = mocker.patch("argenta.orchestrator.entity.AgentRuntime")
    transport = mocker.MagicMock()

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_agent(sample_app, transport)

    call_args = mock_runtime_cls.call_args[0]
    assert call_args[0] is sample_app
    assert call_args[1] is transport
    mock_runtime_cls.return_value.run.assert_called_once()


def test_run_agent_passes_config_to_container_context(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_agent puts A2UIConfig into the container context"""
    mock_make_container = mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.AgentRuntime")
    config = A2UIConfig(surface_id="custom")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_agent(sample_app, mocker.MagicMock(), config=config)

    assert mock_make_container.call_args[1]["context"][A2UIConfig] is config


def test_run_agent_closes_container_when_runtime_raises(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_agent closes the dishka container even if the runtime raises"""
    mock_container = mocker.MagicMock()
    mocker.patch("argenta.orchestrator.entity.make_container", return_value=mock_container)
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mock_container.__exit__.return_value = False
    mocker.patch(
        "argenta.orchestrator.entity.AgentRuntime",
        return_value=mocker.MagicMock(run=mocker.MagicMock(side_effect=RuntimeError("x"))),
    )

    with pytest.raises(RuntimeError, match="x"):
        Orchestrator(arg_parser=mock_argparser).run_agent(sample_app, mocker.MagicMock())

    mock_container.__exit__.assert_called_once()


# ============================================================================
# Tests for integration with App
# ============================================================================


def test_orchestrator_integrates_with_app_with_router(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App, sample_router: Router
) -> None:
    """Test that Orchestrator properly integrates with App that has routers"""
    mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mock_runtime_cls = mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    sample_app.include_router(sample_router)

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)

    mock_runtime_cls.return_value.run.assert_called_once()
    assert len(sample_app.registered_routers.registered_routers) == 1


# ============================================================================
# Tests for ArgParser integration
# ============================================================================


def test_orchestrator_passes_argparser_to_container_context(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that Orchestrator passes ArgParser instance to container context"""
    mock_make_container = mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)

    # Verify that ArgParser was passed in context
    call_kwargs = mock_make_container.call_args[1]
    assert "context" in call_kwargs
    assert ArgParser in call_kwargs["context"]
    assert call_kwargs["context"][ArgParser] is mock_argparser


# ============================================================================
# Tests for error handling
# ============================================================================


def test_orchestrator_handles_app_run_repl_exception(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that Orchestrator propagates exceptions from app.run_polling()"""
    mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch(
        "argenta.orchestrator.entity.REPLRuntime",
        return_value=mocker.MagicMock(run=mocker.MagicMock(side_effect=RuntimeError("Test error"))),
    )

    orchestrator = Orchestrator(arg_parser=mock_argparser)

    with pytest.raises(RuntimeError, match="Test error"):
        orchestrator.run_repl(sample_app)


def test_run_repl_closes_container_after_repl_finishes(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl closes the dishka container so provider finalizers run"""
    mock_container = mocker.MagicMock()
    mocker.patch("argenta.orchestrator.entity.make_container", return_value=mock_container)
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mock_container.__exit__.return_value = False
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    Orchestrator(arg_parser=mock_argparser).run_repl(sample_app)

    mock_container.__exit__.assert_called_once()


def test_run_repl_closes_container_when_repl_raises(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl closes the dishka container even if the REPL raises"""
    mock_container = mocker.MagicMock()
    mocker.patch("argenta.orchestrator.entity.make_container", return_value=mock_container)
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mock_container.__exit__.return_value = False
    mocker.patch(
        "argenta.orchestrator.entity.REPLRuntime",
        return_value=mocker.MagicMock(run=mocker.MagicMock(side_effect=RuntimeError("Test error"))),
    )

    with pytest.raises(RuntimeError, match="Test error"):
        Orchestrator(arg_parser=mock_argparser).run_repl(sample_app)

    mock_container.__exit__.assert_called_once()


# ============================================================================
# Tests for multiple providers
# ============================================================================


def test_orchestrator_accepts_multiple_custom_providers(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that Orchestrator accepts multiple custom providers"""
    provider1 = Provider()
    provider2 = Provider()
    mock_make_container = mocker.patch("argenta.orchestrator.entity.make_container")
    mocker.patch("argenta.orchestrator.entity.setup_dishka")
    mocker.patch("argenta.orchestrator.entity.REPLRuntime")

    orchestrator = Orchestrator(arg_parser=mock_argparser, custom_providers=[provider1, provider2])
    orchestrator.run_repl(sample_app)

    call_args = mock_make_container.call_args[0]
    assert provider1 in call_args
    assert provider2 in call_args
