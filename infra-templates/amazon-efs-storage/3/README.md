# PastureStack Amazon EFS Storage

This infrastructure entry installs a global Amazon Elastic File System volume
driver on each managed host.

Existing filesystems are the safe default. Supply an `fsid` in the workload
volume options. Cloud provisioning is disabled unless an administrator
explicitly enables it while installing the infrastructure stack. Provisioning
requires an operator-selected subnet and security group; this driver does not
create a security group or add unrestricted NFS ingress.

IAM instance profiles are preferred. Static or temporary credentials are
optional compatibility inputs and remain visible to administrators through
container configuration, so use the narrowest practical permissions.

```yaml
version: '2'
services:
  app:
    image: example.invalid/application:v1.0.0
    volumes:
    - shared:/data
volumes:
  shared:
    driver: pasturestack-efs
    driver_opts:
      fsid: fs-0123456789abcdef0
      export: /
      mntOptions: vers=4.1
```
