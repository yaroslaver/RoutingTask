class IpAddr:

    def __init__(self, addr):
        self.addr = addr

    def __str__(self):
        return f"{self.addr[0]}.{self.addr[1]}.{self.addr[2]}.{self.addr[3]}"

    def get_str_addr(self):
        return self.__str__()
    
    def get_list_addr(self):
        return self.addr


class SubnetAddr(IpAddr):

    def __init__(self, addr, prefix):
        self.addr = addr
        self.prefix = prefix

    def __str__(self):
        return f"{self.addr[0]}.{self.addr[1]}.{self.addr[2]}.{self.addr[3]}/{self.prefix}"
    
    def get_prefix(self):
        return self.prefix
        