# PastureStack Route 53 DNS 紀錄同步

> PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher
> 1.6 生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

此基礎架構範本會把相容環境的服務位址同步到既有的 Amazon Route 53
託管區域。

- 映像：`ghcr.io/pasturestack/external-dns-sync:v0.8.0`
- 原始碼：
  [`PastureStack/external-dns-sync@v0.8.0`](https://github.com/PastureStack/external-dns-sync/tree/v0.8.0)
- 上游：
  [`rancher-archives/external-dns`](https://github.com/rancher-archives/external-dns)

映像一律使用語意化版本標籤。公開商店資訊不顯示映像摘要，以免過長的
摘要文字破壞舊版服務介面；不可變更的映像識別資料會另行保留在發布
驗證證據中。

## DNS 行為

預設 A 紀錄名稱如下：

```text
<服務>.<堆疊>.<環境>.<託管區域>
```

服務也會維護一筆所有權 TXT 紀錄，並利用該紀錄只更新或移除自己建立
的 A 紀錄，不會管理託管區域內其他既有紀錄。

相容控制平面會透過代理程式角色協定注入環境範圍的 API 登入資訊。
執行環境會把這些值映射到中性的 PastureStack API 契約。若環境使用
私有憑證授權單位，可選擇以唯讀方式掛載經審核的主機 CA 檔案。

## AWS 權限

建議優先使用 IAM 角色。若必須使用存取金鑰，請建立專用金鑰，並把
權限限制在此堆疊使用的託管區域。最低 API 權限如下：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:GetHostedZone",
        "route53:GetHostedZoneCount",
        "route53:ListHostedZonesByName",
        "route53:ListResourceRecordSets"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "route53:ChangeResourceRecordSets",
      "Resource": "arn:aws:route53:::hostedzone/<HOSTED_ZONE_ID>"
    }
  ]
}
```

請以選取的區域識別碼取代 `<HOSTED_ZONE_ID>`。請勿提交登入資訊，
也不要把登入資訊放入問題回報、螢幕擷取畫面或診斷日誌。

## 升級相容性

中性的 PastureStack DNS 政策標籤具有較高優先順序。執行環境仍會
讀取四個已記錄的歷史服務與主機標籤，確保既有工作負載就地升級時保留
DNS 政策。精確且有範圍限制的協定介面請參閱執行專案的
`COMPATIBILITY.md`。

同一組環境與託管區域只能由一個執行中的 DNS 同步服務管理。從
0.6 以前版本升級並變更 TTL 時，請先完成執行環境升級，再以第二次
操作變更 TTL。

## 執行界線

容器以 UID/GID `10001:10001` 執行，不使用特權模式、主機網路、
Docker Socket 或可寫入的主機儲存空間。會感知相依服務狀態的健康
端點只在容器連接埠 `10000` 提供。

範本採 MIT 授權。External DNS Sync 保留 Apache-2.0 授權，隨附
相依套件保留各自的授權及聲明。原始碼儲存庫保留上游 Git 歷史及
作者資訊。
