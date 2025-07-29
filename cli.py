# cli.py

from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem
from textual.reactive import reactive
from textual import events
from rich.text import Text

class MenuApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    menu_items = ["Dev Jokes", "Code Roaster", "Commit Therapist", "Exit"]
    selection = reactive(0)

    def compose(self) -> ComposeResult:
        yield Static(" DevFun\n\nWhat's your vibe today, dev?\n(Chaos? Jokes? Roasts? Pick your poison.)\n", id="title")
        self.list_view = ListView(
            *[ListItem(Static(f" {item}")) for item in self.menu_items]
        )
        yield self.list_view

    def on_mount(self) -> None:
        self.update_highlight()

    def on_key(self, event: events.Key) -> None:
        if event.key == "up":
            self.selection = (self.selection - 1) % len(self.menu_items)
        elif event.key == "down":
            self.selection = (self.selection + 1) % len(self.menu_items)
        elif event.key == "enter":
            self.handle_selection()
        self.update_highlight()

    def update_highlight(self) -> None:
        for i, item in enumerate(self.list_view.children):
            item.highlight = (i == self.selection)

    def handle_selection(self) -> None:
        selected = self.menu_items[self.selection]
        self.exit(message=f"\nYou selected: {selected}\n")

def run():
    MenuApp().run()
