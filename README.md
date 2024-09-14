# WikiProject
## 概要
Wikiのようなページを作成、編集、閲覧できるWebアプリケーション。
AWSのサービスを利用してサーバーレスで構築されている。
フレームワークとして[had](https://github.com/h-akira/had)を用いている。
## 構築用メモ
### CloudFomationの管理外の部分
- S3バケット`hakira0627-wiki-stg`は手動で作成
- CloudFrontは`add.yaml`でCloudFomationにより作成されるが、それに伴いS3のバケットポリシーを手動で設定する必要がある
  - バケットポリシーの内容はマネジメントコンソールCloudFrontのページから取得できる
- CloudFrontは独自ドメインを用いるが、Route53のホストゾーンは別途作成してそこにレコードを登録する必要がある
- ACMで証明書も作成しておく必要がある（`add.yaml`中でarnが指定されている）
- API GatewayがCloudFront以外から直接アクセスされることを防ぐためにはAPI Gatewayに下記のリソースポリシーを手動で設定する
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:ap-northeast-1:アカウントのID:APIのID/*/*/*",
      "Condition": {
        "StringNotEquals": {
          "aws:Referer": "a22Gds3goG2"
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:ap-northeast-1:アカウントのID:APIのID/*/*/*"
    }
  ]
}
```
- API Gatewayのデプロイは手動で行う
    - CloudFrontのOriginPathを`add.yaml`で指定しているので、それに合わせてStage名はを`stage-01`にする必要がある
