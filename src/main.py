from subnet_generator import SubnetGen
from addresses import IpAddr
from router import Router

def validate_ip(ip_addr):
    ip_addr = ip_addr.split(sep=".")

    if len(ip_addr) != 4:
        raise ValueError("Incorrect IP entry. (Template x.x.x.x).")

    for oct in ip_addr:
        if len(oct) > 3:
            raise ValueError("All octets must be in the range [0 - 255].")
        elif len(oct) > 1 and oct.startswith("0"):
            raise ValueError("All octets must be in the range [0 - 255].")

    try:
        ip_addr = [int(oct) for oct in ip_addr]
    except ValueError:
        raise ValueError("All octets must be in the range [0 - 255].")

    for oct in ip_addr:
        if oct < 0 or oct > 255:
            raise ValueError("All octets must be in the range [0 - 255].")
    
    return IpAddr(ip_addr)

def validate_n(n):
    if len(n) > 1 and n.startswith("0"):
        raise ValueError("Number of subnets must be positive integer number.")

    try:
        n = int(n)
    except ValueError:
        raise ValueError("Number of subnets must be positive integer number.")

    if n <= 0:
        raise ValueError("Number of subnets must be positive integer number.")

    return n


if __name__ == "__main__":
    try:
        try:
            with open("data/in.txt", "r") as in_file:
                n = in_file.readline().strip()
                ip_addr = in_file.readline().strip()
        except FileNotFoundError:
            raise FileNotFoundError("File in.txt was not found.")

        n = validate_n(n)
        ip_addr = validate_ip(ip_addr)

        router = Router(ip_addr)
        sg = SubnetGen(n)
        sg.generate_subnet_addrs()
        best_subnet = router.find_subnet(n)
        router.write_subnet_to_file(best_subnet)
    except ValueError as val_err:
        print(val_err)
    except FileNotFoundError as file_err:
        print(file_err)
