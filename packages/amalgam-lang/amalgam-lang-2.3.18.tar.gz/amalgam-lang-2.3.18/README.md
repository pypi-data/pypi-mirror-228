# Howso Amalgam Python API

This module loads an Amalgam library, and exposes an api for communicating to it.

## Setup

The default location for the Amalgam library files is _~/.howso/lib/dev/amlg/_ ie _~/.howso/lib/dev/amlg/amalgam.so_ for linux and _~/.howso/lib/dev/amlg/amalgam.dll for windows.

```python
return Amalgam(version='10.0.3', download=True, debug=True)
```

Setting version to 'latest' can be used to automatically update to the latest on every use.

## Versioning

Versioning will occur automatically.  Patch versions are the default, change the PR name suffix to MAJOR/MINOR to change the incremented version level.  Use the PR pipeline build to validate the resulting version.
