# Hosting Notes

Tectori's public website is prepared for free GitHub Pages hosting from the `docs/` folder.

## GitHub Pages

- Repository: `k3rt4s/tectori`
- Branch: `main`
- Publishing source: `/docs`
- Custom domain: `www.tectori.com`

## Domain

Public RDAP shows `tectori.com` is registered with Dynadot Inc and uses
Dynadot nameservers.

Set these DNS records in Dynadot after GitHub Pages is enabled:

| Type  | Host | Value                |
| ----- | ---- | -------------------- |
| CNAME | www  | k3rt4s.github.io     |
| A     | @    | 185.199.108.153      |
| A     | @    | 185.199.109.153      |
| A     | @    | 185.199.110.153      |
| A     | @    | 185.199.111.153      |
| AAAA  | @    | 2606:50c0:8000::153  |
| AAAA  | @    | 2606:50c0:8001::153  |
| AAAA  | @    | 2606:50c0:8002::153  |
| AAAA  | @    | 2606:50c0:8003::153  |

The `docs/CNAME` file sets `www.tectori.com` as the canonical hostname.
