# bazel build on copr

This is the rpm spec for generating rpm and/or src.rpm to build [bazel](https://bazel.build/).
The resulting builds can be found on https://copr.fedorainfracloud.org/coprs/vbatts/bazel/.

## build it yourself

### Building in a fedora/centos container:

* produce a src.rpm, for use on your own copr, or build system, or even then:

```shell
make container.rebuild
```

* get a bash cli in the target build environment

```shell
make container.run
```

* kick of a build on [copr](https://copr.fedorainfracloud.org/coprs/vbatts/bazel/)

```shell
make container.copr
```

### Building on the target Fedora or Centos Host:

* build the source RPM

```shell
make srpm
```

* produce a src.rpm, for use on your own copr, or build system, or even then:

```shell
rpmbuild --rebuild ...src.rpm
```

* If you are building local, just:

```shell
make rpm
```

* kick of a build on [copr](https://copr.fedorainfracloud.org/coprs/vbatts/bazel/)

```shell
make copr
```

which builds through to the binary rpm.


## Major versions

This git repo, `master` will track my latest iteration on the build.
But as upstream bazel have an aggressive release cycle for major version with breaking changes, there will be a corresponding branch.

Likewise, the package name will track the major version (i.e. `bazel2` rpm will be built for the `v2.y.z` upstream release)

## Prior versions

If you need a prior version than is found on the COPR repo, check out the [tagged releases](https://github.com/vbatts/copr-build-bazel/releases).
(Whether downloading that source bundle or git checkout the tag)
