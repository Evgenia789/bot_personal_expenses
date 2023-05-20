#!/usr/bin/env bash

while true
do
  echo "Server start at " `date '+%Y-%m-%d %H:%M:%S'`
  docker-compose up -d --build 
  if [ $? -ne 0 ]; then
    echo "Server failed with exit code $?, restarting..."
  else
    echo "Server stopped at " `date '+%Y-%m-%d %H:%M:%S'`
  fi
  sleep 1
done