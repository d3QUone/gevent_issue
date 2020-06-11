import sys
from errno import EWOULDBLOCK
from select import select, poll, POLLIN, POLLOUT
from socket import error


def apply_gevent_hack_py3(recv_timeout):
    import gevent.socket
    import gevent.monkey
    import urllib3.util.wait
    import _socket

    true_select = gevent.monkey.saved.get("select", {}).get("select", select)
    true_poll = gevent.monkey.saved.get("select", {}).get("poll", poll)

    def patched_recv_info(self, *args):
        sock = self._sock  # keeping the reference so that fd is not closed during waiting
        while True:
            ready, _, _ = true_select([sock], [], [], recv_timeout)
            if not ready:
                self._wait(self._read_event)  # здесь переключение гринлетов
                continue

            try:
                return _socket.socket.recv_into(sock, *args)
            except error as ex:
                if ex.args[0] != EWOULDBLOCK or self.timeout == 0.0:
                    raise
            self._wait(self._read_event)

    def poll_wait_for_socket(sock, read=False, write=False, timeout=None):
        # копипаста из urllib3.util.wait.wait_for_socket
        # Нужна для того, чтобы отключить переключение гринлетов при
        # проверке состояния соединения (как было в старом requests)
        if not read and not write:
            raise RuntimeError("must specify at least one of read=True, write=True")
        mask = 0
        if read:
            mask |= POLLIN
        if write:
            mask |= POLLOUT
        poll_obj = true_poll()
        poll_obj.register(sock, mask)

        # For some reason, poll() takes timeout in milliseconds
        def do_poll(t):
            if t is not None:
                t *= 1000
            return poll_obj.poll(t)

        return bool(do_poll(timeout))

    gevent.socket.socket.recv_into = patched_recv_info
    urllib3.util.wait.wait_for_socket = poll_wait_for_socket
