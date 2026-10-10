# haiku

俳句を投稿・閲覧できるWebアプリケーションです。

## 構成

| ディレクトリ   | 役割            | 技術スタック                                              |
| -------------- | --------------- | --------------------------------------------------------- |
| `haiku_server` | バックエンドAPI | Python 3.8 / Django 3.1 / Django REST Framework / JWT認証 |
| `haiku_front`  | フロントエンド  | Vue.js 3 / TypeScript / Vuex / Vue Router                 |
| `haiku_api`    | API仕様書       | OpenAPI 3.0（参考資料、単体では動作しません）             |

`docker-compose.yml` は `haiku_server` と `haiku_front` を1つのコンテナ（`dev`）にまとめて起動します。バックエンド（ポート8000）とフロントエンド（ポート8080）の開発サーバーが同じコンテナの中で両方動きます。

## 必要なもの

- Docker Desktop（Docker Compose v2以上）
- VS Code
- VS Code拡張機能「Dev Containers」（`ms-vscode-remote.remote-containers`）

## 実行環境の作成方法（初回セットアップ）

1. `.env` を確認する

   ```
   cp .env.example .env
   ```

   すでに `.env` がある場合はそのままでOKです。DBは `docker-compose.yml` の `db` サービス（ローカルMySQLコンテナ）に接続する設定になっており、追加の設定なしで起動できます。本番相当（例: RDSなど外部のMySQL）に繋ぎたい場合は `.env` 内の `DB_HOST` 等を実際の値に置き換えてください。

2. イメージをビルドして起動する

   ```
   docker compose up --build
   ```

   初回はPython/Node両方の依存関係をインストールするのでビルドに数分かかります。起動時に自動でバックエンドのマイグレーション（`migrate`）も実行されます。

3. アクセス先
   - フロントエンド: http://localhost:8080
   - バックエンドAPI: http://localhost:8000
   - Django管理画面: http://localhost:8000/admin/（利用するにはsuperuserの作成が必要、下記参照）

## 現在の起動設定について（自動起動オフ）

現在 `entrypoint.sh` はコメントアウトして、コンテナ起動時にバックエンド（migrate+runserver）・フロントエンド（npm run serve）を**自動実行しない**設定にしています。`docker compose up` してもサーバーは立ち上がらず、コンテナが待機するだけです。

VS Codeでコンテナに接続した後、ターミナルを2つ開いて手動で起動してください。

```
# ターミナル1（バックエンド）
cd haiku_server
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000

# ターミナル2（フロントエンド）
cd haiku_front
npm run serve -- --host 0.0.0.0 --port 8080
```

`python manage.py migrate` は、新しいモデルを追加したり、既存モデルのフィールドを変更したりしたときに実行する、Djangoのコマンドです。`models.py` の定義に合わせてデータベースのテーブル構造を作成・更新します（事前に `makemigrations` でマイグレーションファイルを生成しておく必要があります。`makemigrations` の実行方法は下記「よく使うコマンド」を参照）。

`--noinput` は、実行中に出ることがある確認プロンプト（y/nで答える質問）をスキップし、デフォルトの選択肢で自動的に進めるオプションです。人が対話的に答えられないスクリプトや自動起動処理（`entrypoint.sh`）の中から実行する場合は、このオプションが必須です。

元の自動起動に戻したい場合は、`entrypoint.sh` を開いてコメントアウトされている2箇所（Backend / Frontend）を元に戻し、末尾の `exec tail -f /dev/null` を削除してください。

## 起動方法（2回目以降）

```
docker compose up
```

バックグラウンドで起動したい場合:

```
docker compose up -d
```

停止:

```
docker compose down
```

（フォアグラウンドで起動している場合は `Ctrl+C` でも停止できます）

## 管理ユーザーの作成（任意）

Django管理画面 (`/admin/`) を使う場合は、コンテナ起動後に一度だけ実行します。

```
docker compose exec dev python haiku_server/manage.py createsuperuser
```

## 開発環境：VS Codeでコンテナに接続する方法

このプロジェクトの開発は「`docker compose up` でコンテナを起動 → VS Codeをそのコンテナにアタッチ」というスタイルを想定しています。ソースコードはbind mountでホストと同期しているため、どちらで編集しても即座に反映されます。

コンテナは1つ（`dev`）だけなので、VS Codeのウィンドウも1つで済みます。`haiku_server/` と `haiku_front/` の両方が同じウィンドウのエクスプローラーに表示され、ターミナルを2つ開けば（Django側・Vue側）両方同時に作業できます。

1. `docker compose up`（または `-d`）でコンテナを起動しておく（すでに起動している場合、VS Code側で自動検知してそのまま使われます）
2. VS Codeに拡張機能「Dev Containers」をインストールする
3. コマンドパレットを開く（`Cmd+Shift+P` / `Ctrl+Shift+P`）
4. 「**Dev Containers: Reopen in Container**」（このリポジトリを開いていない場合は「**Dev Containers: Open Folder in Container...**」）を選択する
5. VS Codeウィンドウがコンテナ内で `/workspace`（リポジトリ全体）を開いた状態で立ち上がり、`devcontainer.json` に列挙された拡張機能（Python/Pylance、autopep8、Vue.volar、ESLint、Prettier、GitLens）が自動でインストールされ、保存時の自動整形（Python→autopep8（2スペース設定）、TS/Vue/JS→Prettier）も有効になります
   - コンテナ内にインストールされているPython/Node、および依存パッケージがそのまま使えます
   - ターミナルタブを増やして、片方で `cd haiku_server && python manage.py ...`、もう片方で `cd haiku_front && npm run ...` のように使い分けられます

**補足**

- `devcontainer.json` の `shutdownAction` は `none` にしてあるので、VS Codeのウィンドウを閉じてもコンテナは停止しません（`docker compose down` するまで起動したままです）。
- 入れたい拡張機能を追加・変更したい場合は、`.devcontainer/devcontainer.json` の `customizations.vscode.extensions` に拡張機能IDを追記してください（次回アタッチ時から反映されます）。
- 単純にコンテナへアタッチしたいだけの場合は「**Dev Containers: Attach to Running Container...**」から `haiku_dev` を選ぶことも可能です。ただしこの方法では拡張機能は自動で入らないため、通常は上記の「Reopen in Container」経由を推奨します。

## よく使うコマンド

- ログを確認する: `docker compose logs -f dev`
- コンテナ内でシェルを開く: `docker compose exec dev bash`
- マイグレーションファイルを作成する: `docker compose exec dev python haiku_server/manage.py makemigrations`
- マイグレーションを適用する: `docker compose exec dev python haiku_server/manage.py migrate`
- Pythonコードを整形する: `docker compose exec dev autopep8 --in-place --recursive --indent-size 2 haiku_server`（VS Codeでは保存時に自動整形されます）。標準的なPythonフォーマッタのBlackはインデント幅が4スペース固定で変更できないため、このプロジェクト（2スペースインデント）ではautopep8を使っています
- Pythonコードをlintする: `docker compose exec dev pylint haiku_server/api`
- フロントエンド（.ts/.vue/.js）コードを整形する: `docker compose exec dev bash -c "cd haiku_front && npx prettier --write src"`（VS Codeでは保存時に自動整形されます）
- フロントエンドコードをlintする: `docker compose exec dev bash -c "cd haiku_front && npm run lint"`
- 依存関係を追加した後の再ビルド: `docker compose up --build`

## コンテナ内でgitを使う

コンテナ内に `git` コマンドと `openssh-client` をインストールし、Macの `~/.gitconfig` と `~/.ssh` を読み取り専用でコンテナにマウントしています。これにより、コンテナ内のターミナル（VS Codeのターミナルなど）からMacと同じユーザー名・メールアドレス・SSH鍵でそのまま `git clone` / `git pull` / `git push` などが行えます。

**前提**

- Dockerfileと`docker-compose.yml`を変更したので、一度 `docker compose up --build` で再ビルドしてください。
- Macに `~/.gitconfig`（`git config --global user.name` / `user.email` などを一度でも設定していればあります）と `~/.ssh`（SSH鍵があれば）が存在している必要があります。どちらか片方でも無い場合、Docker側がその場所に空のディレクトリを自動作成してしまうことがあるので、心当たりがない場合は先にMac側のターミナルで `git config --global user.name "..."` / `git config --global user.email "..."` を実行しておいてください。
- 共有は読み取り専用（`:ro`）ですが、コンテナ内のプロセスからMacのSSH秘密鍵が読める状態になる点は理解した上で使ってください。

**補足**

- `/workspace` はMac側ユーザー所有のままバインドマウントされている一方、コンテナ内はrootで動くため、gitが安全のため拒否する「detected dubious ownership」エラーが出ないよう、`entrypoint.sh` がコンテナ起動のたびに `/root/.gitconfig` を生成し、`safe.directory = /workspace` を自動追加しています（手動で `/root/.gitconfig` を編集しても次回起動時に上書きされます）。
- SSH初回接続時に known_hosts へのホストキー追記が必要な場合、`~/.ssh` が読み取り専用マウントのため書き込みに失敗する警告が出ることがあります（接続自体は可能です）。気になる場合はMac側で一度接続して known_hosts に登録しておいてください。
- もし再ビルド時に `apt-get install` のステップで失敗する場合は、以前別のパッケージ追加時にdpkgの展開処理が落ちる問題が見つかっているビルド環境固有の既知の問題の可能性があります。その場合は教えてください（Node.jsと同様、他イメージからgitバイナリをマルチステージCOPYで持ってくる方式に切り替えます）。

## haiku_api（OpenAPI定義）からのコード生成

`haiku_api/openapi.yaml` から、[OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) の公式Dockerイメージ（`openapitools/openapi-generator-cli`）を使ってクライアントコードなどを自動生成できます。Java等をローカルに用意する必要はありません。

プロジェクトルート直下で実行してください。

TypeScript（フロントエンド用のaxiosクライアント）:

```bash
docker run --rm -v "$(pwd):/local" openapitools/openapi-generator-cli generate \
  -i /local/haiku_api/openapi.yaml \
  -g typescript-axios \
  -o /local/haiku_api/generated/typescript-axios
```

Python用クライアント:

```bash
docker run --rm -v "$(pwd):/local" openapitools/openapi-generator-cli generate \
  -i /local/haiku_api/openapi.yaml \
  -g python \
  -o /local/haiku_api/generated/python
```

- `-i`: 入力となるOpenAPI定義ファイル
- `-g`: 生成する言語/フレームワーク（ジェネレーター名）
- `-o`: 生成先ディレクトリ

選べるジェネレーターの一覧は以下で確認できます。

```bash
docker run --rm openapitools/openapi-generator-cli list
```

## データベースについて

MySQL（`docker-compose.yml` の `db` サービス、公式 `mysql:8.0` イメージ）を使います。SQLiteは使用していません。

- 接続情報: `.env` の `DB_NAME`/`DB_USER`/`DB_PASSWORD`/`DB_HOST`/`DB_PORT`（ローカルではすべて `haiku`、ホストは `db`、ポートは `3306`）
- データは `mysql_data` という名前付きボリュームに保存されるため、`docker compose down` しても残ります（完全に消したい場合は `docker compose down -v`）
- 初回のみマイグレーションが必要です

  ```
  docker compose exec dev python haiku_server/manage.py migrate
  ```

本番相当（例: RDSなど外部のMySQL）に繋ぎたい場合は、`.env` の `DB_HOST` 等を実際のホスト・認証情報に置き換えてください。

### MySQLに外部（Macのクライアントアプリなど）から接続する

`db` サービスは `docker-compose.yml` で `3306:3306` と公開しているので、Mac側からは `localhost:3306` にそのまま接続できます。

- ホスト: `localhost`（または `127.0.0.1`）
- ポート: `3306`
- ユーザー: `haiku`
- パスワード: `haiku`
- データベース名: `haiku`

TablePlusやMySQL Workbench、DBeaverなどのGUIクライアントにこの情報を入力するだけで接続できます。コマンドラインからの場合（Mac側に `mysql` コマンドがあれば）:

```
mysql -h 127.0.0.1 -P 3306 -u haiku -p haiku
```

接続するには `db` コンテナが起動している必要があります。「[Dev Containers: Reopen in Container](#開発環境vscodeでコンテナに接続する方法)」でVS Codeから接続した場合も、`devcontainer.json` が参照している `docker-compose.yml` に `db` サービスが含まれているため、`dev` コンテナと一緒に自動で起動します（`db` 用に別途 `docker compose up` する必要はありません）。

もしMac側に別のMySQL（Homebrewで入れたものなど）がすでにポート3306で動いている場合は競合してこの `db` コンテナが起動できません。その場合は `docker-compose.yml` の `db` サービスの `ports` を `"3307:3306"` のように変更し、接続時のポートもそれに合わせてください。

## トラブルシューティング

- ポート `8000` / `8080` が既に使われている場合は、`docker-compose.yml` の `ports` の左側（ホスト側ポート）を変更してください。
- フロントエンドの `node_modules` がおかしくなった場合は、一度ボリュームごと削除してから再ビルドしてください。

  ```
  docker compose down -v
  docker compose up --build
  ```
