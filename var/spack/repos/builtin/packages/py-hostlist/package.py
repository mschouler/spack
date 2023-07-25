# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHostlist(PythonPackage):
    """Hostlist expands and collects LLNL hostlists."""

    homepage = "https://www.nsc.liu.se/~kent/python-hostlist/"
    pypi = "python-hostlist/python-hostlist-1.23.0.tar.gz"
    git = "https://github.com/LLNL/py-hostlist.git"

    version("master", branch="master")
    version("1.23.0", sha256="56e0156b501f792c078114f07324f34f37827041581ee5d1ffdce89cca533219")

    # build dependencies
    depends_on("py-setuptools", type=("build"))
