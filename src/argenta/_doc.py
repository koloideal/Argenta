from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Doc:
    """
    Private. ``Annotated`` metadata documenting a configuration field:
    ``field: Annotated[int, Doc("what the field controls")] = 1``
    """

    text: str
