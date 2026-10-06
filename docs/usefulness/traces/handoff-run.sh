# usage: source run.sh ; r <cmd...>  -> prints cmd, exit, bytes, output
LAB=/home/claude/ai-for-ai-lab/src
r() { local out; out=$(eval "$@" 2>&1); local ec=$?; printf '$ %s\n[exit=%s bytes=%s]\n%s\n\n' "$*" "$ec" "$(printf '%s' "$out" | wc -c)" "$out"; }
lab() { PYTHONPATH=$LAB python3 -m ai_for_ai_lab "$@"; }
