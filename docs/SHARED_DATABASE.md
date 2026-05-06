# Shared Database Architecture

## Overview

The Enterprise Incentive Intelligence System uses a **unified PostgreSQL database** (Neon) as the single source of truth for all incentive and performance data. Multiple services and dashboards connect to this shared schema, ensuring data consistency and enabling real-time cross-system visibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   NEON POSTGRESQL (Shared)                  │
│                                                             │
│  ┌──────────  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Employee   │ Perform  │  │Incentive │  │  Indexes │    │
│  │ (id, name, │ ance     │  │(id,      │  │ (PK, FK,│    │
│  │ role,      │(id,e_id, │  │e_id,     │  │ Quarter)│    │
│  │ region)    │quarter)  │  │quarter)  │  │         │    │
│  └──────────  └──────────┘  └──────────┘  └──────────┘    │
│                                                             │
│  Connection: postgresql://...?sslmode=require              │
│  Pooling: Neon Connection Pooler (recommended)             │
│  Database URL: Stored in DATABASE_URL environment variable │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ▲                 ▲
        ┌─────────────────┴─────────────────┴──────────┐
        │                                              │
   ┌────────────┐                            ┌────────────────┐
   │  Dashboard │                            │   API Service  │
   │ (Next.js)  │──── read/write ────────────│  (Next.js API) │
   │            │   via Prisma               │                │
   └────────────┘                            └────────────────┘
         │                                           │
         └─────────── Shared Schema ────────────────┘
                (Employee, Performance, Incentive)
```

## Shared Schema

### Models

**Employee**
- Central entity: represents each employee in the system
- Fields: id, name, role, region, isManager, createdAt
- Relations: One-to-many with Performance and Incentive records
- Indexes: region, role (for filtering queries)

**Performance**
- Tracks quarterly sales and growth metrics
- Fields: id, employeeId (FK), quarter, year, sales, target, growth, createdAt
- Relations: Belongs to Employee; One-to-one with Incentive
- Constraints: Unique on (employeeId, quarter, year) — prevents duplicates
- Indexes: employeeId, (quarter, year)

**Incentive**
- Calculated payouts based on business rules
- Fields: id, employeeId (FK), performanceId (FK), payout, breakdown (JSON), anomalies (array), createdAt
- Relations: Belongs to Employee and Performance
- Cascade Deletes: If Employee/Performance deleted, Incentive is removed too
- Indexes: employeeId, createdAt (for audit trails)

## Connection & Configuration

### Environment Variable

```bash
# .env.local or Vercel environment settings
DATABASE_URL="postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require"
```

**Example (Neon):**
```
DATABASE_URL="postgresql://neondb_owner:abc123xyz@ep-lively-brook.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

### Connection Pooling

- **Neon Pooler**: Use the pooler endpoint (hosted by Neon) for serverless environments
- **Direct Connection**: Use regular endpoint for local development
- **SSL Mode**: Always use `?sslmode=require` for security

### Prisma Configuration

Located in `prisma/schema.prisma`:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

Prisma auto-loads `DATABASE_URL` and connects on startup.

## Multi-Service Usage

### Service 1: Web Dashboard (Next.js)

**File:** `lib/prisma.ts`

```typescript
import { PrismaClient } from '@prisma/client'

export const prisma = global.prisma ?? new PrismaClient()
```

**Usage in Pages/APIs:**

```typescript
// app/page.tsx - Dashboard
const employees = await prisma.employee.findMany()
const incentives = await prisma.incentive.aggregate({ _sum: { payout: true } })
```

### Service 2: Analytics API

```typescript
// app/api/top-performers/route.ts
const topPerformers = await prisma.incentive.findMany({
  take: 10,
  orderBy: { payout: 'desc' },
  include: { employee: true }
})
```

### Service 3: Audit Service (Future)

Any service can connect to the same database:

```typescript
const auditRecord = await prisma.incentive.findUnique({
  where: { id: 'xyz' },
  include: { employee: true, performance: true }
})
```

## Data Integrity

### Cascade Deletes

If an employee is deleted, all related Performance and Incentive records are automatically deleted:

```prisma
employee Employee @relation(..., onDelete: Cascade)
```

This ensures no orphaned records.

### Unique Constraints

- `Performance`: Unique on (employeeId, quarter, year) — prevents duplicate quarterly records
- `Incentive`: performanceId is unique — one incentive per performance

### Referential Integrity

All foreign keys use `@relation` with proper constraints. Database enforces referential integrity.

## Deployment

### Local Development

1. **Create Neon Database:**
   ```bash
   # Visit https://neon.tech
   # Create project → create branch → copy connection string
   ```

2. **Set Environment:**
   ```bash
   # .env.local
   DATABASE_URL="postgresql://...?sslmode=require"
   ```

3. **Initialize Schema:**
   ```bash
   npx prisma generate
   npx prisma db push
   npm run seed
   ```

### Production (Vercel)

1. **Set Environment Variables in Vercel:**
   - Key: `DATABASE_URL`
   - Value: Neon connection string for production branch

2. **Build Script:** (Already configured in `package.json`)
   ```json
   "build": "npx prisma generate && next build"
   ```

3. **Deploy:**
   ```bash
   git push origin main  # Vercel auto-deploys
   ```

4. **Seed Production (one-time):**
   ```bash
   curl -X POST https://your-app.vercel.app/api/generate-data
   curl -X POST https://your-app.vercel.app/api/calculate-incentives
   ```

## Performance Optimization

### Indexes

Defined in schema for common query patterns:

- `Employee[region]` — Filter employees by region (Analytics page)
- `Employee[role]` — Filter by job role (Analytics page)
- `Performance[employeeId, quarter, year]` — Unique constraint for period lookups
- `Incentive[employeeId]` — Employee audit trails
- `Incentive[createdAt]` — Time-based queries and audit logs

### Connection Pooling

Neon's connection pooler handles:
- Connection reuse across serverless functions
- Automatic idle timeout and cleanup
- Load balancing

### Query Patterns

Use Prisma's `include` and `select` to optimize:

```typescript
// Good: Only fetch needed fields
await prisma.incentive.findMany({
  select: { id: true, payout: true, employee: { select: { name: true } } }
})

// Avoid: Fetching unnecessary relations
await prisma.incentive.findMany({ include: { anything: true } })
```

## Monitoring & Maintenance

### Database Health

Check Neon dashboard for:
- Connection count
- Query performance
- Storage usage

### Data Consistency

Periodically verify data integrity:

```typescript
// Find orphaned incentives (shouldn't exist with cascade delete)
const orphaned = await prisma.incentive.findMany({
  where: { employee: null }
})

// Verify unique constraint on Performance
const duplicates = await prisma.performance.groupBy({
  by: ['employeeId', 'quarter', 'year'],
  having: { id: { _count: { gt: 1 } } }
})
```

### Backups

Neon automatically creates backups. Access them in the Neon dashboard under Branch → Backups.

## Adding New Services

To connect another service to the shared database:

1. **Install Prisma:**
   ```bash
   npm install @prisma/client prisma
   ```

2. **Copy Schema:**
   ```bash
   # Copy prisma/schema.prisma from this repo
   ```

3. **Set DATABASE_URL:**
   ```bash
   # Same Neon connection string used by all services
   DATABASE_URL="postgresql://...?sslmode=require"
   ```

4. **Generate Client:**
   ```bash
   npx prisma generate
   ```

5. **Use in Code:**
   ```typescript
   import { PrismaClient } from '@prisma/client'
   const prisma = new PrismaClient()
   const employees = await prisma.employee.findMany()
   ```

## Troubleshooting

### "Error: Prisma Client not generated"

**Fix:**
```bash
npx prisma generate
```

### "Error: connect ECONNREFUSED"

**Fix:** Verify DATABASE_URL is set and reachable:
```bash
echo $DATABASE_URL
psql $DATABASE_URL -c "SELECT 1"
```

### "Error: Too many connections"

**Fix:** Ensure Prisma singleton is used (not creating new clients):
```typescript
// lib/prisma.ts
export const prisma = global.prisma ?? new PrismaClient()
```

### "PrismaClientInitializationError" on Vercel

**Fix:** Ensure build script includes `npx prisma generate`:
```json
"build": "npx prisma generate && next build"
```

## References

- [Neon Documentation](https://neon.tech/docs/)
- [Prisma PostgreSQL Provider](https://www.prisma.io/docs/concepts/database-connectors/postgresql)
- [Prisma Relations](https://www.prisma.io/docs/concepts/relations)
- [Cascade Deletes](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference#cascade)
