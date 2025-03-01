# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tandem(CMakePackage):
    """Tandem is a scientific software for SEAS modelling and for solving Poisson
    and linear elasticity problems. It implements the Symmetric Interior Penalty
    Galerkin (SIPG) method using unstructured simplicial meshes (triangle meshes
    in 2D, tetrahedral meshes in 3D)."""

    homepage = "https://tandem.readthedocs.io/en/latest/"
    git = "https://github.com/TEAR-ERC/tandem.git"
    version("main", branch="main", submodules=True)

    # we cannot use the tar.gz file because it does not contains submodules
    version("1.0", tag="v1.0", submodules=True)
    patch("fix_v1.0_compilation.diff", when="@1.0")

    maintainers("dmay23", "Thomas-Ulrich")
    variant("polynomial_degree", default="2")
    variant("domain_dimension", default="2", values=("2", "3"), multi=False)
    variant("min_quadrature_order", default="0")
    variant("libxsmm", default=False, description="installs libxsmm-generator")

    depends_on("mpi")
    depends_on("parmetis +int64 +shared")
    depends_on("metis +int64 +shared")
    depends_on("libxsmm@1.17 +generator", when="+libxsmm target=x86_64:")
    depends_on("lua@5.3.2:5.4.4")
    depends_on("eigen@3.4.0")
    depends_on("zlib@1.2.8:1.2.13")
    depends_on("petsc@3.14.6:3.18.5 +int64 +mumps +scalapack")
    depends_on("petsc@3.14.6:3.18.5 +int64 +mumps +scalapack +knl", when="target=skylake:")
    # see https://github.com/TEAR-ERC/tandem/issues/45
    conflicts("%intel")

    def cmake_args(self):
        args = [
            self.define_from_variant("DOMAIN_DIMENSION", "domain_dimension"),
            self.define_from_variant("POLYNOMIAL_DEGREE", "polynomial_degree"),
            self.define_from_variant("MIN_QUADRATURE_ORDER", "min_quadrature_order"),
        ]

        arch_dic = {}
        arch_dic["skylake"] = "skl"
        arch_dic["skylake_avx512"] = "skx"
        arch_dic["haswell"] = "hsw"
        arch_dic["sandybridge"] = "snb"
        arch_dic["zen2"] = "rome"
        arch_dic["zen"] = "naples"
        target = str(self.spec.target)

        if target in arch_dic:
            args.append("-DARCH=" + arch_dic[target])
        else:
            print(target, "not in arch list of tandem, using native")
            args.append("-DARCH=native")

        return args

    def install(self, spec, prefix):
        self.cmake(spec, prefix)
        self.build(spec, prefix)
        install_tree(self.build_directory, prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.app)
