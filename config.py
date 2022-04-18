class Base:
    port = 5867


class Test(Base):
    listen_address = ''
    data_rows = (
        b'first response',
        b'second response',
        b'third response',
    )
    allowed_hosts = (
        '127.0.0.1',
    )


class Prod(Base):
    listen_address = ''
    data_rows = (
        '',
    )
    allowed_hosts = (
        '',
    )
