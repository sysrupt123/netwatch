# Each rule is (list of domain endings, category). The first match wins,
# so more specific groups (ads) come before broader ones (Google).
RULES = [
    (["doubleclick.net", "googlesyndication.com", "google-analytics.com",
      "googletagmanager.com", "adservice.google.com", "googleadservices.com",
      "scorecardresearch.com", "hotjar.com", "adnxs.com"], "Ads and trackers"),
    (["google.com", "gstatic.com", "googleapis.com", "googleusercontent.com",
      "youtube.com", "ytimg.com", "googlevideo.com"], "Google"),
    (["microsoft.com", "windows.com", "msftconnecttest.com", "live.com",
      "office.com", "bing.com"], "Microsoft"),
    (["facebook.com", "fbcdn.net", "instagram.com", "whatsapp.com",
      "whatsapp.net", "twitter.com", "x.com", "tiktok.com",
      "snapchat.com"], "Social media"),
    (["cloudflare.com", "akamai.net", "akamaiedge.net", "fastly.net",
      "cloudfront.net", "azureedge.net"], "CDN / infrastructure"),
    (["kali.org", "debian.org", "ubuntu.com", "github.com",
      "githubusercontent.com", "pypi.org", "pythonhosted.org"],
     "Dev and system updates"),
    (["mozilla.org", "mozilla.com", "mozilla.net", "firefox.com"],
     "Browser (Mozilla)"),
]


def categorize(domain):
    domain = domain.lower()
    for endings, category in RULES:
        for ending in endings:
            # match the whole domain or a sub-domain, so "x.com" does not match "netflix.com"
            if domain == ending or domain.endswith("." + ending):
                return category
    return "Other"
