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
    monkeypatch.setenv("MATOMO_SERVER_URL", "https://example.com/")
    monkeypatch.setenv("MATOMO_SITE_ID", "1")
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/")
    assert '<script src="/-/matomo-tracking.js"' in response.text
