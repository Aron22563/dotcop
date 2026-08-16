import yaml
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.utils.formatter import Formatter
from dotcop.utils.expand_path import expand_path_from_string
from dotcop.utils.exceptions.PackageIdentTripletInvalid import PackageIdentTripletInvalid
from dotcop.data.PackageDatabaseDAL import PackageDatabaseDAL
from dotcop.data.ConfigFileDAL import ConfigFileDAL
from dotcop.data.exceptions.LinkDestinationExists import LinkDestinationExists
from dotcop.data.exceptions.LinkSourceNotFound import LinkSourceNotFound
from dotcop.data.exceptions.MetadataKeyMissing import MetadataKeyMissing

class MetaDirDAL():
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def get_package_meta_path(self, package_name):
        package_folder = PackageDatabaseDAL().get_package_folder(package_name)
        package_path = ConfigFileDAL().get_package_path() / package_folder
        self._validate_package_meta_path(package_path)
        return package_path

    def get_package_metafile_path(self, package_name):
        package_path = self.get_package_meta_path(package_name)
        metafile_path = package_path / "metadata.yaml"
        self._validate_package_metafile_path(metafile_path)
        return metafile_path

    def get_package_files_dict(self, package_name):
        try:
            package_metadata = self._get_package_metadata(package_name)
        except YAMLError:
            self.logger.error("Package files list retrieval failed because of a parsing error in the metadata file")
            raise
        except FileNotFoundError:
            self.logger.error("Package files list retrieval failed because of a missing file or directory")
            raise
        except LinkDestinationExists:
            self.logger.error("Package files list retrieval failed because of an existing file that would cause an overwrite")
            raise
        except LinkSourceNotFound:
            self.logger.error("Package files list retrieval failed because of a missing source file")
            raise
        except PackageIdentTripletInvalid as e:
            self.logger.error("Package files list retrieval failed because of an invalid triplet in the metadata file")
            e.set_package_name(package_name)
            raise e
        adapted_files_section = self._adapt_package_files(package_name, package_metadata)
        return adapted_files_section

    def _adapt_package_files(self, package_name, package_metadata):
        meta_path = self.get_package_meta_path(package_name)
        files_dict = package_metadata['files']
        paths = []
        for pair in files_dict:
            src = expand_path_from_string(pair["from"])
            dst = expand_path_from_string(pair["to"])
            src_path = meta_path /"files"/ src
            if not src_path.is_file():
                self.logger.error("No file at link source found: %s", src_path)
                raise LinkSourceNotFound(src_path, "No file at link source found")
            dst_path = dst
            if dst_path.exists():
                self.logger.error("Existing file at link destination: %s", dst_path)
                raise LinkDestinationExists(dst_path, "Existing file at link destination")
            self.logger.info("Validated paths: %s -> %s", src_path, dst_path)
            paths.append((src, dst))
        return paths


    def _get_package_metadata(self, package_name):
        """
        Returns the content of metadata.yaml
        """
        metafile_path = self.get_package_metafile_path(package_name)
        try:
            with open(metafile_path, "r") as file:
                metadata = yaml.safe_load(file)
        except YAMLError:
            self.logger.error("Failed to parse metadata file at: %s", metafile_path)
            raise
        self._validate_metadata_file(package_name, metadata)
        return metadata

    def _validate_package_metafile_path(self, metafile_path):
        if not metafile_path.is_file():
            self.logger.error("Metadata file not found at: %s", metafile_path)
            raise FileNotFoundError()

    def _validate_package_meta_path(self, meta_path):
        if not meta_path.is_dir():
            self.logger.error("Meta directory not found at: %s", meta_path)
            raise FileNotFoundError()

    def _validate_package_setup(self, package_name):
        self.logger.info("Package validation triggered for: %s", package_name)
        package_folder = PackageDatabaseDAL().get_package_folder(package_name)
        package_path = ConfigFileDAL().get_package_path() / package_folder

        if not self.package_path.is_dir():
            self.logger.error("Package was not found at expected path: %s", self.package_path)
            raise FileNotFoundError()

        metadata_file_path = package_path / "metadata.yaml"
        if not metadata_file_path.is_file():
            self.logger.error("Metadata file not found in folder: %s", metadata_file_path)
            raise FileNotFoundError()

        files_folder_path = package_path / "files"
        if not files_folder_path.is_dir():
            self.logger.error("Files folder not found in: %s", files_folder_path)
            raise FileNotFoundError()

    def _validate_metadata_file(self, package_name, metadata):
        ident_triplet = metadata.copy()
        if "files" in ident_triplet:
            del ident_triplet['files']
        self._validate_identifying_triplet(ident_triplet)

        try:
            files_dict = metadata.copy()['files']
        except KeyError:
            exception_message = "Files section missing from package metadata file"
            self.logger.error(exception_message)
            raise MetadataKeyMissing('files', exception_message)
        meta_path = self.get_package_meta_path(package_name)
        self._validate_files_dict(meta_path, files_dict)

    def _validate_identifying_triplet(self, ident_triplet):
        try:
            Formatter().check_identifying_triplet(ident_triplet)
        except PackageIdentTripletInvalid:
            raise

    def _validate_files_dict(self, meta_path, files_dict):
        self.logger.warn("Files section validation")
        for pair in files_dict:
            src = expand_path_from_string(pair["from"])
            dst = expand_path_from_string(pair["to"])
            src_path = meta_path /"files"/ src
            if not src_path.is_file():
                self.logger.error("No file at link source found: %s", src_path)
                raise LinkSourceNotFound(src_path, "No file at link source found")
            dst_path = dst
            if dst_path.exists():
                self.logger.error("Existing file at link destination: %s", dst_path)
                raise LinkDestinationExists(dst_path, "Existing file at link destination")
