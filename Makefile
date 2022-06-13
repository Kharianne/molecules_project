.POSIX:

TEMP_DIR = /tmp/molecules-tmp-dir

all: image-nginx image-app

image-nginx:
	podman build -f Containerfile.nginx -t molecule-nginx .

image-app:
	podman build -f Containerfile.app -t molecule-app .

run:
	mkdir $(TEMP_DIR)
	mkdir $(TEMP_DIR)/static
	mkdir $(TEMP_DIR)/images
	podman pod create -n molecules -p 127.0.0.1:8080:80
	podman run --pod molecules -d --name molecules-nginx \
		--mount type=bind,src=$(TEMP_DIR)/static,dst=/opt/molecules/static,Z \
		--mount type=bind,src=$(TEMP_DIR)/images,dst=/opt/molecules/images,Z \
		molecule-nginx
	podman run --pod molecules -d --name molecules-app \
		--mount type=bind,src=$${DB_PATH_HOST:?},dst=/run/db,Z \
		--mount type=bind,src=$(TEMP_DIR)/static,dst=/opt/molecules/static,Z \
		--mount type=bind,src=$(TEMP_DIR)/images,dst=/opt/molecules/images,Z \
		-e SECRET_KEY \
		-e DB_PATH=/run/db/db.sqlite3 \
		molecule-app

stop:
	podman pod rm -f molecules
	rm -rf $(TEMP_DIR)