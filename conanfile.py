from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import glob
import os


class NamedTypeConan(ConanFile):
    name = "namedtype"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/joboccara/NamedType"
    description = "Implementation of strong types in C++"
    topics = ("strong types")
    settings = "compiler"
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "5",
            "Visual Studio": "14",
            "clang": "3.4",
            "apple-clang": "5.1",
        }

    def configure(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 14)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if not minimum_version:
            self.output.warn("namedtype requires C++14. Your compiler is unknown. Assuming it supports C++14.")
        elif tools.Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration("namedtype requires C++14, which your compiler does not support.")

    def package_id(self):
        self.info.header_only()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob("NamedType-*")[0]
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        if self.version == "20190324":
            self.copy("*.hpp", dst=os.path.join("include", "NamedType"), src=self._source_subfolder)
        else:
            self.copy("*.hpp", dst="include", src=os.path.join(self._source_subfolder, "include"))
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
