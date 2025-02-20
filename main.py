import tools
import logger
import streamClasses
import wget
import sys
import os

# Get M3U URL from environment variable
ipttvurl = os.getenv('TVEPISODES_M3U_URL')
if not ipttvurl:
    print("Warning: TVEPISODES_M3U_URL environment variable is not set - skipping TV episodes processing")

iptmovieurl = os.getenv('MOVIES_M3U_URL')
if not iptmovieurl:
    print("Warning: MOVIES_M3U_URL environment variable is not set - skipping movies processing")

# Create m3u directory if it doesn't exist
os.makedirs('m3u', exist_ok=True)

# Process movies if URL is provided
if iptmovieurl:
    print(wget.download(iptmovieurl, ('m3u/iptmovies.m3u')))
    apollomovies = streamClasses.rawStreamList('m3u/iptmovies.m3u')

# Process TV episodes if URL is provided
if ipttvurl:
    # Process base TV shows URL
    try:
        base_url = f"{ipttvurl}/"
        print(f"\nTrying to fetch TV shows from base URL: {base_url}")
        wget.download(base_url, 'm3u/apollotvshows-base.m3u')
        apollotvshows = streamClasses.rawStreamList('m3u/apollotvshows-base.m3u')
    except Exception as e:
        print(f"\nError with base TV shows URL: {str(e)}")
    
    # Process additional numbered TV show URLs
    for i in range(1, 21):  # 1 to 20
        try:
            url = f"{ipttvurl}/{i}"
            print(f"\nTrying to fetch additional TV shows from: {url}")
            wget.download(url, (f'm3u/apollotvshows-{i}.m3u'))
            apollolist = streamClasses.rawStreamList(f'm3u/apollotvshows-{i}.m3u')
        except Exception as e:
            print(f"\nNo additional TV shows found at index {i} or error occurred: {str(e)}")
            continue

