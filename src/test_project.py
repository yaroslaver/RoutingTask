import pytest
import os.path
from subnet_generator import SubnetGen
from addresses import IpAddr, SubnetAddr
from main import validate_ip, validate_n
from router import Router

PATH_TO_SUBNETS = "data/autogen.txt"
PATH_TO_OUTFILE = "data/out.txt"

class TestSubnetGen:

    def test_check_file_exists(self):
        n = 5
        subnet_gen = SubnetGen(n)
        subnet_gen.generate_subnet_addrs()
        assert os.path.isfile(PATH_TO_SUBNETS)
        os.remove(PATH_TO_SUBNETS)

    def test_quantity_gen_1(self):
        n = 5
        subnet_gen = SubnetGen(n)
        subnet_gen.generate_subnet_addrs()
        with open(PATH_TO_SUBNETS, "r") as out_file:
            assert n == len(out_file.readlines())
        os.remove(PATH_TO_SUBNETS)

    def test_quantity_gen_2(self):
        n = 1000
        subnet_gen = SubnetGen(n)
        subnet_gen.generate_subnet_addrs()
        with open(PATH_TO_SUBNETS, "r") as out_file:
            assert n == len(out_file.readlines())
        os.remove(PATH_TO_SUBNETS)

class TestAddressClasses:

    def test_ip_addr_str(self):
        ip_list = [127, 0, 0, 1]
        ip_addr = IpAddr(ip_list)
        assert ip_addr.get_str_addr() == "127.0.0.1"

    def test_ip_addr_list(self):
        ip_list = [127, 0, 0, 1]
        ip_addr = IpAddr(ip_list)
        assert ip_addr.get_list_addr() == ip_list

    def test_subnet_addr_str(self):
        subnet_list = [204, 25, 0, 0, 16]
        subnet_addr = SubnetAddr(subnet_list[:-1], subnet_list[-1])
        assert subnet_addr.get_str_addr() == "204.25.0.0/16"

    def test_subnet_addr_list(self):
            subnet_list = [204, 25, 0, 0, 16]
            subnet_addr = SubnetAddr(subnet_list[:-1], subnet_list[-1])
            assert subnet_addr.get_list_addr() == [204, 25, 0, 0]

    def test_subnet_addr_prefix(self):
            subnet_list = [204, 25, 0, 0, 16]
            subnet_addr = SubnetAddr(subnet_list[:-1], subnet_list[-1])
            assert subnet_addr.get_prefix() == 16

class TestMainValidate:

    def test_validate_n_1(self):
        with pytest.raises(ValueError):
            validate_n("-1")

    def test_validate_n_2(self):
        with pytest.raises(ValueError):
            validate_n("")

    def test_validate_n_3(self):
        with pytest.raises(ValueError):
            validate_n(" ")

    def test_validate_n_4(self):
        with pytest.raises(ValueError):
            validate_n("5.7")

    def test_validate_n_5(self):
        with pytest.raises(ValueError):
            validate_n("-5.7")
        
    def test_validate_n_6(self):
        with pytest.raises(ValueError):
            validate_n("number")

    def test_validate_n_7(self):
        with pytest.raises(ValueError):
            validate_n("n")

    def test_validate_n_8(self):
        with pytest.raises(ValueError):
            validate_n("01")

    def test_validate_n_9(self):
        with pytest.raises(ValueError):
            validate_n("000100")

    def test_validate_n_10(self):
        assert 10 == validate_n("10")

    def test_validate_ip_1(self):
        with pytest.raises(ValueError):
            validate_ip("0.01.0.0")

    def test_validate_ip_2(self):
        with pytest.raises(ValueError):
            validate_ip("0.010.0.0")

    def test_validate_ip_3(self):
        with pytest.raises(ValueError):
            validate_ip("0.000.0.0")

    def test_validate_ip_4(self):
        with pytest.raises(ValueError):
            validate_ip("0.0.1124.0")

    def test_validate_ip_5(self):
        with pytest.raises(ValueError):
            validate_ip("0..0.0")

    def test_validate_ip_6(self):
        with pytest.raises(ValueError):
            validate_ip("185.64.0.0.")

    def test_validate_ip_7(self):
        with pytest.raises(ValueError):
            validate_ip("185.64.0")

    def test_validate_ip_8(self):
        with pytest.raises(ValueError):
            validate_ip("185.6gdg4.0.0")

    def test_validate_ip_9(self):
        with pytest.raises(ValueError):
            validate_ip("185.64.256.0")

    def test_validate_ip_10(self):
        with pytest.raises(ValueError):
            validate_ip("185.64.-154.0")

    def test_validate_ip_11(self):
        with pytest.raises(ValueError):
            validate_ip("")

    def test_validate_ip_12(self):
        with pytest.raises(ValueError):
            validate_ip(" ")

    def test_validate_ip_13(self):
        with pytest.raises(ValueError):
            validate_ip("155.62.62.5.128")

    def test_validate_ip_14(self):
        assert "127.0.0.1" == validate_ip("127.0.0.1").get_str_addr()

class TestRouter:

    def test_find_subnet_1(self):
        ip_list = [127, 16, 0, 64]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet_list = ["127.16.0.0/16\n", "1.64.0.0/10\n"]
        with open(PATH_TO_SUBNETS, "w") as autogen_file:
            autogen_file.writelines(subnet_list)
        subnet = router.find_subnet(len(subnet_list))
        assert subnet.get_str_addr() == "127.16.0.0/16"
        os.remove(PATH_TO_SUBNETS)

    def test_find_subnet_2(self):
        ip_list = [127, 16, 0, 64]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet_list = ["127.16.0.0/16\n", "127.16.0.0/24\n"]
        with open(PATH_TO_SUBNETS, "w") as autogen_file:
            autogen_file.writelines(subnet_list)
        subnet = router.find_subnet(len(subnet_list))
        assert subnet.get_str_addr() == "127.16.0.0/24"
        os.remove(PATH_TO_SUBNETS)

    def test_find_subnet_3(self):
        ip_list = [127, 16, 0, 64]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet_list = ["123.16.0.0/16\n", "1.64.0.0/10\n"]
        with open(PATH_TO_SUBNETS, "w") as autogen_file:
            autogen_file.writelines(subnet_list)
        subnet = router.find_subnet(len(subnet_list))
        assert subnet is None
        os.remove(PATH_TO_SUBNETS)

    def test_find_subnet_4(self):
        ip_list = [127, 16, 0, 64]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet_list = ["127.16.0.0/16\n", "127.16.0.0/16\n"]
        with open(PATH_TO_SUBNETS, "w") as autogen_file:
            autogen_file.writelines(subnet_list)
        subnet = router.find_subnet(len(subnet_list))
        assert subnet.get_str_addr() == "127.16.0.0/16"
        os.remove(PATH_TO_SUBNETS)

    # network address case
    def test_find_subnet_5(self):
        ip_list = [127, 16, 0, 64]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet_list = ["127.16.0.0/16\n", "127.16.0.64/26\n"]
        with open(PATH_TO_SUBNETS, "w") as autogen_file:
            autogen_file.writelines(subnet_list)
        subnet = router.find_subnet(len(subnet_list))
        assert subnet.get_str_addr() == "127.16.0.0/16"
        os.remove(PATH_TO_SUBNETS)

    # broadcast address case
    def test_find_subnet_6(self):
        ip_list = [127, 16, 0, 127]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet_list = ["127.16.0.0/16\n", "127.16.0.64/26\n"]
        with open(PATH_TO_SUBNETS, "w") as autogen_file:
            autogen_file.writelines(subnet_list)
        subnet = router.find_subnet(len(subnet_list))
        assert subnet.get_str_addr() == "127.16.0.0/16"
        os.remove(PATH_TO_SUBNETS)

    def test_write_to_file_1(self):
        ip_list = [127, 16, 0, 127]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet = None
        router.write_subnet_to_file(subnet)
        with open(PATH_TO_OUTFILE, "r") as out_file:
            first_line = out_file.readline().strip()
            second_line = out_file.readline().strip()
        os.remove(PATH_TO_OUTFILE)
        assert first_line == router.ip_addr.get_str_addr()
        assert second_line == "default gateway"

    def test_write_to_file_2(self):
        ip_list = [127, 16, 0, 127]
        ip_addr = IpAddr(ip_list)
        router = Router(ip_addr)
        subnet = SubnetAddr([127, 16, 0, 0], 16)
        router.write_subnet_to_file(subnet)
        with open(PATH_TO_OUTFILE, "r") as out_file:
            first_line = out_file.readline().strip()
            second_line = out_file.readline().strip()
        os.remove(PATH_TO_OUTFILE)
        assert first_line == router.ip_addr.get_str_addr()
        assert second_line == subnet.get_str_addr()
