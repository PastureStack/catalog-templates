# PastureStack Vault 存取權杖磁碟區

此基礎架構項目會安裝一個非特權的環境橋接服務，並在每台符合條件的受管
主機安裝一個主機本機 Docker 磁碟區驅動程式。工作負載提出允許的存取
政策集合後，驅動程式會以主機身分金鑰簽署要求；橋接服務先確認主機仍為
作用中，再向 Vault 申請短效且經回應封裝的子權杖。

橋接服務使用既有的平台機密資料，其中包含一個可續期且權限範圍最小化的
發行用權杖。該機密資料以唯讀方式掛載，並由檔案讀取；不會寫入 Compose
環境值、命令列參數、健康狀態回應或日誌。

## Vault 事前準備

建立一個權杖角色，將其允許的存取政策限制在本環境內的應用程式。接著
建立一個可續期的發行用權杖；該權杖只能透過此角色建立子權杖及撤銷其
Accessor。請將權杖存入平台機密資料，並在安裝本卡片時選取該機密資料。
子權杖與回應封裝的存留時間均應保持精簡。

商店允許清單是額外的安全界線：工作負載提出的政策必須是安裝時所填半形
逗號分隔政策的子集合。

## 工作負載使用方式

```yaml
version: '2'
services:
  application:
    image: example/application:v1.0.0
    volumes:
    - vault-token:/run/vault:ro

volumes:
  vault-token:
    driver: pasturestack-vault-volume
    driver_opts:
      io.pasturestack.vault.policies: default,application
      io.pasturestack.vault.file: token
      io.pasturestack.vault.uid: '1000'
      io.pasturestack.vault.gid: '1000'
      io.pasturestack.vault.mode: '0400'
    per_container: true
```

檔案內存放的是回應封裝權杖，不是發行用權杖或已解封裝的子權杖。應用程式
透過 Vault API 解封裝一次即可使用。最後一個工作負載使用者釋放磁碟區後，
驅動程式會要求橋接服務撤銷子權杖 Accessor，並清除記憶體磁碟區。

## 安全界線

橋接服務使用
`ghcr.io/pasturestack/vault-secrets-bridge:v0.1.1`。程序以 UID 65532
執行、移除全部 Linux capabilities、使用唯讀根檔案系統，且只在專用狀態
磁碟區保存加密後的 Accessor 紀錄。

驅動程式使用
`ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.0`。程序先移除全部
capabilities，再僅加入隔離 `tmpfs` 生命週期及指定唯讀擁有權所需的
`SYS_ADMIN`、`CHOWN` 與 `FOWNER`。它不使用特權模式、主機網路、主機
PID 命名空間或容器引擎 Socket。

兩個映像皆可公開取得；商店與使用者介面只顯示語意版本標籤。映像資訊摘要
僅保留於發行驗證證據，不會顯示為部署座標。

原始碼、安全性說明、授權與發行證據請參閱
[Vault 機密資料橋接服務](https://github.com/PastureStack/vault-secrets-bridge)
及
[機密資料磁碟區驅動程式](https://github.com/PastureStack/secrets-flexvolume-plugin)。

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher
1.6 生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。
