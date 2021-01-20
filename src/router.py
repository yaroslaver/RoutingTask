from addresses import SubnetAddr


class Router:

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self.best_subnet = None

    def find_subnet(self, n):
        with open("data/autogen.txt", "r") as file:
            for _ in range(0, n):
                cur_subnet = file.readline().strip()
                cur_subnet = self.__parse_subnet(cur_subnet)
                
                # cheking for network address
                if cur_subnet.get_list_addr() == self.ip_addr.get_list_addr():
                    continue

                bin_xor_res = []
                for oct_sub, oct_ip in zip(cur_subnet.get_list_addr(), self.ip_addr.get_list_addr()):
                    bin_oct = bin(oct_sub ^ oct_ip)[2:].zfill(8)
                    bin_xor_res.append(bin_oct)
                
                bin_xor_res = "".join(bin_xor_res)

                if bin_xor_res.startswith("0" * cur_subnet.get_prefix()):
                    # checking for broadcast address
                    if bin_xor_res.endswith("1" * (32 - cur_subnet.get_prefix())):
                        continue
                    else:
                        if self.best_subnet is None:
                            self.best_subnet = cur_subnet
                        elif self.best_subnet.get_prefix() < cur_subnet.get_prefix():
                            self.best_subnet = cur_subnet

        return self.best_subnet

    def write_subnet_to_file(self, subnet):
        with open("data/out.txt", "w") as out_file:
            if subnet is not None:
                out_file.write(f"{self.ip_addr}\n{subnet}")
            else:
                out_file.write(f"{self.ip_addr}\ndefault gateway")

    def __parse_subnet(self, str_subnet):
        str_subnet = str_subnet.replace('/', '.')
        subnet = str_subnet.split(sep=".")
        subnet = [int(elem) for elem in subnet]
        subnet = SubnetAddr(subnet[0:-1], subnet[-1])

        return subnet
