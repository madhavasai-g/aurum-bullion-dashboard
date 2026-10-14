# Aurum Bullion Dashboard

A mobile-friendly, dark glassmorphism gold spot dashboard designed for free GitHub Pages hosting.

## Features
- Live XAU/USD spot reference from [Gold API](https://gold-api.com/), no API key.
- USD/INR conversion reference from [Open ER-API](https://www.exchangerate-api.com/docs/free).
- Automatic spot-equivalent values for 1g, 1.5g, 2g, 3g, 5g, 8g, and 10g.
- Custom weight and purity calculator; optional retail estimate with explicitly editable assumptions.
- GitHub Actions snapshot workflow scheduled twice per hour, plus manual workflow dispatch.
- Source and update timestamps; stored history for comparison.

## Publish on GitHub Pages (free)
1. Create a public GitHub repository, for example `aurum-bullion-dashboard`.
2. Upload the contents of this folder to the repository root. Keep `.github/workflows/update-gold.yml` in place.
3. Open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select `main` and `/(root)`, then Save.
4. Open **Actions**. If prompted, enable workflows. Select **Update gold spot snapshot → Run workflow** once to seed `data/latest.json` and history.
5. If the workflow cannot push, open **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, and save. Then run the workflow again.
6. Your site URL will appear in **Settings → Pages** (usually `https://YOUR-USERNAME.github.io/REPOSITORY/`).

## Price methodology and limits
- The API reports gold in USD per troy ounce. The dashboard converts using 31.1034768 grams per troy ounce and a published USD/INR reference rate.
- This is an indicative international spot-equivalent, **not** the exact local Indian 24K/22K jeweller or coin selling price. Retail rates can include GST, dealer/mint premium, packaging, delivery, and local differences.
- The FX provider's reference rate may refresh daily while gold can update more often. The UI displays source timestamps when available.
- GitHub Actions schedules are best-effort and may be delayed. It is not a continuous 24/7 process. The dashboard also attempts direct refresh in the browser every five minutes while open.
- Public GitHub Pages repositories expose committed data publicly. Do not store secrets in this repository.

## Product links
This first version focuses on bullion spot math and does not pretend to have verified coin listings. Product links are intentionally omitted until each product URL, weight, purity, seller and final price can be validated. Retailer scraping may be blocked or disallowed and can be brittle; prefer an authorized affiliate/product API or a retailer feed for automated catalogue data.

## Sources
- Gold spot: https://api.gold-api.com/price/XAU — documentation: https://gold-api.com/docs
- USD/INR reference: https://open.er-api.com/v6/latest/USD — documentation: https://www.exchangerate-api.com/docs/free


## Marketplace jewellery comparison
The dashboard includes quick navigation links and a marketplace search section for Amazon India, AJIO, Myntra, and Flipkart. Enter a jewellery type and choose purity/weight to build search links for each store. This is a search-based comparison helper, not a live price aggregator: marketplaces do not expose a shared, reliable free product-price API for this static GitHub Pages site. Confirm purity, hallmark, net gold weight, taxes, making charges, shipping, seller, and return policy on each listing.
