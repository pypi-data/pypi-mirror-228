import click
import subprocess


@click.command()
@click.option(
    "--port",
    "-p",
    default=8501,
    type=int,
    required=False,
    help="Specify alternate port [default: 8501]",
)
@click.option(
    "--address",
    "-a",
    default="127.0.0.1",
    type=str,
    required=False,
    help="specify alternate bind address (default: 127.0.0.1)",
)
def main(port: int, address: str):
    subprocess.call(
        [
            "streamlit",
            "run",
            __file__.replace("s3_browser_cli/cli.py", "s3_browser/Welcome.py"),
            f"--server.port={port}",
            f"--server.address={address}",
            "--browser.gatherUsageStats=False",
        ]
    )


if __name__ == "__main__":
    main()
