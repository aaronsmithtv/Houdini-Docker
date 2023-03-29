# <img src="https://static.sidefx.com/images/apple-touch-icon.png" width="25" height="25" alt="Hbuild Logo"> Houdini-Docker
[![Aaron Smith's Personal Website](https://img.shields.io/badge/aaronsmith-.tv-blue?style=flat-square)](https://aaronsmith.tv)
![Docker Pulls](https://img.shields.io/docker/pulls/aaronsmithtv/hbuild)

## Houdini Production Build Docker Image

Houdini-Docker is a project that automatically builds and pushes Docker images for the latest production build of SideFX Houdini. This project ensures you always have an up-to-date Docker image for Houdini, making it easier to create and deploy containerized environments for your 3D graphics projects.

Whether you're new to Python, Docker, or Houdini, this README aims to provide you with friendly, helpful, and informative instructions to get you started with Hbuild.

## Table of Contents

- [Using Hbuild Images](#using-hbuild-images)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Using Hbuild Images

If you want to get started quickly with using Houdini-Docker images, follow these simple steps:

1. Ensure you have [Docker](https://www.docker.com/products/docker-desktop) installed on your system. 

2. Open a terminal (Command Prompt, PowerShell, or Terminal, depending on your operating system).

3. Pull the most recently generated Houdini image by running the following command:
    ```shell
    docker pull aaronsmithtv/hbuild:latest
    ```
4. To create and run a container from the pulled image, execute the following command:
    ```shell
    docker run -it --name houdini-container aaronsmithtv/hbuild:latest
    ```

5. Now, you can use Houdini within the container by running the appropriate command for your desired Houdini application, with a default `PATH` environment variable configured to allowing you to launch processes such as `hserver`, `hython`, or `sesinetd`.

6. When you're finished, exit the container by typing `exit` and pressing Enter.

## Features

- Automatically checks for the latest Houdini production build every day at midnight.
- Builds a Docker image with the latest Houdini build.
- Pushes the new image to Docker Hub with the build tag and as the latest image.

## Contributing

We welcome contributions to the Houdini-Docker project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

For any questions or discussions, please open an issue or contact the maintainers.

## License

This project is released under the [MIT License](LICENSE).