import shutil
import subprocess


def check_command(command):
    """
    Check if a Linux command exists.
    Example:
    nmap, git, tcpdump
    """

    return shutil.which(command) is not None



def install_package(package):

    print()
    print(f"SPOIL needs '{package}'")
    print()
    print("Install command:")
    print(f"sudo apt install {package} -y")
    print()


    answer = input(
        "Install now? (y/n): "
    ).strip().lower()


    if answer not in ["y", "yes"]:

        print(
            "Installation cancelled."
        )

        return False



    print()
    print(
        f"Installing {package}..."
    )
    print()


    try:

        result = subprocess.run(
            [
                "sudo",
                "apt",
                "install",
                package,
                "-y"
            ]
        )


        if result.returncode == 0:

            print()
            print(
                f"{package} installed successfully."
            )

            return True


        else:

            print()
            print(
                f"Failed installing {package}."
            )

            return False


    except KeyboardInterrupt:

        print(
            "\nInstallation interrupted."
        )

        return False
