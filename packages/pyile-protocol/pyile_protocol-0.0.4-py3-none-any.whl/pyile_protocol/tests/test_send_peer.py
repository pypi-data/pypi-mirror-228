import threading

from pyile_protocol.lib.peers.JoinPeer import JoinPeer
from pyile_protocol.lib.messenger.Messenger import Messenger
from random import randint


def test_peer():
    # Add random int to auth port to avoid conflicts when testing
    messenger = Messenger()
    peer = JoinPeer(address=("172.20.100.99", 4702 + randint(0, 20)), messenger=messenger, alias="peer_1")

    # Normal Instance
    # peer = JoinPeer(("172.20.100.99", 4702 + randint(0, 20)))

    '''
    get_authenticated() returns a boolean value, can be looped until peer is banned
    '''
    # authenticated = peer.get_authenticated(("172.20.100.39", 4702), "password")
    peer.get_authenticated(("172.20.101.26", 4702), "password")

    try:
        connect_thread = threading.Thread(target=peer.connect)
        peer.threads.append(connect_thread)
        connect_thread.start()
    except:
        print("threads terminated")

    while not peer.disconnected:
        data = input("~: ")
        if data == "exit":
            peer.leave()
        elif data == "peers":
            print(peer.peers)
        elif data == "threads":
            print(threading.active_count())
        elif data == "check":
            print(messenger.get_messages())
        elif data == "log":
            print(peer.messenger.seq_list)
        else:
            peer.broadcast(data)
