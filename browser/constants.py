import os.path

_USER_PATH = os.path.expanduser('~')
WALLPAPER_SRC_PATH = os.path.join(
    _USER_PATH,
    'AppData/Local/Packages/'
    'Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/'
    'LocalState/Assets',
)
_WALLPAPER_DST_FILE = 'savepath.txt'

try:
    with open(_WALLPAPER_DST_FILE, encoding='utf-8') as fp:
        WALLPAPER_DST_PATH = fp.readline().strip()
    if not os.path.exists(WALLPAPER_DST_PATH):
        os.makedirs(WALLPAPER_DST_PATH)
except (FileNotFoundError, UnicodeDecodeError) as e:
    print(e)
    WALLPAPER_DST_PATH = os.path.join(_USER_PATH, 'Pictures')
