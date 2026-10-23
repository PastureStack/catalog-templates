# PastureStack Amazon EBS Storage

This infrastructure entry installs a global Amazon Elastic Block Store volume
driver on each managed host.

Existing volumes are the safe default. Supply a `volumeID` in the workload
volume options. Cloud provisioning is disabled unless an administrator
explicitly enables it while installing the infrastructure stack. When enabled,
new volumes are encrypted by default and the driver may create, format, detach,
and delete resources according to the volume lifecycle.

IAM instance profiles are preferred. Static or temporary credentials are
optional compatibility inputs and remain visible to administrators through
container configuration, so use the narrowest practical permissions.

```yaml
version: '2'
services:
  app:
    image: example.invalid/application:v1.0.0
    volumes:
    - data:/data
volumes:
  data:
    driver: pasturestack-ebs
    driver_opts:
      volumeID: vol-0123456789abcdef0
      fs-type: ext4
```
