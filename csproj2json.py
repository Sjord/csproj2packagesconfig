import os
import os.path
from xml.dom import minidom
from collections import namedtuple

Dependency = namedtuple("Dependency", ["package", "version", "target"])


def get_csproj_paths(start="."):
    for root, dirs, files in os.walk(start):
        for f in files:
            if f.endswith(".csproj"):
                yield os.path.join(root, f)


def get_referenced_packages(csproj):
    tree = minidom.parse(csproj)

    try:
        target = tree.getElementsByTagName("TargetFramework")[0].firstChild.nodeValue
    except (IndexError, AttributeError):
        target = None

    refs = tree.getElementsByTagName("PackageReference")
    return [
        Dependency(n.getAttribute("Include"), n.getAttribute("Version"), target)
        for n in refs
    ]


def to_packages_config(refs):
    doc = minidom.getDOMImplementation().createDocument(None, "packages", None)
    packages = doc.documentElement

    for ref in refs:
        package = doc.createElement("package")
        package.setAttribute("id", ref.package)
        package.setAttribute("version", ref.version)
        if ref.target is not None:
            package.setAttribute("targetFramework", ref.target)
        packages.appendChild(package)

    return doc.toxml()


projects = get_csproj_paths()
refs = []
for project in projects:
    refs += get_referenced_packages(project)
print(to_packages_config(refs))
