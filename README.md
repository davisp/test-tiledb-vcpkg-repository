Test Registry
===

This is a test of using vcpkg wiht TileDB.

Updating the Registry
---

If you have a copy of vcpkg cloned into `~/github/microsoft/vcpkg` you can
simply run the update command like such:

```bash
./update-registry.py ~/path/to/tiledb/vcpkg.json
```

If your clone of vcpkg is somewhere else on your filesystem, you can do run
the update command with an extra argument:

```bash
./update-registry.py --repo=path/to/vcpkg path/to/tiledb/vcpkg.json
```

After running `./update-registry.py`, take a look to make sure the diff looks
reasonable on what's being updated. Then you can just run:

```bash
git add ports/ versions/
git commit -m "Upgraded repository packages"
```
