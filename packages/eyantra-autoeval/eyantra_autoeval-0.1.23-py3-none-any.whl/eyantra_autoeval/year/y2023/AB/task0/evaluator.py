"""
evaluator.py

This file is used to evaluate task 0 of AstroTinker Bot theme.

"""
# standard imports
import platform
import subprocess

# third-party imports
import distro
from eyantra_autoeval.utils.common import is_docker, run_shell_command
from rich.console import Console
from rich.prompt import Confirm

# AB Task 0 Evaluator Function
def evaluate():
    """
    Function Name : evaluate
    Arguments     : None
    Description   : Checks the platform information of participants and
                    evaluates them for theme suitability. It also calls
                    the bash script file to create submission zip file.

    """
    result = {}
    console = Console()
    with console.status("[bold green]Gathering data...") as status:
        console.print(f"[green]Gathering system information[/green]")
        distribution = {
            "machine": platform.machine(),
            "version": distro.version(best=True),
            "name": distro.name(),
        }
        result["distro"] = distribution

    # Warning Participants if they are not using recommend OS.
    self_os_declaration = False
    if (
        result["distro"]["name"] != "Ubuntu"
        or "22.04" not in result["distro"]["version"]
        or result["distro"]["machine"] != "x86_64"
    ):
        console.print(
            f"""You seem to be using [bold][blue]{result["distro"]["name"]} {result["distro"]["version"]} ({result["distro"]["machine"]}) on environment[/bold][/blue]. We only support [bold][blue]Ubuntu 22.04 on (x86_64) on baremetal or Windows with WSL[/bold][/blue]. You may continue to use the existing setup, and you shall not be penalized for the same. However, we’ll officially only support Ubuntu 22.04 as the OS of choice, and we won’t be to help you out with any installation related questions or software compatibility issues."""
        )
        self_os_declaration = Confirm.ask(
            "Do you accept to take ownership of your setup and not seek help from e-Yantra for the same?"
        )

    result["self-os-declaration"] = self_os_declaration

    with console.status("[bold green]Gathering data...") as status:
        console.print(f"[green]Gathering information on system packages[/green]")
        result["apt"] = {}
        result["apt"]["packages"] = {}
        packages = (
            subprocess.run(
                "apt list --installed",
                capture_output=True,
                shell=True,
            )
            .stdout.decode()
            .split("\n")
        )
        packages = packages[1:-1]
        packages = [p.split()[0:2] for p in packages]
        for i in packages:
            if (i[0] == 'gcc-riscv64-unknown-elf/jammy,now'):
                result["apt"]["packages"]["installed"] = i

        result["generate"] = True
        console.print(f"[bold][blue]Done!")

    return result
