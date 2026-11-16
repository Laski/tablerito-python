import os

# development or production
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from tablerito.config_production import *
else:
    from tablerito.config_development import *

# Attachments up to 10 MB
ATTACHMENT_LIMIT = 10 * 1024 * 1024
