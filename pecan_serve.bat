#!/usr/bin/env bash

root_app = /pecanrest
root_api = /pecanrest/pecanrest/controllers
dir_app = pecanrest


echo
echo "[TOUCH] Possible missing __init__.py from ${root_api}"
touch "${root_api}/__init__.py"

echo "[PECAN SERVE] Pecan Service Launching ..."
pecan serve pecanrest/config.py
