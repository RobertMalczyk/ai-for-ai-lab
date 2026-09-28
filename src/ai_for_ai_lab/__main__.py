"""JSON stdout; exit 0 fresh/captured, 1 stale, 2 invalid/unreadable."""
import argparse
import json
import sys
from pathlib import Path
from .capsule import CapsuleError, capture, check, loads
from .review import link, review


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("capture")
    create.add_argument("--root", required=True)
    create.add_argument("--goal", required=True)
    create.add_argument("--next-step", required=True)
    create.add_argument("paths", nargs="+")
    verify = sub.add_parser("check")
    verify.add_argument("--root", required=True)
    verify.add_argument("capsule")
    bind = sub.add_parser("link")
    bind.add_argument("capsule")
    bind.add_argument("claims")
    scoped = sub.add_parser("review")
    scoped.add_argument("--root", required=True)
    scoped.add_argument("capsule")
    scoped.add_argument("manifest")
    args = parser.parse_args()
    try:
        if args.command != "link" and not Path(args.root).is_dir():
            raise CapsuleError("root must be an existing directory")
        if args.command == "capture":
            result = capture(args.root, args.goal, args.next_step, args.paths)
            code = 0
        elif args.command == "link":
            result = link(loads(Path(args.capsule).read_text(encoding="utf-8")),
                          loads(Path(args.claims).read_text(encoding="utf-8")))
            code = 0
        elif args.command == "review":
            result = review(args.root, loads(Path(args.capsule).read_text(encoding="utf-8")),
                            loads(Path(args.manifest).read_text(encoding="utf-8")))
            code = 0 if result["fresh"] else 1
        else:
            result = check(args.root, loads(Path(args.capsule).read_text(encoding="utf-8")))
            code = 0 if result["fresh"] else 1
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return code
    except (CapsuleError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
