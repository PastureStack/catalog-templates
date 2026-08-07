# PastureStack Amazon EBS 儲存空間

此基礎架構範本會在每台受管主機上安裝全域的 Amazon Elastic Block
Store 磁碟區驅動程式。

預設只使用既有磁碟區，這是較安全的設定。請在工作負載的磁碟區選項
中提供 `volumeID`。除非管理者安裝此基礎架構堆疊時明確啟用，否則
不會建立雲端資源。啟用後，新建磁碟區預設會加密，驅動程式也能依照
磁碟區生命週期建立、格式化、卸離及刪除資源。

建議優先使用 IAM 執行個體設定檔。為了相容性，也可提供固定或臨時
登入資訊，但管理者仍能從容器設定中看到這些值，因此請授予最小必要
權限。

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
