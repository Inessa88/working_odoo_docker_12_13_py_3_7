FROM debian:buster-slim

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
RUN set -x; \
        apt-get update \
        && apt-get upgrade -y \
        && apt-get install -y --no-install-recommends \
            ca-certificates \
            curl \
            dirmngr \
            fonts-noto-cjk \
            gnupg \
            libssl-dev \
            node-less \
            npm \
            python3-num2words \
            python3-pip \
            python3-phonenumbers \
            python3-pyldap \
            python3-qrcode \
            python3-renderpm \
            python3-setuptools \
            python3-slugify \
            python3-vobject \
            python3-watchdog \
            python3-xlrd \
            python3-xlwt \
            python3-dev \
            python3-wheel \
            python3-venv \
            python3-setuptools \
            xz-utils \
            build-essential \
            wget \
            libxslt-dev \
            libzip-dev \
            libldap2-dev \
            libsasl2-dev \
            node-less \
            zlib1g-dev \
            libncurses5-dev \
            libgdbm-dev \
            libnss3-dev \
            libssl-dev \
            libreadline-dev \
            libffi-dev \
            libpq-dev \
        && curl -O https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz \
        && tar -xf Python-3.7.2.tar.xz \
        && cd Python-3.7.2 \
        && ./configure --enable-optimizations \
        && make altinstall \
        && cd .. && rm -f Python-3.7.2.tar.xz \
        && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb \
        && echo '7e35a63f9db14f93ec7feeb0fce76b30c08f2057 wkhtmltox.deb' | sha1sum -c - \
        && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
        && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# install latest postgresql-client
RUN set -x; \
        echo 'deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main' > /etc/apt/sources.list.d/pgdg.list \
        && export GNUPGHOME="$(mktemp -d)" \
        && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
        && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
        && gpg --batch --armor --export "${repokey}" > /etc/apt/trusted.gpg.d/pgdg.gpg.asc \
        && gpgconf --kill all \
        && rm -rf "$GNUPGHOME" \
        && apt-get update  \
        && apt-get install -y postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# Install rtlcss (on Debian buster)
RUN set -x; \
    npm install -g rtlcss

RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo

COPY ./scripts/wait_for_psql.py /opt/odoo/odoo12/scripts/wait_for_psql.py
COPY ./requirements/ /opt/odoo/odoo12/requirements/
COPY ./scripts/parse_project.py /opt/odoo/odoo12/scripts/parse_project.py
COPY ./odoo_12/entrypoint.sh /entrypoint.sh

RUN chmod +x /opt/odoo/odoo12/scripts/parse_project.py

# Expose Odoo services
EXPOSE 8069 8072 8071

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8
# Set the default config file
ENV ODOO_RC /opt/odoo/odoo12/odoo.conf

# install requirements for python
RUN su - odoo \
    && export PROJECT_PATH=/opt/odoo/odoo12 \
    && python3.7 /opt/odoo/odoo12/scripts/parse_project.py get_command_for_install_requirements \
    && chmod +x /tmp/set_requirements.sh \
    && /tmp/set_requirements.sh \
    && rm /tmp/set_requirements.sh \
    && exit

RUN chmod +x /entrypoint.sh

RUN chown -R odoo /opt/odoo/odoo12/ \
    && mkdir -p /opt/odoo/.local/share/Odoo/ \
    && chown -R odoo /opt/odoo/.local/share/Odoo/

# # Set default user when running the container
USER odoo
