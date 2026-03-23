# Web Crawling Pipeline

CLI 기반의 **실무형 웹 크롤링 데이터 파이프라인 프로젝트**

이 프로젝트는 단순한 크롤러가 아니라,  
**데이터 수집 → 검증 → 정규화 → 저장 → 모니터링**까지 포함된  
**production-like crawling pipeline**을 목표로 설계되었다.

---

## CLI Demo

![CLI Demo](docs/cli-demo.gif)

---

# 1. 프로젝트 개요

## 목적

- 정적/동적 웹 페이지에서 데이터를 수집
- 데이터 품질을 검증하고 정규화
- 구조화된 형태로 저장
- 실행 결과를 기록 및 모니터링

---

## 핵심 파이프라인

```text
crawl → validate → transform → store → monitor
````

---

# 2. 주요 기능

## 2.1 크롤링 (Crawling)

### Static Crawling

* `requests + BeautifulSoup`
* 서버에서 HTML 직접 수신

### Dynamic Crawling

* `Playwright`
* JavaScript 렌더링 이후 데이터 수집

---

## 2.2 Validation

* 필수 필드 검증
* invalid 데이터 분리
* 데이터 품질 확보

---

## 2.3 Transformation

* raw 데이터 → 공통 스키마 변환
* 가격 파싱
* 상태값 정규화
* item_id 추출

---

## 2.4 Storage

```text
data/
  raw/
  validated/
  transformed/
```

* 단계별 데이터 저장
* JSON 기반 파일 시스템 구조

---

## 2.5 Monitoring

* 실행 로그 기록
* run summary 생성

```text
reports/latest_run_summary.json
```

---

## 2.6 안정성 (Robustness)

* retry (재시도 로직)
* rate limiting (요청 간 지연)
* user-agent rotation

---

# 3. 프로젝트 구조

```text
src/
  cli/
  crawlers/
    site_a_requests.py
    site_b_playwright.py
  validators/
  transformers/
  storage/
  monitoring/
  utils/
```

---

# 4. 실행 방법

## 4.1 정적 크롤링

```bash
python main.py --source site_a --max-pages 2 --limit 10
```

---

## 4.2 동적 크롤링

```bash
python main.py --source site_b --max-pages 2 --limit 10
```

---

# 5. 데이터 흐름

## Raw 데이터

```json
{
  "source": "site_a",
  "listing_url": "...",
  "title": "...",
  "price_text": "£51.77",
  "status_text": "In stock"
}
```

---

## Transformed 데이터

```json
{
  "source": "site_a",
  "item_id": "a-light-in-the-attic_1000",
  "title": "A Light in the Attic",
  "price": 51.77,
  "currency": "GBP",
  "status": "in_stock",
  "detail_url": "...",
  "collected_at": "2026-03-23T20:30:00"
}
```

---

# 6. 설계 특징

## 6.1 Multi-source 구조

* 사이트별 crawler 분리
* 공통 pipeline 재사용

```text
site_a → requests
site_b → playwright
```

---

## 6.2 Adapter 패턴

각 사이트는 독립적인 crawler(adapter)로 구현

```text
crawl_site_a()
crawl_site_b()
```

---

## 6.3 Config 기반 설계

* URL
* timeout
* retry
* rate limit
* user-agent

→ 코드와 설정 분리

---

## 6.4 파일 기반 파이프라인

* DB 없이도 상태 추적 가능
* 단계별 데이터 확인 가능

---

# 7. 기술 스택

* Python
* requests
* BeautifulSoup
* Playwright
* argparse
* pathlib
* logging

---

# 8. 프로젝트 의의

이 프로젝트는 다음을 모두 포함한다:

* static + dynamic crawling
* validation / transformation pipeline
* 안정성 (retry / rate limit / UA)
* monitoring (run summary)

즉,

> 단순 크롤러가 아니라
> **실무형 데이터 수집 파이프라인 구조를 구현한 프로젝트**

---

# 9. 한 줄 요약

> Multi-source 웹 크롤링과 데이터 파이프라인 처리를 결합한
> CLI 기반 실무형 크롤링 시스템

---

# 10. 향후 확장

* DB 저장 (PostgreSQL / SQLite)
* proxy 지원
* robots.txt 처리
* 스케줄링 (cron)
* 중복 제거 / upsert
