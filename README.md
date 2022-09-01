Convert dependencies in csproj C# project files to NuGet format.

In project directory:

    $ python3 ~/path/to/csproj2json.py > packages.config
    $ trivy fs packages.config
