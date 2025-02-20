# m3u2strm-docker
convert m3u files to strm files with the folder structure needed to use them in emby / jellfin etc

Until I push to a docker repo you can build locally.

Git clone {repo URL}
cd m3u2strm
docker build -t m3u2strm .
docker run -d \
  --name m3u2STRM \
  -e MOVIES_M3U_URL={Your Movies M3U} \
  -e TVEPISODES_M3U_URL={Your TVEpisods M3U} \
  -e UPDATE_INTERVAL="0 */6 * * *" \
  -v /path/to/movies:/movieoutput \
  -v /path/to/Episodes/STRMS:/TVEpisodesoutput \
  m3u2strm

If the Movies and Episodes libraries are already set up in Emby/Jellyfin scanning library should add the content.
