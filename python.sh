#!/bin/zsh
#
# Created:      2024-07-29 23:30:28
set -eu

# このスクリプトがあるディレクトリに移動
cd `dirname $0`

VERSION=$(jq -r ".python.version" settings.json)
TARGET=$(realpath $(jq -r ".pip.target" settings.json))
mkdir -p $TARGET
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

PROJECT_REAL_PATH=$(realpath $(jq -r ".target" settings.json))
export PYTHONPATH="$PROJECT_REAL_PATH:$TARGET"
python3 $@
deactivate
