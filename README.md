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

Use Odoo shell:
start containers (odoo-ptvsd + proxy + mailhog + postgres)
Come inside container odoo-ptvsd and run:
./entrypoint.sh shell -d origin_odoo_12_2 # origin_odoo_12_2 is name of database to use the shell into
