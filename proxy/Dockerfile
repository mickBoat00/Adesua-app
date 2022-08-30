FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="m.boateng0000@gmail.com"

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]