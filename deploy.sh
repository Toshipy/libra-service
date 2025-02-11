#!/bin/bash
# デプロイ用の一時ディレクトリを作成
mkdir -p package
# 依存パッケージをインストール（packageディレクトリの中に直接インストール）
pip install -r requirements.txt -t package
# ソースコードをコピー
cp src/lambda_function.py package/
# ZIPファイルを作成
cd package && zip -r ../function.zip ./*
# クリーンアップ
cd .. && rm -rf package
