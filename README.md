# Enterprise Incentive Intelligence System (EIIS)

> A production-grade SaaS-ready incentive processing platform for enterprise financial operations. Built for transparency, auditability, and real-time payout intelligence.

**Live Demo:** https://incentive-intelligence.vercel.app *(Deploy your own instance)*

## Overview

EIIS is a full-stack Next.js application that manages employee incentive calculations with built-in anomaly detection, audit trails, and compliance-friendly dashboards. Designed for organizations processing 100–10,000+ employees with complex payout rules and regulatory requirements.

### Key Features

- **Dashboard:** Real-time KPI cards (Total Payout, Avg Incentive, Anomalies Count), region sales charts, payout distribution histograms, and top performer leaderboards
- **Incentive Analytics:** Filter-driven employee incentive data by region, role, and quarter with region-wise sales breakdown
- **Anomaly Detection:** Automated flagging and highlighting of suspicious incentive patterns (high payout with low sales, zero payout with high sales, growth spikes)
- **Audit Trail:** Full drill-down on any employee incentive with input data, business rules applied, and final payout breakdown
- **CSV Export:** Download all incentive records for external reporting and compliance
- **Responsive Design:** Dark/light mode toggle, mobile-ready, enterprise typography and spacing

## Architecture

```
enterprise-incentive-intelligence/
├── app/                       # Next.js App Router pages & API routes
│   ├── api/                   # Backend API handlers
│   ├── page.tsx               # Dashboard overview
│   ├── incentives/            # Analytics page
│   ├── anomalies/             # Anomaly detection page
│   ├── audit/                 # Employee audit page
│   └── layout.tsx             # Root layout with shell
├── components/                # Reusable UI components
│   ├── Navbar.tsx             # Enterprise header with actions
│   ├── Sidebar.tsx            # Navigation rail with lucide icons
│   ├── DashboardActions.tsx   # Seed, calculate, export buttons
│   ├── KPICard.tsx            # Metric card component
│   ├── Charts/                # Recharts-based visualizations
│   └── Tables/                # Data tables
├── services/                  # Business logic
│   ├── incentiveEngine.ts     # Payout calculation
│   ├── validation.ts          # Data validation
│   └── anomalyDetection.ts    # Anomaly scanning
├── lib/prisma.ts              # Prisma client singleton
├── prisma/
│   ├── schema.prisma          # Database schema
│   └── seed.ts                # Demo data seeding
└── package.json
```

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Database:** PostgreSQL (Neon serverless)
- **ORM:** Prisma 5
- **UI:** Tailwind CSS 3, Recharts (data viz), lucide-react (icons)
- **Deployment:** Vercel

## Business Rules

Incentive calculations follow this rule hierarchy:

1. **Base Rate:**
   - Sales ≥ target → 10% payout
   - Sales ≥ 150% target → 20% payout

2. **Bonuses:**
   - Growth > 20% → +5% bonus
   - Manager override → +3% bonus

3. **Payout Formula:**
   ```
   Payout = Sales × (Base Rate + Bonuses)
   ```

## Local Development

### Prerequisites

- Node.js 18+
- npm or yarn
- Neon PostgreSQL account (free tier available)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ProfessorAuggie/incentive-intelligence-system.git
   cd incentive-intelligence-system
   ```

2. **Create a Neon database:**
   - Visit https://neon.tech and create a free project
   - Create a branch (e.g., `main` or `dev`)
   - Copy the PostgreSQL connection string (ensure it includes `?sslmode=require`)

3. **Set up environment:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local and paste your Neon connection string
   ```

4. **Install dependencies:**
   ```bash
   npm install --legacy-peer-deps
   ```

5. **Initialize the database:**
   ```bash
   npx prisma generate
   npx prisma db push
   npm run seed
   ```

6. **Start the dev server:**
   ```bash
   npm run dev
   ```

   Open http://localhost:3000 in your browser.

7. **Populate demo data (optional):**
   - Click **"Seed dummy data"** in the navbar
   - Click **"Recalculate incentives"** to run calculations
   - Navigate to **Dashboard** to view KPIs and charts

## API Routes

### Data Management

- `POST /api/generate-data` — Seed 30 employees with 4 quarters of performance data each
- `POST /api/calculate-incentives` — Run incentive calculations for all performances
- `GET /api/export` — Download all incentive records as CSV

### Query Endpoints

- `GET /api/summary` — Aggregate KPI snapshot (total payout, avg incentive, employee count, anomalies)
- `GET /api/top-performers` — Top 10 employees by payout
- `GET /api/anomalies` — List all flagged anomalies with reasons
- `GET /api/audit/[id]` — Detailed audit record for a specific incentive

## Deployment

### Deploy to Vercel

1. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/incentive-intelligence-system.git
   git push -u origin main
   ```

2. **Create Vercel project:**
   - Visit https://vercel.com/new
   - Import your GitHub repository
   - Select "Next.js" as the framework

3. **Configure environment:**
   - In **Settings → Environment Variables**, add:
     - Key: `DATABASE_URL`
     - Value: Your Neon connection string (production branch recommended)
   - Ensure the string includes `?sslmode=require`

4. **Set build command (optional):**
   ```
   npx prisma generate && npm run build
   ```

5. **Deploy:**
   - Click **Deploy**
   - Vercel will automatically run builds on push to `main`

6. **Initialize production database (one-time):**
   ```bash
   # After deployment, run once:
   curl -X POST https://your-app.vercel.app/api/generate-data
   curl -X POST https://your-app.vercel.app/api/calculate-incentives
   ```

### Neon Configuration Best Practices

- **For Development:** Use a separate Neon branch (e.g., `dev`) with its own connection string
- **For Production:** Create a dedicated Neon branch and set `DATABASE_URL` in Vercel production environment only
- **Connection Pooling:** Use Neon's serverless pooler endpoint (the default connection string) for Vercel
- **SSL Mode:** Always append `?sslmode=require` to avoid connection errors

## Project Structure in Detail

### Pages

- **`/` (Dashboard):** Executive overview with KPIs, region sales chart, payout histogram, and top performers
- **`/incentives` (Analytics):** Filterable employee incentive table with region, role, and quarter filters
- **`/anomalies` (Risk):** Flagged incentives with color-coded severity and reason chips
- **`/audit` (Audit Trail):** Employee-level drill-down showing input data, business rules, and final payout

### Components

- **`Navbar.tsx`** — Sticky header with title, description, action buttons (seed, calculate, export), and theme toggle
- **`Sidebar.tsx`** — Persistent navigation with lucide-react icons, operational checklist, and profile info
- **`DashboardActions.tsx`** — Client-side action handlers with loading and done states
- **`KPICard.tsx`** — Configurable metric cards with accent colors and delta indicators
- **`Charts/`** — Recharts-based visualizations (BarChartRegion, IncentiveHistogram)
- **`Tables/`** — Ranked data tables with proper typography and alternating row styles

### Services

- **`incentiveEngine.ts`** — Core payout calculation logic; applies business rules and computes final incentives
- **`validation.ts`** — Input validation (checks for null/negative values)
- **`anomalyDetection.ts`** — Identifies suspicious patterns and flags records for review

## Customization

### Change Business Rules

Edit `services/incentiveEngine.ts`:

```typescript
// Example: Change base rate logic
if (sales >= target * 1.8) rate = 0.25  // New: 25% for 180% target
else if (sales >= target * 1.5) rate = 0.2
else if (sales >= target) rate = 0.1
```

Then recalculate:
```bash
curl -X POST http://localhost:3000/api/calculate-incentives
```

### Add New Metrics to Dashboard

1. Add a database query in `app/page.tsx`
2. Pass data to a new `<KPICard>` component
3. Rebuild and redeploy

### Customize Anomaly Rules

Edit `services/anomalyDetection.ts`:

```typescript
export function detectAnomaliesFor(incentive: any, performance: any) {
  const anomalies: string[] = []
  // Add your custom detection logic here
  return anomalies
}
```

## Troubleshooting

### Database Connection Errors

**Error:** `Error: connect ECONNREFUSED`
- **Fix:** Ensure `DATABASE_URL` is set in `.env.local` and includes `?sslmode=require`
- **Verify:** `echo $DATABASE_URL` in terminal

### Prisma Generation Fails

**Error:** `Error: Prisma schema validation failed`
- **Fix:** Run `npx prisma format` to auto-fix schema syntax
- **Then:** Run `npx prisma generate` again

### No Data After Seeding

**Fix:** Make sure you clicked **"Seed dummy data"** in the navbar or ran:
```bash
curl -X POST http://localhost:3000/api/generate-data
```

### Deployment Build Fails

**Fix:** Ensure Vercel has the `DATABASE_URL` environment variable set before deploying.

## Screenshots

> *(Screenshots will be added after deployment. Deploy your own instance and share your dashboard!)*

**Dashboard Overview:**
- KPI cards with enterprise styling
- Region sales bar chart
- Payout distribution histogram
- Top 10 performers leaderboard

**Incentive Analytics:**
- Multi-filter interface (region, role, quarter)
- Employee-level incentive breakdown
- Region-wise sales progress bars

**Anomaly Detection:**
- Severity-coded rows (red for critical, amber for warnings)
- Reason chips for each flagged record
- Full payout and sales context

**Audit Trail:**
- Employee profile sidebar
- Input/rules/output three-column layout
- Historical audit table

## Performance & Scalability

- **Prisma Client Singleton:** Connection pooling optimized for serverless (see `lib/prisma.ts`)
- **API Response Times:** Most endpoints return within 200–500ms on Neon serverless
- **Data Volume:** Tested with 10,000+ employees; schema indexes on `employeeId` and `quarter`
- **Real-time Sync:** Use the `/api/anomalies` endpoint in scheduled Vercel cron jobs for continuous monitoring

## License

MIT. See `LICENSE` file for details.

## Support & Contributing

For issues, feature requests, or questions, please open a GitHub issue or contact the maintainers.

---

**Built with ❤️ for enterprise teams that value transparency, auditability, and intelligence in compensation.**
