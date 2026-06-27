from nyx_local.core import Settings


def test_settings_has_default_application_values() -> None:
    settings = Settings()

    assert settings.project_name == "Nyx Local"
    assert settings.version == "0.1.0"
    assert settings.debug is False
