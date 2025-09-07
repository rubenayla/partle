"""
Enhanced middleware for bypassing anti-scraping measures
"""

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import time

class RotateUserAgentMiddleware(UserAgentMiddleware):
    """Rotate user agents to avoid detection"""
    
    USER_AGENTS = [
        # Chrome on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # Chrome on Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Firefox on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        # Safari on Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        # Edge on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    ]
    
    def process_request(self, request, spider):
        ua = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = ua
        spider.logger.debug(f'Using User-Agent: {ua[:50]}...')

class EnhancedRetryMiddleware(RetryMiddleware):
    """Enhanced retry with exponential backoff"""
    
    def process_response(self, request, response, spider):
        if response.status in [403, 429, 503]:
            reason = response_status_message(response.status)
            spider.logger.warning(f'Retrying {request.url} (status {response.status}): {reason}')
            
            # Exponential backoff
            retry_times = request.meta.get('retry_times', 0) + 1
            delay = min(2 ** retry_times, 60)  # Max 60 seconds
            
            spider.logger.info(f'Waiting {delay} seconds before retry...')
            time.sleep(delay)
            
            return self._retry(request, reason, spider) or response
        
        return super().process_response(request, response, spider)

class HeadersMiddleware:
    """Add realistic browser headers"""
    
    def process_request(self, request, spider):
        # Add common browser headers
        request.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })

class CookieMiddleware:
    """Handle cookies properly"""
    
    def process_request(self, request, spider):
        # Accept cookies
        request.meta['dont_redirect'] = False
        request.meta['handle_httpstatus_list'] = [301, 302, 303, 307, 308]