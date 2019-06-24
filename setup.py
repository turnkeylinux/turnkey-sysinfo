from distutils.core import setup

setup(
    name="turnkey-sysinfo",
    version="1.0",
    author="Stefan Davis",
    author_email="stefan@turnkeylinux.org",
    url="https://github.com/turnkeylinux/turnkey-sysinfo",
    packages=["libsysinfo"],
    scripts=["turnkey-sysinfo"]
)
