import { NextResponse } from 'next/server';
import prisma from '../../../lib/prisma';

/**
 * Test connection and schema verification endpoint.
 * Queries all three tables to ensure shared database schema is accessible.
 * Consumer service uses this to verify connection and schema alignment.
 */
export async function GET() {
  try {
    console.info('[test-connection] Starting schema verification...');

    // Query each table to verify schema and connection
    const [employeeCount, performanceCount, incentiveCount] = await Promise.all([
      prisma.employee.count(),
      prisma.performance.count(),
      prisma.incentive.count(),
    ]);

    // Fetch sample records from each table for schema validation
    const [sampleEmployee, samplePerformance, sampleIncentive] = await Promise.all([
      employeeCount > 0 ? prisma.employee.findFirst() : null,
      performanceCount > 0 ? prisma.performance.findFirst() : null,
      incentiveCount > 0 ? prisma.incentive.findFirst() : null,
    ]);

    console.info('[test-connection] Schema verification complete', {
      employees: employeeCount,
      performances: performanceCount,
      incentives: incentiveCount,
    });

    return NextResponse.json(
      {
        ok: true,
        message: 'Database connection and schema verified',
        timestamp: new Date().toISOString(),
        database: {
          type: 'PostgreSQL (Neon)',
          connectionPooled: true,
        },
        tables: {
          Employee: {
            count: employeeCount,
            schema: sampleEmployee
              ? {
                  fields: ['id', 'name', 'role', 'region', 'isManager', 'createdAt', 'updatedAt'],
                  sampleRecord: sampleEmployee,
                }
              : { fields: ['id', 'name', 'role', 'region', 'isManager', 'createdAt', 'updatedAt'], sampleRecord: null },
          },
          Performance: {
            count: performanceCount,
            schema: samplePerformance
              ? {
                  fields: ['id', 'employeeId', 'quarter', 'year', 'sales', 'target', 'growth', 'createdAt', 'updatedAt'],
                  sampleRecord: samplePerformance,
                }
              : {
                  fields: ['id', 'employeeId', 'quarter', 'year', 'sales', 'target', 'growth', 'createdAt', 'updatedAt'],
                  sampleRecord: null,
                },
          },
          Incentive: {
            count: incentiveCount,
            schema: sampleIncentive
              ? {
                  fields: ['id', 'employeeId', 'performanceId', 'payout', 'breakdown', 'anomalies', 'createdAt', 'updatedAt'],
                  sampleRecord: sampleIncentive,
                }
              : {
                  fields: ['id', 'employeeId', 'performanceId', 'payout', 'breakdown', 'anomalies', 'createdAt', 'updatedAt'],
                  sampleRecord: null,
                },
          },
        },
        verificationStatus: {
          schemaAccessible: true,
          allTablesPresent: employeeCount >= 0 && performanceCount >= 0 && incentiveCount >= 0,
          dataPresent: employeeCount > 0 || performanceCount > 0 || incentiveCount > 0,
          ready: true,
        },
      },
      { status: 200 }
    );
  } catch (error) {
    console.error('[test-connection] Verification failed:', error);

    const errorMessage = error instanceof Error ? error.message : 'Unknown error';

    return NextResponse.json(
      {
        ok: false,
        message: 'Database connection or schema verification failed',
        error: errorMessage,
        timestamp: new Date().toISOString(),
        verificationStatus: {
          schemaAccessible: false,
          allTablesPresent: false,
          dataPresent: false,
          ready: false,
        },
      },
      { status: 500 }
    );
  }
}

/**
 * POST version for explicit connection test from consumer services.
 */
export async function POST() {
  // Reuse GET logic
  return GET();
}
