# PastureStack NFS Storage

This infrastructure entry installs a global Docker volume driver for NFS
version 3 and version 4. Each managed volume uses a validated subdirectory of
the configured export base.

Data is retained when a volume is removed unless an operator explicitly selects
`purge`. Purging is restricted to the driver's validated, owned subdirectory.
A volume configured with a direct `host` and `export` reference is always
treated as externally managed and is never recursively deleted.

## Default configuration

Configure the NFS server, exported base directory, mount options, and protocol
version when the stack is installed. Workloads then reference the
`pasturestack-nfs` volume driver:

```yaml
version: '2'
services:
  app:
    image: example.invalid/application:v1.0.0
    volumes:
    - data:/data
volumes:
  data:
    driver: pasturestack-nfs
```

## Per-volume configuration

An individual volume may use a different NFS server and export base:

```yaml
volumes:
  data:
    driver: pasturestack-nfs
    driver_opts:
      host: nfs.internal.example
      exportBase: /exports/applications
      mntOptions: nfsvers=4,proto=tcp
      onRemove: retain
```

A direct `export` reference mounts the named export without creating a
subdirectory and always retains the underlying data.
