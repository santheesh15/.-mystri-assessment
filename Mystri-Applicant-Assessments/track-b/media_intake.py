"""Multi-format customer intake + lightweight image/text assessment (stdlib only).

Production would add Pillow/OpenCV/OCR; this prototype uses format sniffing,
PNG/JPEG structure checks, and explicit human routing for uncertain media.
"""
from __future__ import annotations

import base64
import re
import struct
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_IMAGE = frozenset({'jpeg', 'png', 'webp', 'gif'})
SUPPORTED_DOCUMENT = frozenset({'pdf', 'plain_text', 'csv'})
CONVERT_BY_HUMAN = frozenset({'heic', 'heif', 'bmp', 'tiff', 'unknown'})


@dataclass(frozen=True)
class MediaAssessment:
    filename: str
    detected_format: str
    confidence: str
    size_bytes: int
    width: int | None
    height: int | None
    quality_signals: tuple[str, ...]
    routing: str  # auto_queue | human_review | reject
    handling: str
    algorithms_applied: tuple[str, ...]


def _ext(name: str) -> str:
    return Path(name).suffix.lower().lstrip('.')


def sniff_format(data: bytes, filename: str) -> tuple[str, str]:
    """Magic-byte detection first; extension is a hint only."""
    if len(data) >= 3 and data[:3] == b'\xff\xd8\xff':
        return 'jpeg', 'high'
    if len(data) >= 8 and data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png', 'high'
    if len(data) >= 12 and data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp', 'high'
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif', 'high'
    if data[:4] == b'%PDF':
        return 'pdf', 'high'
    if len(data) >= 12 and data[4:8] == b'ftyp':
        brand = data[8:12]
        if brand in (b'heic', b'heix', b'mif1', b'hevc'):
            return 'heic', 'high'
    text_start = data[:256].decode('utf-8', errors='ignore').lower()
    if text_start.startswith('customer_id,') or _ext(filename) == 'csv':
        return 'csv', 'medium'
    if _ext(filename) in {'txt', 'text'} or _is_mostly_text(data):
        return 'plain_text', 'medium'

    guess = _ext(filename) or 'unknown'
    return guess if guess else 'unknown', 'low'


def _is_mostly_text(data: bytes) -> bool:
    if not data:
        return False
    sample = data[:512]
    printable = sum(1 for b in sample if 32 <= b < 127 or b in (9, 10, 13))
    return printable / len(sample) > 0.85


def _png_dimensions(data: bytes) -> tuple[int | None, int | None]:
    """Parse PNG IHDR width/height (standard chunk layout)."""
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n':
        return None, None
    # First chunk should be IHDR: length(4) type(4) data(13) ...
    if data[12:16] != b'IHDR':
        return None, None
    w, h = struct.unpack('>II', data[16:24])
    return int(w), int(h)


def _jpeg_dimensions(data: bytes) -> tuple[int | None, int | None]:
    """Scan JPEG markers for SOF0/SOF2 to read dimensions (stdlib algorithm)."""
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xC0, 0xC2):
            if i + 7 <= len(data):
                h = struct.unpack('>H', data[i + 3 : i + 5])[0]
                w = struct.unpack('>H', data[i + 5 : i + 7])[0]
                return int(w), int(h)
            break
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD9:
            continue
        if i + 2 > len(data):
            break
        seg_len = struct.unpack('>H', data[i : i + 2])[0]
        i += seg_len
    return None, None


def _brightness_proxy(data: bytes, fmt: str) -> str | None:
    """Crude byte-mean proxy — not real luminance; flags very dark/bright payloads."""
    if fmt not in SUPPORTED_IMAGE or len(data) < 64:
        return None
    sample = data[32:512]
    if not sample:
        return None
    mean = sum(sample) / len(sample)
    if mean < 25:
        return 'very_dark_proxy'
    if mean > 230:
        return 'very_bright_proxy'
    return 'brightness_ok_proxy'


def assess_attachment(filename: str, data: bytes) -> MediaAssessment:
    fmt, confidence = sniff_format(data, filename)
    size = len(data)
    signals: list[str] = []
    algorithms = ['magic_byte_sniff', 'extension_hint']
    width: int | None = None
    height: int | None = None

    if size < 800:
        signals.append('file_very_small_may_be_unusable')
    if size > 2 * 1024 * 1024:
        signals.append('file_over_2mb_policy')

    if fmt == 'png':
        width, height = _png_dimensions(data)
        algorithms.append('png_ihdr_parse')
    elif fmt == 'jpeg':
        width, height = _jpeg_dimensions(data)
        algorithms.append('jpeg_sof_scan')

    if width and height:
        if width < 320 or height < 240:
            signals.append('resolution_below_recommended_min')
        algorithms.append('min_resolution_gate')

    bright = _brightness_proxy(data, fmt)
    if bright:
        signals.append(bright)
        algorithms.append('brightness_byte_proxy')

    if fmt in CONVERT_BY_HUMAN or fmt == 'unknown':
        return MediaAssessment(
            filename,
            fmt,
            confidence,
            size,
            width,
            height,
            tuple(signals),
            'human_review',
            'Convert or relabel file manually; do not auto-attach to quote',
            tuple(algorithms),
        )

    if fmt in SUPPORTED_DOCUMENT:
        if fmt == 'csv':
            text = data.decode('utf-8-sig', errors='replace')
            if not re.search(r'customer_id|invoice|fault|photo', text, re.I):
                signals.append('csv_missing_expected_headers')
        routing = 'human_review' if signals else 'auto_queue'
        handling = 'Coordinator validates document content before updating request row'
        return MediaAssessment(
            filename,
            fmt,
            confidence,
            size,
            width,
            height,
            tuple(signals),
            routing,
            handling,
            tuple(algorithms + ['text_header_probe']),
        )

    if fmt in SUPPORTED_IMAGE:
        routing = 'human_review' if signals else 'auto_queue'
        if routing == 'auto_queue':
            handling = 'Queue to technician human photo quality check (blur/angle still human)'
        else:
            handling = 'Technician review required due to quality signals'
        return MediaAssessment(
            filename,
            fmt,
            confidence,
            size,
            width,
            height,
            tuple(signals),
            routing,
            handling,
            tuple(algorithms),
        )

    return MediaAssessment(
        filename,
        fmt,
        confidence,
        size,
        width,
        height,
        tuple(signals or ('unrecognized_format',)),
        'reject',
        'Ask customer to resend using JPEG/PNG/PDF or plain text',
        tuple(algorithms),
    )


def assess_demo_pack() -> list[dict]:
    """Run built-in samples to show multi-format handling without customer PII."""
    root = Path(__file__).resolve().parent / 'tests' / 'fixtures'
    out: list[dict] = []
    b64 = root / 'tiny.png.b64'
    if b64.exists():
        png = base64.standard_b64decode(b64.read_text().strip())
        out.append(assess_attachment('fault-tiny.png', png).__dict__)

    out.append(assess_attachment('notes.txt', b'Serial number: ABC-123\nModel: WM-9000').__dict__)
    out.append(assess_attachment('photo.heic', b'\x00\x00\x00\x18ftypheic\x00' + b'\x00' * 40).__dict__)
    out.append(assess_attachment('scan.unknown', b'\x00\x01\x02\x03' * 100).__dict__)
    return out
