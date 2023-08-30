import os
from socketserver import TCPServer
import webbrowser
from http.server import SimpleHTTPRequestHandler
import click

SERVE_DIR = f"{os.getcwd()}/target"


@click.command()
@click.option(
    "--port",
    type=click.INT,
    default=8088,
    help="Specify the port number for the documentation static server. Default is 8088",
)
@click.option(
    "--no-browser",
    is_flag=True,
    help="Specify whether you want to open a browser or not",
)
def serve(port, no_browser):
    os.chdir(SERVE_DIR)

    address = "0.0.0.0"

    httpd = TCPServer((address, port), SimpleHTTPRequestHandler)

    if not no_browser:
        try:
            webbrowser.open_new_tab(f"http://127.0.0.1:{port}")
        except webbrowser.Error:
            pass

    click.echo("Serving documentation")
    click.echo(f"Documentation is running at http://127.0.0.1:{port}")

    try:
        httpd.serve_forever()  # blocks
    finally:
        httpd.shutdown()
        httpd.server_close()
