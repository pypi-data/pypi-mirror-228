# Scratch Websocket API
## Overview
このライブラリは、Websocketを通じてScratch（またはTurbowarp）に接続し、そのクラウド変数を変更するために作成されました。
## Installation
Python3が必須となります。Python2は使えないと思います。
```bash
pip install scratch-websocket-api
```
## Usage
```python
conn = login("yosshi---_Cloudvar", ".Cloudsession").connect(885712843, 2, True)
```