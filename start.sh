#!/bin/bash

if [[ "$PATH" =~ "^/www/server/pyporject_evn/214WebServer_venv/bin:.*" ]]; then
    echo "虚拟环境已就绪！"
else
    export PATH="/www/server/pyporject_evn/214WebServer_venv/bin:${PATH}"
    echo "虚拟环境已就绪！"
fi

export DJANGO_SETTINGS_MODULE=214web.settings
daphne -p 8080 214web.asgi:application -b 0.0.0.0