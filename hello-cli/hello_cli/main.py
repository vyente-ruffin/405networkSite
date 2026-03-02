"""Main entry point for the Hello CLI."""

import typer

app = typer.Typer()


@app.command()
def greet(name: str = "World") -> None:
    """Greet someone by name."""
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
