# cli.py
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Header, Footer, Static
from rich.text import Text

# Import the functions from your tools
from tools.dev_jokes import get_joke
from tools.code_roast import get_roast
from tools.commit_excuse import get_excuse
from tools.do_it_now import get_motivation

class DevFunApp(App):
    """A humorous, interactive terminal app for developers."""

    CSS_PATH = "cli.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("up", "cursor_up", "Cursor Up"),
        ("down", "cursor_down", "Cursor Down"),
        ("enter", "select_item", "Select / More"),
        ("escape", "show_menu", "Back to Menu"),
    ]

    def __init__(self):
        super().__init__()
        self.menu_items = ["Dev Jokes", "Code Roast", "Commit Excuse", "Do It Now!", "Exit"]
        self.current_selection = 0
        self.last_action = None
        self.actions = {
            "Dev Jokes": (get_joke, "bold cyan"),
            "Code Roast": (get_roast, "bold magenta"),
            "Commit Excuse": (get_excuse, "bold yellow"),
            "Do It Now!": (get_motivation, "bold green"),
        }

    def compose(self) -> ComposeResult:
        """Create the UI widgets for the app."""
        # Create a styled header with a tagline
        yield Header(show_clock=True, id="app-header")
        with Center():
            with Vertical(id="content-container"):
                yield Static("What would you like to do now!!\n(Anyhow, entertaining is my work 😎)", id="title")
                with Vertical(id="menu"):
                    for item in self.menu_items:
                        yield Static(item, classes="menu-item")
                yield Static(id="message-display", classes="message-box")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        # Set the header text after mounting
        self.query_one(Header).text = "DevFun - Your Daily Dose of Developer Humor"
        self.action_show_menu()
        self.update_highlight()

    def update_highlight(self) -> None:
        """Update the visual highlight on the current menu item."""
        for i, item in enumerate(self.query(".menu-item")):
            item.set_class(i == self.current_selection, "highlighted")

    def show_message_view(self, message: str, style: str):
        """Hides menu/title and shows only the message."""
        self.query_one("#title").display = False
        self.query_one("#menu").display = False
        message_display = self.query_one("#message-display")
        message_display.display = True
        
        prompt = "\n\n[dim](Press Enter for more, ESC for main menu)[/dim]"
        full_text = Text.from_markup(f"{message}{prompt}", style=style, justify="center")
        message_display.update(full_text)

    def action_show_menu(self) -> None:
        """Shows the main menu view."""
        self.query_one("#title").display = True
        self.query_one("#menu").display = True
        self.query_one("#message-display").display = False
        self.last_action = None
        self.update_highlight()

    def action_cursor_up(self) -> None:
        """Move the selection cursor up, only if the menu is visible."""
        if self.query_one("#menu").display:
            self.current_selection = (self.current_selection - 1) % len(self.menu_items)
            self.update_highlight()

    def action_cursor_down(self) -> None:
        """Move the selection cursor down, only if the menu is visible."""
        if self.query_one("#menu").display:
            self.current_selection = (self.current_selection + 1) % len(self.menu_items)
            self.update_highlight()

    def action_select_item(self) -> None:
        """Handles item selection from the menu OR gets another message."""
        if self.last_action:
            action_func, style = self.last_action
            new_message = action_func()
            self.show_message_view(new_message, style)
            return

        if self.query_one("#menu").display:
            selected_item = self.menu_items[self.current_selection]
            
            if selected_item == "Exit":
                self.exit()
                return

            if selected_item in self.actions:
                action_func, style = self.actions[selected_item]
                self.last_action = (action_func, style)
                message = action_func()
                self.show_message_view(message, style)

def run():
    """Run the application."""
    app = DevFunApp()
    app.run()
