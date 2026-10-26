#!/usr/bin/env python3
"""Optional web-grounded answers; not a CSH receiver or evidence admission."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import math
import os

DEFAULT_MODEL = 'openai/gpt-5.6-sol'


def retry_delay(value):
    """Parse Retry-After without echoing arbitrary response headers."""
    if value is None:
        return None
    try:
        seconds = float(value)
    except ValueError:
        try:
            seconds = (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds()
        except (ValueError, TypeError, OverflowError):
            return None
    return max(0, math.ceil(seconds)) if math.isfinite(seconds) else None


def answer(question, *, model=DEFAULT_MODEL, previous_response_id=None,
           max_output_tokens=512, client=None):
    if not isinstance(question, str) or not question.strip():
        return {'status': 'INVALID_INPUT'}
    if not isinstance(model, str) or not model.strip() or not 1 <= max_output_tokens <= 8192:
        return {'status': 'INVALID_INPUT'}
    if client is None and not os.environ.get('PERPLEXITY_API_KEY'):
        return {'status': 'CREDENTIAL_UNAVAILABLE', 'request_attempted': False}
    try:
        from perplexity import Perplexity, APIStatusError, APIConnectionError
    except ImportError:
        return {'status': 'DEPENDENCY_UNAVAILABLE', 'request_attempted': False}
    owned = client is None
    try:
        if owned:
            # No hidden retries or credential-bearing debug logs.
            import logging
            for name in ('perplexity', 'httpx', 'httpcore'):
                logging.getLogger(name).setLevel(logging.WARNING)
            client = Perplexity(api_key=os.environ['PERPLEXITY_API_KEY'],
                                base_url='https://api.perplexity.ai',
                                max_retries=0, timeout=60.0)
        request = dict(model=model, input=question, tools=[{'type': 'web_search'}],
                       max_output_tokens=max_output_tokens, max_steps=2, stream=False)
        if previous_response_id:
            request['previous_response_id'] = previous_response_id
        raw = client.responses.with_raw_response.create(**request)
        response = raw.parse()
        data = response.model_dump(mode='json')
        text = response.output_text
        sources, citations = [], []
        for item in data.get('output') or []:
            if item.get('type') == 'search_results':
                sources.extend(item.get('results') or [])
            if item.get('type') == 'message':
                for part in item.get('content') or []:
                    if part.get('type') == 'output_text':
                        citations.extend(a for a in part.get('annotations') or []
                                         if a.get('type') == 'url_citation')
        complete = (raw.status_code == 200 and data.get('status') == 'completed'
                    and not data.get('error') and not data.get('incomplete_details')
                    and isinstance(text, str) and bool(text.strip()))
        return {'status': 'PASS' if complete else 'RESPONSE_INCOMPLETE',
                'http_status': raw.status_code, 'response_status': data.get('status'),
                'response_id': data.get('id'), 'model': data.get('model'),
                'output_text': text, 'search_results': sources, 'citations': citations,
                'grounding_metadata_present': bool(sources or citations),
                'usage': data.get('usage'),
                'boundary': 'Provider answer and source metadata; not verified truth or CSH execution.'}
    except APIStatusError as exc:
        return {'status': ('AUTHENTICATION_ERROR' if exc.status_code == 401 else
                           'RATE_LIMITED' if exc.status_code == 429 else 'HTTP_ERROR'),
                'http_status': exc.status_code,
                'retry_after_seconds': retry_delay(exc.response.headers.get('Retry-After'))}
    except APIConnectionError:
        return {'status': 'CONNECTION_ERROR'}
    except Exception as exc:
        # Exception messages/bodies may contain secrets or input; never expose them.
        return {'status': 'EXECUTION_ERROR', 'error_type': type(exc).__name__}
    finally:
        if owned and client is not None:
            client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question', nargs='?')
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--previous-response-id')
    parser.add_argument('--max-output-tokens', type=int, default=512)
    parser.add_argument('--smoke', action='store_true', help='Minimal request; print status/shape only')
    args = parser.parse_args()
    if not args.smoke and not args.question:
        parser.error('provide a question or --smoke')
    result = answer('Search the web for the Python documentation and give its URL in one sentence.'
                    if args.smoke else args.question,
                    model=args.model, previous_response_id=args.previous_response_id,
                    max_output_tokens=256 if args.smoke else args.max_output_tokens)
    if args.smoke:
        result = {k: v for k, v in result.items() if k in
                  ('status', 'http_status', 'response_status', 'grounding_metadata_present',
                   'retry_after_seconds', 'request_attempted')}
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
