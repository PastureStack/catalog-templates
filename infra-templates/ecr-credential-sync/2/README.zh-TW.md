<!-- SPDX-License-Identifier: MIT -->

# PastureStack Amazon ECR 登入資訊同步 v3.1.0

此基礎架構服務會更新 Amazon Elastic Container Registry 提供的短效
Docker 登入資訊。服務啟動後會立即同步，之後每六小時同步一次。

## 已審核映像

- 映像：`ghcr.io/pasturestack/ecr-credential-sync:v3.1.0`
- 原始碼：
  [`PastureStack/ecr-credential-sync@v3.1.0`](https://github.com/PastureStack/ecr-credential-sync/tree/v3.1.0)
- 上游：
  [`rancher/rancher-ecr-credentials`](https://github.com/rancher/rancher-ecr-credentials)
- 原始碼採 Apache-2.0 授權；Ubuntu 與隨附的 Go 相依套件保留各自
  的上游授權及聲明。
- 執行身分：`10001:10001`
- Trivy 掃描結果為 HIGH 0、CRITICAL 0。
- 公開 GHCR 與未登入存取版本標籤的驗證已通過。

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher
1.6 生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

## 安全性界線

請使用環境範圍的 API 金鑰，並只授予呼叫 ECR 授權權杖 API 所需的
最小 AWS 權限。啟動表單會遮蔽密碼欄位，但部署後服務仍會從容器環境
變數取得這些值，因此必須限制堆疊、服務設定與主機執行環境的存取權限。

同步目前環境時，相容控制平面會透過 `io.rancher.*` 代理程式標籤及
歷史 `CATTLE_*` 變數注入環境 API 登入資訊。啟動命令會把這些相容
協定識別名稱映射到中性的 `PLATFORM_*` 執行契約。

共用 AWS 設定檔掛載預設為停用。啟用後，選取的主機目錄會以唯讀方式
掛載到 `/home/pasturestack/.aws`。服務不需要特權模式、主機網路、
Docker Socket，也不會存取該選用登入資訊目錄以外的主機檔案系統。

## 驗證與生命週期

此版本已通過啟用競爭偵測的單元測試、靜態分析、模擬 Amazon ECR
請求簽章、登錄與登入資訊建立／更新整合測試、健康狀態端點、非 root
執行、OCI 中繼資料、授權檔、弱點及機密資料掃描，以及隔離容器生命
週期測試。日誌檢查也確認不會洩漏 AWS、環境 API、授權權杖或角色
登入資訊。

需要回復時，請把此堆疊升級到先前已審核的商店修訂版與語意化映像
標籤。只移除這個元件建立的精確堆疊、服務及選用設定檔掛載，不需進行
大範圍主機清理。
