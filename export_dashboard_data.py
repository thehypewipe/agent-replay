"""Export demo data to JSON for dashboard"""

import sqlite3
import json

conn = sqlite3.connect("./demo_runs.db")
conn.row_factory = sqlite3.Row

# Get all runs with their messages
cursor = conn.execute("""
    SELECT
        run_id,
        feature,
        provider,
        model,
        tokens_in,
        tokens_out,
        cost,
        created_at,
        metadata
    FROM runs
    ORDER BY created_at DESC
""")

runs = []
for row in cursor.fetchall():
    run_data = dict(row)

    # Parse metadata
    if run_data['metadata']:
        run_data['metadata'] = json.loads(run_data['metadata'])

    # Get messages for this run
    msg_cursor = conn.execute("""
        SELECT role, content
        FROM messages
        WHERE run_id = ?
        ORDER BY id ASC
    """, (run_data['run_id'],))

    run_data['messages'] = [dict(m) for m in msg_cursor.fetchall()]
    runs.append(run_data)

# Get feature summaries
cursor = conn.execute("""
    SELECT
        feature,
        COUNT(*) as run_count,
        SUM(cost) as total_cost,
        AVG(cost) as avg_cost,
        SUM(tokens_in) as total_tokens_in,
        SUM(tokens_out) as total_tokens_out,
        provider,
        model
    FROM runs
    GROUP BY feature, provider, model
""")

features = [dict(row) for row in cursor.fetchall()]

# Get provider breakdown
cursor = conn.execute("""
    SELECT
        provider,
        COUNT(*) as run_count,
        SUM(cost) as total_cost
    FROM runs
    GROUP BY provider
""")

providers = [dict(row) for row in cursor.fetchall()]

conn.close()

# Write to JSON
data = {
    "runs": runs,
    "features": features,
    "providers": providers,
    "generated_at": "2026-09-21T16:20:00Z"
}

with open("dashboard_data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Exported {len(runs)} runs to dashboard_data.json")
print(f"Features: {len(features)}")
print(f"Providers: {len(providers)}")
