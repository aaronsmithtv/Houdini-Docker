from os import environ


def actions_write_output(name: str, value: str):
    """
    Write to the GitHub actions $GITHUB_OUTPUT file
    """
    gh_output_env = environ.get("GITHUB_OUTPUT")
    if gh_output_env:
        with open(gh_output_env, "a") as fh:
            print(f"{name}={value}", file=fh)
