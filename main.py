import sys
import socket
import datetime

from dataclasses import dataclass

@dataclass
class IcmpHeader:
    icmp_type: int
    icmp_code: int
    icmp_checksum: str = ''

def main():
    icmph = IcmpHeader(8, 0)

    dest_arg = sys.argv[1]

    # dest_port = 80 if True else 443
    dest_tuple = (socket.gethostbyname(dest_arg), 80)

    try:
        n_of_pings = sys.argv[2]
    except IndexError:
        n_of_pings = -1

    icmp_type_bits = int_to_bits(icmph.icmp_type)
    print(icmp_type_bits)

    icmp_code_bits = int_to_bits(icmph.icmp_code)
    print(icmp_code_bits)

    icmph.icmp_checksum = create_checksum(icmp_type_bits, icmp_code_bits)
    print(icmph.icmp_checksum)

    print(datetime.datetime.now().isoformat())
    listen(int(n_of_pings), dest_tuple, icmph)

def listen(wanted_n_of_pings: int, dest: tuple, icmp_header: IcmpHeader):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)

    # n_of_pings = 0
    # end = False

    # while True:
    try:
        sock.connect(dest)
    except (TimeoutError, InterruptedError):
        print("Connection timeouted or got interrupetd by some other connection")

    # TODO: Send icmp_header as an actual header in bits
    for _ in range(wanted_n_of_pings):
        sock.send(icmp_header)
        start_time = datetime.datetime.now().isoformat()

        end_time = datetime.datetime.now().isoformat()

        time_between_messages = calculate_time(start_time, end_time)
        print(time_between_messages)

    # The socket needs to be shutdown before closing connection
    sock.shutdown(1)
    sock.close()


def int_to_bits(icmp_int: int) -> str:
    bits = []
    mask = 1 << 8 - 1

    for _ in range(8):
        if (icmp_int & mask):
            bits.append('1')
        else:
            bits.append('0')

        mask >>= 1

    return ''.join(bits)

def create_checksum(icmp_type: str, icmp_code: str) -> str:
    icmp_bit_sum = bit_string_sum(icmp_type, icmp_code)
    return ''.join(ones_complement(icmp_bit_sum))

def bit_string_sum(icmp_type: str, icmp_code: str) -> str:
    result = ''
    length = 8
    carry = 0

    for i in range(length -1, -1, -1):
        icmp_type_bit = int(icmp_type[i])
        icmp_code_bit = int(icmp_code[i])

        sum = (icmp_type_bit ^ icmp_code_bit ^ carry) + 48
        result = chr(sum) + result

        carry = (icmp_type_bit & icmp_code_bit) | (icmp_code_bit & carry) | (icmp_type_bit & carry)

    if carry == 1:
        result = '1' + result

    return result

def ones_complement(icmp_header_sum: str) -> list:
    sum = []
    i = len(icmp_header_sum) - 1

    while i >= 0:
        if i == 1:
            sum.append('0')
        else:
            sum.append('1')

        i = i - 1

    return sum

def calculate_time(start_time, end_time):
    return end_time - start_time


if __name__ == "__main__":
    main()

