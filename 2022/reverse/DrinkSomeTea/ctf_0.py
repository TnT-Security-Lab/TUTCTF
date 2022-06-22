def main():
    try:
        import unicorn
    except ModuleNotFoundError:
        print("unicorn Error: pip install unicorn")
        exit()
    import unicorn.x86_const
    import base64

    flag = input("input your password: ")
    if not len(flag) == 32:
        print("wrong")
        return
    CODE_ADDR = 0x41000
    CODE_LEN = 0x10000
    DATA_ADDR = 0x51000
    DATA_LEN = 0x10000
    STACK_ADDR = DATA_ADDR + 0x9000
    data = bytearray([ord(c) ^ 0xAB for c in flag])
    keys = base64.b64decode(b"Z0UjAe/Nq4mYutz+EDJUdg==")
    code = base64.b64decode(
        b"SDPASD2vAAAAfw2QkJCQgDQHfEj/wOvrPSs9Kj0pPSgpKyovNfWxNPWrwXx8fHyXKvWsvZx4fYw68UB+OE2EPfWrPb2TeT19ozhNhH29Pf2UtfodOvW0vZx4OH2kOvFAfThNhD31sz29k3k5fas4TYR9vj3/vX09/4VjAsg99XI99WhY/7l+/4F7A1M0H7kx8Qj5fD33cjHxGPl4PfdoWPdL9yN4OPcjdDj3K3A9xXx8fHw9xHx8fHyXwCciIyE9ID0hPSI9Iw=="
    )
    machine = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    machine.mem_map(CODE_ADDR, CODE_LEN)
    machine.mem_write(CODE_ADDR, code)
    machine.mem_map(DATA_ADDR, DATA_LEN)
    machine.mem_write(DATA_ADDR, bytes(data))
    machine.mem_write(DATA_ADDR + 0x1000, keys)
    machine.reg_write(unicorn.x86_const.UC_X86_REG_RBP, STACK_ADDR)
    machine.reg_write(unicorn.x86_const.UC_X86_REG_RSP, STACK_ADDR)
    machine.reg_write(unicorn.x86_const.UC_X86_REG_RCX, DATA_ADDR)
    machine.reg_write(unicorn.x86_const.UC_X86_REG_RDX, DATA_ADDR + 0x1000)
    machine.reg_write(unicorn.x86_const.UC_X86_REG_RDI, CODE_ADDR + 0x18)
    machine.emu_start(CODE_ADDR, CODE_ADDR + len(code))
    data = bytearray(machine.mem_read(DATA_ADDR, 32))
    if base64.b64encode(data) == b"M0EVk4axKRsXVUSramrA4wfg5xarslKPxZgP3WVYDOY=":
        print("success")
    else:
        print("wrong, try harder")


if __name__ == "__main__":
    main()
