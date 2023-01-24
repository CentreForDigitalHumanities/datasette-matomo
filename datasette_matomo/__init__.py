import os
from string import Template

from datasette import hookimpl, Response


matomo_server_url = os.environ.get('MATOMO_SERVER_URL', "<not set>")
matomo_site_id = os.environ.get('MATOMO_SITE_ID', "<not set>")
matomo_tracking_code_tmpl = Template("""
let _paq = window._paq = window._paq || [];
/* tracker methods like "setCustomDimension" should be called before "trackPageView" */
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
let u="$MATOMO_SERVER_URL";
_paq.push(['setTrackerUrl', u+'matomo.php']);
_paq.push(['setSiteId', '$MATOMO_SITE_ID']);
let d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
g.type='text/javascript'; g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
})();
""")

matomo_tracking_code = matomo_tracking_code_tmpl.substitute(
    MATOMO_SERVER_URL=matomo_server_url,
    MATOMO_SITE_ID=matomo_site_id,
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
    return ["/-/matomo-tracking.js"]
