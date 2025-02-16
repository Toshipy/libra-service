### Cloudflared tunnel
```
brew install cloudflared
cloudflared tunnel --url http://localhost:9200
```

### デプロイ
```
serverless deploy --verbose
```
### デプロイ情報を確認
``` 
serverless info
```
### ローカルで実行
```
serverless offline
```
### 直近のログを表示
serverless logs -f api

### リソースの削除
```
serverless remove --verbose
```
