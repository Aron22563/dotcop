
def load_manifest_dir(meta_directory):
    manifest_path = meta_directory / "manifests"
    manifest_path.mkdir(parents=True, exist_ok=True)
    return manifest_path
