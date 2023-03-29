import os
import hinstall.util.dlutils as hio
import logging

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    srv_build = {
        'download_url': os.environ.get('SIDEFX_DL_URL'),
        'filename': os.environ.get('SIDEFX_DL_NAME'),
        'hash': os.environ.get('SIDEFX_DL_HASH'),
    }

    hio.download_hou_file(dl_request=srv_build)

    hio.verify_hou_checksum(dl_request=srv_build)

    hio.extract_hou_tar(dl_request=srv_build)
