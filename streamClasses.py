import asyncio
import logger
import os
import re
import tools
class Movie(object):
  '''A class used to construct the Movie filename.

  :param title: The Title of the Movie (required)
  :type title: str.
  :param url: The url to the location of the stream (required)
  :type url: str.
  :param year: The Year the movie was made (optional)
  :type year: str.
  :param resolution: The resolution of the stream (optional)
  :type resolution: str.
  '''
  def __init__(self, title, url, year=None, resolution=None, language=None):
    self.title = title.strip()
    self.url = url
    self.year = year
    self.resolution = resolution
    self.language = language
    self.output_dir = '/movieoutput'  # Movies output directory

  def getFilename(self):
    '''Getter to get the filename for the stream file
    
    :returns: the fully constructed filename with type directory ea. "movies/The Longest Yard - 720p.strm"
    :rtype: str
    '''
    filestring = [self.title.replace(':','-').replace('*','_').replace('/','_').replace('?','')]
    if self.year:
      if self.year[0] == "(":
        filestring.append(self.year)
      else:
        self.year = "(" + self.year + ")"
        filestring.append(self.year)
    else:
      self.year = "A"
    if self.resolution:
      filestring.append(self.resolution)
    return os.path.join(self.output_dir, 'movies', self.title.replace(':','-').replace('*','_').replace('/','_').replace('?','') + ' - ' + self.year, ' - '.join(filestring) + ".strm")
  
  def makeStream(self):
    filename = self.getFilename()
    directory = os.path.dirname(filename)
    
    if not directory:
        print(f"Error: Invalid directory path generated for file {filename}")
        return
        
    # Create the directory if it doesn't exist
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Created/verified directory: {directory}")
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return
    
    # Create the STRM file
    try:
        tools.makeStrm(filename, self.url)
    except Exception as e:
        print(f"Error creating STRM file {filename}: {e}")
  
class TVEpisode(object):
  '''A class used to construct the TV filename.

  :param showtitle: The Title of the TVshow (required)
  :type showtitle: str.
  :param url: The url to the location of the stream (required)
  :type url: str.
  :param seasonnumber: The season number of this episode. (optional)
  :type seasonnumber: str
  :param episodenumber: The episode number of this episode. (optional)
  :type episodenumber: str
  :param resolution: The resolution of the stream (optional)
  :type resolution: str.
  :param year: The Year the show was made (optional)
  :type year: str.
  :param episodename: The name of the episode. (optional)
  :type episodename: str
  :param airdate: The date the show aired, for daily or nightly shows like news (optional)
  :type airdate: str
  '''
  def __init__(self, showtitle, url, seasonnumber=None, episodenumber=None ,resolution=None, language=None, episodename=None, airdate=None):
    self.showtitle = showtitle
    self.episodenumber = episodenumber
    self.seasonnumber = seasonnumber
    self.episodenumber = episodenumber
    self.url = url
    self.resolution = resolution
    self.language = language
    self.episodename = episodename
    self.airdate = airdate
    self.sXXeXX = "S" + str(self.seasonnumber) + "E" + str(self.episodenumber)
    self.output_dir = '/TVEpisodesoutput'  # TV Episodes output directory

  def getFilename(self):
    '''Getter to get the filename for the stream file
    
    :returns: the fully constructed filename with type directory ea. "tvshows/Star Trek the Next Generation - Season 02/Star Trek the Next Generation - S02E07 - The Borgs kill Picard - 1080p.strm"
    :rtype: str
    '''
    filestring = [self.showtitle.replace(':','-').replace('*','_').replace('/','_').replace('?','')]
    if self.airdate:
      filestring.append(self.airdate.strip())
    else:
      filestring.append(self.sXXeXX.strip())
    if self.episodename:
      filestring.append(self.episodename.strip())
    if self.language:
      filestring.append(self.language.strip())
    if self.resolution:
      filestring.append(self.resolution.strip())
    
    base_path = os.path.join(self.output_dir, 'tvshows', self.showtitle.strip().replace(':','-').replace('/','_').replace('*','_').replace('?',''))
    if self.seasonnumber:
      season_path = os.path.join(base_path, f"Season {str(self.seasonnumber.strip()).zfill(2)}")
      return os.path.join(season_path, ' - '.join(filestring).replace(':','-').replace('*','_') + ".strm")
    else:
      return os.path.join(base_path, ' - '.join(filestring).replace(':','-').replace('*','_') + ".strm")
  
  def makeStream(self):
    filename = self.getFilename()
    directory = os.path.dirname(filename)
    
    if not directory:
        print(f"Error: Invalid directory path generated for file {filename}")
        return
        
    # Create the directory if it doesn't exist
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Created/verified directory: {directory}")
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return
    
    # Create the STRM file
    try:
        tools.makeStrm(filename, self.url)
    except Exception as e:
        print(f"Error creating STRM file {filename}: {e}")

class rawStreamList(object):
  def __init__(self, filename):
    self.log = logger.Logger(__file__, log_level=logger.LogLevel.DEBUG)
    self.streams = {}
    self.filename = filename
    # Initialize counters for movies
    self.movie_success = 0
    self.movie_failed = 0
    self.movie_skipped = 0
    # Initialize counters for TV episodes
    self.tv_success = 0
    self.tv_failed = 0
    self.tv_skipped = 0
    self.readLines()
    self.parseLine()
    # Print summary after processing
    self.print_summary()

  def print_summary(self):
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    print("\nMOVIES:")
    print(f"  Successful: {self.movie_success}")
    print(f"  Failed: {self.movie_failed}")
    print(f"  Skipped: {self.movie_skipped}")
    print(f"  Total Processed: {self.movie_success + self.movie_failed + self.movie_skipped}")
    
    print("\nTV EPISODES:")
    print(f"  Successful: {self.tv_success}")
    print(f"  Failed: {self.tv_failed}")
    print(f"  Skipped: {self.tv_skipped}")
    print(f"  Total Processed: {self.tv_success + self.tv_failed + self.tv_skipped}")
    print("\n" + "="*50 + "\n")

  def readLines(self):
    self.lines = [line.rstrip('\n') for line in open(self.filename, encoding="utf8")]
    return len(self.lines)
 
  def parseLine(self):
    linenumber=0
    for j in range(len(self.lines)):
      numlines = len(self.lines)
      if linenumber >= numlines:
        return 0
      if not linenumber:
        linenumber = 0
      thisline = self.lines[linenumber]
      nextline = self.lines[linenumber + 1]
      firstline = re.compile('EXTM3U', re.IGNORECASE).search(thisline)
      if firstline:
        linenumber += 1
        continue
      if thisline[0] == "#" and nextline[0] == "#":
        if tools.verifyURL(self.lines[linenumber+2]):
          self.log.write_to_log(msg=' '.join(["raw stream found:", str(linenumber),'\n', ' '.join([thisline, nextline]),self.lines[linenumber+2]]))
          self.parseStream(' '.join([thisline, nextline]),self.lines[linenumber+2])
          linenumber += 3
          #self.parseLine(linenumber)
        else:
          self.log.write_to_log(msg=' '.join(['Error finding raw stream in linenumber:', str(linenumber),'\n', ' '.join(self.lines[linenumber:linenumber+2])]))
          linenumber += 1
          #self.parseLine(linenumber)
      elif tools.verifyURL(nextline):
        self.log.write_to_log(msg=' '.join(["raw stream found: ", str(linenumber),'\n', '\n'.join([thisline,nextline])]))
        self.parseStream(thisline, nextline)
        linenumber += 2
        #self.parseLine(linenumber)

  def parseStreamType(self, streaminfo):
    typematch = tools.tvgTypeMatch(streaminfo)
    ufcwwematch = tools.ufcwweMatch(streaminfo)
    if ufcwwematch:
      return 'live'
    if typematch:
      streamtype = tools.getResult(typematch)
      if streamtype == 'tvshows':
        return 'vodTV'
      if streamtype == 'movies':
        return 'vodMovie'
      if streamtype == 'live':
        return 'live'
    
    tvshowmatch = tools.sxxExxMatch(streaminfo)
    if tvshowmatch:
      return 'vodTV'
    
    airdatematch = tools.airDateMatch(streaminfo)
    if airdatematch:
      return 'vodTV'

    channelmatch = tools.tvgChannelMatch(streaminfo)
    if channelmatch:
      return 'live'
    
    logomatch = tools.tvgLogoMatch(streaminfo)
    if logomatch:
      return 'live'

    tvgnamematch = tools.tvgNameMatch(streaminfo)
    if tvgnamematch:
      if not tools.imdbCheck(tools.getResult(tvgnamematch)):
        return 'live'
    return 'vodMovie'


  def parseStream(self, streaminfo, streamURL):
    streamtype = self.parseStreamType(streaminfo)
    if streamtype == 'vodTV':
      self.parseVodTv(streaminfo, streamURL)
    elif streamtype == 'vodMovie':
      self.parseVodMovie(streaminfo, streamURL)
    else:
      self.parseLiveStream(streaminfo, streamURL)
  
  def parseVodTv(self, streaminfo, streamURL):
    # Get and validate title
    title = tools.infoMatch(streaminfo)
    if not title:
        print(f"Skipping: No title match found in stream info: {streaminfo}")
        self.tv_skipped += 1
        return
        
    title = tools.parseMovieInfo(title.group())
    if not title or not title.strip():
        print(f"Skipping: Empty or invalid title after parsing: {streaminfo}")
        self.tv_skipped += 1
        return
    
    # Clean the title
    title = title.strip()
    
    # Handle resolution
    resolution = tools.resolutionMatch(streaminfo)
    if resolution:
        resolution = tools.parseResolution(resolution)
        title = tools.stripResolution(title)
    
    # Parse episode information
    try:
        episodeinfo = tools.parseEpisode(title)
        if not episodeinfo:
            print(f"Skipping: Could not parse episode information from title: {title}")
            self.tv_skipped += 1
            return
            
        # Create episode based on info type
        if len(episodeinfo) == 3:
            showtitle = episodeinfo[0]
            if not showtitle or not showtitle.strip():
                print(f"Skipping: Empty show title after parsing: {title}")
                self.tv_skipped += 1
                return
                
            airdate = episodeinfo[2]
            episodename = episodeinfo[1]
            episode = TVEpisode(
                showtitle=showtitle.strip(),
                url=streamURL,
                resolution=resolution,
                episodename=episodename,
                airdate=airdate
            )
        else:
            showtitle = episodeinfo[0]
            if not showtitle or not showtitle.strip():
                print(f"Skipping: Empty show title after parsing: {title}")
                self.tv_skipped += 1
                return
                
            episodename = episodeinfo[1]
            seasonnumber = episodeinfo[2]
            episodenumber = episodeinfo[3]
            language = episodeinfo[4] if len(episodeinfo) > 4 else None
            
            # Validate season and episode numbers
            if not seasonnumber or not episodenumber:
                print(f"Skipping: Missing season or episode number: {title}")
                self.tv_skipped += 1
                return
                
            episode = TVEpisode(
                showtitle=showtitle.strip(),
                url=streamURL,
                seasonnumber=seasonnumber,
                episodenumber=episodenumber,
                resolution=resolution,
                language=language,
                episodename=episodename
            )
        
        print(f"Debug: Parsed TV Show - {episode.__dict__}")
        print(f"Debug: Generated filename: {episode.getFilename()}")
        episode.makeStream()
        self.tv_success += 1
        
    except Exception as e:
        print(f"Error processing TV episode: {str(e)}")
        print(f"Stream info: {streaminfo}")
        print(f"Title: {title}")
        self.tv_failed += 1
        return

  def parseLiveStream(self, streaminfo, streamURL):
    #print(streaminfo, "LIVETV")
    pass

  def parseVodMovie(self, streaminfo, streamURL):
    title = tools.parseMovieInfo(streaminfo)
    
    # Skip if title is empty, None, or just whitespace
    if not title or not title.strip():
        print(f"Skipping: Empty or invalid title found in stream info: {streaminfo}")
        self.movie_skipped += 1
        return
    
    # Clean the title
    title = title.strip()
    
    resolution = tools.resolutionMatch(streaminfo)
    if resolution:
        resolution = tools.parseResolution(resolution)
    
    year = tools.yearMatch(streaminfo)
    if year:
        title = tools.stripYear(title)
        year = year.group().strip()
    
    # Ensure title is a string and still valid after processing
    if not isinstance(title, str) or not title.strip():
        print(f"Skipping: Invalid title after processing: {title}")
        self.movie_skipped += 1
        return
    
    language = tools.languageMatch(title)
    if language:
        title = tools.stripLanguage(title)
        language = language.group().strip()
    
    # Final check to ensure title is still valid after all processing
    if not title.strip():
        print(f"Skipping: Title became empty after processing")
        self.movie_skipped += 1
        return
    
    try:
        moviestream = Movie(title, streamURL, year=year, resolution=resolution, language=language)
        print(f"Debug: Parsed movie - {{'title': '{title}', 'url': '{streamURL}', 'year': '{year}', 'resolution': {resolution}, 'language': {language}'}}") # Debug line
        moviestream.makeStream()  # Actually create the STRM file
        self.movie_success += 1
    except Exception as e:
        print(f"Error creating movie: {str(e)}")
        print(f"Stream info: {streaminfo}")
        print(f"Title: {title}")
        self.movie_failed += 1
        return






