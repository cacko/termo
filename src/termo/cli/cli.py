import typer

cli = typer.Typer()


@cli.command()
def app():
    from termo import start
    start()