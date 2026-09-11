# trivia

雑学（トリビア）を投稿・検索・閲覧できるWebアプリケーションです。

## 構成

| ディレクトリ | 役割 | 技術スタック |
|---|---|---|
| `trivia_server` | バックエンドAPI | Python 3.8 / Django 3.1 / Django REST Framework / JWT認証 |
| `trivia_front` | フロントエンド | Vue.js 3 / TypeScript / Vuex / Vue Router |
| `trivia_api` | API仕様書 | OpenAPI 3.0（参考資料、単体では動作しません） |

`docker-compose.yml` は `trivia_server` と `trivia_front` を1つのコンテナ（`dev`）にまとめて起動します。バックエンド（ポート8000）とフロントエンド（ポート8080）の開発サーバーが同じコンテナの中で両方動きます。

## 必要なもの

- Docker Desktop（Docker Compose v2以上）
- VS Code
- VS Code拡張機能「Dev Containers」（`ms-vscode-remote.remote-containers`）

## 実行環境の作成方法（初回セットアップ）

1. `.env` を確認する

   ```
   cp .env.example .env
   ```

   すでに `.env` がある場合はそのままでOKです。デフォルトはSQLiteを使う設定になっており、追加の設定なしで起動できます。MySQL（本番相当）に繋ぎたい場合は `.env` 内の `DB_ENGINE=mysql` 以下のコメントを外して値を埋めてください。

2. イメージをビルドして起動する

   ```
   docker compose up --build
   ```

   初回はPython/Node両方の依存関係をインストールするのでビルドに数分かかります。起動時に自動でバックエンドのマイグレーション（`migrate`）も実行されます。

3. アクセス先

   - フロントエンド: http://localhost:8080
   - バックエンドAPI: http://localhost:8000
   - Django管理画面: http://localhost:8000/admin/（利用するにはsuperuserの作成が必要、下記参照）

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
docker compose exec dev python trivia_server/manage.py createsuperuser
```

## 開発環境：VS Codeでコンテナに接続する方法

このプロジェクトの開発は「`docker compose up` でコンテナを起動 → VS Codeをそのコンテナにアタッチ」というスタイルを想定しています。ソースコードはbind mountでホストと同期しているため、どちらで編集しても即座に反映されます。

コンテナは1つ（`dev`）だけなので、VS Codeのウィンドウも1つで済みます。`trivia_server/` と `trivia_front/` の両方が同じウィンドウのエクスプローラーに表示され、ターミナルを2つ開けば（Django側・Vue側）両方同時に作業できます。

1. `docker compose up`（または `-d`）でコンテナを起動しておく（すでに起動している場合、VS Code側で自動検知してそのまま使われます）
2. VS Codeに拡張機能「Dev Containers」をインストールする
3. コマンドパレットを開く（`Cmd+Shift+P` / `Ctrl+Shift+P`）
4. 「**Dev Containers: Reopen in Container**」（このリポジトリを開いていない場合は「**Dev Containers: Open Folder in Container...**」）を選択する
5. VS Codeウィンドウがコンテナ内で `/workspace`（リポジトリ全体）を開いた状態で立ち上がり、`devcontainer.json` に列挙された拡張機能（Python/Pylance、Vue.volar、ESLint）が自動でインストールされます
   - コンテナ内にインストールされているPython/Node、および依存パッケージがそのまま使えます
   - ターミナルタブを増やして、片方で `cd trivia_server && python manage.py ...`、もう片方で `cd trivia_front && npm run ...` のように使い分けられます

**補足**

- `devcontainer.json` の `shutdownAction` は `none` にしてあるので、VS Codeのウィンドウを閉じてもコンテナは停止しません（`docker compose down` するまで起動したままです）。
- 入れたい拡張機能を追加・変更したい場合は、`.devcontainer/devcontainer.json` の `customizations.vscode.extensions` に拡張機能IDを追記してください（次回アタッチ時から反映されます）。
- 単純にコンテナへアタッチしたいだけの場合は「**Dev Containers: Attach to Running Container...**」から `trivia_dev` を選ぶことも可能です。ただしこの方法では拡張機能は自動で入らないため、通常は上記の「Reopen in Container」経由を推奨します。

## よく使うコマンド

- ログを確認する: `docker compose logs -f dev`
- コンテナ内でシェルを開く: `docker compose exec dev bash`
- マイグレーションファイルを作成する: `docker compose exec dev python trivia_server/manage.py makemigrations`
- マイグレーションを適用する: `docker compose exec dev python trivia_server/manage.py migrate`
- 依存関係を追加した後の再ビルド: `docker compose up --build`

## データベースについて

デフォルトはSQLite（`trivia_server/db.sqlite3`）です。このファイルはbind mountされているため、コンテナを削除してもデータは消えません。MySQLへの切り替え方法は `.env` 内のコメントを参照してください。

## トラブルシューティング

- ポート `8000` / `8080` が既に使われている場合は、`docker-compose.yml` の `ports` の左側（ホスト側ポート）を変更してください。
- フロントエンドの `node_modules` がおかしくなった場合は、一度ボリュームごと削除してから再ビルドしてください。

  ```
  docker compose down -v
  docker compose up --build
  ```
