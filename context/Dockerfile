# clouderp/odoo
#
# VERSION       0.0.1


ARG ODOO_VERSION
ARG BUILD_FROM=cerp/odoo:testing-$ODOO_VERSION

# Root stage
FROM $BUILD_FROM

USER root
RUN pip3 install -U boto3 google-cloud-billing
USER odoo
