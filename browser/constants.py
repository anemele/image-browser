from pathlib import Path

_USER_PATH = Path.home()  # os.path.expanduser('~')
WALLPAPER_SRC_PATH = _USER_PATH / (
    'AppData/Local/Packages/'
    'Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/'
    'LocalState/Assets'
)
_WALLPAPER_DST_FILE = 'savepath.txt'

try:
    with open(_WALLPAPER_DST_FILE, encoding='utf-8') as fp:
        WALLPAPER_DST_PATH = Path(fp.readline().strip())
    if not WALLPAPER_DST_PATH.exists():
        WALLPAPER_DST_PATH.mkdir()
except (FileNotFoundError, UnicodeDecodeError) as e:
    print(e)
    WALLPAPER_DST_PATH = _USER_PATH / 'Pictures'
