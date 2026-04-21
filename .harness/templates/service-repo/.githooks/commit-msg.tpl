#!/bin/sh
set -eu

MSG_FILE="${1:?commit message file is required}"
HEADER="$(sed -n '1p' "$MSG_FILE" | tr -d '\r')"

case "$HEADER" in
  Merge\ *|Revert\ *|fixup!\ *|squash!\ *)
    exit 0
    ;;
esac

if [ -z "$HEADER" ]; then
  echo "commit subject is required" >&2
  exit 1
fi

if [ "${#HEADER}" -gt 50 ]; then
  echo "commit subject must be 50 characters or fewer" >&2
  exit 1
fi

if printf '%s' "$HEADER" | grep -Eq '\.$'; then
  echo "commit subject must not end with a period" >&2
  exit 1
fi

if ! printf '%s' "$HEADER" | grep -Eq '^(feat|fix|build|chore|ci|docs|style|refactor|test|release): [A-Z]'; then
  echo "commit subject must follow '<type>: <Subject>' with an allowed type" >&2
  exit 1
fi

NON_COMMENT_FROM_THIRD_LINE="$(sed -n '3,$p' "$MSG_FILE" | grep -Ev '^(#|$)' || true)"
SECOND_LINE="$(sed -n '2p' "$MSG_FILE" | tr -d '\r')"

if [ -n "$NON_COMMENT_FROM_THIRD_LINE" ] && [ -n "$SECOND_LINE" ]; then
  echo "leave one blank line between the subject and the body" >&2
  exit 1
fi

awk '
  NR <= 2 { next }
  /^#/ { next }
  length($0) > 72 {
    print "commit body lines must be 72 characters or fewer" > "/dev/stderr"
    exit 1
  }
' "$MSG_FILE"
