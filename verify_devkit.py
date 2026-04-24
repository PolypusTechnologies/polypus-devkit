#!/usr/bin/env python3
"""
verify_devkit.py — Polypus Master Dev Kit verifier (v3)

Parses the <script id="devkit-data"> JSON block from polypus_devkit.html, then:
  • HEAD/GET every JS CDN URL → confirms the file actually loads
  • Hits PyPI JSON API for every Python package → reports latest version
Runs concurrently so ~200 checks finish in under 20 seconds.

Usage:
    python verify_devkit.py                          # defaults to polypus_devkit.html
    python verify_devkit.py polypus_devkit.html
    python verify_devkit.py Polypus_DevKit.html.bak  # verify the original
    python verify_devkit.py --parse-only             # dry run, no network
    python verify_devkit.py --report report.md       # write markdown report
    python verify_devkit.py --no-cdn                 # skip CDN checks
    python verify_devkit.py --no-pypi                # skip PyPI checks

Exits 0 if every entry passes, 1 if any fail, 2 on setup error.
"""

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: this script needs `requests`. Install with:")
    print("    pip install requests")
    sys.exit(2)

# Rich is optional — script still works in plain mode without it
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None
    print("Note: install `rich` for prettier output:  pip install rich\n")


USER_AGENT = 'PolypusDevKitVerifier/3.0 (+https://polypus.tech)'


# ─── Parser ──────────────────────────────────────────────────
def parse_devkit(html: str):
    """Extract data from either v3 JSON block or legacy const JS_LIBS format."""
    # v3 format: <script id="devkit-data"> JSON </script>
    m = re.search(
        r'<script[^>]+id="devkit-data"[^>]*>\s*(\{.*?\})\s*</script>',
        html, re.DOTALL
    )
    if m:
        try:
            data = json.loads(m.group(1))
            return data.get('js', {}), data.get('py', {})
        except json.JSONDecodeError as e:
            raise ValueError(f"v3 JSON block failed to parse: {e}")

    # Legacy format: const JS_LIBS = {...}; const PY_PKGS = {...};
    js_libs, py_pkgs = {}, {}

    js_match = re.search(r'const\s+JS_LIBS\s*=\s*\{(.*?)^\};', html, re.DOTALL | re.MULTILINE)
    if js_match:
        body = js_match.group(1)
        for sec_m in re.finditer(r"(?:^|\s)(['\"]?)([a-zA-Z0-9_-]+)\1\s*:\s*\[(.*?)\n\s*\],", body, re.DOTALL):
            sec = sec_m.group(2)
            items = []
            for em in re.finditer(r"\{([^{}]*?)\}", sec_m.group(3), re.DOTALL):
                entry_text = em.group(1)
                nm = re.search(r"name:\s*'([^']+)'", entry_text)
                cdn = re.search(r"cdn:\s*'([^']+)'", entry_text)
                if nm:
                    items.append({'name': nm.group(1), 'cdn': cdn.group(1) if cdn else ''})
            if items:
                js_libs[sec] = items

    py_match = re.search(r'const\s+PY_PKGS\s*=\s*\{(.*?)^\};', html, re.DOTALL | re.MULTILINE)
    if py_match:
        body = py_match.group(1)
        for sec_m in re.finditer(r"'([a-zA-Z0-9_-]+)'\s*:\s*\[(.*?)\n\s*\],", body, re.DOTALL):
            sec = sec_m.group(1)
            items = []
            for em in re.finditer(r"\{([^{}]*?)\}", sec_m.group(2), re.DOTALL):
                entry_text = em.group(1)
                nm = re.search(r"name:\s*'([^']+)'", entry_text)
                if nm:
                    items.append({'name': nm.group(1)})
            if items:
                py_pkgs[sec] = items

    if js_libs or py_pkgs:
        return js_libs, py_pkgs

    raise ValueError(
        "Couldn't find <script id=\"devkit-data\"> JSON block OR "
        "legacy const JS_LIBS/PY_PKGS declarations in HTML."
    )


# ─── Checkers ─────────────────────────────────────────────────
def check_cdn(section: str, entry: dict) -> dict:
    name = entry['name']
    url = entry.get('cdn', '')
    out = {
        'kind': 'cdn',
        'section': section,
        'name': name,
        'url': url,
        'status': 'fail',
        'detail': '',
        'latency_ms': 0,
    }

    if not url or not url.startswith('http'):
        out['status'] = 'skip'
        out['detail'] = 'native API — no CDN'
        return out

    t0 = time.time()
    try:
        # HEAD first (faster)
        r = requests.head(
            url,
            timeout=12,
            allow_redirects=True,
            headers={'User-Agent': USER_AGENT},
        )
        # Some CDNs / hosts reject HEAD → fall back to GET
        if r.status_code in (403, 405, 501):
            r = requests.get(
                url,
                timeout=12,
                allow_redirects=True,
                headers={'User-Agent': USER_AGENT},
                stream=True,
            )
            # Pull a small chunk to confirm body exists
            chunk = next(r.iter_content(chunk_size=2048), b'') or b''
            r.close()
            if r.status_code == 200 and len(chunk) < 30:
                out['detail'] = f'200 OK but body tiny ({len(chunk)}b — empty?)'
                return out

        out['latency_ms'] = int((time.time() - t0) * 1000)

        if r.status_code == 200:
            redirect_note = ' ↪' if r.url != url else ''
            out['status'] = 'ok'
            out['detail'] = f'200 OK {out["latency_ms"]}ms{redirect_note}'
        else:
            out['detail'] = f'HTTP {r.status_code}'

    except requests.Timeout:
        out['detail'] = 'timeout (>12s)'
    except requests.ConnectionError as e:
        out['detail'] = f'connection error: {str(e)[:60]}'
    except Exception as e:
        out['detail'] = f'{type(e).__name__}: {str(e)[:60]}'

    return out


def check_pypi(section: str, entry: dict) -> dict:
    name = entry['name']
    out = {
        'kind': 'pypi',
        'section': section,
        'name': name,
        'url': f'https://pypi.org/pypi/{name}/json',
        'status': 'fail',
        'detail': '',
        'latency_ms': 0,
    }

    t0 = time.time()
    try:
        r = requests.get(
            f'https://pypi.org/pypi/{name}/json',
            timeout=10,
            headers={'User-Agent': USER_AGENT},
        )
        out['latency_ms'] = int((time.time() - t0) * 1000)

        if r.status_code == 200:
            info = r.json().get('info', {})
            version = info.get('version', '?')
            out['status'] = 'ok'
            out['detail'] = f'v{version}'
            out['version'] = version
        elif r.status_code == 404:
            out['detail'] = 'NOT FOUND on PyPI (wrong package name?)'
        else:
            out['detail'] = f'HTTP {r.status_code}'

    except requests.Timeout:
        out['detail'] = 'timeout (>10s)'
    except Exception as e:
        out['detail'] = f'{type(e).__name__}: {str(e)[:60]}'

    return out


# ─── Output ───────────────────────────────────────────────────
def print_plain(results, elapsed, js_sections, py_sections):
    """Plain-ANSI output when rich isn't installed."""
    G, R, Y, C, M, DIM, B, X = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[95m', '\033[2m', '\033[1m', '\033[0m'

    def color_status(s):
        return {'ok': f'{G}✓ OK  {X}', 'fail': f'{R}✗ FAIL{X}', 'skip': f'{Y}• SKIP{X}'}.get(s, s)

    by_section = {}
    for r in results:
        by_section.setdefault(r['section'], []).append(r)

    for sec in list(js_sections) + list(py_sections):
        if sec not in by_section:
            continue
        items = by_section[sec]
        ok = sum(1 for r in items if r['status'] == 'ok')
        fail = sum(1 for r in items if r['status'] == 'fail')
        skip = sum(1 for r in items if r['status'] == 'skip')
        color = C if sec in js_sections else M
        print(f"\n{color}{B}━━ {sec} ━━{X}  {G}{ok} OK{X}  {R}{fail} fail{X}  {Y}{skip} skip{X}  {DIM}({len(items)} total){X}")
        for r in items:
            name_col = f"{r['name']:<28}"
            if r['status'] == 'fail':
                name_col = f"{R}{name_col}{X}"
            print(f"  {color_status(r['status'])}  {name_col}  {DIM}{r['detail']}{X}")

    total_ok = sum(1 for r in results if r['status'] == 'ok')
    total_fail = sum(1 for r in results if r['status'] == 'fail')
    total_skip = sum(1 for r in results if r['status'] == 'skip')

    print(f"\n{B}{'═' * 55}{X}")
    print(f"{B}SUMMARY{X}  ({elapsed:.1f}s)")
    print(f"  {G}{total_ok:>3} verified{X}")
    print(f"  {R}{total_fail:>3} failed{X}")
    print(f"  {Y}{total_skip:>3} skipped{X}")
    print(f"  {B}{len(results):>3} total{X}")

    failures = [r for r in results if r['status'] == 'fail']
    if failures:
        print(f"\n{R}{B}⚠  Failures — fix these in your HTML:{X}")
        for f in failures:
            kind = 'CDN' if f['kind'] == 'cdn' else 'PyPI'
            print(f"  {R}✗{X} [{f['section']}] {B}{f['name']}{X} ({kind}) — {f['detail']}")
            if f.get('url'):
                print(f"       {DIM}{f['url']}{X}")


def print_rich(results, elapsed, js_sections, py_sections):
    """Pretty rich output."""
    by_section = {}
    for r in results:
        by_section.setdefault(r['section'], []).append(r)

    status_icon = {'ok': '[green]✓[/]', 'fail': '[red]✗[/]', 'skip': '[yellow]•[/]'}

    for sec in list(js_sections) + list(py_sections):
        if sec not in by_section:
            continue
        items = by_section[sec]
        ok = sum(1 for r in items if r['status'] == 'ok')
        fail = sum(1 for r in items if r['status'] == 'fail')
        skip = sum(1 for r in items if r['status'] == 'skip')

        header_color = "cyan" if sec in js_sections else "magenta"
        title = (f"[{header_color} bold]{sec}[/]  "
                 f"[green]{ok} ok[/]  [red]{fail} fail[/]  [yellow]{skip} skip[/]")

        table = Table(show_header=True, header_style="bold dim", box=None, padding=(0, 1))
        table.add_column("", width=2)
        table.add_column("Name", style="bold", no_wrap=True)
        table.add_column("Detail", style="dim")

        for r in items:
            name_style = "[red]" + r['name'] + "[/]" if r['status'] == 'fail' else r['name']
            table.add_row(status_icon[r['status']], name_style, r['detail'])

        console.print()
        console.print(title)
        console.print(table)

    total_ok = sum(1 for r in results if r['status'] == 'ok')
    total_fail = sum(1 for r in results if r['status'] == 'fail')
    total_skip = sum(1 for r in results if r['status'] == 'skip')

    summary = (
        f"[green]{total_ok:>3} verified[/]\n"
        f"[red]{total_fail:>3} failed[/]\n"
        f"[yellow]{total_skip:>3} skipped[/]\n"
        f"[bold]{len(results):>3} total[/]  [dim]({elapsed:.1f}s)[/]"
    )
    border = "green" if total_fail == 0 else "red"
    console.print()
    console.print(Panel(summary, title="Summary", border_style=border, expand=False))

    failures = [r for r in results if r['status'] == 'fail']
    if failures:
        t = Table(title="[red bold]⚠  Failures[/]", show_header=True, header_style="bold red", box=None)
        t.add_column("Section")
        t.add_column("Name", style="bold")
        t.add_column("Kind")
        t.add_column("Detail")
        t.add_column("URL", style="dim")
        for f in failures:
            t.add_row(
                f['section'],
                f['name'],
                'CDN' if f['kind'] == 'cdn' else 'PyPI',
                f['detail'],
                f.get('url', '')
            )
        console.print()
        console.print(t)


def write_markdown_report(path: Path, results, elapsed, html_file):
    """Write full markdown report."""
    total_ok = sum(1 for r in results if r['status'] == 'ok')
    total_fail = sum(1 for r in results if r['status'] == 'fail')
    total_skip = sum(1 for r in results if r['status'] == 'skip')

    lines = [
        f"# Polypus Dev Kit — Verification Report",
        f"",
        f"- **Source**: `{html_file}`",
        f"- **Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Duration**: {elapsed:.1f}s",
        f"- **Total**: {len(results)} entries",
        f"- **Passed**: {total_ok}",
        f"- **Failed**: {total_fail}",
        f"- **Skipped**: {total_skip}",
        f"",
    ]

    if total_fail:
        lines.append(f"## ⚠ Failures ({total_fail})")
        lines.append("")
        lines.append("| Section | Name | Kind | Detail | URL |")
        lines.append("|---------|------|------|--------|-----|")
        for r in results:
            if r['status'] == 'fail':
                lines.append(
                    f"| {r['section']} | **{r['name']}** | "
                    f"{'CDN' if r['kind'] == 'cdn' else 'PyPI'} | "
                    f"{r['detail']} | `{r.get('url', '')}` |"
                )
        lines.append("")

    lines.append("## Full Results")
    lines.append("")
    lines.append("| Status | Section | Kind | Name | Detail |")
    lines.append("|--------|---------|------|------|--------|")
    icon = {'ok': '✅', 'fail': '❌', 'skip': '⚪'}
    for r in sorted(results, key=lambda x: (x['section'], x['name'])):
        lines.append(
            f"| {icon[r['status']]} | {r['section']} | "
            f"{'CDN' if r['kind'] == 'cdn' else 'PyPI'} | "
            f"{r['name']} | {r['detail']} |"
        )

    path.write_text('\n'.join(lines), encoding='utf-8')


# ─── Main ─────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description='Verify every library in Polypus Dev Kit actually exists on CDN / PyPI.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument('html', type=Path, nargs='?', default=Path('polypus_devkit.html'),
                    help='Path to dev kit HTML (default: polypus_devkit.html)')
    ap.add_argument('--workers', type=int, default=20, help='Concurrent workers (default 20)')
    ap.add_argument('--report', type=Path, help='Write markdown report to this path')
    ap.add_argument('--timeout', type=int, default=12, help='Per-request timeout (default 12s)')
    ap.add_argument('--no-cdn', action='store_true', help='Skip CDN checks')
    ap.add_argument('--no-pypi', action='store_true', help='Skip PyPI checks')
    ap.add_argument('--parse-only', action='store_true', help='Parse only, no network')
    args = ap.parse_args()

    if not args.html.exists():
        print(f"ERROR: file not found: {args.html}")
        sys.exit(2)

    # Banner
    if HAS_RICH:
        console.print(Panel.fit(
            f"[bold cyan]Polypus Dev Kit Verifier[/]\n"
            f"[dim]Target:[/] {args.html}\n"
            f"[dim]Workers:[/] {args.workers}",
            border_style="cyan",
        ))
    else:
        print(f"\n━━ Polypus Dev Kit Verifier ━━")
        print(f"Target:  {args.html}")
        print(f"Workers: {args.workers}\n")

    html_text = args.html.read_text(encoding='utf-8')
    try:
        js_libs, py_pkgs = parse_devkit(html_text)
    except ValueError as e:
        print(f"\nERROR: {e}")
        sys.exit(2)

    total_js = sum(len(v) for v in js_libs.values())
    total_py = sum(len(v) for v in py_pkgs.values())

    print(f"Parsed: {total_js} JS libs across {len(js_libs)} sections, "
          f"{total_py} Python pkgs across {len(py_pkgs)} sections "
          f"→ {total_js + total_py} total entries\n")

    if args.parse_only:
        for sec, items in js_libs.items():
            print(f"  JS  {sec:<14} {len(items):>3} entries")
        for sec, items in py_pkgs.items():
            print(f"  PY  {sec:<14} {len(items):>3} entries")
        print("\nParse-only mode — exiting without network checks.")
        sys.exit(0)

    # Build task list
    tasks = []
    if not args.no_cdn:
        for sec, items in js_libs.items():
            for entry in items:
                tasks.append(('cdn', sec, entry))
    if not args.no_pypi:
        for sec, items in py_pkgs.items():
            for entry in items:
                tasks.append(('pypi', sec, entry))

    if not tasks:
        print("Nothing to check (both --no-cdn and --no-pypi set).")
        sys.exit(0)

    t0 = time.time()
    results = []

    def run_task(task):
        kind, sec, entry = task
        return check_cdn(sec, entry) if kind == 'cdn' else check_pypi(sec, entry)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_task, t) for t in tasks]

        if HAS_RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.completed}/{task.total}"),
                TimeElapsedColumn(),
                console=console,
                transient=True,
            ) as progress:
                task_id = progress.add_task("Checking CDNs and PyPI...", total=len(futures))
                for fut in as_completed(futures):
                    results.append(fut.result())
                    progress.update(task_id, advance=1)
        else:
            done = 0
            for fut in as_completed(futures):
                results.append(fut.result())
                done += 1
                if done % 10 == 0 or done == len(futures):
                    print(f"\r  checking... {done}/{len(futures)}", end='', flush=True)
            print()

    elapsed = time.time() - t0

    # Print results
    if HAS_RICH:
        print_rich(results, elapsed, js_libs.keys(), py_pkgs.keys())
    else:
        print_plain(results, elapsed, js_libs.keys(), py_pkgs.keys())

    # Write markdown report
    if args.report:
        write_markdown_report(args.report, results, elapsed, args.html)
        print(f"\n📝 Markdown report written to: {args.report}")

    total_fail = sum(1 for r in results if r['status'] == 'fail')
    sys.exit(0 if total_fail == 0 else 1)


if __name__ == '__main__':
    main()
