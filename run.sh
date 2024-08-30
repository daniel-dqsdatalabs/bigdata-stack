#!/bin/bash
set -ex

function create() {
  docker-compose up -d
}

function start() {
  docker-compose start 
}

function stop() {
  docker-compose stop 
}

function down() {
  docker-compose down 
}

function clean() {
  docker-compose down -v
}

if [ "$1" == "" ]; then
  start
else
  eval $1
fi