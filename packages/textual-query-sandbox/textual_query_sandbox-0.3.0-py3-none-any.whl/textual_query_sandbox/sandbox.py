"""A simple textual DOM query sandbox."""

from __future__ import annotations

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Input, Pretty, Static


class Playground(Vertical, inherit_css=False):
    """The playground container."""

    BORDER_TITLE = "Playground"

    DEFAULT_CSS = """
    Playground {
        border: panel cornflowerblue;
        height: 2fr;
    }
    """


def title(widget: Widget, main_title: str | None = None) -> Widget:
    """Add a title to a widget.

    Args:
        widget: The widget to name.
        main_title: The optional title to give the widget.

    Returns:
        The widget.
    """
    border_title = main_title
    if main_title is None:
        border_title = widget.__class__.__name__
        if widget.id is not None:
            border_title = f"{border_title}#{widget.id}"
        if widget.classes:
            border_title = f"{border_title}.{'.'.join(widget.classes)}"
    widget.border_title = border_title
    return widget


class QuerySandboxApp(App[None]):
    """A Textual CSS query sandbox application."""

    CSS = """
    Input {
        width: 1fr;
    }

    #input {
        height: 4;
    }

    Playground * {
        margin: 1;
        border: panel red 40%;
    }

    .hit {
        border: panel green;
        background: green 10%;
    }

    VerticalScroll {
        margin-top: 1;
        height: 1fr;
        border: panel cornflowerblue 60%;
        padding: 1;
    }

    VerticalScroll:focus {
        border: panel cornflowerblue;
    }

    #results {
        width: 3fr;
    }

    #tree {
        width: 2fr;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the DOM for the application."""
        with Horizontal(id="input"):
            yield Input()
            yield Button("Query")
        with Playground():
            with title(Vertical(id="one", classes="foo bar")):
                with title(Vertical(id="two")):
                    with title(Horizontal(id="three", classes="baz")):
                        for n in range(3):
                            yield title(
                                Vertical(id=f"three-{n}", classes=f"wibble wobble-{n}")
                            )
                    with title(Vertical(id="four")):
                        yield title(Vertical(id="innermost", classes="foo baz"))
        with Horizontal():
            with title(VerticalScroll(id="results"), "Query Results"):
                yield Pretty([])
            with title(VerticalScroll(id="tree"), "Playground DOM Tree"):
                yield Static("")

    def on_mount(self) -> None:
        self.query_one("#tree > Static", Static).update(self.query_one(Playground).tree)

    @on(Input.Submitted)
    @on(Button.Pressed)
    def do_query(self) -> None:
        """Perform the query and show the result."""
        self.query("Playground *").remove_class("hit")
        result: list[Widget] | Exception
        try:
            hits = self.query_one(Playground).query(self.query_one(Input).value)
            hits.add_class("hit")
            result = list(hits)
        except Exception as error:  # pylint:disable=broad-exception-caught
            result = error
        self.query_one("#results > Pretty", Pretty).update(result)
        self.query_one(Input).focus()


### sandbox.py ends here
