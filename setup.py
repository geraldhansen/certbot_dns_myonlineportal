import setuptools

with open("Readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.0.1"

install_requires = [
    "acme>=0.29.0",
    "certbot>=0.34.0",
    "setuptools",
    "requests",
    "mock",
    "requests-mock",
]

setuptools.setup(
    name="certbot_dns_myonlineportal",
    version=version,
    author="geraldhansen",
    url="https://github.com/geraldhansen/certbot_dns_myonlineportal",
    description="Obtain certificates using a DNS TXT record for MyOnlinePortal.net domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration"
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-myonlineportal = certbot_dns_myonlineportal.dns_myonlineportal:Authenticator",
        ]
    }
)
