#####################################
########## Django settings ##########
#####################################
# See <https://docs.djangoproject.com/en/1.11/ref/settings/>
# for more info and help. If you are stuck, you can try Googling about
# Django - many of these settings below have external documentation about them.
#
# The settings listed here are of special interest in configuring the site.

# SECURITY WARNING: keep the secret key used in production secret!
# You may use <http://www.miniwebtool.com/django-secret-key-generator/>
# to generate this key.

SECRET_KEY = os.environ.get("SECRET_KEY", "")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "0") == "1"
HOST = os.environ.get("HOST", "")
ADDITIONAL_HOSTS = os.environ.get("ADDITIONAL_HOSTS", None)

# Uncomment and set to the domain names this site is intended to serve.
# You must do this once you set DEBUG to False.
ALLOWED_HOSTS = [HOST]
if ADDITIONAL_HOSTS:
    ALLOWED_HOSTS += ADDITIONAL_HOSTS.split(",")

# Optional apps that DMOJ can make use of.
INSTALLED_APPS += ()

# Caching. You can use memcached or redis instead.
# Documentation: <https://docs.djangoproject.com/en/1.11/topics/cache/>
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    }
}

# Your database credentials. Only MySQL is supported by DMOJ.
# Documentation: <https://docs.djangoproject.com/en/1.11/ref/databases/>
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("MYSQL_DATABASE", ""),
        "USER": os.environ.get("MYSQL_USER", ""),
        "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
        "HOST": os.environ.get("MYSQL_HOST", "db"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "sql_mode": "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION",
        },
    }
}

# Sessions.
# Documentation: <https://docs.djangoproject.com/en/1.11/topics/http/sessions/>
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Internationalization.
# Documentation: <https://docs.djangoproject.com/en/1.11/topics/i18n/>
LANGUAGE_CODE = "en-au"
DEFAULT_USER_TIME_ZONE = "Australia/Melbourne"
USE_I18N = True
USE_L10N = True
USE_TZ = True

## django-compressor settings, for speeding up page load times by minifying CSS and JavaScript files.
# Documentation: https://django-compressor.readthedocs.io/en/latest/
COMPRESS_OUTPUT_DIR = "cache"
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
STATICFILES_FINDERS += ("compressor.finders.CompressorFinder",)


#########################################
########## Email configuration ##########
#########################################
# See <https://docs.djangoproject.com/en/1.11/topics/email/#email-backends>
# for more documentation. You should follow the information there to define
# your email settings.

# Use this if you are just testing.
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_KEY", "")
AWS_SES_REGION_NAME = "ap-southeast-2"

EMAIL_BACKEND = "django_ses.SESBackend"
DEFAULT_FROM_EMAIL = "MonashAPS Judge <judge@monashaps.com>"

# To use Mailgun, uncomment this block.
# You will need to run `pip install django-mailgun` for to get `MailgunBackend`.
# EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
# MAILGUN_ACCESS_KEY = '<your Mailgun access key>'
# MAILGUN_SERVER_NAME = '<your Mailgun domain>'

# You can also use Sendgrid, with `pip install sendgrid-django`.
# EMAIL_BACKEND = 'sgbackend.SendGridBackend'
# SENDGRID_API_KEY = '<Your SendGrid API Key>'

# The DMOJ site is able to notify administrators of errors via email,
# if configured as shown below.

# A tuple of (name, email) pairs that specifies those who will be mailed
# when the server experiences an error when DEBUG = False.
ADMINS = ()

# The sender for the aforementioned emails.
SERVER_EMAIL = "MAPS Judge <judge@monashaps.com>"


##################################################
########### Static files configuration. ##########
##################################################
# See <https://docs.djangoproject.com/en/1.11/howto/static-files/>.

# Change this to somewhere more permanent., especially if you are using a
# webserver to serve the static files. This is the directory where all the
# static files DMOJ uses will be collected to.
# You must configure your webserver to serve this directory as /static/ in production.
STATIC_ROOT = "/assets/static/"

# URL to access static files.
STATIC_URL = "/static/"

# Uncomment to use hashed filenames with the cache framework.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

############################################
########## DMOJ-specific settings ##########
############################################

## DMOJ site display settings.
SITE_NAME = "MonashAPS Judge"
SITE_LONG_NAME = "Monash Algorithms and Problem Solving Team"
SITE_ADMIN_EMAIL = "admin@monashaps.com"
TERMS_OF_SERVICE_URL = None

## Bridge controls.
# The judge connection address and port; where the judges will connect to the site.
# You should change this to something your judges can actually connect to
# (e.g., a port that is unused and unblocked by a firewall).
BRIDGED_JUDGE_ADDRESS = [("bridged", 9999)]

# The bridged daemon bind address and port to communicate with the site.
BRIDGED_DJANGO_ADDRESS = [("bridged", 9998)]

## DMOJ features.
# Set to True to enable full-text searching for problems.
ENABLE_FTS = True

# Set of email providers to ban when a user registers, e.g., {'throwawaymail.com'}.
BAD_MAIL_PROVIDERS = set()

## Event server.
# Uncomment to enable live updating.
EVENT_DAEMON_USE = True

# Uncomment this section to use websocket/daemon.js included in the site.
# EVENT_DAEMON_POST = '<ws:// URL to post to>'

# If you are using the defaults from the guide, it is this:
EVENT_DAEMON_POST = "ws://wsevent:15101/"

# These are the publicly accessed interface configurations.
# They should match those used by the script.
EVENT_DAEMON_GET = "ws://{host}/event/".format(host=HOST)
EVENT_DAEMON_GET_SSL = "wss://{host}/event/".format(host=HOST)
EVENT_DAEMON_POLL = "/channels/"

# If you would like to use the AMQP-based event server from <https://github.com/DMOJ/event-server>,
# uncomment this section instead. This is more involved, and recommended to be done
# only after you have a working event server.
# EVENT_DAEMON_AMQP = '<amqp:// URL to connect to, including username and password>'
# EVENT_DAEMON_AMQP_EXCHANGE = '<AMQP exchange to use>'

## CDN control.
# Base URL for a copy of ace editor.
# Should contain ace.js, along with mode-*.js.
ACE_URL = "//cdnjs.cloudflare.com/ajax/libs/ace/1.2.3/"
JQUERY_JS = "//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js"
SELECT2_JS_URL = "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js"
SELECT2_CSS_URL = "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css"

# A map of Earth in Equirectangular projection, for timezone selection.
# Please try not to hotlink this poor site.
TIMEZONE_MAP = "http://naturalearth.springercarto.com/ne3_data/8192/textures/3_no_ice_clouds_8k.jpg"

## Camo (https://github.com/atmos/camo) usage.
# DMOJ_CAMO_URL = "<URL to your camo install>"
# DMOJ_CAMO_KEY = "<The CAMO_KEY environmental variable you used>"

# Domains to exclude from being camo'd.
# DMOJ_CAMO_EXCLUDE = ("https://dmoj.ml", "https://dmoj.ca")

# Set to True to use https when dealing with protocol-relative URLs.
# See <http://www.paulirish.com/2010/the-protocol-relative-url/> for what they are.
# DMOJ_CAMO_HTTPS = False

# HTTPS level. Affects <link rel='canonical'> elements generated.
# Set to 0 to make http URLs canonical.
# Set to 1 to make the currently used protocol canonical.
# Set to 2 to make https URLs canonical.
# DMOJ_HTTPS = 0

## PDF rendering settings.
# Directory to cache the PDF.
DMOJ_PDF_PROBLEM_CACHE = "/pdfcache"

# Path to use for nginx's X-Accel-Redirect feature.
# Should be an internal location mapped to the above directory.
DMOJ_PDF_PROBLEM_INTERNAL = "/pdfcache"

DMOJ_USER_DATA_DOWNLOAD = True
DMOJ_USER_DATA_CACHE = "/datacache"
DMOJ_USER_DATA_INTERNAL = "/datacache"

#############
## Mathoid ##
#############
# Documentation: https://github.com/wikimedia/mathoid
MATHOID_URL = "http://mathoid:10044"
MATHOID_CACHE_ROOT = "/cache/mathoid/"
MATHOID_CACHE_URL = "//{host}/mathoid/".format(host=HOST)

############
## Pdfoid ##
############

DMOJ_PDF_PDFOID_URL = "http://pdfoid:8888"

############
## Texoid ##
############

TEXOID_URL = "http://texoid:8888"
TEXOID_CACHE_ROOT = "/cache/texoid/"
TEXOID_CACHE_URL = "//{host}/texoid/".format(host=HOST)

## ======== Logging Settings ========
# Documentation: https://docs.djangoproject.com/en/1.9/ref/settings/#logging
#                https://docs.python.org/2/library/logging.config.html#logging-config-dictschema
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "format": "%(levelname)s %(asctime)s %(module)s %(message)s",
        },
        "simple": {
            "format": "%(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "file",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

## ======== Integration Settings ========
## Python Social Auth
# Documentation: https://python-social-auth.readthedocs.io/en/latest/
# You can define these to enable authentication through the following services.
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
# SOCIAL_AUTH_FACEBOOK_KEY = ''
# SOCIAL_AUTH_FACEBOOK_SECRET = ''
# SOCIAL_AUTH_GITHUB_SECURE_KEY = ''
# SOCIAL_AUTH_GITHUB_SECURE_SECRET = ''
# SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = ''
# SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = ''

## ======== Custom Configuration ========
# You may add whatever django configuration you would like here.
# Do try to keep it separate so you can quickly patch in new settings.

# Uncomment if you're using HTTPS to ensure CSRF and session cookies are
# sent only with an HTTPS connection.
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

REGISTRATION_OPEN = True
DMOJ_RATING_COLORS = True
X_FRAME_OPTIONS = "DENY"

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

DMOJ_PROBLEM_DATA_ROOT = "/problems/"

DMOJ_RESOURCES = "/assets/resources/"

MEDIA_ROOT = "/media/"
MEDIA_URL = "/media/"

# ======== Display scoreboards ========
# Standalone ICPC-style scoreboards for multi-division events, served at
# /scoreboard/<key> and driven by judge.views.live_scoreboard.
#
# Each entry groups the contests that run as divisions of one event. Add a new
# entry per year; the old ones keep working, so past boards stay linkable.
#
# The page deliberately ignores each contest's `scoreboard_visibility`, so it
# still works while the contest's own ranking page is hidden from entrants.
# Treat these URLs as public: anyone who has one can watch the live standings.
# The frozen results are the exception -- they are only ever sent to users who
# can edit every contest in the event.
#
# Full form, with the optional keys and their defaults:
#
#   'mcpc2026': {
#       'title': 'MCPC 2026',                       # heading on the page
#       'contests': ['mcpc2026-a', 'mcpc2026-b'],   # contest keys, in display order
#       'labels': {'mcpc2026-a': 'Division A'},     # defaults to the contest name
#       'freeze_minutes': 60,                       # final N minutes hidden
#       'poll_seconds': 20,                         # how often the board refreshes
#       'feed_limit': 120,                          # events kept in the sidebar feed
#       'preview_top_seconds': 4,                   # see below
#       'preview_scroll_seconds': 12,
#       'preview_bottom_seconds': 4,
#       'badges': ['mcpc-onsite', 'mcpc-first-year'],    # see below
#       'in_person_organization': 'mcpc-onsite',
#       'theme': 'olympics',                        # see below
#       'template': 'contest/live-scoreboard.html', # see below
#       'flags': '/media/flags/{username}.png',     # see below
#   },
#
# ---- The auto-preview ----
#
# The board does not rotate on its own; someone presses play. One cycle sits at
# the top of a division for `preview_top_seconds`, scrolls slowly to the bottom
# over `preview_scroll_seconds`, sits there for `preview_bottom_seconds`, then
# swaps to the next division. A division short enough to fit on screen skips
# the scroll. Set `preview_scroll_seconds` to 0 to never scroll at all.
#
# ---- Theming one event ----
#
# 'theme': names a template in the site's
#     `templates/contest/scoreboard-themes/` -- 'olympics' means
#     `olympics.html`. It is pulled into the page's <head> after the built-in
#     styles, so anything it declares wins: redeclare the :root custom
#     properties for a recolour, or write rules against the hooks the board
#     exposes (`body.theme-olympics`, `tr.rank-1|2|3`.
#
# 'template': swaps the whole page, for a theme that needs different markup as
#     well as different styling. Extend the default page and override only the
#     blocks that change (`base_styles`, `theme_styles`, `extra_head`,
#     `body_class`, `body_start`, `body_end`) rather than copying it.
#
# Both default to `MCPC_SCOREBOARD_THEME` / `MCPC_SCOREBOARD_TEMPLATE` below if
# those are set, which is how you would theme every event at once.
#
# ---- Flags ----
#
# 'flags': a URL pattern taking `{username}`, drawn as a small flag to the left
#     of each competitor's name. The board formats it per competitor and hands
#     it to the page; it never checks it, and the page drops an image that
#     fails to load, so a competitor with no file simply has no flag and a
#     half-finished set is not a broken board.
#
#     Defaults to `MCPC_SCOREBOARD_FLAGS` below. An event with neither shows no
#     flags at all, exactly as before.
#
# ---- Badges and the in-person toggle ----
#
# Who is in the hall is read from organisation membership, not from a list
# here, so it can be changed during the event from the admin site without a
# deploy or a restart. This file only names which organisations matter:
#
#   'badges': shown beside each competitor, in the order given. Each entry is
#       an organisation *slug*, or a dict for more control:
#
#           'badges': [
#               'mcpc-onsite',
#               {'organization': 'mcpc-first-year', 'label': '1st yr',
#                'color': '#8957e5'},
#           ],
#
#       The label defaults to the organisation's short name -- the field DMOJ
#       already uses to label users during contests.
#
#   'in_person_organization': the slug whose members are competing in the hall.
#       Setting it puts an All / In person toggle on the board, which re-ranks
#       among whoever is shown, so the in-person view reads 1, 2, 3 with no
#       gaps. Omit it and the toggle does not appear.
#
# A slug matching no organisation is skipped rather than fatal -- a typo should
# not take the hall display down mid-contest -- and is reported in the page
# footer for admins.
#
# To change who counts as in-person on the day, edit that organisation's
# membership in the admin site. Any staff user with permission to change
# organisations can do it, and the board picks it up on its next poll.
#
# Shorthand, when the defaults are fine:
#
#   'mcpc2026': ['mcpc2026-a', 'mcpc2026-b'],

MCPC_SCOREBOARDS = {
    # Points at the development fixture data from `./scripts/dev_seed`.
    "dev": {
        "title": "MCPC-Dev",
        "contests": ["devcon1", "devcon2"],
        "labels": {
            "devcon1": "Division B",
            "devcon2": "Division A",
        },
        # Organisations created by `./scripts/dev_seed`.
        "badges": [
            "dev-onsite",
            {"organization": "dev-beginner", "label": "Beginner", "color": "#1f6feb"},
        ],
        "in_person_organization": "dev-onsite",
        "theme": "olympics",
        "flags": "/static/scoreboard-flags/dev/{username}.svg",
    },
    # The real MCPC problem set
    "mcpc26": {
        "title": "MCPC 2026",
        "contests": ["mcpc2026diva", "mcpc2026divb"],
        "labels": {
            "diva": "Division A",
            "divb": "Division B",
        },
        # I don't think we'll use these, given national participation is through DMOJ, but if we want to!
        "badges": [
            "mcpc26-onsite",
            {
                "organization": "mcpc26-beginner",
                "label": "Beginner",
                "color": "#1f6feb",
            },
        ],
        "in_person_organization": "mcpc26-onsite",
        "theme": "olympics",
        # Flags will be hosted on jackson's personal site for easy participant changes
        "flags": "https://me.glipr.xyz/mcpc26/{username}.png",
    },
}

# Defaults applied to any event that does not override them.
# MCPC_SCOREBOARD_THEME = None       # theme every event, unless one opts out
# MCPC_SCOREBOARD_TEMPLATE = None    # defaults to 'contest/live-scoreboard.html'
# MCPC_SCOREBOARD_FLAGS = None       # e.g. '/media/flags/{username}.png'
MCPC_SCOREBOARD_FREEZE_MINUTES = 60
MCPC_SCOREBOARD_POLL_SECONDS = 20
MCPC_SCOREBOARD_FEED_LIMIT = 120
MCPC_SCOREBOARD_PREVIEW_TOP_SECONDS = 4
MCPC_SCOREBOARD_PREVIEW_SCROLL_SECONDS = 12
MCPC_SCOREBOARD_PREVIEW_BOTTOM_SECONDS = 4
