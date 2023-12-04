from pathlib import Path

_USER_PATH = Path.home()  # os.path.expanduser('~')
WALLPAPER_SRC_PATH = _USER_PATH / (
    'AppData/Local/Packages/'
    'Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/'
    'LocalState/Assets'
)
_WALLPAPER_DST_FILE = Path('savepath.txt')


def _get_dst():
    if not _WALLPAPER_DST_FILE.exists():
        return _USER_PATH / 'Pictures'

    try:
        return Path(_WALLPAPER_DST_FILE.read_text(encoding='utf-8').strip())
    except Exception as e:
        print(e)
        exit(1)


WALLPAPER_DST_PATH = _get_dst()
if not WALLPAPER_DST_PATH.exists():
    WALLPAPER_DST_PATH.mkdir()
