from datetime import datetime
from typing import Dict, Union

from sqlalchemy import Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from config import DATE_FORMAT


class Base(DeclarativeBase):
    pass


class Result(Base):
    __tablename__ = 'result'

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(Integer())  # Timestamp
    isp: Mapped[str] = mapped_column(String(128))  # ISP
    server_country: Mapped[str] = mapped_column(String(128))  # Server Country
    server_host: Mapped[str] = mapped_column(String(128))  # Server Host
    server_id: Mapped[str] = mapped_column(String(128))  # Server ID
    server_ip: Mapped[str] = mapped_column(String(128))  # Server IP
    server_location: Mapped[str] = mapped_column(String(128))  # Server Location
    server_name: Mapped[str] = mapped_column(String(128))  # Server Name
    server_port: Mapped[str] = mapped_column(String(128))  # Server Port
    ping_jitter: Mapped[str] = mapped_column(String(128))  # Ping Jitter
    ping_latency: Mapped[str] = mapped_column(String(128))  # Ping Latency
    download_bandwidth: Mapped[str] = mapped_column(String(128))  # Download Bandwidth (bytes/sec)
    download_bytes: Mapped[str] = mapped_column(String(128))  # Download Bytes
    download_elapsed: Mapped[str] = mapped_column(String(128))  # Download Elapsed
    upload_bandwidth: Mapped[str] = mapped_column(String(128))  # Upload Bandwidth (bytes/sec)
    upload_bytes: Mapped[str] = mapped_column(String(128))  # Upload Bytes
    upload_elapsed: Mapped[str] = mapped_column(String(128))  # Upload Elapsed
    interface_externalIp: Mapped[str] = mapped_column(String(128))  # Interface ExternalIp
    interface_internalIp: Mapped[str] = mapped_column(String(128))  # Interface InternalIp
    interface_isVpn: Mapped[str] = mapped_column(String(128))  # Interface IsVpn
    interface_macAddr: Mapped[str] = mapped_column(String(128))  # Interface MacAddr
    interface_name: Mapped[str] = mapped_column(String(128))  # Interface Name
    result_url: Mapped[str] = mapped_column(String(128))  # Result URL
    result_id: Mapped[str] = mapped_column(String(128))  # Result ID

    @classmethod
    def add_data(cls, engine: Engine, data: Dict[str, Union[str, Dict[str, str]]]) -> 'Result':
        result = Result.add(
            engine=engine,
            timestamp=data['timestamp'],
            isp=data['isp'],  # ISP
            server_country=data['server']['country'],  # Server Country
            server_host=data['server']['host'],  # Server Host
            server_id=data['server']['id'],  # Server ID
            server_ip=data['server']['ip'],  # Server IP
            server_location=data['server']['location'],  # Server Location
            server_name=data['server']['name'],  # Server Name
            server_port=data['server']['port'],  # Server Port
            ping_jitter=data['ping']['jitter'],  # Ping Jitter
            ping_latency=data['ping']['latency'],  # Ping Latency
            download_bandwidth=data['download']['bandwidth'],  # Download Bandwidth (bytes/sec)
            download_bytes=data['download']['bytes'],  # Download Bytes
            download_elapsed=data['download']['elapsed'],  # Download Elapsed
            upload_bandwidth=data['upload']['bandwidth'],  # Upload Bandwidth (bytes/sec)
            upload_bytes=data['upload']['bytes'],  # Upload Bytes
            upload_elapsed=data['upload']['elapsed'],  # Upload Elapsed
            interface_external_ip=data['interface']['externalIp'],  # Interface ExternalIp
            interface_internal_ip=data['interface']['internalIp'],  # Interface InternalIp
            interface_is_vpn=data['interface']['isVpn'],  # Interface IsVpn
            interface_mac_addr=data['interface']['macAddr'],  # Interface MacAddr
            interface_name=data['interface']['name'],  # Interface Name
            result_url=data['result']['url'],  # Result URL
            result_id=data['result']['id'],  # Result ID
        )
        return result

    @classmethod
    def add(
        cls,
        engine: Engine,
        timestamp: Union[int, str],
        isp: str,
        server_country: str,
        server_host: str,
        server_id: str,
        server_ip: str,
        server_location: str,
        server_name: str,
        server_port: str,
        ping_jitter: str,
        ping_latency: str,
        download_bandwidth: str,
        download_bytes: str,
        download_elapsed: str,
        upload_bandwidth: str,
        upload_bytes: str,
        upload_elapsed: str,
        interface_external_ip: str,
        interface_internal_ip: str,
        interface_is_vpn: str,
        interface_mac_addr: str,
        interface_name: str,
        result_url: str,
        result_id: str,
    ) -> 'Result':
        with Session(engine) as session:
            result = Result(
                timestamp=(
                    timestamp if isinstance(timestamp, int) else datetime.strptime(timestamp, DATE_FORMAT).timestamp()
                ),
                isp=isp,
                server_country=server_country,
                server_host=server_host,
                server_id=server_id,
                server_ip=server_ip,
                server_location=server_location,
                server_name=server_name,
                server_port=server_port,
                ping_jitter=ping_jitter,
                ping_latency=ping_latency,
                download_bandwidth=download_bandwidth,
                download_bytes=download_bytes,
                download_elapsed=download_elapsed,
                upload_bandwidth=upload_bandwidth,
                upload_bytes=upload_bytes,
                upload_elapsed=upload_elapsed,
                interface_externalIp=interface_external_ip,
                interface_internalIp=interface_internal_ip,
                interface_isVpn=interface_is_vpn,
                interface_macAddr=interface_mac_addr,
                interface_name=interface_name,
                result_url=(
                    f'https://www.speedtest.net/result/c/{result_id}'
                    if result_url is None or result_url == 'Unknown'
                    else result_url
                ),
                result_id=result_id,
            )
            session.add(result)
            session.commit()
            return result
