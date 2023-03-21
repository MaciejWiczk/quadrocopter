import click

from quadrocopter import check_quadrocopter_route, Radar, Point


@click.command()
@click.option(
    "-s",
    "--start",
    nargs=2,
    type=(int, int),
    required=True,
    help="Pass starting point as tuple[int, int] ie: -s 2,4 or --start 2,4",
)
@click.option(
    "-f",
    "--finish",
    nargs=2,
    type=(int, int),
    required=True,
    help="Pass finishing point as tuple[int, int] ie: -f 2,4 or --finish 2,4",
)
@click.option(
    "-r",
    "--radars",
    type=(int, int, int),
    multiple=True,
    required=True,
    help="Pass finishing point as tuple[int, int] ie: -f 2,4 or --finish 2,4",
)
def main(
    start: tuple[int, int],
    finish: tuple[int, int],
    radars: tuple[tuple[int, int, int]],
) -> None:
    """Entrypoint for quadrocopter application."""

    start = Point(*start)
    finish = Point(*finish)
    radars = [Radar(Point(radar[0], radar[1]), radar[2]) for radar in radars]

    if check_quadrocopter_route(start=start, finish=finish, radars=radars):
        click.echo("Route possible")
    else:
        click.echo("Route impossible")
