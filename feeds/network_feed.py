# http://reflect-live1-lmctv.cablecast.tv//live/live.m3u8
# Need to parse the different bitrate streams
# gst-launch-1.0 http://reflect-live1-lmctv.cablecast.tv//live/CELL-496k-270p/CELL-496k-270p.m3u8 ! hlsdemux ! decodebin ! videoconvert !  ximagesink

# gst-launch-1.0 http://reflect-live1-lmctv.cablecast.tv//live/CELL-496k-270p/CELL-496k-270p.m3u8 ! hlsdemux name=demux demux. ! decodebin ! videoconvert ! ximagesink demux. ! decodebin ! audioconvert ! autoaudiosink
