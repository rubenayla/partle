# Spanish Retailer Scraping Strategy

## Priority Targets

### Tier 1 - Major Spanish Retailers (Implement First)

1. **El Corte Inglés** (`elcorteingles.es`)
   - Spain's largest department store
   - Categories: Everything (electronics, tools, home, fashion)
   - Products: ~1M+ SKUs
   - Technical: No API, structured HTML, may need session handling
   - Store Type: Physical + Online

2. **Carrefour Spain** (`carrefour.es`)
   - Major French hypermarket chain in Spain
   - Categories: Groceries, electronics, home, tools
   - Products: ~500K+ SKUs
   - Technical: Structured JSON-LD data, relatively easy to scrape
   - Store Type: Physical + Online

3. **MediaMarkt** (`mediamarkt.es`)
   - Leading electronics retailer
   - Categories: Electronics, appliances, gaming
   - Products: ~50K+ SKUs
   - Technical: React SPA, may need Selenium/Playwright
   - Store Type: Physical + Online

4. **Leroy Merlin** (`leroymerlin.es`) ✅ Already have scraper
   - Major hardware/DIY chain
   - Categories: Construction, tools, garden, home improvement
   - Products: ~100K+ SKUs
   - Status: Scraper exists but needs anti-blocking improvements
   - Store Type: Physical

5. **Bricodepot** (`bricodepot.es`) ✅ Already have scraper
   - Budget hardware store
   - Categories: Construction materials, tools, bathroom, kitchen
   - Products: ~20K+ SKUs
   - Status: Scraper exists but needs fixing
   - Store Type: Physical

### Tier 2 - Specialized Retailers

6. **Bauhaus** (`bauhaus.es`)
   - German DIY chain, competitor to Leroy Merlin
   - Categories: Tools, garden, construction, workshop
   - Products: ~40K+ SKUs
   - Technical: Standard e-commerce site, should be straightforward
   - Store Type: Physical + Online

7. **PcComponentes** (`pccomponentes.com`)
   - Spain's leading tech/computer retailer
   - Categories: Computers, components, electronics
   - Products: ~70K+ SKUs
   - Technical: Has structured data, API-like endpoints
   - Store Type: Mainly Online

8. **ManoMano** (`manomano.es`)
   - Marketplace for DIY/tools
   - Categories: Tools, garden, construction
   - Products: ~1M+ SKUs (marketplace)
   - Technical: Marketplace model, may have API
   - Store Type: Online marketplace

### Tier 3 - Future Considerations

9. **Wallapop** - Second-hand marketplace
   - Has public API endpoints
   - Better for dynamic/real-time queries
   - Don't store, query on-demand

10. **Amazon.es** - Marketplace giant
    - Complex anti-scraping
    - Consider Product Advertising API instead

## Technical Implementation Strategy

### Phase 1: Fix Existing Scrapers
- [ ] Debug Leroy Merlin anti-blocking issues
- [ ] Fix Bricodepot scraper failures
- [ ] Add better error handling and retry logic
- [ ] Implement proxy rotation if needed

### Phase 2: New Basic Scrapers
- [ ] Carrefour (easiest, has JSON-LD)
- [ ] Bauhaus (standard site structure)
- [ ] El Corte Inglés (challenging but high value)

### Phase 3: Advanced Scrapers
- [ ] MediaMarkt (needs JavaScript rendering)
- [ ] PcComponentes (high volume, rate limiting)
- [ ] ManoMano (marketplace complexity)

### Phase 4: API Integrations
- [ ] Wallapop search API (real-time queries)
- [ ] Google Shopping API (aggregated data)
- [ ] Facebook Marketplace (if accessible)

## Database Store IDs

```sql
-- Existing stores
-- Leroy Merlin: 4063
-- Bricodepot: 4064

-- To be created:
-- El Corte Inglés: TBD
-- Carrefour Spain: TBD
-- MediaMarkt: TBD
-- Bauhaus: TBD
-- PcComponentes: TBD
-- ManoMano: TBD
```

## Anti-Blocking Strategies

1. **User-Agent Rotation**: Rotate between real browser user agents
2. **Request Delays**: Add random delays between requests (1-3 seconds)
3. **Session Management**: Maintain cookies and session data
4. **Proxy Rotation**: Use residential proxies for difficult sites
5. **Headless Browser**: Use Playwright for JavaScript-heavy sites
6. **Rate Limiting**: Respect robots.txt and implement reasonable limits

## Data Priority

Focus on high-value product categories:
1. Tools & Hardware (Leroy Merlin, Bricodepot, Bauhaus)
2. Electronics (MediaMarkt, PcComponentes)
3. Home & Garden (Carrefour, El Corte Inglés)
4. Construction Materials (All hardware stores)

## Success Metrics

- Target: 500K+ products from Spanish retailers
- Update frequency: Weekly for prices, monthly for catalog
- Coverage: Major cities (Madrid, Barcelona, Valencia, Sevilla)
- Accuracy: 95%+ price accuracy, 90%+ availability accuracy

## Notes

- Spanish sites often use different URL structure (.es domains)
- Many require accepting cookies before scraping
- Some sites have regional pricing (different prices in Canary Islands)
- Consider Spanish language product names for better search