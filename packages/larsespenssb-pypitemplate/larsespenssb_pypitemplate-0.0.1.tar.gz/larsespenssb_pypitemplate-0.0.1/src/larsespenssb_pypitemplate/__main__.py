"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Larsespenssb Pypitemplate."""


if __name__ == "__main__":
    main(prog_name="larsespenssb-pypitemplate")  # pragma: no cover
