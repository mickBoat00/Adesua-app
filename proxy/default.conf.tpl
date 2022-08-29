server {
    listen ${LISTEN_PORT};

    location /media {
        alias /vol/media;
    }

    location / {
        uwsgi_pass ${APP_HOST}:${APP_PORT};
        include /etc/nginx/uwsgi_pass;
        client_max_body_size 10M;
    }
}