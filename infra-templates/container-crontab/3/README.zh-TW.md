<!-- SPDX-License-Identifier: MIT -->

# 舊版 Container Crontab 第 3 版保留來源

此目錄的 `docker-compose.yml`、`rancher-compose.yml` 與英文 `README.md`
逐位元組保留自官方
[`rancher/rancher-catalog@52a5850bc49247eadd84045da890deaeaeddb9a4`](https://github.com/rancher/rancher-catalog/tree/52a5850bc49247eadd84045da890deaeaeddb9a4/infra-templates/container-crontab/3)
（`v1.6-release` 分支），用於既有安裝的版本讀回與正式升級回復。

其中 `rancher/container-crontab:v0.5.0` 是未重新驗證安全狀態的歷史映像，
不是新建安裝的預設映像，也不宣稱通過現行安全閘門。
相容項目不出現在新建目錄清單；新建安裝請使用 Container Schedule。

既有 `catalog://library:infra*container-crontab:3` 可透過唯讀相容解析，
使用正常的 Stack 升級進入第 4 版；升級確認前可使用正常 rollback 回復。
請參閱第 4 版的交接與驗收說明。
