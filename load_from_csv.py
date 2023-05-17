from datetime import datetime

import pandas as pd

from db_models import Base, Result
from engine import engine


def to_dt(s: str) -> int:
    try:
        return int(datetime.strptime(s, '%m/%d/%Y %H:%M:%S').timestamp())
    except:
        return int(datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timestamp())


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    for file in [
        'Speedtest - Speedtest [server 16974] data.csv',
        'Speedtest - Speedtest [server 1783] data.csv',
    ]:
        df = pd.read_csv(file)

        for col in df.columns:
            print(f'{col:40} -> {df[col].map(str).map(len).max()}')

        for row in df.iterrows():
            result_id = row[1]['result_id']
            result_url = row[1]['result_url']
            result_url = f'https://www.speedtest.net/result/c/{result_id}' if pd.isna(result_url) else result_url
            Result.add(
                engine=engine,
                timestamp=to_dt(row[1]['ts']),
                isp=row[1]['isp'],
                server_country=row[1]['server_country'],
                server_host=row[1]['server_host'],
                server_id=row[1]['server_id'],
                server_ip=row[1]['server_ip'],
                server_location=row[1]['server_location'],
                server_name=row[1]['server_name'],
                server_port=row[1]['server_port'],
                ping_jitter=row[1]['ping_jitter'],
                ping_latency=row[1]['ping_latency'],
                download_bandwidth=row[1]['download_bandwidth_bytes_sec'],
                download_bytes=row[1]['download_bytes'],
                download_elapsed=row[1]['download_elapsed'],
                upload_bandwidth=row[1]['upload_bandwidth_bytes_sec'],
                upload_bytes=row[1]['upload_bytes'],
                upload_elapsed=row[1]['upload_elapsed'],
                interface_external_ip=row[1]['interface_externalip'],
                interface_internal_ip=row[1]['interface_internalip'],
                interface_is_vpn=row[1]['interface_isvpn'],
                interface_mac_addr=row[1]['interface_macaddr'],
                interface_name=row[1]['interface_name'],
                result_url=result_url,
                result_id=result_id,
            )
