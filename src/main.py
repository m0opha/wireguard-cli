import argparse

from .installer import installer
from .delete_peer import deletePeer
from .create_peer import createPeer
from .block_peer import blockPeer
from .unblock_peer import unblockPeer

def main():
    parser = argparse.ArgumentParser(description="WireGuard Management Tool")
    parser.add_argument("--install", "-I", action="store_true", help="Install and configure WireGuard")
    subparsers = parser.add_subparsers(dest="command")

    # create-peer
    parser_create = subparsers.add_parser("create-peer", help="Create a new peer")
    parser_create.add_argument("name", help="Name of the peer")

    # delete-peer
    parser_delete = subparsers.add_parser("delete-peer", help="Delete a peer")
    parser_delete.add_argument("name", help="Name of the peer")

    # block-peer
    parser_block = subparsers.add_parser("block-peer", help="Block a peer")
    parser_block.add_argument("name", help="Name of the peer")

    # unblock-peer
    parser_unblock = subparsers.add_parser("unblock-peer", help="Unblock a peer")
    parser_unblock.add_argument("name", help="Name of the peer")

    args = parser.parse_args()

    # --install flag
    if args.install:
        installer()

    elif args.command == "create-peer":
        count = 1  # default
        # Si args.name es un número, úsalo como count
        if args.name.isdigit():
            count = int(args.name)
            createPeer(count=count)
        else:
            createPeer(forced_number=args.name)  # si quieres crear peer con nombre específico

    elif args.command == "delete-peer":
        deletePeer(args.name)

    elif args.command == "block-peer":
        blockPeer(args.name)
    
    elif args.command == "unblock-peer":
        unblockPeer(args.name)
