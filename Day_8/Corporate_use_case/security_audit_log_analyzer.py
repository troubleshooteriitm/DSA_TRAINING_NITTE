"""
Security Audit Log Analysis & Monitoring Tool
==============================================
Corporate Use Case -- Day 8: File Handling & Data Processing

This tool demonstrates a real-world security audit log analyzer that:
1. Generates/parses security log entries
2. Detects suspicious patterns (brute force, after-hours access, etc.)
3. Classifies threats by severity level
4. Produces CSV and JSON reports

Modules used: csv, json, datetime, collections, os, pathlib
"""

import csv
import json
import os
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# ============================================================
# 1. SAMPLE SECURITY LOG DATA
# ============================================================

# Embedded sample security log entries simulating a corporate environment
SECURITY_LOGS = [
    # Normal business hours activity
    {"timestamp": "2025-05-15 08:30:15", "user": "alice.johnson", "action": "LOGIN",
     "ip": "192.168.1.101", "status": "SUCCESS", "details": "Standard login"},
    {"timestamp": "2025-05-15 08:45:22", "user": "bob.smith", "action": "LOGIN",
     "ip": "192.168.1.102", "status": "SUCCESS", "details": "Standard login"},
    {"timestamp": "2025-05-15 09:00:10", "user": "alice.johnson", "action": "FILE_ACCESS",
     "ip": "192.168.1.101", "status": "SUCCESS", "details": "Accessed /reports/Q1_2025.pdf"},
    {"timestamp": "2025-05-15 09:15:33", "user": "charlie.davis", "action": "LOGIN",
     "ip": "192.168.1.103", "status": "SUCCESS", "details": "Standard login"},
    {"timestamp": "2025-05-15 09:30:45", "user": "bob.smith", "action": "FILE_ACCESS",
     "ip": "192.168.1.102", "status": "SUCCESS", "details": "Accessed /shared/budget.xlsx"},

    # Suspicious failed login attempts (potential brute force)
    {"timestamp": "2025-05-15 10:00:01", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.55", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 10:00:05", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.55", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 10:00:09", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.55", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 10:00:14", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.55", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 10:00:18", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.55", "status": "FAILURE", "details": "Invalid password"},

    # Permission changes (sensitive operation)
    {"timestamp": "2025-05-15 11:00:00", "user": "charlie.davis", "action": "PERMISSION_CHANGE",
     "ip": "192.168.1.103", "status": "SUCCESS",
     "details": "Changed permissions on /etc/config to 777"},
    {"timestamp": "2025-05-15 11:30:00", "user": "alice.johnson", "action": "PERMISSION_CHANGE",
     "ip": "192.168.1.101", "status": "SUCCESS",
     "details": "Added bob.smith to admin group"},

    # Normal activity continues
    {"timestamp": "2025-05-15 12:00:00", "user": "alice.johnson", "action": "LOGOUT",
     "ip": "192.168.1.101", "status": "SUCCESS", "details": "Standard logout"},
    {"timestamp": "2025-05-15 13:00:00", "user": "alice.johnson", "action": "LOGIN",
     "ip": "192.168.1.101", "status": "SUCCESS", "details": "Standard login"},
    {"timestamp": "2025-05-15 14:00:00", "user": "diana.lee", "action": "LOGIN",
     "ip": "192.168.1.104", "status": "SUCCESS", "details": "Standard login"},
    {"timestamp": "2025-05-15 14:15:00", "user": "diana.lee", "action": "FILE_ACCESS",
     "ip": "192.168.1.104", "status": "SUCCESS", "details": "Accessed /hr/payroll.csv"},

    # More failed logins from different IP (distributed attack)
    {"timestamp": "2025-05-15 15:00:00", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.77", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 15:00:05", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "10.0.0.78", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 15:00:10", "user": "root", "action": "FAILED_LOGIN",
     "ip": "10.0.0.77", "status": "FAILURE", "details": "Invalid password"},

    # After-hours activity (suspicious)
    {"timestamp": "2025-05-15 22:30:00", "user": "bob.smith", "action": "LOGIN",
     "ip": "10.0.0.99", "status": "SUCCESS", "details": "VPN login"},
    {"timestamp": "2025-05-15 22:35:00", "user": "bob.smith", "action": "FILE_ACCESS",
     "ip": "10.0.0.99", "status": "SUCCESS",
     "details": "Accessed /confidential/merger_plans.docx"},
    {"timestamp": "2025-05-15 22:40:00", "user": "bob.smith", "action": "FILE_ACCESS",
     "ip": "10.0.0.99", "status": "SUCCESS",
     "details": "Accessed /confidential/financial_projections.xlsx"},
    {"timestamp": "2025-05-15 23:00:00", "user": "bob.smith", "action": "LOGOUT",
     "ip": "10.0.0.99", "status": "SUCCESS", "details": "Standard logout"},

    # Late night failed attempt
    {"timestamp": "2025-05-15 03:15:00", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "203.0.113.42", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 03:15:05", "user": "admin", "action": "FAILED_LOGIN",
     "ip": "203.0.113.42", "status": "FAILURE", "details": "Invalid password"},
    {"timestamp": "2025-05-15 03:15:10", "user": "root", "action": "FAILED_LOGIN",
     "ip": "203.0.113.42", "status": "FAILURE", "details": "Invalid password"},

    # End of day activity
    {"timestamp": "2025-05-15 17:00:00", "user": "charlie.davis", "action": "LOGOUT",
     "ip": "192.168.1.103", "status": "SUCCESS", "details": "Standard logout"},
    {"timestamp": "2025-05-15 17:30:00", "user": "diana.lee", "action": "LOGOUT",
     "ip": "192.168.1.104", "status": "SUCCESS", "details": "Standard logout"},
    {"timestamp": "2025-05-15 18:00:00", "user": "bob.smith", "action": "LOGOUT",
     "ip": "192.168.1.102", "status": "SUCCESS", "details": "Standard logout"},
]

# Business hours definition (used for after-hours detection)
BUSINESS_HOURS_START = 7   # 7:00 AM
BUSINESS_HOURS_END = 19    # 7:00 PM


# ============================================================
# 2. LOG PARSER
# ============================================================

def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse a timestamp string into a datetime object.

    Args:
        timestamp_str: Timestamp in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        Parsed datetime object.
    """
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")


def is_after_hours(timestamp: datetime) -> bool:
    """
    Check if a timestamp falls outside business hours.

    Args:
        timestamp: The datetime to check.

    Returns:
        True if the activity is after hours (before 7 AM or after 7 PM).
    """
    hour = timestamp.hour
    return hour < BUSINESS_HOURS_START or hour >= BUSINESS_HOURS_END


# ============================================================
# 3. ANALYSIS FUNCTIONS
# ============================================================

def analyze_failed_logins(logs: list) -> dict:
    """
    Analyze failed login attempts per user.

    Returns:
        Dictionary with user -> count of failed logins.
    """
    failed_logins = Counter()
    for log in logs:
        if log["action"] == "FAILED_LOGIN":
            failed_logins[log["user"]] += 1
    return dict(failed_logins.most_common())


def detect_suspicious_ips(logs: list, threshold: int = 3) -> list:
    """
    Detect IPs with multiple failed login attempts (potential brute force).

    Args:
        logs: List of log entry dictionaries.
        threshold: Minimum failed attempts to flag as suspicious.

    Returns:
        List of dictionaries with suspicious IP details.
    """
    ip_failures = Counter()
    ip_users_targeted = defaultdict(set)

    for log in logs:
        if log["action"] == "FAILED_LOGIN":
            ip_failures[log["ip"]] += 1
            ip_users_targeted[log["ip"]].add(log["user"])

    suspicious = []
    for ip, count in ip_failures.most_common():
        if count >= threshold:
            suspicious.append({
                "ip": ip,
                "failed_attempts": count,
                "users_targeted": list(ip_users_targeted[ip]),
                "threat_level": "CRITICAL" if count >= 5 else "HIGH",
            })

    return suspicious


def analyze_file_access_patterns(logs: list) -> dict:
    """
    Analyze file access patterns by user.

    Returns:
        Dictionary with user -> list of accessed files and timestamps.
    """
    access_patterns = defaultdict(list)

    for log in logs:
        if log["action"] == "FILE_ACCESS":
            timestamp = parse_timestamp(log["timestamp"])
            access_patterns[log["user"]].append({
                "file": log["details"].replace("Accessed ", ""),
                "timestamp": log["timestamp"],
                "ip": log["ip"],
                "after_hours": is_after_hours(timestamp),
            })

    return dict(access_patterns)


def detect_after_hours_activity(logs: list) -> list:
    """
    Detect all activity that occurs outside business hours.

    Returns:
        List of after-hours log entries with additional context.
    """
    after_hours = []

    for log in logs:
        timestamp = parse_timestamp(log["timestamp"])
        if is_after_hours(timestamp):
            entry = log.copy()
            entry["hour"] = timestamp.hour
            entry["is_weekend"] = timestamp.weekday() >= 5
            after_hours.append(entry)

    return after_hours


def analyze_permission_changes(logs: list) -> list:
    """
    Extract all permission change events for audit review.

    Returns:
        List of permission change entries.
    """
    return [log for log in logs if log["action"] == "PERMISSION_CHANGE"]


# ============================================================
# 4. THREAT CLASSIFICATION
# ============================================================

def classify_threat_level(
    failed_logins: dict,
    suspicious_ips: list,
    after_hours: list,
    permission_changes: list,
) -> dict:
    """
    Generate an overall security threat assessment.

    Args:
        failed_logins: Failed login counts per user.
        suspicious_ips: List of suspicious IP entries.
        after_hours: List of after-hours activity entries.
        permission_changes: List of permission change entries.

    Returns:
        Dictionary containing threat summary and overall level.
    """
    threats = []

    # Check for brute force indicators
    for user, count in failed_logins.items():
        if count >= 5:
            threats.append({
                "type": "BRUTE_FORCE",
                "level": "CRITICAL",
                "description": f"User '{user}' has {count} failed login attempts",
            })
        elif count >= 3:
            threats.append({
                "type": "SUSPICIOUS_LOGIN",
                "level": "HIGH",
                "description": f"User '{user}' has {count} failed login attempts",
            })

    # Check suspicious IPs
    for ip_info in suspicious_ips:
        threats.append({
            "type": "SUSPICIOUS_IP",
            "level": ip_info["threat_level"],
            "description": (
                f"IP {ip_info['ip']} made {ip_info['failed_attempts']} "
                f"failed attempts targeting: {', '.join(ip_info['users_targeted'])}"
            ),
        })

    # Check after-hours confidential file access
    for entry in after_hours:
        if entry["action"] == "FILE_ACCESS" and "confidential" in entry.get("details", "").lower():
            threats.append({
                "type": "AFTER_HOURS_CONFIDENTIAL_ACCESS",
                "level": "HIGH",
                "description": (
                    f"User '{entry['user']}' accessed confidential files at "
                    f"{entry['timestamp']} from IP {entry['ip']}"
                ),
            })

    # Check permission changes
    for change in permission_changes:
        if "777" in change.get("details", "") or "admin" in change.get("details", "").lower():
            threats.append({
                "type": "RISKY_PERMISSION_CHANGE",
                "level": "MEDIUM",
                "description": f"User '{change['user']}': {change['details']}",
            })

    # Determine overall threat level
    levels = [t["level"] for t in threats]
    if "CRITICAL" in levels:
        overall = "CRITICAL"
    elif "HIGH" in levels:
        overall = "HIGH"
    elif "MEDIUM" in levels:
        overall = "MEDIUM"
    else:
        overall = "LOW"

    return {
        "overall_threat_level": overall,
        "total_threats": len(threats),
        "threats": threats,
        "summary": {
            "critical": levels.count("CRITICAL"),
            "high": levels.count("HIGH"),
            "medium": levels.count("MEDIUM"),
            "low": levels.count("LOW"),
        },
    }


# ============================================================
# 5. REPORT GENERATION
# ============================================================

def generate_console_report(
    failed_logins: dict,
    suspicious_ips: list,
    file_access: dict,
    after_hours: list,
    permission_changes: list,
    threat_assessment: dict,
) -> None:
    """Print a formatted security report to the console."""
    separator = "=" * 70

    print(f"\n{separator}")
    print("       SECURITY AUDIT LOG ANALYSIS REPORT")
    print(f"       Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(separator)

    # Overall threat level
    level = threat_assessment["overall_threat_level"]
    level_emoji = {
        "CRITICAL": "", "HIGH": "", "MEDIUM": "", "LOW": ""
    }
    print(f"\n  Overall Threat Level: {level_emoji.get(level, '')} {level}")
    print(f"  Total Threats Detected: {threat_assessment['total_threats']}")
    summary = threat_assessment["summary"]
    print(f"    Critical: {summary['critical']} | High: {summary['high']} "
          f"| Medium: {summary['medium']} | Low: {summary['low']}")

    # Failed login analysis
    print(f"\n{separator}")
    print("  [1] FAILED LOGIN ANALYSIS")
    print(separator)
    if failed_logins:
        for user, count in failed_logins.items():
            bar = "" * count
            flag = "   ALERT" if count >= 3 else ""
            print(f"    {user:<20} | {count:>3} attempts | {bar}{flag}")
    else:
        print("    No failed login attempts detected.")

    # Suspicious IPs
    print(f"\n{separator}")
    print("  [2] SUSPICIOUS IP ADDRESSES")
    print(separator)
    if suspicious_ips:
        for ip_info in suspicious_ips:
            print(f"    IP: {ip_info['ip']:<18} | "
                  f"Attempts: {ip_info['failed_attempts']} | "
                  f"Threat: {ip_info['threat_level']}")
            print(f"      Targeted users: {', '.join(ip_info['users_targeted'])}")
    else:
        print("    No suspicious IPs detected.")

    # File access patterns
    print(f"\n{separator}")
    print("  [3] FILE ACCESS PATTERNS")
    print(separator)
    for user, accesses in file_access.items():
        print(f"\n    User: {user}")
        for access in accesses:
            flag = " [AFTER HOURS]" if access["after_hours"] else ""
            print(f"      {access['timestamp']} | {access['file']}{flag}")

    # After-hours activity
    print(f"\n{separator}")
    print("  [4] AFTER-HOURS ACTIVITY")
    print(separator)
    if after_hours:
        for entry in after_hours:
            print(f"    {entry['timestamp']} | {entry['user']:<20} | "
                  f"{entry['action']:<18} | IP: {entry['ip']}")
    else:
        print("    No after-hours activity detected.")

    # Permission changes
    print(f"\n{separator}")
    print("  [5] PERMISSION CHANGES (Audit Trail)")
    print(separator)
    if permission_changes:
        for change in permission_changes:
            print(f"    {change['timestamp']} | {change['user']:<20} | "
                  f"{change['details']}")
    else:
        print("    No permission changes detected.")

    # Threat details
    print(f"\n{separator}")
    print("  [6] THREAT DETAILS")
    print(separator)
    for i, threat in enumerate(threat_assessment["threats"], 1):
        print(f"\n    Threat #{i}")
        print(f"      Type:  {threat['type']}")
        print(f"      Level: {level_emoji.get(threat['level'], '')} {threat['level']}")
        print(f"      Info:  {threat['description']}")

    print(f"\n{separator}")
    print("  END OF REPORT")
    print(f"{separator}\n")


def export_to_csv(threat_assessment: dict, output_path: str) -> None:
    """
    Export the threat assessment to a CSV report.

    Args:
        threat_assessment: Dictionary containing threat analysis results.
        output_path: File path for the CSV output.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    fieldnames = ["threat_number", "type", "level", "description"]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, threat in enumerate(threat_assessment["threats"], 1):
            writer.writerow({
                "threat_number": i,
                "type": threat["type"],
                "level": threat["level"],
                "description": threat["description"],
            })

    print(f"   CSV report exported to: {output_path}")


def export_to_json(
    threat_assessment: dict,
    after_hours: list,
    output_path: str,
) -> None:
    """
    Export the full security report to a JSON file.

    Args:
        threat_assessment: Dictionary containing threat analysis results.
        after_hours: List of after-hours activity entries.
        output_path: File path for the JSON output.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    report = {
        "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "overall_threat_level": threat_assessment["overall_threat_level"],
        "threat_summary": threat_assessment["summary"],
        "threats": threat_assessment["threats"],
        "after_hours_activity_count": len(after_hours),
        "after_hours_entries": after_hours,
    }

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(report, jsonfile, indent=4, default=str)

    print(f"   JSON report exported to: {output_path}")


# ============================================================
# 6. MAIN EXECUTION
# ============================================================

def main():
    """Run the complete security audit log analysis pipeline."""
    print("\n Security Audit Log Analyzer -- Starting Analysis...\n")
    print(f"   Analyzing {len(SECURITY_LOGS)} log entries...")

    # Step 1: Analyze failed logins
    failed_logins = analyze_failed_logins(SECURITY_LOGS)
    print(f"    Failed login analysis complete ({sum(failed_logins.values())} failures)")

    # Step 2: Detect suspicious IPs
    suspicious_ips = detect_suspicious_ips(SECURITY_LOGS, threshold=3)
    print(f"    Suspicious IP detection complete ({len(suspicious_ips)} flagged)")

    # Step 3: Analyze file access patterns
    file_access = analyze_file_access_patterns(SECURITY_LOGS)
    print(f"    File access analysis complete ({len(file_access)} users)")

    # Step 4: Detect after-hours activity
    after_hours = detect_after_hours_activity(SECURITY_LOGS)
    print(f"    After-hours detection complete ({len(after_hours)} entries)")

    # Step 5: Analyze permission changes
    permission_changes = analyze_permission_changes(SECURITY_LOGS)
    print(f"    Permission change audit complete ({len(permission_changes)} changes)")

    # Step 6: Classify overall threat level
    threat_assessment = classify_threat_level(
        failed_logins, suspicious_ips, after_hours, permission_changes
    )
    print(f"    Threat classification complete")

    # Step 7: Generate console report
    generate_console_report(
        failed_logins, suspicious_ips, file_access,
        after_hours, permission_changes, threat_assessment,
    )

    # Step 8: Export reports to CSV and JSON
    # Use the script's directory for output
    script_dir = Path(__file__).parent
    csv_path = script_dir / "security_report.csv"
    json_path = script_dir / "security_report.json"

    export_to_csv(threat_assessment, str(csv_path))
    export_to_json(threat_assessment, after_hours, str(json_path))

    print("\n Analysis complete. Review reports for action items.\n")


if __name__ == "__main__":
    main()
