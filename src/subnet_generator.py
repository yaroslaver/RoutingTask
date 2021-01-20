import random
from addresses import SubnetAddr


class SubnetGen:

    def __init__(self, n=1000):
        self.n = n

    def generate_subnet_addrs(self):
        with open("data/autogen.txt", "w") as out_file:
            for _ in range(self.n):
                prefix = random.randint(0, 30) # more than 2 hosts in subnet
                full_octets = prefix // 8
                rest_of_octet = prefix % 8

                subnet_addr = self.__generate_subnet_addr(full_octets, rest_of_octet, prefix)
                out_file.write(f"{subnet_addr}\n")

    def __generate_subnet_addr(self, full_octets, rest_of_octet, prefix):
        result_addr = [random.randint(0, 255) for _ in range(full_octets)]
        if rest_of_octet != 0:
            bits_of_octet = [random.randint(0, 1) for _ in range(rest_of_octet)]
            octet = 0
            i = 0
            while i < rest_of_octet:
                octet += bits_of_octet[i] * 2**(7 - i)
                i += 1
            result_addr.append(octet)
            result_addr += [0] * (4 - full_octets - 1)
        else:
            result_addr += [0] * (4 - full_octets)

        subnet_addr = SubnetAddr(result_addr, prefix)

        return subnet_addr
