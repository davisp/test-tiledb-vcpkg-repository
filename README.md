Test Registry
===

I am playing with vpckg.

Importing an Existing Port
---

```bash
export VCPKG_ROOT=/path/to/vcpkg
cp ${VCPKG_ROOT}/ports/$name ports
# If the version directory doesn't yet exist, create a directory
# "versions/$X-" where $X is the first letter of the package name.
mkdir versions/X-
cp ${VCPKG_ROOT}/versions/X-/$name.json versions/X-/
git add . && git commit -m "Imported $name at versions $something"
```
