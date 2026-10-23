<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows 容器網路

此基礎架構項目會定義相容 Windows 容器工作負載使用的 `nat` 與 `transparent`
Docker 網路驅動程式。請在 PastureStack Windows 網路服務之前安裝。

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher 1.6
生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

Compose 服務只用來選取既有 Windows 代理程式；相容服務結構雖然要求提供映像，
但不會將該映像當成 Windows 工作負載啟動。歷史選取值僅屬控制協定識別值，
不能在尚未同步更換 Windows 代理程式契約前單獨移除。

此範本已通過 Catalog Service 解析，並限制於 Windows 協調模式。由於目前沒有
Windows 主機完成網路驅動程式的端對端驗證，此項目仍屬候選版本。
