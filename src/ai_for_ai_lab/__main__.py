"""JSON stdout; exit 0 fresh/captured, 1 stale, 2 invalid/unreadable."""
import argparse
import json
import sys
from pathlib import Path
from .capsule import CapsuleError, capture, check, loads
from .review import link, review
from .checkpoint import inspect, refresh


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise CapsuleError(message, "invalid_arguments")


def main():
    parser = JsonArgumentParser(description=__doc__)
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
    checkpoint = sub.add_parser("checkpoint")
    checkpoint.add_argument("--root", required=True)
    checkpoint.add_argument("--refresh", action="store_true",
                            help="replace the baseline after reviewing changes and running tests")
    try:
        args = parser.parse_args()
        if args.command == "capture":
            result = capture(args.root, args.goal, args.next_step, args.paths)
            code = 0
        elif args.command == "checkpoint":
            result = refresh(args.root) if args.refresh else inspect(args.root)
            code = 0 if args.refresh or result["fresh"] else 1
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
    except CapsuleError as exc:
        result = {"error": str(exc), "code": exc.code}
    except UnicodeError as exc:
        result = {"error": str(exc), "code": "invalid_json"}
    except OSError as exc:
        result = {"error": str(exc), "code": "io_error"}
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 2


if __name__ == "__main__":
    sys.exit(main())
