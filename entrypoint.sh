#!/bin/sh
set -e

# Macの ~/.gitconfig (docker-compose.ymlでread-onlyマウント)を取り込みつつ、
# /workspace はホスト所有のままバインドマウントされている一方でこのコンテナは
# rootで動くため、gitが安全のため拒否する「dubious ownership」エラーを避ける
# safe.directory をコンテナ内だけに追加する。/root/.gitconfig はコンテナ起動の
# たびに生成し直すので、手動で編集しても次回起動時に上書きされる点に注意。
if [ -f /root/.gitconfig-host ]; then
  cat > /root/.gitconfig << 'GITCONFIG'
[include]
	path = /root/.gitconfig-host
[safe]
	directory = /workspace
GITCONFIG
fi

# 自動起動を止めている間: コンテナはVS Codeから接続して手動でサーバーを
# 起動するためだけに待機する。元に戻す(自動起動を再開する)には、下の
# 2行のコメントアウトを外して、この行(tail -f /dev/null)を削除・コメントアウトする。

# # Backend: migrate then run the dev server in the background.
# (cd haiku_server && python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000) &

# # Frontend: run the dev server in the foreground so the container's
# # main process stays attached to it.
# cd haiku_front && exec npm run serve -- --host 0.0.0.0 --port 8080

exec tail -f /dev/null
