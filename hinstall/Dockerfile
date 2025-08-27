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

# Install dependencies and clean up in single layer
RUN pip install --upgrade --no-cache-dir -r hinstall/requirements.txt && \
    pip cache purge

# Set the PYTHONPATH environment variable to include the hinstall directory
ENV PYTHONPATH=/code
RUN mkdir /houdini
RUN python3 hinstall/houinstall.py && \
    # Clean up after download/extraction
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /root/.cache && \
    find /code -name "*.pyc" -delete && \
    find /code -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# SECOND STAGE: Install Houdini
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
    x11-utils x11-xserver-utils \
    libgl1-mesa-dev libglu1-mesa-dev \
    libgomp1 libglvnd0 \
    xvfb \
    ca-certificates && \
    # Clean up package manager cache and temp files
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/* /var/tmp/* && \
    update-ca-certificates

COPY --from=houdini-downloader /houdini /houdiniInstaller

# Please update the following EULA_DATE to match the latest updated
# date of EULA in yyyy-mm-dd format. E.g. "2020-05-05"
# For Houdini 18.0 and previous versions, EULA_DATE should be left empty
ARG EULA_DATE="2021-10-13"
# Force progress on all optional queries
RUN yes | /houdiniInstaller/build/houdini.install --auto-install --accept-EULA ${EULA_DATE} --make-dir /opt/houdini/build && \
    rm -rf /houdiniInstaller && \
    rm -rf /tmp/* /var/tmp/*

# THIRD STAGE: Final image
FROM debian:12-slim
COPY --from=houdini-install / /

# Add houdini bins to path env variable
ENV PATH="${PATH}:/opt/houdini/build/houdini/sbin:/opt/houdini/build/bin"

# POCL installation (OpenCL 1.2)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ocl-icd-libopencl1 ocl-icd-opencl-dev pocl-opencl-icd opencl-headers clinfo \
    libhwloc-dev libtinfo5 libpocl2 && \
    # Clean up after install
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/* /var/tmp/* && \
    # Create OpenCL vendor configuration
    mkdir -p /etc/OpenCL/vendors && \
    echo "libpocl.so" > /etc/OpenCL/vendors/pocl.icd
