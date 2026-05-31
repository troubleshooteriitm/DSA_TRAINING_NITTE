"""
Automated IT Ticket Routing & Priority Assignment System
=========================================================

Business Use Case:
    In large organizations, the IT help desk receives hundreds of support
    tickets daily. Manually reading each ticket, classifying it, assigning
    a priority, and routing it to the correct team is slow, inconsistent,
    and error-prone.

    This system automates the entire triage pipeline:
        1. **Classification** -- Analyzes the ticket description using keyword
           matching to determine the category (Hardware, Software, Network,
           or Security).
        2. **Priority Assignment** -- Assigns a priority level (Critical, High,
           Medium, Low) based on the severity keywords found in the
           description and the category.
        3. **Team Routing** -- Routes the ticket to the appropriate support
           team based on category and priority.
        4. **Processing** -- Produces a complete routing decision with all
           metadata for the ticket.

    This demonstrates heavy use of:
        - Loops (for iterating over keywords, tickets, rules)
        - Conditionals (if-elif-else chains, nested conditions)
        - Dictionaries and lists for configuration-driven logic
        - Classes and methods for encapsulation

Author: DSA Training -- Day 3 (Control Flow: Loops & Conditionals)
"""

from datetime import datetime


# =============================================================================
# Constants & Configuration
# =============================================================================

# Ticket categories
CATEGORIES = {
    "Hardware":  "Issues with physical devices, peripherals, or equipment",
    "Software":  "Application errors, crashes, installations, or updates",
    "Network":   "Connectivity, VPN, Wi-Fi, DNS, or bandwidth issues",
    "Security":  "Security incidents, breaches, access control, malware",
}

# Priority levels (ordered by severity)
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

# Team assignments per category
TEAM_ASSIGNMENTS = {
    "Hardware":  "Desktop Support",
    "Software":  "Application Support",
    "Network":   "Network Operations",
    "Security":  "Security Operations",
}

# Keywords mapped to categories (checked in order; first match wins)
CATEGORY_KEYWORDS = {
    "Security": [
        "breach", "hack", "malware", "virus", "phishing", "unauthorized",
        "ransomware", "suspicious", "intrusion", "vulnerability", "firewall",
        "threat", "compromised", "spyware", "exploit",
    ],
    "Network": [
        "network", "internet", "wifi", "wi-fi", "vpn", "dns", "connectivity",
        "slow network", "bandwidth", "latency", "packet loss", "router",
        "switch", "ping", "timeout", "disconnected",
    ],
    "Hardware": [
        "monitor", "keyboard", "mouse", "printer", "laptop", "desktop",
        "hardware", "screen", "battery", "charger", "docking station",
        "headset", "usb", "disk", "hard drive", "overheating", "broken",
    ],
    "Software": [
        "crash", "error", "bug", "install", "update", "software", "app",
        "application", "freeze", "not responding", "license", "login",
        "password", "reset", "slow", "performance", "loading", "blue screen",
    ],
}

# Severity keywords that influence priority
SEVERITY_KEYWORDS = {
    "Critical": [
        "breach", "ransomware", "compromised", "data loss", "system down",
        "all users affected", "production down", "outage", "critical",
        "emergency", "exploit",
    ],
    "High": [
        "crash", "not working", "cannot access", "urgent", "hack",
        "malware", "virus", "broken", "multiple users", "deadline",
        "blue screen", "overheating",
    ],
    "Medium": [
        "slow", "intermittent", "sometimes", "error", "glitch",
        "performance", "delayed", "lag", "timeout", "latency",
    ],
    "Low": [
        "install", "request", "setup", "new", "how to", "question",
        "info", "cosmetic", "minor", "enhancement", "nice to have",
    ],
}


# =============================================================================
# TicketRouter Class
# =============================================================================

class TicketRouter:
    """
    Automated ticket routing engine that classifies, prioritizes, and
    routes IT support tickets based on keyword analysis.
    """

    def __init__(self):
        self.processed_tickets = []
        self.category_counts = {cat: 0 for cat in CATEGORIES}
        self.priority_counts = {pri: 0 for pri in PRIORITY_LEVELS}

    # -----------------------------------------------------------------
    # classify_ticket: Determine the ticket category
    # -----------------------------------------------------------------
    def classify_ticket(self, description: str) -> str:
        """
        Analyze the ticket description and return the most appropriate
        category by matching keywords.

        Priority order: Security > Network > Hardware > Software
        Default: Software (most common catch-all)
        """
        description_lower = description.lower()

        # Check each category's keywords
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category

        # Default fallback
        return "Software"

    # -----------------------------------------------------------------
    # assign_priority: Determine the priority level
    # -----------------------------------------------------------------
    def assign_priority(self, description: str, category: str) -> str:
        """
        Assign priority based on severity keywords found in the
        description. Security tickets get an automatic priority boost.

        Returns one of: Critical, High, Medium, Low
        """
        description_lower = description.lower()

        # Check severity keywords from most severe to least
        for priority in PRIORITY_LEVELS:
            keywords = SEVERITY_KEYWORDS[priority]
            for keyword in keywords:
                if keyword in description_lower:
                    # Security tickets: boost Medium -> High, Low -> Medium
                    if category == "Security":
                        if priority == "Medium":
                            return "High"
                        elif priority == "Low":
                            return "Medium"
                    return priority

        # Default priority based on category
        default_priorities = {
            "Security": "High",
            "Network":  "Medium",
            "Hardware":  "Medium",
            "Software":  "Low",
        }
        return default_priorities.get(category, "Low")

    # -----------------------------------------------------------------
    # route_ticket: Determine the assigned team
    # -----------------------------------------------------------------
    def route_ticket(self, category: str, priority: str) -> str:
        """
        Route the ticket to the appropriate team based on category.
        Critical tickets get escalated with a special note.
        """
        base_team = TEAM_ASSIGNMENTS.get(category, "General Support")

        if priority == "Critical":
            return f"{base_team} (ESCALATED -- Manager notified)"
        return base_team

    # -----------------------------------------------------------------
    # process_ticket: Full routing pipeline
    # -----------------------------------------------------------------
    def process_ticket(
        self, ticket_id: str, description: str, reporter: str
    ) -> dict:
        """
        Run a ticket through the complete routing pipeline:
            1. Classify -> category
            2. Assign priority
            3. Route to team
            4. Package the routing decision

        Returns a dictionary with all routing metadata.
        """
        # Step 1: Classify
        category = self.classify_ticket(description)

        # Step 2: Assign priority
        priority = self.assign_priority(description, category)

        # Step 3: Route
        assigned_team = self.route_ticket(category, priority)

        # Step 4: Build routing decision
        routing_decision = {
            "ticket_id":     ticket_id,
            "reporter":      reporter,
            "description":   description,
            "category":      category,
            "priority":      priority,
            "assigned_team": assigned_team,
            "timestamp":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Update internal counters
        self.processed_tickets.append(routing_decision)
        self.category_counts[category] += 1
        self.priority_counts[priority] += 1

        return routing_decision

    # -----------------------------------------------------------------
    # print_summary: Display processing statistics
    # -----------------------------------------------------------------
    def print_summary(self):
        """Print a summary of all processed tickets."""
        total = len(self.processed_tickets)
        print("\n" + "=" * 70)
        print(f"  ROUTING SUMMARY -- {total} tickets processed")
        print("=" * 70)

        print("\n  Category Breakdown:")
        for category, count in self.category_counts.items():
            bar = "" * count + "" * (total - count)
            print(f"    {category:<12} {bar}  {count}/{total}")

        print("\n  Priority Breakdown:")
        for priority, count in self.priority_counts.items():
            bar = "" * count + "" * (total - count)
            print(f"    {priority:<12} {bar}  {count}/{total}")

        print("=" * 70)


# =============================================================================
# Helper: Pretty-print a routing decision
# =============================================================================

def print_routing_decision(decision: dict):
    """Display a single routing decision in a formatted layout."""
    print("-" * 60)
    print(f"  Ticket ID    : {decision['ticket_id']}")
    print(f"  Reporter     : {decision['reporter']}")
    print(f"  Description  : {decision['description']}")
    print(f"  Category     : {decision['category']}")
    print(f"  Priority     : {decision['priority']}")
    print(f"  Assigned Team: {decision['assigned_team']}")
    print(f"  Timestamp    : {decision['timestamp']}")
    print("-" * 60)


# =============================================================================
# Main -- Process Sample Tickets
# =============================================================================

if __name__ == "__main__":

    # Instantiate the router
    router = TicketRouter()

    # Define sample tickets: (ticket_id, description, reporter)
    sample_tickets = [
        (
            "TKT-001",
            "My laptop screen is broken and I can't work",
            "Rahul Sharma"
        ),
        (
            "TKT-002",
            "Received a phishing email with suspicious attachment -- possible breach",
            "Priya Nair"
        ),
        (
            "TKT-003",
            "Application crashes every time I open the reports module",
            "Amit Verma"
        ),
        (
            "TKT-004",
            "VPN disconnected and I cannot access the internal network",
            "Sneha Patel"
        ),
        (
            "TKT-005",
            "Need to install Python 3.12 on my desktop for the new project",
            "Deepak Kumar"
        ),
        (
            "TKT-006",
            "Ransomware alert -- multiple files encrypted, system compromised",
            "Anita Rao"
        ),
        (
            "TKT-007",
            "Slow network speed during video conferencing -- lag and packet loss",
            "Karthik Iyer"
        ),
        (
            "TKT-008",
            "Blue screen error on laptop after the latest Windows update",
            "Meena Joshi"
        ),
        (
            "TKT-009",
            "Printer on 3rd floor not responding to print requests",
            "Vikram Singh"
        ),
        (
            "TKT-010",
            "Unauthorized login attempt detected on admin account -- urgent",
            "Security Team"
        ),
    ]

    # Process each ticket through the routing pipeline
    print("=" * 60)
    print("  IT TICKET ROUTING SYSTEM -- Processing Tickets")
    print("=" * 60)

    all_decisions = []
    for ticket_id, description, reporter in sample_tickets:
        decision = router.process_ticket(ticket_id, description, reporter)
        all_decisions.append(decision)
        print_routing_decision(decision)

    # Print the summary
    router.print_summary()

    # =====================================================================
    # Verification -- Assert expected routing for key tickets
    # =====================================================================
    # TKT-001: broken laptop screen -> Hardware
    assert all_decisions[0]["category"] == "Hardware"

    # TKT-002: phishing/breach -> Security, should be Critical or High
    assert all_decisions[1]["category"] == "Security"
    assert all_decisions[1]["priority"] in ["Critical", "High"]

    # TKT-003: application crash -> Software, High
    assert all_decisions[2]["category"] == "Software"
    assert all_decisions[2]["priority"] == "High"

    # TKT-004: VPN/network -> Network
    assert all_decisions[3]["category"] == "Network"

    # TKT-005: install software -> Software, Low
    assert all_decisions[4]["category"] == "Software"
    assert all_decisions[4]["priority"] == "Low"

    # TKT-006: ransomware/compromised -> Security, Critical
    assert all_decisions[5]["category"] == "Security"
    assert all_decisions[5]["priority"] == "Critical"

    # TKT-007: slow network/packet loss -> Network, Medium
    assert all_decisions[6]["category"] == "Network"

    # TKT-008: blue screen -> Software, High
    assert all_decisions[7]["category"] == "Software"
    assert all_decisions[7]["priority"] == "High"

    # TKT-009: printer not responding -> Hardware
    assert all_decisions[8]["category"] == "Hardware"

    # TKT-010: unauthorized/security -> Security
    assert all_decisions[9]["category"] == "Security"

    print("\nAll test cases passed!")
