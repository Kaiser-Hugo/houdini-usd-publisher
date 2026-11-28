from core import *


def test_validate_asset_name():
	assert validate_asset_name("table")


def test_validate_asset_name_with_underscore():
	assert validate_asset_name("chaise_bar")


def test_validate_asset_name_empty():
	assert validate_asset_name("") is False


def test_validate_asset_name_with_uppercase():
	assert validate_asset_name("Table") is False


def test_validate_asset_name_with_space():
	assert validate_asset_name("ma table") is False


def test_parse_asset_name():
	assert parse_asset_name("table_v003.usd") == ("table", 3)


def test_parse_asset_name_invalid():
	assert parse_asset_name("") is None


def test_asset_dir(tmp_path):
	path= asset_dir(tmp_path, "props", "table")
	assert path == tmp_path / "assets" / "props" / "table"
	assert not path.exists()


def test_list_versions(tmp_path):
	assert list_versions(tmp_path, "table") == []


def test_list_versions_created(tmp_path):
	for version in [1, 2]:
		version_dir = tmp_path / f"v{version:03d}"
		version_dir.mkdir()
		(version_dir / f"table_v{version:03d}.usd").touch()


	versions = list_versions(tmp_path, "table")
	assert [v["version"] for v in versions] == [2, 1]


def test_next_version(tmp_path):
	assert next_version(tmp_path, "table") == 1


def test_next_version_created(tmp_path):
	for version in [1, 2]:
		version_dir = tmp_path / f"v{version:03d}"
		version_dir.mkdir()
		(version_dir / f"table_v{version:03d}.usd").touch()


	versions = next_version(tmp_path, "table")
	assert next_version(tmp_path, "table") == 3
