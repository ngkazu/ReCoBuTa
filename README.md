# ReCoBuTAとは?

ReCoBuTAは **Re**mote **Co**ntrol **B**ot **u**sing **T**witter **A**PI の略  
Twitterを使い外部から遠隔操作を可能とするpythonスクリプトです  
TwitterAPIのラッパーとして**tweepy**を使用しています  

・・・githubのアドレスを記載・・・
で公開をしています

# 使い方

botアカウントに*mention tweet*を送ることで実装されている機能を実行します  

基本コマンドとして：
> @*bot* *function* [*cmmand-1* *command-2* ...] 

mentionは必ず接頭にある必要があります  
functionおよびcommandはスペース区切りで記載をします

functionは呼び出す機能、*command*はその機能の引数となります  

つまり：
- 1st word: botへのmention  
- 2nd word: function(機能)
- 3rd word以降: function(機能)に対するcommnad(命令)
となります  

現在、実装されている*function*は以下の3つ:
1. hello:
    - レスポンス確認用
2. balus:
    - 滅びの呪文
    いいまじないに力を与えるには、悪い言葉も知らなければいけないって。でも決して使うなって…。教わったとき、怖くて眠れなかった…。
3. radiru:
    - NHKのサイマル配信サービスを録音する機能
    - NHKサイマル放送の録音には @matchy2 (GithubGist)さんが作ったスクリプトを使用します
        - https://gist.github.com/matchy2/f03205246e1a12b3b027

# function(機能)説明

## hello

この機能はスクリプトが実行されているを外部から確認するためのものです  
もっとも基本的な作りとなっています  
hello(or hi)を送るとリプライが返ってきます  

### 使用方法

>@*bot* hello

もしくは

>@*bot* hi

helloもしくはhi以降スペースを入れ文言を加えても反応します  

>@*bot hi how are u? #ReCoBuTA


## radiru

### 使用方法

## balus

アレの滅びの呪文  
この機能を呼び出すと外部からの遠隔操作は不能となります  
だってスクリプトが強制終了されるから…  

### 使用方法

>@bot balus


# カスタマイズの方法
