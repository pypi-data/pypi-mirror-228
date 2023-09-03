"""Scraper for https://kabuyoho.jp/sp/reportDps"""
from __future__ import annotations

import logging
import urllib.parse

from ..base import Website, webpage_property
from ..util import str2float
from .kabuyoho_webpage import KabuyohoWebpage

logger = logging.getLogger(__name__)


class ReportDps(KabuyohoWebpage):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportDps?bcode={self.security_code}")
        super().__init__()

    @webpage_property
    def actual_dividend_yield(self) -> float | None:
        """Actual dividend yield(実績配当利回り)."""
        amount = self.select_one('th:-soup-contains("実績配当利回り") + td')
        return str2float(amount.text)

    @webpage_property
    def expected_dividend_yield(self) -> float | None:
        """Expected dividend yield(予想配当利回り)."""
        amount = self.select_one('th:-soup-contains("予想配当利回り") + td')
        return str2float(amount.text)

    @webpage_property
    def dividend_payout_ratio(self) -> float | None:
        """Expected dividend yield(予想配当利回り)."""
        amount = self.select_one('h2:-soup-contains("前期配当性向") + div td')
        return str2float(amount.text)
