import sys

from opsctl import backup, keys, policy, portal, status


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: cli.py [status|status --passive|keys|policy|portal|backup]")
        raise SystemExit(1)
    cmd = sys.argv[1]
    if cmd == "status":
        mode = "passive" if "--passive" in sys.argv else "active"
        status.run(mode)
    elif cmd == "keys":
        keys.run()
    elif cmd == "policy":
        policy.run()
    elif cmd == "portal":
        portal.run()
    elif cmd == "backup":
        backup.run()
    else:
        raise SystemExit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
