# PastureStack NFS 儲存空間

此基礎架構範本會在每台受管主機上安裝支援 NFS 第 3 版與第 4 版的
全域 Docker 磁碟區驅動程式。每個受管磁碟區都使用已驗證、位於設定
匯出基底目錄下的子目錄。

移除磁碟區時預設保留資料；只有管理者明確選擇 `purge` 才會清除。
清除範圍只限於經驅動程式驗證且由驅動程式管理的子目錄。若磁碟區直接
指定 `host` 與 `export`，系統一律視為外部管理，不會遞迴刪除資料。

## 預設設定

安裝堆疊時請設定 NFS 伺服器、匯出基底目錄、掛載選項及協定版本。
工作負載即可引用 `pasturestack-nfs` 磁碟區驅動程式：

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

## 個別磁碟區設定

個別磁碟區可使用不同的 NFS 伺服器及匯出基底目錄：

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

直接指定 `export` 時，系統會直接掛載該匯出目錄，不會建立子目錄，
而且永遠保留底層資料。
