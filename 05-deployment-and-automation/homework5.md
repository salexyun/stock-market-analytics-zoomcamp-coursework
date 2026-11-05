# Module 5 Homework — Research Ideas

---

## Q1: Supply-contract disclosures at under-covered KOSDAQ companies

**Market and scope.** KOSDAQ companies under ~KRW 500bn market cap with 0–1 analysts covering them. Horizon: 1–20 trading days after a disclosure.

**Investment thesis.** Korean listed companies must disclose large supply contracts (단일판매·공급계약체결) and state each contract's size as a percentage of recent revenue. For a small company, a contract worth 30%+ of revenue materially changes next year's sales. I expect prices to underreact at first and drift upward over the following weeks.

**Potential edge.** The filings are Korean-language tables, not news stories. Foreign investors and data vendors rarely parse them, and with no analyst coverage nobody turns them into earnings revisions.

**Data and sources.** OpenDART API (disclosure text and timestamps; available, field parsing to verify); KRX/pykrx (prices and market cap; delisted-company coverage to verify); FnGuide or Naver (analyst coverage counts; access to verify).

**Research approach.** An event study of abnormal returns vs. the KOSDAQ index from the next open to day +20, bucketed by contract size and analyst coverage. The rule: buy when the contract exceeds X% of revenue and coverage is ≤1, then hold N days.

**Validation and risks.** Benchmark: the KOSDAQ index and size-matched portfolios bought on random days. I'd reject the idea if no abnormal return remains after day +1 net of costs. Risks: cancelled contracts, thin liquidity, ±30% daily price limits, the securities transaction tax, and contract announcements used as promotion ahead of share offerings.

---

## Q2: Korean 10-day semiconductor exports as an early read on memory earnings

**Market and scope.** SK Hynix, Samsung Electronics and Micron. Horizon: 1–3 months, up to the next earnings release.

**Investment thesis.** Korea's customs agency publishes semiconductor exports for the first 10 and 20 days of each month, weeks before the chipmakers report. Export value reflects both memory prices and volumes, so faster-than-expected export growth should lead to earnings beats and stock rerating.

**Potential edge.** The headline number is widely reported and probably priced in quickly. Any edge would come from refinements: adjusting for working days, using the change in growth rather than the level, and splitting by product (HS code) and destination.

**Data and sources.** KCS/TRASS trade statistics by HS code and country (to verify history and 10-day archives); MOTIE monthly trade releases (available); company earnings and historical consensus (source to verify).

**Research approach.** First, regress quarterly revenue surprises on export growth as known at each release date. Then trade it: go long SK Hynix vs. the KOSPI while adjusted export growth is accelerating, and hold to the next release.

**Validation and risks.** Benchmark: buy-and-hold SK Hynix, and a signal that uses only the headline number. I'd reject the idea if the refined signal doesn't beat the headline one, or if prices fully react on the release day. Risks: only ~40 quarters of history, currency effects in USD export values, a single memory cycle dominating results, and the shift to HBM changing the product mix.

---

## Q3: Pairs trade on preferred vs. common shares of the same Korean company

**Market and scope.** Korean companies with both common and preferred shares listed, e.g. Samsung Electronics (005930/005935) and Hyundai Motor (005380/005385). Horizon: weeks to months per trade.

**Investment thesis.** Both share classes claim the same cash flows. The preferred shares get a slightly higher dividend but no votes, so their price ratio should stay near a stable level. Index and foreign flows that hit only the common shares push the ratio away temporarily, and the gap should then close.

**Potential edge.** The pair is linked by structure, not just by statistical correlation. Knowing local drivers of the discount (governance, inheritance, the Value-up program, buybacks of preferred shares) helps separate a temporary gap from a permanent shift.

**Data and sources.** KRX/pykrx daily prices for both share classes (available); DART dividend and buyback filings (available); KOSPI200 rebalancing announcements (archive to verify).

**Research approach.** Track the z-score of the log price ratio over a 1-year rolling window. When |z| > 2, switch holdings into the relatively cheap share class, and switch back near z ≈ 0. A switch needs no short position, which matters because short selling in Korea is restricted.

**Validation and risks.** Benchmark: buy-and-hold the common shares. I'd reject the idea if switching doesn't beat holding after the transaction tax, or if the ratio trends instead of reverting. Risks: governance reform permanently narrowing the discount, preferred-share liquidity outside Samsung, and few independent trades per pair.
