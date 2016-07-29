# nupkg-downloader
NuGet package downloader. It downloads the package and its dependencies recursively.

Sample:
```python
downloadNupkg('https://www.nuget.org/packages/NetTopologySuite/', r'e:\')
```

This is NuGet package downloader. It downloads the package and its dependencies recursively.
```cmd
usage: nupkg-cli.py nupkg_url [out_dir] [-h | --h]
```

Remark:
- *`nupkg_url`* can be an uri of the repository from [nuget](www.nuget.org) website; it can also be a txt file with following format:
```txt
https://www.nuget.org/packages/NetTopologySuite
https://www.nuget.org/packages/PdfSharp/1.32.3057
https://www.nuget.org/packages/Microsoft.SqlServer.Types
https://www.nuget.org/packages/System.Data.SQLite
https://www.nuget.org/packages/fleesharp/0.9.27-pre
https://www.nuget.org/packages/CS-Script.bin
```
