# ReCoBuTA

ReCoBuTA は **Re**mote **Co**ntrol **B**ot **u**sing **T**witter **A**PI の略です。Twitter の bot アカウントへのメンションを受け取り、登録済みユーザーからのコマンドを実行する Python スクリプトです。Twitter API クライアントとして [Tweepy](https://www.tweepy.org/) を使用します。

## 動作の概要

bot アカウントへのメンションに、機能名と引数を続けて投稿します。

```text
@bot function [argument ...]
```

メンション、機能名、引数はスペースで区切ります。メンションは先頭に置いてください。`src/myConf.py` の `okAccount` に登録されたアカウントからのメンションだけが機能を実行できます。未登録のアカウントには拒否メッセージを返信します。

利用できる機能は次のとおりです。

| 機能 | 説明 |
| --- | --- |
| `hello` / `hi` | 動作確認用の返信 |
| `balus` | 終了メッセージを投稿してプロセスの終了を試みる機能 |
| `radiru` | `at` コマンドで NHK ラジオ録音を予約・取り消しする機能 |

## 準備と起動

### 必要なもの

- Python
- このコードが利用する旧形式の Tweepy API（`StreamListener`、`userstream`）に対応する Tweepy
- Twitter API の OAuth 認証情報と、bot アカウントでの投稿・ストリーミングに必要な API 利用権限
- `radiru` を使う場合は Unix 系環境の `at` コマンドと、録音用シェルスクリプト

Python と Tweepy のバージョンはこのリポジトリでは固定されていません。特に現在の Tweepy では旧形式の API が利用できない場合があるため、互換性を確認してください。

### 設定

`src/myConf.py` を環境に合わせて設定します。

- OAuth 認証情報: `consumer_key`、`consumer_secret`、`access_token`、`access_token_secret`
- bot のアカウント名: `myAccount`
- コマンドを実行できるアカウント名のリスト: `okAccount`
- `radiru` の録音スクリプト、録音先、一時ファイル置き場: `doRadiru_rec_script_path`、`doRadiru_rec_folder`、`doRadiru_tmp_folder`

**認証情報を公開リポジトリやログに含めないでください。** このコードは認証情報を `myConf.py` から読み込みます。既に公開された認証情報がある場合は失効させ、新しいものを発行してください。環境変数から読み込む機能は現状ありません。

### 起動

リポジトリのルートディレクトリから実行します。

```sh
python src/recobuta.py
```

プロセスが起動すると Twitter のストリームを監視します。停止する場合は実行環境からプロセスを終了してください（`balus` の既知の制約については後述）。

## コマンド

### `hello` / `hi`

応答確認用の機能です。機能名の後に追加の文言があっても返信します。

```text
@bot hello
@bot hi
@bot hi how are you?
```

### `radiru`

#### ヘルプ

```text
@bot radiru hlp
```

#### 録音予約

```text
@bot radiru rec CHANNEL MINUTES YYYY/MM/DD HH:MM PREFIX
```

例:

```text
@bot radiru rec NHK1 30 2026/11/15 21:00 evening
```

- `CHANNEL`: 次のいずれか。`NHK1`、`NHK2`、`FM`、`NHK1_SENDAI`、`FM_SENDAI`、`NHK1_NAGOYA`、`FM_NAGOYA`、`NHK1_OSAKA`、`FM_OSAKA`
- `MINUTES`: 録音時間（分）
- `YYYY/MM/DD HH:MM`: 録音開始日時。日付と時刻をそれぞれ指定します
- `PREFIX`: 録音スクリプトに渡すファイル名用の接頭辞。現状の実装では省略できません

予約には `src/myConf.py` で指定した録音スクリプトが必要です。NHK サイマル放送の録音スクリプトとして、[@matchy2 さんのスクリプト](https://gist.github.com/matchy2/f03205246e1a12b3b027)を利用する構成になっています。利用時はスクリプトの内容・利用条件を確認し、`doRadiru_rec_script_path` と録音先を環境に合わせてください。

#### 予約の取り消し

```text
@bot radiru can AT_JOB_ID
```

`AT_JOB_ID` には、録音予約時に `at` が返すジョブ ID を指定します。取り消しには `at -r` が使われます。

### `balus`

```text
@bot balus
```

終了メッセージを投稿した後、15 秒待ってプロセスを終了する機能です。ただし現在の `src/myFunc.py` では `sys` が import されていないため、終了処理で `NameError` になります。確実に停止するには、実行環境からプロセスを終了してください。

## 注意事項

- このプロジェクトは旧形式の Twitter/Tweepy ストリーミング API を前提としており、現在の API やライブラリでそのまま動作するとは限りません。
- `radiru` は Unix 系の `at` コマンドと外部録音スクリプトに依存します。これらはリポジトリに含まれていません。
- `radiru` の引数はスペース区切りで解析されます。`PREFIX` にスペースは使用できません。
