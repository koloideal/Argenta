from argenta.app.presentation import BlockKind, PlainRenderer
from argenta.repl import DynamicDividingLine, REPLConfig, StaticDividingLine, TerminalLayout


def _layout(config: REPLConfig) -> tuple[TerminalLayout, list[str]]:
    printed: list[str] = []
    return TerminalLayout(printed.append, PlainRenderer(), config), printed


def test_gap_before_block_follows_its_kind() -> None:
    layout, printed = _layout(REPLConfig(startup_messages_gap=1, command_groups_gap=3))

    layout.present(BlockKind.BANNER, lambda: printed.append("banner"))
    layout.present(BlockKind.STARTUP_MESSAGES, lambda: printed.append("startup"))
    layout.present(BlockKind.COMMAND_GROUPS, lambda: printed.append("groups"))

    assert printed == ["banner", "", "startup", "", "", "", "groups"]


def test_output_without_dividing_line_is_not_framed() -> None:
    layout, printed = _layout(REPLConfig())

    layout.present(BlockKind.OUTPUT, lambda: printed.append("out"))

    assert printed == ["out"]


def test_static_line_frames_output_and_system_blocks() -> None:
    layout, printed = _layout(REPLConfig(dividing_line=StaticDividingLine("~", length=3)))

    layout.present(BlockKind.SYSTEM, lambda: printed.append("err"))

    assert printed == ["~~~", "", "err", "", "~~~"]


def test_frame_padding_is_configurable() -> None:
    config = REPLConfig(dividing_line=StaticDividingLine("~", length=3), frame_padding=0)
    layout, printed = _layout(config)

    layout.present(BlockKind.OUTPUT, lambda: printed.append("out"))

    assert printed == ["~~~", "out", "~~~"]


def test_dynamic_line_sized_to_captured_output() -> None:
    layout, printed = _layout(REPLConfig(dividing_line=DynamicDividingLine("-")))

    layout.present(BlockKind.OUTPUT, lambda: print("x" * 12))

    assert printed == ["-" * 12, "", "x" * 12, "", "-" * 12]


def test_dynamic_line_falls_back_to_static_when_not_capturable() -> None:
    layout, printed = _layout(REPLConfig(dividing_line=DynamicDividingLine("-")))

    layout.present(BlockKind.OUTPUT, lambda: printed.append("ask"), capturable=False)

    assert printed == ["-" * 25, "", "ask", "", "-" * 25]


def test_farewell_is_never_framed() -> None:
    layout, printed = _layout(REPLConfig(dividing_line=StaticDividingLine("~", length=3)))

    layout.present(BlockKind.FAREWELL, lambda: printed.append("bye"))

    assert printed == ["bye"]


def test_read_input_surrounds_prompt_with_gap() -> None:
    layout, printed = _layout(REPLConfig(prompt_gap=2))

    entered = layout.read_input(lambda: "cmd")

    assert entered == "cmd"
    assert printed == ["", "", "", ""]
