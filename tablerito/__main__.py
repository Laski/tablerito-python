import os
import signal

from waitress import serve

from tablerito.app import create_app

signal.signal(signal.SIGTERM, lambda *args: os._exit(0))

serve(create_app(), host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
