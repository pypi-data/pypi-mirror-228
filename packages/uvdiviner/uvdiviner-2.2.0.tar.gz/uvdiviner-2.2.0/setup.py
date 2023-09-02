import uvdiviner
import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = "uvdiviner",
    version = uvdiviner.__version__,
    author = "Night Resurgent <fu050409@163.com>",
    author_email = "fu050409@163.com",
    description = "基于周易蓍草占卜原理实现的中国古占卜.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitee.com/unvisitor/diviner",
    project_urls = {
        "Bug Tracker": "https://gitee.com/unvisitor/diviner/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license = "Apache-2.0",
    packages = setuptools.find_packages(),
    install_requires = [
        'colorama'
    ],
    python_requires=">=3",
)