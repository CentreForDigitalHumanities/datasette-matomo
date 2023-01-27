import os
from string import Template
import sys

from datasette import hookimpl, Response


def get_extra_js():
    # NOTE: storing the env variables and extra_js list in global variables does not work
    # Using startup() hookimpl does not seem to help either.
    extra_js = []
    ds_matomo_server_url = os.environ.get('DATASETTE_MATOMO_SERVER_URL', "<not set>")
    ds_matomo_site_id = os.environ.get('DATASETTE_MATOMO_SITE_ID', "<not set>")
    if any(i in ['<not set>', ''] for i in [ds_matomo_server_url, ds_matomo_site_id]):
        print('Warning: datasette-matomo configuration not defined', file=sys.stderr)
    if ds_matomo_server_url.endswith('/') is False:
        print('Warning: DATASETTE_MATOMO_SERVER_URL should end with "/"', file=sys.stderr)
    else:
        extra_js = ["/-/matomo-tracking.js"]
    return extra_js


matomo_tracking_code_tmpl = Template("""
let _paq = window._paq = window._paq || [];
/* tracker methods like "setCustomDimension" should be called before "trackPageView" */
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
let u="$DATASETTE_MATOMO_SERVER_URL";
_paq.push(['setTrackerUrl', u+'matomo.php']);
_paq.push(['setSiteId', '$DATASETTE_MATOMO_SITE_ID']);
let d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
g.type='text/javascript'; g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
})();
""")

matomo_tracking_code = matomo_tracking_code_tmpl.substitute(
    DATASETTE_MATOMO_SERVER_URL=os.environ.get('DATASETTE_MATOMO_SERVER_URL', "<not set>"),
    DATASETTE_MATOMO_SITE_ID=os.environ.get('DATASETTE_MATOMO_SITE_ID', "<not set>"),
)


def get_matomo_tracking_code():
    response = Response(
        matomo_tracking_code,
        content_type="application/javascript",
    )
    return response


@hookimpl
def register_routes():
    return [("^/-/matomo-tracking.js$", get_matomo_tracking_code)]


@hookimpl
def extra_js_urls():
    return get_extra_js()
