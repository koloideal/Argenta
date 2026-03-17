import pytest
from dishka import Provider
from pytest_mock import MockerFixture

from argenta import App, Router
from argenta.command import Command
from argenta.orchestrator import Orchestrator
from argenta.orchestrator.argparser import ArgParser
from argenta.response import Response


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_argparser(mocker: MockerFixture) -> ArgParser:
    """Create a mock ArgParser that doesn't actually parse sys.argv"""
    argparser = ArgParser(processed_args=[])
    mocker.patch.object(argparser, '_parse_args')
    return argparser


@pytest.fixture
def sample_app() -> App:
    """Create a sample App for testing"""
    return App(override_system_messages=True)


@pytest.fixture
def sample_router() -> Router:
    """Create a sample Router with a test command"""
    router = Router()
    
    @router.command(Command('test'))
    def handler(_res: Response) -> None:
        print('test command executed')
    
    return router


# ============================================================================
# Tests for Orchestrator initialization
# ============================================================================


def test_orchestrator_initializes_with_no_argparser(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with no ArgParser"""
    mocker.patch('sys.argv', ['test_program'])
    orchestrator = Orchestrator()
    assert orchestrator._arg_parser is None


def test_orchestrator_initializes_with_custom_argparser(mock_argparser: ArgParser) -> None:
    """Test Orchestrator initialization with custom ArgParser"""
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    assert orchestrator._arg_parser is mock_argparser


def test_orchestrator_initializes_with_custom_providers(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with custom providers"""
    mocker.patch('sys.argv', ['test_program'])
    custom_provider = Provider()
    orchestrator = Orchestrator(custom_providers=[custom_provider])
    assert custom_provider in orchestrator._custom_providers


def test_orchestrator_initializes_with_auto_inject_disabled(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with auto_inject_handlers disabled"""
    mocker.patch('sys.argv', ['test_program'])
    orchestrator = Orchestrator(auto_inject_handlers=False)
    assert orchestrator._auto_inject_handlers is False


def test_orchestrator_initializes_with_auto_inject_enabled(mocker: MockerFixture) -> None:
    """Test Orchestrator initialization with auto_inject_handlers enabled (default)"""
    mocker.patch('sys.argv', ['test_program'])
    orchestrator = Orchestrator()
    assert orchestrator._auto_inject_handlers is True


def test_orchestrator_parses_args_on_initialization(mocker: MockerFixture, mock_argparser: ArgParser) -> None:
    """Test that Orchestrator calls _parse_args on initialization"""
    parse_spy = mocker.spy(mock_argparser, '_parse_args')
    _orchestrator = Orchestrator(arg_parser=mock_argparser)
    parse_spy.assert_called_once()


# ============================================================================
# Tests for run_repl method
# ============================================================================


def test_run_repl_creates_dishka_container(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl creates a dishka container"""
    mock_make_container = mocker.patch('argenta.orchestrator.entity.make_container')
    _mock_setup_dishka = mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)
    
    mock_make_container.assert_called_once()
    assert mock_make_container.call_args[1]['context'] == {ArgParser: mock_argparser}


def test_run_repl_calls_setup_dishka_with_auto_inject_enabled(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl calls setup_dishka with auto_inject=True"""
    mock_container = mocker.MagicMock()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    mocker.patch('argenta.orchestrator.entity.make_container', return_value=mock_container)
    mock_setup_dishka = mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(arg_parser=mock_argparser, auto_inject_handlers=True)
    orchestrator.run_repl(sample_app)
    
    mock_setup_dishka.assert_called_once_with(sample_app, mock_container, auto_inject=True)


def test_run_repl_calls_setup_dishka_with_auto_inject_disabled(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl calls setup_dishka with auto_inject=False"""
    mock_container = mocker.MagicMock()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    mocker.patch('argenta.orchestrator.entity.make_container', return_value=mock_container)
    mock_setup_dishka = mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(arg_parser=mock_argparser, auto_inject_handlers=False)
    orchestrator.run_repl(sample_app)
    
    mock_setup_dishka.assert_called_once_with(sample_app, mock_container, auto_inject=False)


def test_run_repl_calls_app_run_repl(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl calls app.run_polling()"""
    mocker.patch('argenta.orchestrator.entity.make_container')
    mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mock_run_repl = mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)
    
    mock_run_repl.assert_called_once()


def test_run_repl_includes_custom_providers_in_container(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that run_repl includes custom providers in container"""
    custom_provider = Provider()
    mock_make_container = mocker.patch('argenta.orchestrator.entity.make_container')
    mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(arg_parser=mock_argparser, custom_providers=[custom_provider])
    orchestrator.run_repl(sample_app)
    
    # Check that custom_provider was passed to make_container
    call_args = mock_make_container.call_args[0]
    assert custom_provider in call_args


# ============================================================================
# Tests for integration with App
# ============================================================================


def test_orchestrator_integrates_with_app_with_router(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App, sample_router: Router
) -> None:
    """Test that Orchestrator properly integrates with App that has routers"""
    mocker.patch('argenta.orchestrator.entity.make_container')
    mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mock_run_repl = mocker.patch.object(sample_app, '_run_repl')
    
    sample_app.include_router(sample_router)
    
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)
    
    mock_run_repl.assert_called_once()
    assert len(sample_app.registered_routers.registered_routers) == 1


# ============================================================================
# Tests for ArgParser integration
# ============================================================================


def test_orchestrator_passes_argparser_to_container_context(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that Orchestrator passes ArgParser instance to container context"""
    mock_make_container = mocker.patch('argenta.orchestrator.entity.make_container')
    mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    orchestrator.run_repl(sample_app)
    
    # Verify that ArgParser was passed in context
    call_kwargs = mock_make_container.call_args[1]
    assert 'context' in call_kwargs
    assert ArgParser in call_kwargs['context']
    assert call_kwargs['context'][ArgParser] is mock_argparser


# ============================================================================
# Tests for error handling
# ============================================================================


def test_orchestrator_handles_app_run_repl_exception(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that Orchestrator propagates exceptions from app.run_polling()"""
    mocker.patch('argenta.orchestrator.entity.make_container')
    mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl', side_effect=RuntimeError("Test error"))
    
    orchestrator = Orchestrator(arg_parser=mock_argparser)
    
    with pytest.raises(RuntimeError, match="Test error"):
        orchestrator.run_repl(sample_app)


# ============================================================================
# Tests for multiple providers
# ============================================================================


def test_orchestrator_accepts_multiple_custom_providers(
    mocker: MockerFixture, mock_argparser: ArgParser, sample_app: App
) -> None:
    """Test that Orchestrator accepts multiple custom providers"""
    provider1 = Provider()
    provider2 = Provider()
    mock_make_container = mocker.patch('argenta.orchestrator.entity.make_container')
    mocker.patch('argenta.orchestrator.entity.setup_dishka')
    mocker.patch.object(sample_app, '_run_repl')
    
    orchestrator = Orchestrator(
        arg_parser=mock_argparser,
        custom_providers=[provider1, provider2]
    )
    orchestrator.run_repl(sample_app)
    
    call_args = mock_make_container.call_args[0]
    assert provider1 in call_args
    assert provider2 in call_args
