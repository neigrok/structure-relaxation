FROM nginx:alpine

# Install envsubst
RUN apk add --no-cache gettext

COPY nginx.conf /etc/nginx/templates/default.conf.template

CMD ["/bin/sh", "-c", "envsubst '${FRONTEND_URL} ${BACKEND_URL} ${CONSTRUCTOR_APP_PREFIX}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
