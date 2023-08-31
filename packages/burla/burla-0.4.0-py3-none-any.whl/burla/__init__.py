from fire import Fire

# Imported here to avoid cyclic imports
_BURLA_SERVICE_URL = "https://service-v2.burla.dev"

# _BURLA_SERVICE_URL = "http://127.0.0.1:5000"
# _BURLA_SERVICE_URL = "https://burla-webservice-0-4-0-zqhes3whbq-uc.a.run.app"
# "https://burla-webservice-y66ufvpuua-uc.a.run.app"

from burla._auth import login, login_cmd as _login_cmd
from burla._remote_parallel_map import remote_parallel_map


def init_cli():
    Fire({"login": _login_cmd})
