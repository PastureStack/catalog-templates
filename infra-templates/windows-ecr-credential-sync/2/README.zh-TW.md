<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows ECR 登入資訊同步

此基礎架構堆疊會從相容的 Windows 環境定期更新 Amazon Elastic Container
Registry 的短效登入資訊，而且只會排程至具有
`io.rancher.host.os=windows` 相容標籤的主機。

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher 1.6
生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

## 使用需求

- 相容於 Windows Server 2022 的容器主機。
- 可要求 ECR 授權權杖且權限範圍最小化的 AWS 登入資訊。
- 選擇其他環境時，必須提供該環境範圍的 API 登入資訊。

Catalog 使用 `v3.1.2-windows-ltsc2022` 語意版本標籤，不會在使用者看得到的
Compose 定義中放入映像摘要。此項目的來源、Windows 執行檔格式、映像內容、
授權檔案、公開下載及弱點掃描均已檢查；目前尚未取得 Windows 主機完成端對端
執行驗證，因此仍屬候選版本。
