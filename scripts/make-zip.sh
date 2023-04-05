#!/bin/bash

set -eu
set -o pipefail

readonly ROOT_DIR="$(cd "$(dirname "${0}")/.." && pwd)"

source "${ROOT_DIR}/scripts/support/print.sh"

function main {
  local path

  while [[ "${#}" != 0 ]]; do
    case "${1}" in
    --help | -h)
      shift 1
      usage
      exit 0
      ;;

    *)
      path="${1}"
      shift 1
      ;;
    esac
  done

  if [[ -z "${path:-}" ]]; then
    usage
    echo
    util::print::error "path is required"
  fi

  make::zip "${path}"
}

function usage() {
  cat <<-USAGE
make-zip.sh <path>

Creates a ZIP file of the contents of the specified path.

OPTIONS
  --help|-h  prints the command usage
USAGE
}

function make::zip() {
  local path
  path="${1}"

  cd ${path} &>/dev/null || (util::print::error "Path not found: ${path}" && exit)
  current_dirname=${PWD##*/}            # to assign to a variable
  current_dirname=${current_dirname:-/} # to correct for the case where PWD=/
  zip -r ${current_dirname}.zip * &>/dev/null
  cd - &>/dev/null || exit

  util::print::success "Created file at ${path}/${current_dirname}.zip"
}

main "${@:-}"
