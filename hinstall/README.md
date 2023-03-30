# <img src="https://static.sidefx.com/images/apple-touch-icon.png"  width="25" height="25" alt=""> Hbuild
[![Hbuild GitHub Repository](https://img.shields.io/badge/GitHub-Houdini--Docker-f06c00?style=flat-square&logo=github)](https://github.com/aaronsmithtv/houdini-docker)
 ![Docker Pulls](https://img.shields.io/docker/pulls/aaronsmithtv/hbuild)

Hbuild is the repository Houdini-Docker generated images. The images are based on `debian:11-slim`. Hbuild provides a complete, lightweight installation of [*Houdini*](https://www.sidefx.com/products/houdini/), a powerful 3D software by SideFX; You can use this image to run Houdini in a containerized environment, making it easy to set up and manage across various platforms and systems, and at a compressed size of ~2.09GB, it is significantly more portable than the average Houdini installation image of ~6.7GB. 

## Table of Contents

- [Image Tags](#image-tags)
- [Usage](#usage)
- [Quick Start](#quick-start)
- [Support](#support)
- [SideFX EULA](#sidefx-eula)

## Image Tags

- `aaronsmithtv/hbuild:19.5.*-base`
- `aaronsmithtv/hbuild:latest`

## Usage

To run a container with the latest Hbuild Houdini image, use the following command:

```shell
docker run -it --rm aaronsmithtv/hbuild:latest
```

## Quick Start

Once you have started the Docker container using Hbuild, you can quickly get started by running `hserver` (a local service that provides communication with a `sesinetd` license server) alongside `sesictrl` (a utility that interacts with `sesinetd` licenses).

You can optionally allow these services to access to your [*SideFX API credentials*](https://www.sidefx.com/oauth2/applications/).

```shell
hserver -C -S https://www.sidefx.com/license/sesinetd --clientid $SIDEFX_CLIENT --clientsecret $SIDEFX_SECRET
sesictrl ping --client-id $SIDEFX_CLIENT --client-secret $SIDEFX_SECRET
```

If the request is successful, you should eventually see a response indicating the length of time taken to get a response from the license server (Hserver may initially need to restart itself in order to update the credentials).

```shell
2023-03-28 18:15:39 houapi  | Pinging: 'https://www.sidefx.com/license/sesinetd'
2023-03-28 18:15:39 houapi  |   Successfully pinged. 
2023-03-28 18:15:39 houapi  | Total time 319.4ms
2023-03-28 18:15:39 houapi  |  Connect time 4.646ms
```

Feel free to customize the container by mounting local directories, exposing ports, or setting environment variables as needed.

## Support
This Docker image is provided as-is and is not officially supported by SideFX. If you have any questions, issues, or suggestions, please submit them through the appropriate channels.

- For questions or issues related to Houdini software, visit the [*SideFX Forums*](https://www.sidefx.com/forum/).
- For questions or issues related to this Docker image, you can open a new issue in the [Houdini-Docker GitHub repository](https://github.com/aaronsmithtv/houdini-docker) or email me at *aaron@aaronsmith.tv*.

## Contributing
Contributions to this project are welcome! Please feel free to submit a pull request or open an issue on the [Houdini-Docker GitHub repository](https://github.com/aaronsmithtv/houdini-docker).

## SideFX EULA
All Hbuild Docker images are built and distributed with and under the terms of the specified Houdini [*End User License Agreement (EULA)*](https://www.sidefx.com/legal/license-agreement/) date (as of October 13, 2021). You must be aware of the EULA terms and conditions when using this image. By using this image, you agree to abide by the terms and conditions of the Houdini EULA.
