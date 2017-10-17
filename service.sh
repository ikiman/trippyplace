#!/bin/bash

### BEGIN INIT INFO
# Provides: trippybot
# Required-Start: $docker
# Required-Stop:
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: TrippyBot
#
### END INIT INFO

USRCMD="exec su - dkr -c"
CMDBASE="/usr/local/bin/docker-compose -f /home/dkr/trippyplace/docker-compose.yml"

case "$1" in
  start)
    $USRCMD "$CMDBASE up -d"
    ;;
  stop)
    $USRCMD "$CMDBASE down"
    ;;
  restart)
    $USRCMD "$CMDBASE restart"
    ;;
  *)
  Echo "Usage: $0 {start | stop | restart}"
  exit 1
  ;;
esac

exit  0
