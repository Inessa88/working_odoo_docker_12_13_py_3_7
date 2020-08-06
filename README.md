# working_odoo_docker_12_13_py_3_7
git clone https://github.com/Inessa88/working_odoo_docker_12_13_py_3_7.git

cd working_odoo_docker_12_13_py_3_7

Create directory: mkdir -p vendor/odoo/cc

cd vendor/odoo/cc

git clone https://github.com/odoo/odoo.git

git checkout 12.0 OR git checkout 13.0

Return to main directory (working_odoo_docker_12_13_py_3_7): cd ../../../..

docker-compose up

ctrl + c

docker-compose up odoo-ptvsd

Start debagger in VScode (button)

Open in browser: odoo.localhost
