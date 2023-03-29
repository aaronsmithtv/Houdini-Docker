# Using autobuild.py
### Creating daily Houdini Docker builds

`autobuild.py` is the script that runs an automated Houdini-API to Docker process, checking the SideFX website for new production builds, and subsequently pushing them to the directed Docker Hub repository.

The workflow described in `.github/workflows/houdocker_autobuild.yml` schedules a routine process to execute `autobuild.py`.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Troubleshooting](#troubleshooting)

## Prerequisites

To use this script, you'll need:

- A Docker Hub account to store the built images.
- SideFX API credentials to download Houdini builds.
- A GitHub account with access to GitHub Actions.

## Getting Started

1. Fork this repository to your GitHub account.

2. Go to your repository's **Settings** > **Secrets** and add the following secrets:

   - `SIDEFX_CLIENT`: Your SideFX API Client ID.
   - `SIDEFX_SECRET`: Your SideFX API Client Secret.
   - `DOCKER_USER`: Your Docker Hub username.
   - `DOCKER_SECRET`: Your Docker Hub access token or password.

3. The GitHub Actions workflow will now run daily at midnight, building and pushing the latest Houdini Docker image to your Docker Hub account.

4. *(Optional)* Execute the GitHub Action `workflow_dispatch` event trigger and create a Docker image from the latest Houdini production build.

Now that you have automated a Houdini to Docker workflow, you can use the images generated however you like.

1. Pull your image from Docker Hub:

    ```shell
    docker pull <your-docker-username>/hbuild:latest
    ```

2. Run your Docker container:

    ```shell
    docker run -it --rm <your-docker-username>/hbuild:latest
    ```


This command will launch an interactive session within the Houdini Docker container.

## Troubleshooting

If you encounter issues while setting up or using the project, try the following troubleshooting steps:

1. Check the GitHub Actions logs for any errors during the build process.
2. Ensure that your SideFX API credentials and Docker Hub credentials are correct and have the necessary permissions.
3. Verify that your Docker installation is up-to-date and functioning correctly.

If you still face issues, feel free to open an issue on the GitHub repository or email me at *aaron@aaronsmith.tv*.
