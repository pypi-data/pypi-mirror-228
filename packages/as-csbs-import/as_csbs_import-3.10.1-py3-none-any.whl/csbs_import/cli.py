from pprint import PrettyPrinter
from typing import Optional

from pathlib import Path

import requests
import requests_file
import rfc3986
import typer

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .lib import DEFAULT_OPA_URL, DEFAULT_DATA_URL_FMT
from .lib import get_operational_areas, get_operational_area_details
from .generator import generate_opa_code
from .version import version


def check_config():
    if not Path("pyproject.toml").exists():
        print("Cannot find pyproject.toml of target python package")
        return

    with open("pyproject.toml", "rb") as pf:
        config = tomllib.load(pf)

    try:
        section = config["tool"]["csbs"]
    except KeyError:
        print("Cannot find tool.csbs section in pyproject.toml")
        return

    for key in ["area", "output_path"]:
        try:
            area = section[key]
        except KeyError:
            print(f"Cannot find key '{key}', which is required.")
            return

    for key in ["area_device_registry", "area_mock_registry", 
                "component_factory", "mixins_import"]:
        try:
            output = section[key]
        except KeyError:
            print(f"Cannot find key '{key}', which is optional.")

    return section

app = typer.Typer(add_completion=False)


def url_validator(url: str) -> str:
    if not rfc3986.is_valid_uri(url, require_scheme=True):
        raise typer.BadParameter("URL required.")
    return url


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"csbs-import: {version()}")
        raise typer.Exit()


@app.command()
def main(
    opa_url: Optional[str] = typer.Option(
        DEFAULT_OPA_URL,
        metavar="URL",
        callback=url_validator,
        help="Use an absolute file:// URL to load a file.",
    ),
    data_url: Optional[str] = typer.Option(
        DEFAULT_DATA_URL_FMT,
        metavar="URL",
        callback=url_validator,
        help="Use an absolute file:// URL to load a file.",
    ),
    dump_area: Optional[bool] = typer.Option(
        None, "--dump-area", help="For debugging, dump data for an area."
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show version and exit."
    ),
) -> None:
    sess = requests.Session()
    sess.mount("file://", requests_file.FileAdapter())

    config = check_config()
    if not config:
        raise typer.Exit()

    print("Verifying area...", end='', flush=True)
    area = config["area"]
    opas = get_operational_areas(sess, opa_url)
    for opa in opas:
        if opa.shortname == area:
            break
    else:
        print(f"Unknown area: {area}")
        raise typer.Abort()
    print("done.")

    data_url = data_url.format(area=opa.csbsid)

    print(f'Downloading data "{data_url}", can take thirty seconds...', end='', flush=True)

    get_operational_area_details(opa, sess, data_url)
    print("done")


    if dump_area:
        pp = PrettyPrinter(indent=0, width=200)
        pp.pprint(opa)
        raise typer.Exit()

    generate_opa_code(opa, config)


def run() -> None:
    app()


if __name__ == "__main__":
    app()
