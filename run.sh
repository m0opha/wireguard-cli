BASENAME="wireguard-cli"
VENV=".env"
packages=("nuitka")

set_virtualenv(){
  if [ ! -d "$VENV" ]; then
    virtualenv "$VENV"
  fi
  source "$VENV/bin/activate"
  pip_install "${packages[@]}"
}

execute(){
    set_virtualenv
    pip_install "${packages[@]}"
    python3 "$BASENAME".py
}

pip_install(){
    for package in "$@"; do
        echo "Instalando $package..."
        pip install "$package"
        if [ $? -eq 0 ]; then
            echo "$package instalado correctamente."
        else
            echo "Error al instalar $package."
        fi
    done
}

build() {
  local BASENAME="$1"
  shift

  local SCRIPT="$BASENAME.py"
  local BIN_NAME="$BASENAME.bin"
  local INSTALL_DIR="$HOME/.config/$BASENAME"
  local LOCAL_BIN="$HOME/bin"
  local SYMLINK="$LOCAL_BIN/$BASENAME"

  set_virtualenv

  if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
  fi
  mkdir -p "$INSTALL_DIR"

  local INCLUDE_ARGS=()

  for dir in "$@"; do
    # Elimina comillas si vienen de argumentos como ".src scripts"
    IFS=' ' read -r -a parts <<< "$dir"
    for part in "${parts[@]}"; do
      if [ -d "$part" ]; then
        INCLUDE_ARGS+=(--include-data-dir="$part=$part")
      else
        echo -e "\033[0;33m[!]\033[0m Warning: directory '$part' not found, skipping."
      fi
    done
  done

  python3 -m nuitka \
    --standalone \
    --no-deployment-flag=self-execution \
    --output-dir="$INSTALL_DIR" \
    --remove-output \
    --follow-imports \
    --lto=yes \
    --clang \
    --jobs=6 \
    --assume-yes-for-downloads \
    "${INCLUDE_ARGS[@]}" \
    "$SCRIPT"

  mkdir -p "$LOCAL_BIN"

  if [ -f "$SYMLINK" ]; then
    rm "$SYMLINK"
  fi

  ln -sf "$INSTALL_DIR/$BASENAME.dist/$BIN_NAME" "$SYMLINK"
}

if [ $# -eq 0 ]; then
  build "$BASENAME"
else
  case "$1" in
    execute)
      shift
      execute "$@"
      ;;
    *)
      echo "Not recognized."
      exit 1
      ;;
  esac
fi

if command -v deactivate >/dev/null 2>&1; then
  deactivate
    fi