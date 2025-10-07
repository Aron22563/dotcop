import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Dotcop: Configuration package manager"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("help", help="Show help message")
    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List installed configurations")
    subparsers.add_parser("install", help="Install a configuration")
    subparsers.add_parser("remove", help="Remove a configuration")

    args = parser.parse_args()

    if args.command == "help":
        parser.print_help()
    elif args.command == "status":
        print("Coming soon...")
    elif args.command == "list":
        print("Coming soon...")
    elif args.command == "install":
        print("Coming soon...")
    elif args.command == "remove":
        print("Coming soon...")
    else:
        parser.print_help()
