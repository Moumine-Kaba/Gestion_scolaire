# views/preload_cache.py
# Cache partagé simple entre Splash et Login

class _Cache:
    auth_manager = None   # rempli par le Splash
    error = None
    pil = {}              # ex: {'login_bg': PIL.Image, 'logo_40': PIL.Image, ...}

CACHE = _Cache()
