# m3u2strm-docker
Hi there, 
Been looking for a way to add VOD content from my IPTV service to Emby or Jellyfin, so rebuilt a docker container of a fork from the original m3u2strm python and made some updates.
Convert m3u files to strm files with the folder structure needed to use them in emby / jellfin etc
For TVshows it will append your base m3u_url with /X from 1-20 as most providers need more than one m3u file.

``docker run -d \
  --name m3u2STRM \
  -e MOVIES_M3U_URL={Your Movies M3U} \
  -e TVEPISODES_M3U_URL={Your TVEpisods M3U} \
  -e UPDATE_INTERVAL="0 */6 * * *" \
  -v /path/to/movies:/movieoutput \
  -v /path/to/Episodes:/TVEpisodesoutput \
  m3u2strm-docker:latest``

If the Movies and Episodes libraries are already set up in Emby/Jellyfin scanning library should add the content.

<a href="https://buymeacoffee.com/jamieeburgess" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
