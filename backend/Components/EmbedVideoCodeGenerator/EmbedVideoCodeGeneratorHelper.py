from urllib.parse import quote, urlparse

def generate_embed_code(video_url: str, width: int = 640, height: int = 360, autoplay: bool = False) -> str:
    safe_url = quote(video_url, safe='/:?=&')
    autoplay_str = "&autoplay=1" if autoplay else ""
    embed_src = f"{safe_url}{autoplay_str}"

    return f'<iframe width="{width}" height="{height}" src="{embed_src}" frameborder="0" allowfullscreen></iframe>'

def generate_markdown_embed(video_url: str, alt_text: str = "Video") -> str:
    safe_url = quote(video_url, safe='/:?=&')
    return f"![{alt_text}]({safe_url})"

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
    
def generate_js_player_embed(video_url: str, player_id: str = "video-player") -> str:
    """
    Generates an embeddable HTML+JS video player snippet.
    """
    safe_url = quote(video_url, safe='/:?=&')
    return f'''
<div id="{player_id}" style="width: 100%; max-width: 640px;">
  <video width="100%" height="auto" controls>
    <source src="{safe_url}" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>
'''

def generate_videojs_embed(video_url: str, width: int = 640, height: int = 360, player_id: str = "videojs-player") -> str:
    """
    Generates an embed code using the Video.js player.
    """
    safe_url = quote(video_url, safe='/:?=&')
    return f'''
<link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
<script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>

<video
  id="{player_id}"
  class="video-js vjs-default-skin"
  controls
  preload="auto"
  width="{width}"
  height="{height}"
  data-setup='{{}}'>
  <source src="{safe_url}" type="video/mp4" />
  <p class="vjs-no-js">
    To view this video please enable JavaScript, and consider upgrading to a web browser that
    <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
  </p>
</video>
'''