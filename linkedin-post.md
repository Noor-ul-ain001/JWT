## LinkedIn Post Options

Pick whichever style fits your voice best, or mix and match.

---

### Option 1 — Short & Punchy

Ever wondered why logging in twice gives you two completely different JWTs — even with the same username and password?

I built a quick demo to visualize exactly why.

Here's the secret: JWTs contain timestamps.

Every time you log in, the server stamps the token with:
- `iat` — the exact moment it was issued
- `exp` — when it expires

Different timestamps = different payload = different HMAC signature = completely different token string.

Same credentials. Different token. Every single time.

The formula is simple:
JWT = base64(header) + "." + base64(payload) + "." + HMAC(header+payload, secret)

Change even one byte in the payload, and the entire signature changes.

That's not a bug — it's a feature. It's what makes JWTs secure against replay attacks and token reuse.

Built this with Flask + PyJWT to make it click visually. Color-coded the three parts of the token, highlighted what changes between logins, and added a real-time comparison view.

Sometimes the best way to learn security concepts is to watch them happen live.

#JWT #WebSecurity #Authentication #Python #Flask #BackendDevelopment #CyberSecurity #LearnInPublic #SoftwareEngineering

---

### Option 2 — Storytelling / Beginner-Friendly

I kept asking myself: "Why is my JWT different every time I log in?"

Same username. Same password. Different token. Every. Single. Time.

So I built a tiny app to find out.

Here's what I learned:

A JWT has three parts:
1. Header — the algorithm used (stays the same)
2. Payload — your data + timestamps (changes every login)
3. Signature — a hash of 1 + 2 + a secret key

The key insight? The payload includes `iat` (issued-at time). Since you log in at a different moment each time, the timestamp changes. And since the signature is computed FROM the payload, it changes too.

One different second = one completely different token.

This is actually brilliant security design:
- Prevents token replay attacks
- Each session is uniquely identifiable
- Expired tokens can't be reused

I visualized this with a Flask app where you can log in multiple times side by side and literally watch the tokens diverge. Color-coded the header (pink), payload (purple), and signature (blue) so you can see which parts change.

If you're learning about authentication, build something like this. Reading docs is good. Watching it happen is better.

#JWT #Authentication #WebDev #Python #InfoSec #LearningByDoing #BackendDev #SoftwareEngineering #CyberSecurity

---

### Option 3 — Technical / Senior Audience

JWT tokens are deterministic in structure but non-deterministic in output. Here's why that matters.

Given identical credentials, two login requests will always produce different JWTs because the payload includes time-dependent claims:

```
{
  "sub": "admin",       // same
  "iat": 1738944000.1,  // different — issued NOW
  "exp": 1738947600.1   // different — expires in 1hr from NOW
}
```

Since HMAC-SHA256 is computed over header + payload, even a fractional-second difference in `iat` cascades into a completely different signature — and therefore a completely different token.

This isn't accidental. It's by design:
- Replay resistance — stolen tokens expire
- Session isolation — each login is independently revocable
- Audit trails — `iat` tells you exactly when a session began

Built a visual demo (Flask + PyJWT) that color-codes the three JWT segments and diffs payloads across logins in real time. Useful for teaching auth concepts to junior devs or onboarding teams.

Sometimes the simplest builds teach the most.

#JWT #HMAC #Authentication #APISecurity #Python #WebSecurity #SoftwareArchitecture #BackendEngineering

---

### Option 4 — Carousel / Slide Deck Script

If you're making a LinkedIn carousel (PDF slides), here's the slide-by-slide content:

**Slide 1 (Hook)**
"Same password. Different token. Every time. Here's why."

**Slide 2**
What is a JWT?
A JSON Web Token has 3 parts:
- Header (algorithm info)
- Payload (your data)
- Signature (proof it wasn't tampered with)

**Slide 3**
The payload includes timestamps:
- `iat` = issued at (when you logged in)
- `exp` = expiry (when the token dies)

**Slide 4**
Login at 10:00:01 AM → iat = 1738944001
Login at 10:00:05 AM → iat = 1738944005
Same user. Different payload.

**Slide 5**
The signature = HMAC(header + payload, secret)
Different payload → different signature → different JWT

**Slide 6**
Why this matters:
- Replay attack resistance
- Each session is unique and traceable
- Expired tokens can't be recycled

**Slide 7 (CTA)**
I built a live demo to visualize this.
Flask app, color-coded tokens, real-time comparison.
Link in comments / DM me for the code.

---
