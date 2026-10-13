"""Settings behaviour: env-driven and fail-fast on missing variables."""

import pytest
from pydantic import ValidationError

from src.config import Settings


def test_settings_load_from_environment() -> None:
    settings = Settings()

    assert settings.secret_key == "test-secret"
    assert settings.database_url.startswith("postgresql+asyncpg://")


def test_settings_fail_fast_naming_the_missing_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(ValidationError) as excinfo:
        Settings()

    assert "secret_key" in str(excinfo.value).lower()
