#!/usr/bin/python3

import socket
import struct
import time

# Communication with the DAC happens over TCP on port 7765
COMMUNICATION_PORT = 7765

# The DAC sends UDP broadcast messages on port 7654
BROADCAST_PORT = 7654

# Commands
COMMAND_PREPARE_STREAM = ord("p")
COMMAND_BEGIN_PLAYBACK = ord("b")
COMMAND_QUEUE_RATE_CHANGE = ord("q")
COMMAND_WRITE_DATA = ord("d")
COMMAND_STOP = ord("s")
COMMAND_EMERGENCY_STOP = 0
COMMAND_CLEAR_ESTOP = ord("c")
COMMAND_PING = ord("?")
COMMAND_UPDATE = ord("u")

# Responses
RESPONSE_ACK = ord("a")
RESPONSE_NAK_FULL = ord("F")
RESPONSE_NAK_INVALID = ord("I")
RESPONSE_NAK_STOP_CONDITION = ord("!")

# Playback states
PLAYBACK_STATE_IDLE = 0
PLAYBACK_STATE_PREPARED = 1
PLAYBACK_STATE_PLAYING = 2

# Light engine states
LE_STATE_READY = 0
LE_STATE_WARMUP = 1
LE_STATE_COOLDOWN = 2
LE_STATE_ESTOP = 3


def pack_point(x, y, r, g, b, i=-1, u1=0, u2=0, flags=0):
    """Pack some color values into a struct dac_point.

    Values must be specified for x, y, r, g, and b. If a value is not
    passed in for the other fields, i will default to max(r, g, b); the
    rest default to zero.
    """

    if i < 0:
        i = max(r, g, b)

    return struct.pack("<HhhHHHHHH", flags, x, y, i, r, g, b, u1, u2)


class ProtocolError(Exception):
    """Exception used when a protocol error is detected."""

    pass


class Status:
    """Represents a status response from the DAC.

    Protocol reference: https://ether-dream.com/protocol.html#status
    """

    def __init__(self, data):
        """Initialize from a chunk of data."""
        (
            self.protocol_version,
            self.light_engine_state,
            self.playback_state,
            self.source,
            self.light_engine_flags,
            self.playback_flags,
            self.source_flags,
            self.fullness,
            self.point_rate,
            self.point_count,
        ) = struct.unpack("<BBBBHHHHII", data)

    def dump(self, prefix=" - "):
        """Dump to a string."""
        lines = [
            "Light engine: state %d, flags 0x%x"
            % (self.light_engine_state, self.light_engine_flags),
            "Playback: state %d, flags 0x%x"
            % (self.playback_state, self.playback_flags),
            "Buffer: %d points" % (self.fullness,),
            "Playback: %d kpps, %d points played" % (self.point_rate, self.point_count),
            "Source: %d, flags 0x%x" % (self.source, self.source_flags),
        ]
        for l in lines:
            print(prefix + l)


class BroadcastPacket:
    """Represents a broadcast packet from the DAC.

    Protocol reference: https://ether-dream.com/protocol.html#broadcast
    """

    def __init__(self, data, ip=None):
        """Initialize from a chunk of data."""
        self.mac = data[:6]
        (
            self.hw_revision,
            self.sw_revision,
            self.buffer_capacity,
            self.max_point_rate,
        ) = struct.unpack("<HHHI", data[6:16])
        self.status = Status(data[16:36])

    def dump(self, prefix=" - "):
        """Dump to a string."""
        lines = [
            "MAC: " + self.macstr(),
            "HW %d, SW %d" % (self.hw_revision, self.sw_revision),
            "Capabilities: max %d points, %d kpps"
            % (self.buffer_capacity, self.max_point_rate),
        ]
        for l in lines:
            print(prefix + l)
        self.status.dump(prefix)

    def macstr(self):
        return "".join("%02x" % c for c in self.mac)


class DAC:
    """A connection to a DAC.

    Protocol reference: https://ether-dream.com/protocol.html
    """

    def __init__(self, host, bp):
        self.macstr = bp.macstr()
        self.firmware_string = "-"
        self.got_broadcast(bp)

        try:
            t1 = time.time()
            self.connect(host)
            t = time.time() - t1
            self.conn_status = "ok (%d ms)" % (t * 500)

            if self.last_broadcast.sw_revision < 2:
                self.firmware_string = "(old)"
            else:
                cmd = struct.pack("<B", ord("v"))
                self.conn.sendall(cmd)
                self.firmware_string = self.read(32).replace("\x00", " ").strip()
        except Exception as e:
            self.conn_status = str(e)
            raise Exception("Could not initialize: " + str(e))

    def got_broadcast(self, bp):
        self.last_broadcast = bp
        self.last_broadcast_time = time.time()

    def read(self, l):
        """Read exactly length bytes from the connection."""
        while l > len(self.buf):
            self.buf += self.conn.recv(4096)

        obuf = self.buf
        self.buf = obuf[l:]
        return obuf[:l]

    def read_response(self, cmd):
        """Read a response from the DAC."""
        data = self.read(22)
        response = data[0]
        cmdR = data[1]
        status = Status(data[2:])

        status.dump()

        if cmdR != cmd:
            raise ProtocolError("expected resp for %r, got %r" % (cmd, cmdR))

        if response != RESPONSE_ACK:
            raise ProtocolError("expected ACK, got %r" % (response,))

        self.last_status = status
        return status

    def connect(self, host, port=COMMUNICATION_PORT):
        """Connect to the DAC over TCP."""
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(0.2)
        conn.connect((host, port))
        self.conn = conn
        self.buf = b""

        first_status = self.read_response(COMMAND_PING)
        first_status.dump()

    def begin(self, low_water_mark, point_rate):
        cmd = struct.pack("<BHI", COMMAND_BEGIN_PLAYBACK, low_water_mark, point_rate)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_BEGIN_PLAYBACK)

    def update(self, low_water_mark, point_rate):
        cmd = struct.pack("<BHI", COMMAND_UPDATE, low_water_mark, point_rate)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_UPDATE)

    def encode_point(self, point):
        return pack_point(*point)

    def write(self, points):
        epoints = list(map(self.encode_point, points))
        cmd = struct.pack("<BH", COMMAND_WRITE_DATA, len(epoints))
        self.conn.sendall(cmd + b"".join(epoints))
        return self.read_response(COMMAND_WRITE_DATA)

    def prepare(self):
        cmd = struct.pack("<B", COMMAND_PREPARE_STREAM)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_PREPARE_STREAM)

    def stop(self):
        cmd = struct.pack("<B", COMMAND_STOP)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_STOP)

    def estop(self):
        cmd = struct.pack("<B", COMMAND_EMERGENCY_STOP)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_EMERGENCY_STOP)

    def clear_estop(self):
        cmd = struct.pack("<B", COMMAND_CLEAR_ESTOP)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_CLEAR_ESTOP)

    def ping(self):
        cmd = struct.pack("<B", COMMAND_PING)
        self.conn.sendall(cmd)
        return self.read_response(COMMAND_PING)

    def play_stream(self, stream, point_rate=30000, buf_size=1799):
        # First, prepare the stream
        if self.last_status.playback_state == PLAYBACK_STATE_PLAYING:
            raise Exception("Could not play stream. DAC already playing.")
        elif self.last_status.playback_state == PLAYBACK_STATE_IDLE:
            self.prepare()

        started = False

        while True:
            # How much room is there in the buffer?
            cap = buf_size - self.last_status.fullness
            points = []
            for _ in range(cap):
                try:
                    point = next(stream)
                    points.append(point)
                except StopIteration:
                    break

            if cap < 100:
                time.sleep(0.005)
                cap += 150

            self.write(points)

            if not started:
                self.begin(0, point_rate)
                started = True


def find_dac():
    """Listen for a single broadcast packet from the DAC, and return a new instance of DAC when found."""

    print("Finding DAC...")

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", BROADCAST_PORT))

    data, addr = s.recvfrom(1024)
    bp = BroadcastPacket(data)
    print("DAC found. Broadcast packet from %s: " % (addr,))
    bp.dump()

    return DAC(str(addr[0]), bp)
