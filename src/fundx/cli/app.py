"""Main CLI application."""

import typer

from fundx.cli.commands.analyze import analyze
from fundx.cli.commands.ratios_cmd import ratios
from fundx.cli.commands.search import search
from fundx.cli.commands.statements import statements

app = typer.Typer(
    name="fundx",
    help="Advanced fundamental analysis CLI tool for stocks.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

app.command("analyze", help="Full fundamental analysis")(analyze)
app.command("statements", help="Display financial statements")(statements)
app.command("ratios", help="Display financial ratios")(ratios)
app.command("search", help="Search tickers by company name")(search)


if __name__ == "__main__":
    app()
