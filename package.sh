#!/bin/bash

set -x

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly VENV="queue-scheduler/.venv"
readonly PYTHON="python3.9"
readonly ZIP_FILE="package.zip"
readonly SITE_PACKAGES=${VENV}/lib/${PYTHON}/site-packages

cd "${SCRIPT_DIR}"

${PYTHON} -m venv "${VENV}"
source "${VENV}/bin/activate"

pip3 install -r requirements.txt

pushd ${SITE_PACKAGES}
    zip -r -q ${SCRIPT_DIR}/queue-scheduler/${ZIP_FILE} . -x "/*__pycache__/*"
popd

zip -g "queue-scheduler/${ZIP_FILE}" index.py