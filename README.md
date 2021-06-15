# CMake Glob Performance

This is a Python script for testing CMake glob overhead on an N
file flat directory. It does the following:

1. Creates a CMake project with N sources, explicitly listed
2. Builds that project
3. Runs a no-op build on that project, records time spent
4. Repeats the above steps with a `CONFIGURE_DEPENDS` glob in
   place of the explicit list
5. Reports the difference

```shell
usage: test-glob.py [-h] [--generator GEN] [--source SOURCE] [--build BUILD] [-n N]

Test CMake glob performance

optional arguments:
  -h, --help       show this help message and exit
  --generator GEN  the CMake generator to use (e.g. Ninja)
  --source SOURCE  directory in which to place the test case
  --build BUILD    directory in which to build the test case
  -n N             number of files to create
```

See the GitHub Actions logs for some performance numbers. Below is a table
with some experiments I ran locally.

| GitHub User   | Disk                | Filesystem | OS               | Generator | N      | Time (s) |
| ------------- | ------------------- | ---------- | ---------------- | --------- | ------ | -------- |
| @alexreinking | SanDisk SDSSDHII    | ext4       | Ubuntu 20.04 LTS | Ninja     | 1000   | 0.0162   |
| @alexreinking | SanDisk SDSSDHII    | ext4       | Ubuntu 20.04 LTS | Ninja     | 10000  | 0.0594   |
| @alexreinking | SanDisk SDSSDHII    | ext4       | Ubuntu 20.04 LTS | Ninja     | 100000 | 0.4383   |
| @alexreinking | SanDisk SDSSDHII    | NTFS (3g)  | Ubuntu 20.04 LTS | Ninja     | 1000   | 0.1170   |
| @alexreinking | SanDisk SDSSDHII    | NTFS (3g)  | Ubuntu 20.04 LTS | Ninja     | 10000  | 1.1119   |
| @alexreinking | Samsung SSD 970 EVO | NTFS (3g)  | Ubuntu 20.04 LTS | Ninja     | 1000   | 0.1146   |
| @alexreinking | Samsung SSD 970 EVO | NTFS (3g)  | Ubuntu 20.04 LTS | Ninja     | 10000  | 1.4825   |


Open an issue with your own tests and reports and I'll add them to the table!

