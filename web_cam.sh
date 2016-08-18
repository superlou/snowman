#!/bin/bash
CONTROL_PIPE=/tmp/feed1-control-pipe
width=704
height=576
framerate='25/1'
which gst-launch-1.0 2>/dev/null 1>&2

gstlaunch=gst-launch-1.0
SHMSIZE='shm-size='`echo "$width * $height * 4 * 22"|bc`
MIXERFORMAT='video/x-raw, format=BGRA, pixel-aspect-ratio=1/1, interlace-mode=progressive'
SCALE='videoconvert ! videoscale ! videoconvert'

SRC='v4l2src device=/dev/video0 '
SHMOPTION="wait-for-connection=0 sync=true"
SHMSINK1="shmsink socket-path=$CONTROL_PIPE $SHMSIZE $SHMOPTION"
while true ; do
    # Remove the named pipe if it exist
    rm -f $CONTROL_PIPE
    $gstlaunch -v          \
        $SRC              !\
        $SCALE            !\
        "$MIXERFORMAT,width=$width, height=$height, framerate=$framerate" !\
        $SHMSINK1
    sleep 2
done
exit
