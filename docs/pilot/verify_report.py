"""Check the packaged pilot report using only Python's standard library."""
from pathlib import Path
from decimal import Decimal as D
import csv
import hashlib
import json
import re
import struct
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def table(name):
    with (ROOT / 'data' / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def png_info(path):
    raw = path.read_bytes()
    require(raw[:8] == b'\x89PNG\r\n\x1a\n', 'Invalid PNG: ' + path.name)
    pos, dimensions, ended = 8, None, False
    import zlib
    while pos < len(raw):
        size = struct.unpack('>I', raw[pos:pos+4])[0]
        kind, content = raw[pos+4:pos+8], raw[pos+8:pos+8+size]
        require(pos + 12 + size <= len(raw), 'Truncated PNG')
        crc = struct.unpack('>I', raw[pos+8+size:pos+12+size])[0]
        require(zlib.crc32(kind + content) & 0xffffffff == crc, 'PNG CRC mismatch')
        require(kind not in {b'eXIf', b'tIME', b'tEXt', b'iTXt', b'zTXt'}, 'Unexpected image metadata')
        if kind == b'IHDR':
            dimensions = list(struct.unpack('>II', content[:8]))
        if kind == b'IEND':
            ended = True
        pos += size + 12
    require(dimensions and min(dimensions) > 0 and ended, 'Incomplete PNG')
    return dimensions

def anchor(heading):
    value = heading.strip().lower()
    value = ''.join(c for c in value if unicodedata.category(c)[0] not in {'P', 'S'} or c in '_-')
    return value.replace(' ', '-')

def jpeg_info(path):
    raw = path.read_bytes()
    require(raw[:3] == b'\xff\xd8\xff' and raw[-2:] == b'\xff\xd9', 'Invalid JPEG: ' + path.name)
    pos, dimensions = 2, None
    while pos < len(raw):
        require(raw[pos] == 255, 'Invalid JPEG marker')
        while raw[pos] == 255:
            pos += 1
        marker = raw[pos]
        pos += 1
        if marker in {0xD9,0xDA}:
            break
        size = struct.unpack('>H', raw[pos:pos+2])[0]
        require(size >= 2 and pos+size <= len(raw), 'Truncated JPEG')
        content = raw[pos+2:pos+size]
        if marker in {0xC0,0xC1,0xC2}:
            height,width = struct.unpack('>HH',content[1:5])
            dimensions = [width,height]
        if 0xE0 <= marker <= 0xEF or marker == 0xFE:
            require(marker == 0xE0 and content.startswith(b'JFIF\x00'), 'Unexpected JPEG metadata')
        pos += size
    require(dimensions and min(dimensions) > 0, 'JPEG dimensions missing')
    return dimensions

def check_links():
    count = 0
    for document in ROOT.glob('*.md'):
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', document.read_text(encoding='utf-8')):
            if target.startswith(('https://', 'http://', 'mailto:')):
                continue
            file_part, _, fragment = target.partition('#')
            path = (document.parent / file_part).resolve() if file_part else document
            require(path.is_relative_to(ROOT), 'Link escapes package: ' + target)
            require(path.exists(), 'Missing link target: ' + target)
            if fragment:
                headings = re.findall(r'^#{1,6}\s+(.+)$', path.read_text(encoding='utf-8'), re.M)
                require(fragment in {anchor(h) for h in headings}, 'Missing heading: ' + target)
            count += 1
    html = (ROOT / 'dashboard.html').read_text(encoding='utf-8')
    for target in re.findall(r'(?:href|src)="([^"]+)"', html):
        if target.startswith('#'):
            require(f'id="{target[1:]}"' in html, 'Missing dashboard view')
        else:
            path = (ROOT / target).resolve()
            require(path.is_relative_to(ROOT) and path.exists(), 'Missing dashboard target')
        count += 1
    require(not re.search(r'https?://|fetch\(|XMLHttpRequest|WebSocket', html), 'Dashboard has external requests')
    return count

def validate():
    metrics = table('metrics.csv')
    require(len({r['metric'] for r in metrics}) == len(metrics), 'Duplicate metric names')
    values = {r['metric']: D(r['value']) for r in metrics}
    require(all(r['unit'] and r['label'] for r in metrics), 'Metric definition missing')
    daily = table('daily.csv')
    require([int(r['source_day']) for r in daily] == list(range(1, 11)), 'Daily order mismatch')
    require([r['pilot_date'] for r in daily] == [f'2026-10-{d:02d}' for d in range(1, 11)], 'Pilot dates mismatch')
    totals = {k: sum(int(r[k]) for r in daily) for k in ['visitors', 'registrations', 'profiles']}
    require(totals == dict(visitors=486, registrations=131, profiles=418), 'Daily totals mismatch')
    require(values['visitors'] == totals['visitors'] and values['accounts'] == totals['registrations']
            and values['build_success'] == totals['profiles'], 'Daily totals differ from metrics')
    require(values['build_success'] + values['build_abandon'] + values['build_error'] == values['build_requests'], 'Build totals mismatch')
    require(sum(values[k] for k in ['nps_promoters', 'nps_passives', 'nps_detractors']) == values['survey_responses'] == 21, 'NPS groups mismatch')
    require(sum(values[k] for k in ['limit_sufficient', 'limit_five', 'limit_unlimited']) == 21, 'Quota groups mismatch')
    require(abs(values['nps_recalculated'] - (values['nps_promoters'] - values['nps_detractors']) / 21 * 100) < D('.0001'), 'NPS mismatch')
    fractions = {
        'outreach_acceptance': (9,14), 'reach_share': (11200,34600), 'reach_to_visit': (486,11200),
        'visit_to_signup_start': (187,486), 'signup_completion': (131,187), 'account_activation': (104,131),
        'visit_activation': (104,486), 'survey_response_rate': (21,104), 'limit_users_rate': (37,104),
        'd1_rate': (25,104), 'd7_rate': (5,54), 'active_three_days_rate': (11,104),
        'build_success_rate': (418,497), 'abandon_rate': (47,497), 'build_error_rate': (32,497),
        'ellis_rate': (4,21), 'limit_sufficient_rate': (9,21), 'limit_five_rate': (8,21),
        'limit_unlimited_rate': (4,21), 'conversion_recalculated': (131,486),
    }
    for key, (numerator, denominator) in fractions.items():
        require(abs(values[key] - D(numerator) / denominator * 100) < D('.0001'), 'Fraction mismatch: ' + key)
    require(abs(values['profiles_per_activated_recalculated'] - D(418)/104) < D('.0001'), 'Profiles mean mismatch')
    ratings = table('feature-ratings.csv')
    require(len(ratings) == 9, 'Rating row mismatch')
    for row in ratings:
        bins = [int(row[k]) for k in ['score_9_10', 'score_7_8', 'score_5_6', 'score_0_4']]
        require(sum(bins) == int(row['response_count']) == 21, 'Rating response total mismatch')
        lower = sum(a*b for a,b in zip(bins,[9,7,5,0])) / 21
        upper = sum(a*b for a,b in zip(bins,[10,8,6,4])) / 21
        require(lower-.05 <= float(row['mean_score']) <= upper+.05, 'Impossible rating mean')
        require(D(row['mean_score']) == values['rating_' + {'compare_saved':'compare_saved', 'build_speed':'build_speed'}.get(row['feature'], row['feature'])], 'Rating metric mismatch')
    countries = table('country-distribution.csv')
    require(sum(int(r['percent']) for r in countries) == 100, 'Country percentages mismatch')
    require(len(table('feedback-themes.csv')) == 10, 'Feedback row mismatch')
    criteria = table('success-criteria.csv')
    require(len(criteria) == 8, 'Criterion count mismatch')
    for row in criteria:
        if row['criterion'] == 'expense':
            low, high = map(D, row['reported_value'].split('–'))
            fulfilled = low <= high <= D(row['threshold'])
        else:
            fulfilled = D(row['reported_value']) >= D(row['threshold'])
        require(row['reported_result'].startswith('fulfilled') == fulfilled, 'Criterion result mismatch')
    require(sum(r['reported_result'].startswith('fulfilled') for r in criteria) == 4, 'Criteria totals mismatch')
    provenance = json.loads((ROOT / 'data/provenance.json').read_text(encoding='utf-8'))
    require(provenance['pilot_period'] == {'start':'2026-10-01','end':'2026-10-10','inclusive_days':10}, 'Provenance dates mismatch')
    screenshots = {p.name: png_info(p) for p in sorted((ROOT / 'assets').glob('*.png'))}
    require(set(screenshots) == {'pilot-overview.png','pilot-quality.png','pilot-feedback.png'}, 'Report image set mismatch')
    umami_images = {p.name: jpeg_info(p) for p in sorted((ROOT/'assets').glob('*.jpg'))}
    require(set(umami_images) == {'umami-overview.jpg','umami-events.jpg','umami-sessions.jpg'}, 'Umami image set mismatch')
    capture_info = json.loads((ROOT/'data/umami-capture-info.json').read_text(encoding='utf-8'))
    require(capture_info['status'] == 'PASS' and capture_info['publication_language'] == 'en', 'Umami capture checks missing')
    charts = list((ROOT / 'assets').glob('*.svg'))
    require(len(charts) == 3, 'Chart count mismatch')
    for path in charts:
        tree = ET.fromstring(path.read_text(encoding='utf-8'))
        ns = '{http://www.w3.org/2000/svg}'
        require(tree.tag == ns+'svg' and tree.find(ns+'title') is not None and tree.find(ns+'desc') is not None, 'SVG label missing')
        require(not any(e.tag in {ns+'script', ns+'foreignObject'} for e in tree.iter()), 'Active SVG content')
        require(all(not k.lower().startswith('on') and not k.endswith('href') for e in tree.iter() for k in e.attrib), 'External SVG content')
    return dict(metric_count=len(metrics), daily_totals=totals, percentage_checks=len(fractions),
                nps_recalculated='9.5238', criteria_met=4, criteria_total=8,
                rating_distributions=9, relative_links_checked=check_links(),
                report_image_dimensions=screenshots, umami_image_dimensions=umami_images, svg_charts=3,
                verification_scope='arithmetic_links_assets_and_package_integrity')

def verify_manifest():
    manifest = json.loads((ROOT / 'file-manifest.json').read_text(encoding='utf-8'))
    expected = {r['path'] for r in manifest['files']}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name != 'file-manifest.json' and '__pycache__' not in p.parts}
    require(actual == expected, 'Package file list differs from manifest')
    for row in manifest['files']:
        path = (ROOT / row['path']).resolve()
        require(path.is_relative_to(ROOT), 'Manifest path escapes package')
        raw = path.read_bytes()
        require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'Hash mismatch: ' + row['path'])
    return len(expected)

if __name__ == '__main__':
    try:
        results = validate()
        count = verify_manifest()
        print(f"PASS: {count} files; {results['metric_count']} metrics; arithmetic, links, images and checksums verified")
        print('Scope: report calculations, links, images and file integrity.')
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit('FAIL: ' + str(exc))
