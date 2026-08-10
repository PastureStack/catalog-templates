<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows 網路服務

此基礎架構堆疊會在每台符合條件的 Windows 主機安裝一組中繼資料服務與內部
DNS 服務。請先安裝 PastureStack Windows 容器網路，確保 `nat` 與
`transparent` 網路驅動程式已建立。

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher 1.6
生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

## 使用需求

- 相容於 Windows Server 2022，且具有 `io.rancher.host.os=windows` 相容標籤的主機。
- Windows 容器網路項目已安裝並啟用。
- 透明容器網路內可使用 `169.254.169.250` 與 `169.254.169.251` 連結本機位址。

兩個 Windows 執行檔均已通過交叉編譯與來源測試，並完成 PE 格式、映像內容、
授權檔案、公開下載及弱點報告檢查。由於目前沒有 Windows 主機完成端對端執行
驗證，此項目仍屬候選版本。
