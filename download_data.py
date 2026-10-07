"""Download official data, preserve source rows, and record provenance.

Run: .venv/bin/python download_data.py
No Census API key is required: this script uses official bulk summary files.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import time
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'data' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
YEAR = 2024
TABLES = ['B28002', 'B28003', 'B19013', 'C17002', 'B01002']
BASE = f'https://www2.census.gov/programs-surveys/acs/summary_file/{YEAR}/table-based-SF'
MANIFEST = RAW / 'download_manifest.json'
manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def request(url):
    """Keep TLS certificate verification enabled; retry temporary errors."""
    last = None
    for attempt in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={
                'User-Agent': 'NJ-Digital-Equity-Research/1.0'}), timeout=90)
        except Exception as error:
            last = error
            time.sleep(attempt + 1)
    raise last


def record(path, url, **extra):
    manifest[path.name] = dict(url=url, downloaded_utc=datetime.now(timezone.utc).isoformat(),
                               saved_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), **extra)
    MANIFEST.write_text(json.dumps(manifest, indent=2))


def save_bytes(url, filename):
    path = RAW / filename
    if path.exists() and filename in manifest:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[filename]['saved_sha256']
        print('Cached:', filename, flush=True)
        return
    with request(url) as response:
        payload = response.read()
        json.loads(payload) if filename.endswith('.json') else None
    path.write_bytes(payload)
    record(path, url, bytes=len(payload))
    print('Saved:', filename, len(payload), 'bytes', flush=True)


def save_nj_rows(url, filename, geography=False):
    """Stream national files; retain exact NJ state/county/tract source lines.

    We do not store a second copy of the national data. The manifest records
    the SHA-256 digest and byte count of the entire source stream.
    """
    path = RAW / filename
    if path.exists() and filename in manifest:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[filename]['saved_sha256']
        print('Cached:', filename, flush=True)
        return
    digest = hashlib.sha256()
    rows = 0
    byte_count = 0
    tmp = path.with_suffix(path.suffix + '.partial')
    with request(url) as response, tmp.open('wb') as output:
        header = response.readline()
        assert b'GEO_ID' in header, 'Unexpected file format: ' + url
        digest.update(header)
        byte_count += len(header)
        output.write(header)
        columns = header.decode('utf-8-sig').strip().split('|')
        geo_col = columns.index('GEO_ID')
        for line in response:
            digest.update(line)
            byte_count += len(line)
            geo_id = line.decode('utf-8-sig').split('|')[geo_col]
            if re.fullmatch(r'(0400000US34|0500000US34\d{3}|1400000US34\d{9})', geo_id):
                output.write(line)
                rows += 1
    assert rows > 2000, f'Too few retained geographies: {rows}'
    tmp.replace(path)
    record(path, url, retained_rows=rows, source_bytes=byte_count,
           source_sha256=digest.hexdigest(), selection='NJ state, counties, tracts; component 00')
    print('Saved:', filename, rows, 'NJ geography rows', flush=True)


def main():
    save_bytes('https://data.nj.gov/api/views/yjm4-bujw.json', 'nj_assets_metadata.json')
    # Pagination makes a future larger directory reproducible.
    all_rows, offset = [], 0
    while True:
        url = f'https://data.nj.gov/resource/yjm4-bujw.json?$limit=1000&$offset={offset}&$order=:id'
        filename = f'nj_assets_page_{offset}.json'
        save_bytes(url, filename)
        batch = json.loads((RAW / filename).read_text())
        all_rows.extend(batch)
        if len(batch) < 1000:
            break
        offset += 1000
    (RAW / 'nj_assets_all.json').write_text(json.dumps(all_rows, indent=2))
    record(RAW / 'nj_assets_all.json', 'https://data.nj.gov/resource/yjm4-bujw.json',
           rows=len(all_rows), method='Concatenated preserved pages; :id ordering')
    for table in TABLES:
        save_bytes(f'https://api.census.gov/data/{YEAR}/acs/acs5/groups/{table}.json',
                   f'{table}_metadata.json')
        save_nj_rows(f'{BASE}/data/5YRData/acsdt5y{YEAR}-{table.lower()}.dat',
                     f'nj_{table}.dat')
    save_nj_rows(f'{BASE}/documentation/Geos{YEAR}5YR.txt', 'nj_geographies.txt', True)
    print('Download complete. ACS 2024 5-year = 2020-2024 period estimates.', flush=True)


if __name__ == '__main__':
    main()
