# Polypus Dev Kit — Verification Report

- **Source**: `index.html.bak`
- **Generated**: 2026-04-25 01:10:53
- **Duration**: 1.8s
- **Total**: 194 entries
- **Passed**: 182
- **Failed**: 11
- **Skipped**: 1

## ⚠ Failures (11)

| Section | Name | Kind | Detail | URL |
|---------|------|------|--------|-----|
| animation | **CountUp.js** | CDN | HTTP 404 | `https://cdnjs.cloudflare.com/ajax/libs/CountUp.js/2.8.0/countUp.umd.js` |
| animation | **Motion One** | CDN | HTTP 404 | `https://cdn.jsdelivr.net/npm/motion@10.16.4/dist/motion.js` |
| ui | **Heroicons** | CDN | HTTP 404 | `https://unpkg.com/heroicons@2.0.18/24/outline/index.js` |
| 3d | **Zdog** | CDN | HTTP 404 | `https://unpkg.com/zdog@1/zdog.dist.min.js` |
| animation | **Popmotion** | CDN | HTTP 404 | `https://unpkg.com/popmotion/dist/popmotion.global.min.js` |
| ui | **Lenis** | CDN | HTTP 404 | `https://unpkg.com/@studio-freight/lenis/bundled/lenis.js` |
| utility | **UUID** | CDN | HTTP 404 | `https://cdn.jsdelivr.net/npm/uuid@9.0.0/dist/umd/uuidv4.min.js` |
| utility | **date-fns** | CDN | HTTP 404 | `https://cdn.jsdelivr.net/npm/date-fns@2.30.0/cdn.min.js` |
| charts | **Gauge.js** | CDN | HTTP 404 | `https://cdn.jsdelivr.net/npm/gauge.js@1.3.7/dist/gauge.min.js` |
| py-ai | **deepgram** | PyPI | NOT FOUND on PyPI (wrong package name?) | `https://pypi.org/pypi/deepgram/json` |
| py-finance | **marketaux** | PyPI | NOT FOUND on PyPI (wrong package name?) | `https://pypi.org/pypi/marketaux/json` |

## Full Results

| Status | Section | Kind | Name | Detail |
|--------|---------|------|------|--------|
| ✅ | 3d | CDN | Babylon.js | 200 OK 145ms |
| ✅ | 3d | CDN | Fabric.js | 200 OK 103ms |
| ✅ | 3d | CDN | Konva.js | 200 OK 176ms ↪ |
| ✅ | 3d | CDN | Matter.js | 200 OK 103ms |
| ✅ | 3d | CDN | Particles.js | 200 OK 103ms |
| ✅ | 3d | CDN | PixiJS | 200 OK 112ms |
| ✅ | 3d | CDN | Rough.js | 200 OK 132ms |
| ✅ | 3d | CDN | Three.js | 200 OK 107ms |
| ❌ | 3d | CDN | Zdog | HTTP 404 |
| ✅ | 3d | CDN | tsParticles | 200 OK 101ms |
| ✅ | animation | CDN | AOS | 200 OK 141ms |
| ✅ | animation | CDN | Anime.js | 200 OK 120ms |
| ❌ | animation | CDN | CountUp.js | HTTP 404 |
| ✅ | animation | CDN | GSAP | 200 OK 120ms |
| ✅ | animation | CDN | GSAP ScrollTrigger | 200 OK 125ms |
| ✅ | animation | CDN | GSAP TextPlugin | 200 OK 186ms |
| ✅ | animation | CDN | Lottie Web | 200 OK 120ms |
| ❌ | animation | CDN | Motion One | HTTP 404 |
| ❌ | animation | CDN | Popmotion | HTTP 404 |
| ✅ | animation | CDN | Rellax | 200 OK 103ms |
| ✅ | animation | CDN | Typed.js | 200 OK 112ms |
| ✅ | animation | CDN | Velocity.js | 200 OK 123ms |
| ✅ | charts | CDN | ApexCharts | 200 OK 101ms |
| ✅ | charts | CDN | Billboard.js | 200 OK 113ms |
| ✅ | charts | CDN | Chart.js | 200 OK 123ms |
| ✅ | charts | CDN | D3.js | 200 OK 101ms |
| ✅ | charts | CDN | ECharts | 200 OK 100ms |
| ✅ | charts | CDN | Frappe Charts | 200 OK 107ms |
| ❌ | charts | CDN | Gauge.js | HTTP 404 |
| ✅ | charts | CDN | Plotly.js | 200 OK 175ms |
| ✅ | charts | CDN | ProgressBar.js | 200 OK 99ms |
| ✅ | charts | CDN | uPlot | 200 OK 102ms |
| ✅ | charts | CDN | wordcloud2.js | 200 OK 109ms |
| ✅ | maps | CDN | Deck.gl | 200 OK 240ms |
| ✅ | maps | CDN | Leaflet | 200 OK 120ms |
| ✅ | maps | CDN | Mapbox GL JS | 200 OK 98ms |
| ✅ | maps | CDN | OpenLayers | 200 OK 137ms |
| ✅ | media | CDN | Howler.js | 200 OK 101ms |
| ✅ | media | CDN | MediaPipe | 200 OK 86ms |
| ✅ | media | CDN | Plyr | 200 OK 269ms |
| ✅ | media | CDN | Tone.js | 200 OK 87ms |
| ✅ | media | CDN | Video.js | 200 OK 142ms |
| ✅ | media | CDN | Wavesurfer.js | 200 OK 181ms ↪ |
| ✅ | py-ai | PyPI | anthropic | v0.97.0 |
| ✅ | py-ai | PyPI | chromadb | v1.5.8 |
| ❌ | py-ai | PyPI | deepgram | NOT FOUND on PyPI (wrong package name?) |
| ✅ | py-ai | PyPI | elevenlabs | v2.44.0 |
| ✅ | py-ai | PyPI | faiss-cpu | v1.13.2 |
| ✅ | py-ai | PyPI | google-generativeai | v0.8.6 |
| ✅ | py-ai | PyPI | instructor | v1.15.1 |
| ✅ | py-ai | PyPI | langchain | v1.2.15 |
| ✅ | py-ai | PyPI | langchain-anthropic | v1.4.1 |
| ✅ | py-ai | PyPI | langgraph | v1.1.9 |
| ✅ | py-ai | PyPI | litellm | v1.83.13 |
| ✅ | py-ai | PyPI | llama-index | v0.14.21 |
| ✅ | py-ai | PyPI | openai | v2.32.0 |
| ✅ | py-ai | PyPI | openai-whisper | v20250625 |
| ✅ | py-ai | PyPI | pinecone-client | v6.0.0 |
| ✅ | py-ai | PyPI | sentence-transformers | v5.4.1 |
| ✅ | py-ai | PyPI | tiktoken | v0.12.0 |
| ✅ | py-ai | PyPI | transformers | v5.6.2 |
| ✅ | py-backend | PyPI | alembic | v1.18.4 |
| ✅ | py-backend | PyPI | apscheduler | v3.11.2 |
| ✅ | py-backend | PyPI | celery | v5.6.3 |
| ✅ | py-backend | PyPI | fastapi | v0.136.1 |
| ✅ | py-backend | PyPI | loguru | v0.7.3 |
| ✅ | py-backend | PyPI | motor | v3.7.1 |
| ✅ | py-backend | PyPI | psycopg2-binary | v2.9.12 |
| ✅ | py-backend | PyPI | pydantic | v2.13.3 |
| ✅ | py-backend | PyPI | pymongo | v4.17.0 |
| ✅ | py-backend | PyPI | python-dotenv | v1.2.2 |
| ✅ | py-backend | PyPI | redis | v7.4.0 |
| ✅ | py-backend | PyPI | rich | v15.0.0 |
| ✅ | py-backend | PyPI | sqlalchemy | v2.0.49 |
| ✅ | py-backend | PyPI | uvicorn | v0.46.0 |
| ✅ | py-backend | PyPI | websockets | v16.0 |
| ✅ | py-data | PyPI | lightgbm | v4.6.0 |
| ✅ | py-data | PyPI | matplotlib | v3.10.9 |
| ✅ | py-data | PyPI | mlflow | v3.11.1 |
| ✅ | py-data | PyPI | numba | v0.65.1 |
| ✅ | py-data | PyPI | numpy | v2.4.4 |
| ✅ | py-data | PyPI | optuna | v4.8.0 |
| ✅ | py-data | PyPI | pandas | v3.0.2 |
| ✅ | py-data | PyPI | plotly | v6.7.0 |
| ✅ | py-data | PyPI | polars | v1.40.1 |
| ✅ | py-data | PyPI | pyarrow | v24.0.0 |
| ✅ | py-data | PyPI | scikit-learn | v1.8.0 |
| ✅ | py-data | PyPI | scipy | v1.17.1 |
| ✅ | py-data | PyPI | seaborn | v0.13.2 |
| ✅ | py-data | PyPI | statsmodels | v0.14.6 |
| ✅ | py-data | PyPI | torch | v2.11.0 |
| ✅ | py-data | PyPI | xgboost | v3.2.0 |
| ✅ | py-docs | PyPI | easyocr | v1.7.2 |
| ✅ | py-docs | PyPI | openpyxl | v3.1.5 |
| ✅ | py-docs | PyPI | pdfplumber | v0.11.9 |
| ✅ | py-docs | PyPI | pillow | v12.2.0 |
| ✅ | py-docs | PyPI | pymupdf | v1.27.2.3 |
| ✅ | py-docs | PyPI | pytesseract | v0.3.13 |
| ✅ | py-docs | PyPI | python-docx | v1.2.0 |
| ✅ | py-docs | PyPI | python-pptx | v1.0.2 |
| ✅ | py-docs | PyPI | reportlab | v4.4.10 |
| ✅ | py-docs | PyPI | xlsxwriter | v3.2.9 |
| ✅ | py-finance | PyPI | MetaTrader5 | v5.0.5735 |
| ✅ | py-finance | PyPI | alpaca-trade-api | v3.2.0 |
| ✅ | py-finance | PyPI | backtesting | v0.6.5 |
| ✅ | py-finance | PyPI | backtrader | v1.9.78.123 |
| ✅ | py-finance | PyPI | ccxt | v4.5.50 |
| ❌ | py-finance | PyPI | marketaux | NOT FOUND on PyPI (wrong package name?) |
| ✅ | py-finance | PyPI | pandas-ta | v0.4.71b0 |
| ✅ | py-finance | PyPI | quantstats | v0.0.81 |
| ✅ | py-finance | PyPI | ta-lib | v0.6.8 |
| ✅ | py-finance | PyPI | yfinance | v1.3.0 |
| ✅ | py-util | PyPI | arrow | v1.4.0 |
| ✅ | py-util | PyPI | black | v26.3.1 |
| ✅ | py-util | PyPI | cryptography | v47.0.0 |
| ✅ | py-util | PyPI | faker | v40.15.0 |
| ✅ | py-util | PyPI | humanize | v4.15.0 |
| ✅ | py-util | PyPI | paramiko | v4.0.0 |
| ✅ | py-util | PyPI | phonenumbers | v9.0.28 |
| ✅ | py-util | PyPI | psutil | v7.2.2 |
| ✅ | py-util | PyPI | pycountry | v26.2.16 |
| ✅ | py-util | PyPI | pyfiglet | v1.0.4 |
| ✅ | py-util | PyPI | pytest | v9.0.3 |
| ✅ | py-util | PyPI | qrcode | v8.2 |
| ✅ | py-util | PyPI | schedule | v1.2.2 |
| ✅ | py-util | PyPI | tqdm | v4.67.3 |
| ✅ | py-util | PyPI | typer | v0.24.2 |
| ✅ | py-util | PyPI | validators | v0.35.0 |
| ✅ | py-util | PyPI | watchdog | v6.0.0 |
| ✅ | py-web | PyPI | aiohttp | v3.13.5 |
| ✅ | py-web | PyPI | beautifulsoup4 | v4.14.3 |
| ✅ | py-web | PyPI | cloudscraper | v1.2.71 |
| ✅ | py-web | PyPI | curl-cffi | v0.15.0 |
| ✅ | py-web | PyPI | fake-useragent | v2.2.0 |
| ✅ | py-web | PyPI | httpx | v0.28.1 |
| ✅ | py-web | PyPI | lxml | v6.1.0 |
| ✅ | py-web | PyPI | playwright | v1.58.0 |
| ✅ | py-web | PyPI | requests | v2.33.1 |
| ✅ | py-web | PyPI | scrapy | v2.15.1 |
| ✅ | py-web | PyPI | selectolax | v0.4.7 |
| ✅ | py-web | PyPI | selenium | v4.43.0 |
| ✅ | realtime | CDN | Ably | 200 OK 104ms |
| ⚪ | realtime | CDN | EventSource | native API — no CDN |
| ✅ | realtime | CDN | ReconnectingWebSocket | 200 OK 99ms |
| ✅ | realtime | CDN | Socket.io | 200 OK 100ms |
| ✅ | ui | CDN | Alpine.js | 200 OK 99ms |
| ✅ | ui | CDN | Choices.js | 200 OK 105ms |
| ✅ | ui | CDN | Cleave.js | 200 OK 109ms |
| ✅ | ui | CDN | CodeMirror | 200 OK 118ms |
| ✅ | ui | CDN | Cropper.js | 200 OK 96ms |
| ✅ | ui | CDN | DOMPurify | 200 OK 100ms |
| ✅ | ui | CDN | DataTables | 200 OK 102ms |
| ✅ | ui | CDN | Flatpickr | 200 OK 117ms |
| ✅ | ui | CDN | GLightbox | 200 OK 103ms |
| ✅ | ui | CDN | Grid.js | 200 OK 166ms ↪ |
| ❌ | ui | CDN | Heroicons | HTTP 404 |
| ✅ | ui | CDN | Highlight.js | 200 OK 114ms |
| ✅ | ui | CDN | IMask.js | 200 OK 170ms ↪ |
| ✅ | ui | CDN | KaTeX | 200 OK 95ms |
| ❌ | ui | CDN | Lenis | HTTP 404 |
| ✅ | ui | CDN | Lucide Icons | 200 OK 178ms ↪ |
| ✅ | ui | CDN | Marked | 200 OK 105ms |
| ✅ | ui | CDN | Micromodal | 200 OK 149ms ↪ |
| ✅ | ui | CDN | Notyf | 200 OK 101ms |
| ✅ | ui | CDN | Phosphor Icons | 200 OK 164ms ↪ |
| ✅ | ui | CDN | PhotoSwipe | 200 OK 97ms |
| ✅ | ui | CDN | Prism.js | 200 OK 103ms |
| ✅ | ui | CDN | QRCode.js | 200 OK 99ms |
| ✅ | ui | CDN | Quill | 200 OK 95ms |
| ✅ | ui | CDN | SheetJS | 200 OK 111ms |
| ✅ | ui | CDN | SortableJS | 200 OK 98ms |
| ✅ | ui | CDN | SweetAlert2 | 200 OK 98ms |
| ✅ | ui | CDN | Tabulator | 200 OK 133ms |
| ✅ | ui | CDN | Tailwind CSS | 200 OK 133ms ↪ |
| ✅ | ui | CDN | Tippy.js | 200 OK 159ms ↪ |
| ✅ | ui | CDN | Toastify | 200 OK 100ms |
| ✅ | ui | CDN | Vanilla Tilt | 200 OK 105ms |
| ✅ | ui | CDN | html2canvas | 200 OK 107ms |
| ✅ | ui | CDN | interact.js | 200 OK 108ms |
| ✅ | ui | CDN | jsPDF | 200 OK 110ms |
| ✅ | utility | CDN | Axios | 200 OK 85ms |
| ✅ | utility | CDN | Chroma.js | 200 OK 91ms |
| ✅ | utility | CDN | Clipboard.js | 200 OK 99ms |
| ✅ | utility | CDN | Crypto-JS | 200 OK 114ms |
| ✅ | utility | CDN | Day.js | 200 OK 110ms |
| ✅ | utility | CDN | FileSaver.js | 200 OK 99ms |
| ✅ | utility | CDN | Fuse.js | 200 OK 102ms |
| ✅ | utility | CDN | JSZip | 200 OK 100ms |
| ✅ | utility | CDN | Lodash | 200 OK 82ms |
| ✅ | utility | CDN | Marked | 200 OK 110ms |
| ✅ | utility | CDN | Math.js | 200 OK 107ms |
| ✅ | utility | CDN | PapaParse | 200 OK 109ms |
| ❌ | utility | CDN | UUID | HTTP 404 |
| ❌ | utility | CDN | date-fns | HTTP 404 |