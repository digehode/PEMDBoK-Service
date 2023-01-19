CWD = $(shell pwd)
PORT = 3339
CONTAINERNAME=pemdbox-service-db
DATADIR=data-pemdbok-service
PW=swordfish
USER=pemdbok
DB=pemdbok
ADMIN_PORT=89


serve:
	docker run  -p ${PORT}:3306 --name ${CONTAINERNAME} -v ${CWD}/${DATADIR}:/var/lib/mysql -v ${CWD}/scripts:/scripts -e MARIADB_ROOT_PASSWORD=${PW} -e MARIADB_USER=${USER} -e MARIADB_PASSWORD=${PW} -e MARIADB_ROOT_HOST=localhost -e MARIADB_DATABASE=${DB} -d mariadb:latest

connect:
	docker exec -it ${CONTAINERNAME} mysql -u root -p


shell:
	docker exec -it ${CONTAINERNAME} bash

initialise:
	docker exec -it ${CONTAINERNAME} sh /scripts/initialise.sh

clean:
	-docker kill ${CONTAINERNAME}
	-docker rm ${CONTAINERNAME}
	-sudo rm -rf ./${DATADIR}/*

admin_volume:
	docker volume create ${CONTAINERNAME}-admin-volume

admin:
	docker run --name ${CONTAINERNAME}-admin -v ${CONTAINERNAME}-admin-volume:/etc/phpmyadmin/config.user.inc.php --link ${CONTAINERNAME}:db -p ${ADMIN_PORT}:80 -d phpmyadmin/phpmyadmin
