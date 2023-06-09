# This file is part of tdmclient.
# Copyright 2021 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Miniature Mobile Robots group, Switzerland
# Author: Yves Piguet
#
# SPDX-License-Identifier: BSD-3-Clause

from tdmclient import TDMZeroconfBrowser, TDMConnection
from tdmclient import FlatBuffer, ThymioFB
from tdmclient.clientnode import ClientNode


class DisconnectedError(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class Client(ThymioFB):

    DEFAULT_TDM_PORT = 8596

    def __init__(self,
                 zeroconf=None, tdm_addr=None, tdm_port=None, password=None,
                 **kwargs):

        super(Client, self).__init__(**kwargs)

        if zeroconf is None:
            # use zeroconf if tdm_port isn't specified
            zeroconf = tdm_port is None
        self.tdm_addr = tdm_addr
        self.tdm_port = tdm_port
        self.tdm = None

        def on_zc_change(is_added, addr, port, ws_port):
            if is_added and self.tdm_addr is None:
                if self.debug >= 1:
                    print(f"Zeroconf: TDM {addr}:{port} on")
                if tdm_addr is None:
                    self.tdm_addr = addr
                if tdm_port is None:
                    self.tdm_port = port
                self.connect()
                self.send_handshake(password)
            elif not is_added and addr == self.tdm_addr and port == self.tdm_port:
                if self.debug >= 1:
                    print(f"Zeroconf: TDM {addr}:{port} off")
                self.disconnect()
                self.tdm_addr = None
                self.tdm_port = None

        if zeroconf:
            self.zc = TDMZeroconfBrowser(on_zc_change)
        else:
            self.zc = None
            if self.tdm_port is None:
                self.tdm_port = self.DEFAULT_TDM_PORT
            if tdm_addr is None:
                # localhost by default
                self.tdm_addr = "127.0.0.1"
            if self.debug >= 1:
                print(f"TDM {self.tdm_addr}:{self.tdm_port}")
            self.connect()
            self.send_handshake(password)

    def close(self):
        if self.zc is not None:
            self.zc.close()
            self.zc = None

    def connect(self):
        self.tdm = TDMConnection(self.tdm_addr, self.tdm_port)

    def disconnect(self):
        if self.tdm is not None:
            self.tdm.request_shutdown()
            self.tdm = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def create_node(self, node_dict):
        return ClientNode(self, node_dict)

    def send_packet(self, b, ignore_disconnected_error=False):
        if self.debug >= 2:
            # check decoding
            fb2 = FlatBuffer()
            fb2.parse(b, self.SCHEMA)
            fb2.dump("Send")

        if self.tdm is None:
            if ignore_disconnected_error:
                return
            else:
                raise DisconnectedError("TDM disconnected")

        try:
            self.tdm.send_packet(b)
        except SyntaxError as error:
            if not ignore_disconnected_error:
                raise error

    def send_message(self, msg, schema=None):
        encoded_fb = self.create_message(msg, schema)

        self.send_packet(encoded_fb)

    def send_handshake(self, password=None):
        if self.debug >= 1:
            print("send handshake")
        self.send_packet(self.create_msg_handshake(password))

    def shutdown_tdm(self, **kwargs):
        """Send a shutdown request. No reply should be expected.
        """
        if self.debug >= 1:
            print("send tdm shutdown request")
        self.send_packet(self.create_msg_device_manager_shutdown_request(**kwargs))

    def send_request_list_of_nodes(self):
        """Send a list of nodes request.
        """
        if self.debug >= 1:
            print("send list of nodes request")
        self.send_packet(self.create_msg_request_list_of_nodes())

    def process_waiting_messages(self):
        at_least_one = False
        if self.tdm:
            while True:
                msg = self.tdm.receive_packet()
                if msg is None:
                    break
                if self.debug >= 3:
                    print("recv", msg)
                self.process_message(msg)
                at_least_one = True
        return at_least_one
