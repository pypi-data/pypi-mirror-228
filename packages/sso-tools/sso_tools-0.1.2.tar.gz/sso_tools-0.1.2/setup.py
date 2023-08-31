from setuptools import setup, find_packages


setup(
    name="sso_tools",
    version="0.1.2",
    description="OAuth2 인증을 위한 도구",
    author="lee-lou2",
    author_email="lee@lou2.kr",
    url="https://github.com/lee-lou2/sso-tools",
    install_requires=["requests"],
    packages=find_packages(exclude=[]),
    keywords=["sso", "oauth2"],
    python_requires=">=3.6",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
