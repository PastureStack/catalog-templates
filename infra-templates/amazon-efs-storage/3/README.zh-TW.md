# PastureStack Amazon EFS 儲存空間

此基礎架構範本會在每台受管主機上安裝全域的 Amazon Elastic File
System 磁碟區驅動程式。

預設只使用既有檔案系統，這是較安全的設定。請在工作負載的磁碟區
選項中提供 `fsid`。除非管理者安裝此基礎架構堆疊時明確啟用，否則
不會建立雲端資源。啟用資源建立功能時，必須由管理者指定子網路與
安全性群組；此驅動程式不會建立安全性群組，也不會開放未受限制的
NFS 連入流量。

建議優先使用 IAM 執行個體設定檔。為了相容性，也可提供固定或臨時
登入資訊，但管理者仍能從容器設定中看到這些值，因此請授予最小必要
權限。

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
