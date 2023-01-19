PORT=8003
SRC_DIR=pemdbok_service
IGNORE_MODELS=Session,AbstractBaseSession,AccessPermissions,ContentType,Permission,LogEntry,AbstractUser,AbstractBaseUser,PermissionsMixin,CaptchaStore,Group
LDBPW=swordfish
LDBUSER=pemdbok
LDB=pemdbok
LDBPORT = 3339

debug_serve:
	cd ${SRC_DIR} && ./manage.py runserver 0.0.0.0:${PORT}


models.png: ${SRC_DIR}/*/models.py Makefile
	 cd ${SRC_DIR} && ./manage.py graph_models core -X ${IGNORE_MODE:S} -a -g >../models.dot
	dot -Tpng -Gnewrank=true models.dot>models.png

shell:
	cd ${SRC_DIR} && ./manage.py shell

remote_db_shell:
	PGPASSFILE='./.pgpass' psql --set=sslmode=require

local_db_shell:
	mysql --user=${LDBUSER} --password=${LDBPW} --host=127.0.0.1 --port=${LDBPORT} ${LDB}
