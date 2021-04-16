#!/bin/bash

set -Eeuo pipefail

export ADDONS_PATH=$(python3.7 /opt/odoo/odoo12/scripts/parse_project.py)

# check connection with database
python3.7 /opt/odoo/odoo12/scripts/wait_for_psql.py \
    --db_host=${DB_HOST} \
    --db_port=${DB_PORT} \
    --db_user=${DB_USER} \
    --db_password=${DB_PASSWORD} \
    --timeout 30

# Implemented command options
if [ "$#" -eq 0 ] || [ "${1:0:1}" = '-' ]; then
	set -- run "$@"
fi

CMD=( "$@" )
ODOO_CMD=("/opt/odoo/odoo12/vendor/odoo/cc/odoo/odoo-bin")
SETTINGS=(
    "--config"
    "/opt/odoo/odoo12/odoo.conf"
    "--db_host"
    "${DB_HOST}"
    "--db_password"
    "${DB_PASSWORD}"
    "--db_user"
    "${DB_USER}"
    "--db_port"
    "${DB_PORT}"
    "--longpolling-port"
    "${LONGPOLLING_PORT}"
    "--addons-path"
    "${ADDONS_PATH}"
)

PYTHON_RUN=("python3.7")

if [ "$1" = 'run' ]; then
	CMD=(
            "${PYTHON_RUN}"
            "${ODOO_CMD}"
            "${SETTINGS[@]}"
            "${CMD[@]:1}"
        )
fi

if [ "$1" = 'gevent' ]; then
	CMD=(
            "${PYTHON_RUN}"
            "${ODOO_CMD}"
            "gevent"
            "${SETTINGS[@]}"
            "${CMD[@]:1}"
        )
fi

if [ "$1" = 'shell' ]; then
    CMD=(
            "${PYTHON_RUN}"
            "${ODOO_CMD}"
            "shell"
            "${SETTINGS[@]}"
            "${CMD[@]:1}"
        )
fi

if [ "$1" = 'ptvsd' ]; then
    PTVSD_ARGS=("-m ptvsd --host 0.0.0.0 --port 6899 --wait --multiprocess")
    CMD=(
            "${PYTHON_RUN}"
            "${PTVSD_ARGS}"
            "${ODOO_CMD}"
            "${SETTINGS[@]}"
            "--workers"
            "0"
            "${CMD[@]:1}"
        )
fi

${CMD[@]}

exit 1
