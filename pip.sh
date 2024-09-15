#!/bin/zsh
#
# Created:      2024-07-29 23:30:28
set -eu

# このスクリプトがあるディレクトリに移動
cd `dirname $0`

VERSION=$(jq -r ".python.version" settings.json)
WHERE=$(jq -r ".pip.target" settings.json)
mkdir -p $WHERE
# envディレクトリがない場合は作成
if [ ! -d env ]; then
  python$VERSION -m venv env
  if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment"
    exit 1
  else
    echo "Virtual environment created"
    if [ ! $# -eq 0 ]; then
      echo "Plese run command again."
    fi
  fi
  exit 0
fi
# コマンドライン引数がなければ終了
if [ $# -eq 0 ]; then
  echo "Usage: pip.sh [command] [options]"
  exit 1
fi
# python3のversionが3.12かどうか
if [ `python3 --version | awk '{print $2}' | cut -d. -f1,2` != "$VERSION" ]; then
  echo "Python version is not $VERSION"
  exit 1
fi
source env/bin/activate

if [ $1 = "install" ]; then
  if [ $2 = "-r" ]; then
    pip install -r $3 -t $WHERE
  else
    pip install $2 -t $WHERE
  fi
elif [ $1 = "install2" ]; then
  if [ $2 = "-r" ]; then
    pip install -r $3 -t $WHERE
    pip install -r $3
  else
    pip install $2 -t $WHERE
    pip install $2
  fi
else
  pip $@
fi
deactivate
