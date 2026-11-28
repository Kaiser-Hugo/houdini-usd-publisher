import re
from pathlib import Path
import json

NAME_PATTERN = r"[a-z_0-9]+"


def parse_asset_name(asset_name: str) -> tuple[str, int] | None:
	"""Split the asset name into (asset, version)."""
	split_name = re.fullmatch(rf"({NAME_PATTERN})_v(\d{{3}})\.usd", asset_name)
	if split_name is None:
		return None

	asset = split_name.group(1)
	version = int(split_name.group(2))
	return asset, version


def validate_asset_name(asset_name: str) -> bool :
	"""Checks if the asset name is valid"""
	match_asset_name = re.fullmatch(NAME_PATTERN, asset_name)
	return match_asset_name is not None



def asset_dir(root: Path, category: str, asset: str):
	"""Build path root/<assets>/category/<nom>"""
	asset_path = Path(root /"assets" /category / asset)
	return asset_path


def write_metadata(json_path: Path, metadata: dict) -> None:
	"""Write the metadata dict to a JSON file."""
	with json_path.open("w", encoding="utf-8") as f:
		json.dump(metadata, f, indent=4, ensure_ascii=False)


def read_metadata(json_path: Path) -> dict:
	"""Read metadata from a JSON file; return an empty dict if it does not exist."""
	if not json_path.exists():
		return {}
	try:
		with json_path.open("r", encoding="utf-8") as f:
			return json.load(f)
	except json.JSONDecodeError:
		return {}


def list_versions(publish_dir :Path, asset: str) -> list[dict]:
	"""List all versions of assets"""
	versions = []

	for file in publish_dir.glob("v*/*.usd"):
		parts = parse_asset_name(file.name)
		if parts is None:
			continue
		file_asset, file_version = parts
		if file_asset != asset:
			continue
		versions.append({
			"path": file,
			"version": file_version,
			"metadata": read_metadata(file.with_suffix(".json")),
		})
	return sorted(versions, key=lambda x: x["version"], reverse=True)

def next_version(folder :Path, asset: str):
	"""Get a free version of the asset"""
	version_list = list_versions(folder, asset)
	if len(version_list) == 0:
		return 1

	return version_list[0]["version"] +1


def version_paths():
	"""Return the usd and json version path"""

