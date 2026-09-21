"""CLI commands"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

from .replay import replay_run, list_runs
from .diff import diff_runs
from .detector import detect_hallucinations

console = Console()


@click.group()
def cli():
    """Agent Replay - Local-first agent debugging"""
    pass


@cli.command()
@click.option("--db", default="./agent_runs.db", help="Database path")
@click.option("--feature", help="Filter by feature")
@click.option("--limit", default=20, help="Max results")
def list(db: str, feature: str, limit: int):
    """List recent runs"""
    runs = list_runs(db, feature=feature, limit=limit)

    if not runs:
        console.print("[yellow]No runs found[/yellow]")
        return

    table = Table(title="Agent Runs", box=box.ROUNDED)
    table.add_column("Run ID", style="cyan")
    table.add_column("Feature", style="magenta")
    table.add_column("Model", style="green")
    table.add_column("Cost", style="yellow")
    table.add_column("Created", style="blue")

    for run in runs:
        table.add_row(
            run["run_id"],
            run["feature"],
            run["model"],
            f"${run['cost']:.4f}",
            run["created_at"][:19]
        )

    console.print(table)


@cli.command()
@click.option("--db", default="./agent_runs.db", help="Database path")
@click.option("--feature", help="Filter by feature")
def report(db: str, feature: str):
    """Show cost report"""
    import sqlite3

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row

    if feature:
        cursor = conn.execute("""
            SELECT
                feature,
                model,
                COUNT(*) as runs,
                SUM(cost) as total_cost,
                SUM(tokens_in) as total_tokens_in,
                SUM(tokens_out) as total_tokens_out
            FROM runs
            WHERE feature = ?
            GROUP BY feature, model
        """, (feature,))
    else:
        cursor = conn.execute("""
            SELECT
                feature,
                model,
                COUNT(*) as runs,
                SUM(cost) as total_cost,
                SUM(tokens_in) as total_tokens_in,
                SUM(tokens_out) as total_tokens_out
            FROM runs
            GROUP BY feature, model
        """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]No runs found[/yellow]")
        return

    table = Table(title="Cost Report", box=box.ROUNDED)
    table.add_column("Feature", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Runs", style="magenta")
    table.add_column("Total Cost", style="yellow")
    table.add_column("Tokens In", style="blue")
    table.add_column("Tokens Out", style="blue")

    total_cost = 0.0
    for row in rows:
        table.add_row(
            row["feature"],
            row["model"],
            str(row["runs"]),
            f"${row['total_cost']:.4f}",
            f"{row['total_tokens_in']:,}",
            f"{row['total_tokens_out']:,}"
        )
        total_cost += row["total_cost"]

    console.print(table)
    console.print(f"\n[bold]Total cost:[/bold] [yellow]${total_cost:.4f}[/yellow]")


@cli.command()
@click.argument("run_id")
@click.option("--db", default="./agent_runs.db", help="Database path")
def replay(run_id: str, db: str):
    """Replay a specific run"""
    try:
        run = replay_run(db, run_id)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        return

    console.print(f"\n[bold cyan]Run {run['run_id']}[/bold cyan]")
    console.print(f"Feature: {run['feature']}")
    console.print(f"Model: {run['model']} ({run['provider']})")
    console.print(f"Cost: ${run['cost']:.4f}")
    console.print(f"Tokens: {run['tokens_in']} in, {run['tokens_out']} out")
    console.print(f"Created: {run['created_at']}")

    if run['metadata']:
        console.print(f"Metadata: {json.dumps(run['metadata'], indent=2)}")

    console.print("\n[bold]Messages:[/bold]")
    for i, msg in enumerate(run['messages'], 1):
        role_color = "green" if msg['role'] == "user" else "blue"
        console.print(f"\n[{role_color}]{msg['role'].upper()}:[/{role_color}]")
        console.print(msg['content'][:500] + ("..." if len(msg['content']) > 500 else ""))

    if run['flags']:
        console.print("\n[bold red]Flags:[/bold red]")
        for flag in run['flags']:
            console.print(f"  • [{flag['severity']}] {flag['flag_type']}: {flag['description']}")


@cli.command()
@click.option("--run1", required=True, help="First run ID")
@click.option("--run2", required=True, help="Second run ID")
@click.option("--db", default="./agent_runs.db", help="Database path")
def diff(run1: str, run2: str, db: str):
    """Compare two runs"""
    try:
        comparison = diff_runs(db, run1, run2)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        return

    console.print(f"\n[bold]Comparing runs[/bold]")
    console.print(f"Run 1: {comparison['run1']['run_id']} ({comparison['run1']['created_at'][:19]})")
    console.print(f"Run 2: {comparison['run2']['run_id']} ({comparison['run2']['created_at'][:19]})")

    md = comparison['metadata_diff']

    console.print(f"\n[bold]Metadata:[/bold]")
    console.print(f"Model: {md['model']['run1']} → {md['model']['run2']} " +
                  ("(changed)" if md['model']['changed'] else "(same)"))
    console.print(f"Cost: ${md['cost']['run1']:.4f} → ${md['cost']['run2']:.4f} " +
                  f"(delta: ${md['cost']['delta']:+.4f})")
    console.print(f"Tokens in: {md['tokens']['run1']['in']} → {md['tokens']['run2']['in']} " +
                  f"(delta: {md['tokens']['delta_in']:+d})")
    console.print(f"Tokens out: {md['tokens']['run1']['out']} → {md['tokens']['run2']['out']} " +
                  f"(delta: {md['tokens']['delta_out']:+d})")

    if comparison['message_diffs']:
        console.print(f"\n[bold]Message differences:[/bold]")
        for diff in comparison['message_diffs']:
            console.print(f"\nMessage {diff['index']}: {diff['status']}")
            if diff['status'] == 'changed':
                console.print(diff['diff'][:1000])


@cli.command()
@click.option("--db", default="./agent_runs.db", help="Database path")
@click.option("--output", required=True, help="Output CSV file")
def export(db: str, output: str):
    """Export runs to CSV"""
    import sqlite3
    import csv

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row

    cursor = conn.execute("SELECT * FROM runs ORDER BY created_at DESC")
    rows = cursor.fetchall()

    if not rows:
        console.print("[yellow]No runs to export[/yellow]")
        return

    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))

    conn.close()
    console.print(f"[green]Exported {len(rows)} runs to {output}[/green]")


if __name__ == "__main__":
    cli()
