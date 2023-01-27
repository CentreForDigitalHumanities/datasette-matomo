from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-matomo" in installed_plugins


@pytest.mark.asyncio
async def test_plugin_is_configured(monkeypatch):
    matomo_server_url = "https://example.com/"
    matomo_site_id = "1"
    monkeypatch.setenv("DATASETTE_MATOMO_SERVER_URL", matomo_server_url)
    monkeypatch.setenv("DATASETTE_MATOMO_SITE_ID", matomo_site_id)
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/")
    assert '<script src="/-/matomo-tracking.js"' in response.text
    response = await datasette.client.get("/-/matomo-tracking.js")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plugin_is_not_configured(monkeypatch):
    # Without environment variables
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/")
    assert '<script src="/-/matomo-tracking.js"' not in response.text
