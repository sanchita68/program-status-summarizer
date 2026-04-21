# Copyright © 2026 Sanchita Hosur. All Rights Reserved.
# github.com/sanchita68

import os
import pandas as pd
import anthropic
from dotenv import load_dotenv
from datetime import date

# Load API key from .env file
load_dotenv()

def load_program_data(filepath: str) -> str:
    """Load CSV data and convert to readable text for the LLM."""
    df = pd.read_csv(filepath)
    return df.to_string(index=False)

def generate_status_report(data: str) -> str:
    """Send program data to Claude and get a formatted status report."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""
You are a Senior Technical Program Manager preparing a weekly executive status report.

Below is raw program data from multiple workstreams:

{data}

Generate a structured weekly program status report with the following sections:

1. EXECUTIVE SUMMARY (3 sentences max — overall program health, top win, top risk)
2. STATUS BY WORKSTREAM (for each project: one-line status, RAG rating — Red/Amber/Green)
3. CRITICAL BLOCKERS & RECOMMENDED ACTIONS (only blockers that need escalation)
4. UPCOMING MILESTONES THIS WEEK
5. DECISIONS NEEDED FROM LEADERSHIP

Format it cleanly. Be direct. Use the tone of a TPM reporting to a VP.
"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

def save_report(report: str, output_file: str = "status_report.md"):
    """Save the generated report to a markdown file."""
    today = date.today().strftime("%Y-%m-%d")
    with open(output_file, "w") as f:
        f.write(f"# Weekly Program Status Report\n")
        f.write(f"**Generated:** {today}\n\n")
        f.write(report)
    print(f"\n✅ Report saved to {output_file}")

def main():
    print("🚀 AI Program Status Summarizer")
    print("=" * 40)

    # Load data
    print("\n📊 Loading program data...")
    data = load_program_data("sample_data.csv")
    print("Data loaded successfully.")

    # Generate report
    print("\n🤖 Generating status report with Claude...")
    report = generate_status_report(data)

    # Display report
    print("\n" + "=" * 40)
    print("WEEKLY STATUS REPORT")
    print("=" * 40)
    print(report)

    # Save report
    save_report(report)

if __name__ == "__main__":
    main()
