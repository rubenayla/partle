# Partle Project Knowledge Base

## 📅 Discovery Log

### 2025-09-05: Email System Investigation

#### ❌ What Doesn't Work Anymore
- **MailChannels Free Tier** - DISCONTINUED as of August 31, 2024
  - Previously worked with Cloudflare Workers for free
  - Now returns 401 Unauthorized even with proper Domain Lockdown
  - Attempted fixes that failed:
    - Adding SPF record with `include:relay.mailchannels.net`
    - Adding Domain Lockdown TXT record `_mailchannels`
    - Using various API endpoints
  - **Conclusion**: MailChannels ended their free Cloudflare Workers integration

- **Cloudflare Email Routing API** (`/email/routing/addresses/`) 
  - This is for RECEIVING emails, not sending
  - Common misconception that it can send emails

#### ✅ What Actually Works: Resend (Current Solution)
**Resend API** - The working solution as of 2025-09-05
- **Setup Process**:
  1. Sign up at https://resend.com (free tier: 100 emails/day, 3000/month)
  2. Add domain via Cloudflare integration (automatic DNS setup)
  3. Get API key from Resend dashboard
  4. Add `RESEND_API_KEY` to Cloudflare Worker environment variables
  5. Update Worker code to use Resend API endpoint

- **Required DNS Records** (automatically added via Cloudflare integration):
  - MX record: `send` → `feedback-smtp.eu-west-1.amazonses.com`
  - DKIM record: `resend._domainkey` → (long DKIM key)
  - SPF record: `v=spf1 include:amazonses.com ~all`

- **Worker Configuration**:
  - Environment variable: `RESEND_API_KEY` (as Secret in Cloudflare)
  - API endpoint: `https://api.resend.com/emails`
  - Can send from: `noreply@rubenayla.xyz` after domain verification

#### 🔄 Migration Path
1. **Old Setup** (MailChannels - NO LONGER WORKS):
   - Worker → MailChannels API (`api.mailchannels.net`)
   - Required Domain Lockdown TXT record
   - Free but discontinued

2. **New Setup** (Resend - WORKING):
   - Worker → Resend API (`api.resend.com`)
   - Requires Resend account and API key
   - Free tier sufficient for small projects
   - Better documentation and support

#### 🔑 Key Discoveries
- **MailChannels shutdown** - Despite conflicting documentation, MailChannels free tier is definitively dead as of August 31, 2024
- **Resend is the recommended alternative** - Officially documented by Cloudflare, easy setup
- **Domain verification is critical** - Emails won't send without proper DNS records
- **Cloudflare integration simplifies DNS** - Use "Sign in to Cloudflare" button in Resend for automatic setup

---

## 🏗️ Architecture Decisions

### Email System  
- **Current**: Cloudflare Worker → Resend API
- **Why**: MailChannels discontinued free tier on August 31, 2024
- **Previous approach**: MailChannels (stopped working)
- **Alternative considered**: Direct SMTP from Python backend

### Database
- **ONLY ONE DATABASE**: Hetzner Production (91.98.68.236:5432/partle)
- **Never create local databases** - User explicitly forbid this
- **Always verify DATABASE_URL** before any operation

### Ports
- Frontend: 3000 (React/Vite standard)
- Backend: 8000 (FastAPI standard)  
- Database: 5432 (PostgreSQL standard)

---

## 🔐 Security Incidents

### Git Credential Exposure (2025-09-05)
- **Issue**: Committed `backend/downloaded_server.env` with secrets
- **Resolution**: Rotated all credentials, cleaned Git history
- **Lesson**: Always check files before committing, never hardcode credentials

### Current Credentials Status
- All credentials rotated on 2025-09-05
- Using environment variables exclusively
- Secrets stored in Cloudflare Worker environment variables

---

## 🐛 Common Issues & Solutions

### "Network Error" on Frontend
- **Cause**: Backend not running or wrong port
- **Solution**: Ensure backend runs on port 8000, check VITE_API_BASE

### Email Not Sending
- **Cause**: Missing Domain Lockdown record
- **Solution**: Add `_mailchannels` TXT record with Worker subdomain

### GitHub Actions Failing
- **Cause**: Poetry not in PATH for deploy user
- **Solution**: Add `export PATH="/home/deploy/.local/bin:$PATH"`

---

## 📚 Resources

### Official Documentation
- [Cloudflare Workers Email](https://developers.cloudflare.com/email-routing/email-workers/send-email-workers/)
- [MailChannels Domain Lockdown](https://support.mailchannels.com/hc/en-us/articles/16918954360845)
- [Resend with Cloudflare](https://resend.com/docs/send-with-cloudflare-workers)

### Key Files
- Email Worker: `/stuff/cloudflare-email-worker.js`
- Backend email utils: `/backend/app/auth/utils.py`
- Test scripts: `/backend/test_email_debug.py`

---

## 🎯 TODO: Outstanding Issues
- [ ] Add Domain Lockdown TXT record
- [ ] Verify email delivery works
- [ ] Consider adding DKIM for better deliverability
- [ ] Document final working solution

---

*Last Updated: 2025-09-05*