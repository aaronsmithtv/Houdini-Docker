# FIRST STAGE: Download Houdini
FROM python:3.11-slim AS houdini-downloader
WORKDIR /code
COPY . ./hinstall
ARG DL_URL
ENV SIDEFX_DL_URL=$DL_URL
ARG DL_NAME
ENV SIDEFX_DL_NAME=$DL_NAME
ARG DL_HASH
ENV SIDEFX_DL_HASH=$DL_HASH
RUN pip install --upgrade --no-cache-dir -r hinstall/requirements.txt
# Set the PYTHONPATH environment variable to include the hinstall directory
ENV PYTHONPATH=/code
RUN mkdir /houdini
RUN python3 hinstall/houinstall.py

# SECOND STAGE: Install and initialize Houdini
FROM debian:12-slim as houdini-install

# Update and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    iputils-ping netcat-openbsd inetutils-telnet inetutils-ftp procps \
    libgl1 libglu1 libglx0 \
    libice6 libsm6 \
    libx11-6 libx11-xcb1 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libxcb1 \
    libxcomposite1 libxrender1 libxrandr2 libxcursor1 libxi6 libxtst6 \
    libxdamage1 libxext6 \
    libxss1 \
    libxkbcommon0 libxkbcommon-x11-0 \
    libfontconfig1 \
    libnss3 libpci3 libasound2 \
    bc wget \
    libqt5core5a libqt5gui5 libqt5widgets5 libqt5x11extras5 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
    libxcb-xinerama0 \
    x11-utils x11-xserver-utils \
    libgl1-mesa-dev libglu1-mesa-dev \
    libgomp1 libglvnd0 \
    xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=houdini-downloader /houdini /houdiniInstaller
# Please update the following EULA_DATE to match the latest updated
# date of EULA in yyyy-mm-dd format. E.g. "2020-05-05"
# For Houdini 18.0 and previous version, EULA_DATE should be left empty
ARG EULA_DATE="2021-10-13"
# Force progress on all optional queries
RUN yes | /houdiniInstaller/build/houdini.install --auto-install --accept-EULA ${EULA_DATE} --make-dir /opt/houdini/build
RUN rm -r /houdiniInstaller

# THIRD STAGE: Copy houdini-install image and un-cache unnecessary installation files
FROM debian:12-slim
COPY --from=houdini-install / /

RUN apt-get update && apt-get install -y ca-certificates
RUN update-ca-certificates

# OpenCL installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    ocl-icd-libopencl1 \
    ocl-icd-opencl-dev \
    clinfo \
    mesa-opencl-icd \
    pocl-opencl-icd \
    opencl-headers \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/OpenCL/vendors && \
    echo "libpocl.so" > /etc/OpenCL/vendors/pocl.icd

RUN clinfo
ENV OCL_ICD_VENDORS="/etc/OpenCL/vendors"

# Final environment assignments
ENV PATH="${PATH}:/opt/houdini/build/houdini/sbin:/opt/houdini/build/bin"
ENV HOUDINI_OCL_DEVICETYPE="CPU"
ENV DISPLAY=:99