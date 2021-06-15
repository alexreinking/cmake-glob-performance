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

| GitHub User     | Disk                | Filesystem | OS                 | Generator  | N      | Time (s) |
| --------------- | ------------------- | ---------- | ------------------ | ---------- | ------ | -------- |
| [@alexreinking] | Samsung SSD 970 EVO | ext4 (WSL) | Ubuntu 20.04 (WSL) | Ninja      | 1000   | 0.0069   |
| [@alexreinking] | SanDisk SDSSDHII    | ext4       | Ubuntu 20.04       | Ninja      | 1000   | 0.0162   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS       | Windows 10         | Ninja      | 1000   | 0.0364   |
| [@alexreinking] | Samsung SSD 970 EVO | ext4 (WSL) | Ubuntu 20.04 (WSL) | Ninja      | 10000  | 0.0481   |
| [@alexreinking] | SanDisk SDSSDHII    | ext4       | Ubuntu 20.04       | Ninja      | 10000  | 0.0594   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS       | Windows 10         | VS 2019    | 1000   | 0.0731   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS       | Windows 10         | Ninja      | 1000   | 0.0832   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS       | Windows 10         | VS 2019    | 1000   | 0.1012   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS (3g)  | Ubuntu 20.04       | Ninja      | 1000   | 0.1146   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS (3g)  | Ubuntu 20.04       | Ninja      | 1000   | 0.1170   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS (9p)  | Ubuntu 20.04 (WSL) | Ninja      | 100    | 0.2062   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS (9p)  | Ubuntu 20.04 (WSL) | Ninja      | 100    | 0.2268   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS       | Windows 10         | Ninja      | 10000  | 0.2743   |
| [@alexreinking] | Samsung SSD 970 EVO | ext4 (WSL) | Ubuntu 20.04 (WSL) | Ninja      | 100000 | 0.3712   |
| [@alexreinking] | SanDisk SDSSDHII    | ext4       | Ubuntu 20.04       | Ninja      | 100000 | 0.4383   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS       | Windows 10         | VS 2019    | 10000  | 0.4710   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS       | Windows 10         | Ninja      | 10000  | 0.5616   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS       | Windows 10         | VS 2019    | 10000  | 0.8158   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS (3g)  | Ubuntu 20.04       | Ninja      | 10000  | 1.1119   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS (3g)  | Ubuntu 20.04       | Ninja      | 10000  | 1.4825   |
| [@alexreinking] | SanDisk SDSSDHII    | NTFS (9p)  | Ubuntu 20.04 (WSL) | Ninja      | 1000   | 1.9585   |
| [@alexreinking] | Samsung SSD 970 EVO | NTFS (9p)  | Ubuntu 20.04 (WSL) | Ninja      | 1000   | 2.1879   |

Open a PR with your own tests and reports if you'd like to add them to the table!

[@alexreinking]: https://github.com/alexreinking
