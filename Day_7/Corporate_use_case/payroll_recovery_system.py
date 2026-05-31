"""
Payroll Failure Recovery & Secure Transaction Validation System

This module implements a complete payroll processing system with:
- PayrollTransaction data class for transaction records
- Custom exception hierarchy for payroll-specific errors
- PayrollProcessor class with batch processing capabilities
- Retry logic with exponential backoff (simulated)
- Transaction validation (amount, employee, duplicates)
- Comprehensive logging of all operations
- Recovery mechanism for failed transactions

Usage:
    Run this file directly to see the system process a batch of
    sample transactions, demonstrating both success and failure scenarios.
"""

import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# ============================================================
# Logging Configuration
# ============================================================

# Create a dedicated logger for the payroll system
logger = logging.getLogger("payroll_system")
logger.setLevel(logging.DEBUG)

# Console handler -- show INFO and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Note: In production, you would also add a FileHandler or
# RotatingFileHandler here to persist logs to disk.


# ============================================================
# Enums
# ============================================================

class TransactionType(Enum):
    """Types of payroll transactions."""
    SALARY = "salary"
    BONUS = "bonus"
    DEDUCTION = "deduction"


class TransactionStatus(Enum):
    """Status of a payroll transaction."""
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
    RETRYING = "retrying"


# ============================================================
# Custom Exceptions
# ============================================================

class PayrollError(Exception):
    """Base exception for all payroll-related errors."""
    pass


class InsufficientFundsError(PayrollError):
    """Raised when the payroll fund balance is too low for a transaction."""

    def __init__(self, available: float, required: float):
        self.available = available
        self.required = required
        self.deficit = required - available
        super().__init__(
            f"Insufficient funds: available=₹{available:,.2f}, "
            f"required=₹{required:,.2f}, deficit=₹{self.deficit:,.2f}"
        )


class InvalidTransactionError(PayrollError):
    """Raised when a transaction fails validation checks."""

    def __init__(self, transaction_id: str, reason: str):
        self.transaction_id = transaction_id
        self.reason = reason
        super().__init__(
            f"Invalid transaction [{transaction_id}]: {reason}"
        )


class PayrollProcessingError(PayrollError):
    """Raised when a transaction fails during processing."""

    def __init__(self, transaction_id: str, reason: str,
                 retryable: bool = True):
        self.transaction_id = transaction_id
        self.reason = reason
        self.retryable = retryable
        super().__init__(
            f"Processing error [{transaction_id}]: {reason} "
            f"(retryable={retryable})"
        )


# ============================================================
# Data Classes
# ============================================================

@dataclass
class PayrollTransaction:
    """
    Represents a single payroll transaction.

    Attributes:
        employee_id: Unique identifier for the employee.
        amount: Transaction amount in currency units.
        date: Date of the transaction.
        transaction_type: Type of transaction (salary, bonus, deduction).
        transaction_id: Unique ID auto-generated for each transaction.
        status: Current processing status.
        retry_count: Number of times processing has been retried.
        error_message: Description of the last error, if any.
    """
    employee_id: str
    amount: float
    date: datetime
    transaction_type: TransactionType
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: TransactionStatus = TransactionStatus.PENDING
    retry_count: int = 0
    error_message: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"Txn[{self.transaction_id}] "
            f"Emp={self.employee_id} "
            f"Type={self.transaction_type.value} "
            f"Amount=₹{self.amount:,.2f} "
            f"Status={self.status.value}"
        )


# ============================================================
# Payroll Processor
# ============================================================

class PayrollProcessor:
    """
    Processes payroll transactions with validation, error handling,
    retry logic, and recovery mechanisms.

    Attributes:
        fund_balance: Total available funds for payroll disbursement.
        valid_employees: Set of valid employee IDs in the system.
        max_retries: Maximum number of retry attempts for failed transactions.
        processed_transactions: List of successfully processed transactions.
        failed_transactions: List of transactions that failed permanently.
        recovery_queue: List of transactions awaiting retry.
    """

    def __init__(
        self,
        fund_balance: float,
        valid_employees: set[str],
        max_retries: int = 3,
    ):
        self.fund_balance = fund_balance
        self.valid_employees = valid_employees
        self.max_retries = max_retries

        # Transaction tracking
        self.processed_transactions: list[PayrollTransaction] = []
        self.failed_transactions: list[PayrollTransaction] = []
        self.recovery_queue: list[PayrollTransaction] = []

        # Track processed transaction IDs to detect duplicates
        self._processed_ids: set[str] = set()

        logger.info(
            "PayrollProcessor initialized | Fund balance: ₹%s | "
            "Valid employees: %d | Max retries: %d",
            f"{fund_balance:,.2f}",
            len(valid_employees),
            max_retries,
        )

    def validate_transaction(self, txn: PayrollTransaction) -> None:
        """
        Validates a transaction before processing.

        Checks:
            1. Amount must be positive.
            2. Employee ID must exist in the valid employees set.
            3. Transaction must not be a duplicate.

        Raises:
            InvalidTransactionError: If any validation check fails.
        """
        # Check 1: Amount must be positive
        if txn.amount <= 0:
            raise InvalidTransactionError(
                txn.transaction_id,
                f"Amount must be positive, got ₹{txn.amount:,.2f}",
            )

        # Check 2: Employee must exist
        if txn.employee_id not in self.valid_employees:
            raise InvalidTransactionError(
                txn.transaction_id,
                f"Unknown employee ID: {txn.employee_id}",
            )

        # Check 3: No duplicate transactions
        if txn.transaction_id in self._processed_ids:
            raise InvalidTransactionError(
                txn.transaction_id,
                "Duplicate transaction detected",
            )

        logger.debug("Validation passed for %s", txn)

    def _process_single(self, txn: PayrollTransaction) -> bool:
        """
        Process a single transaction.

        Returns True on success, False on failure.
        """
        try:
            # Step 1: Validate
            self.validate_transaction(txn)

            # Step 2: Check funds (only for salary and bonus disbursements)
            if txn.transaction_type in (
                TransactionType.SALARY, TransactionType.BONUS
            ):
                if txn.amount > self.fund_balance:
                    raise InsufficientFundsError(
                        self.fund_balance, txn.amount
                    )

            # Step 3: Simulate processing (in real system, this would
            # interact with a payment gateway or banking API)
            self._execute_transaction(txn)

            # Step 4: Update fund balance
            if txn.transaction_type in (
                TransactionType.SALARY, TransactionType.BONUS
            ):
                self.fund_balance -= txn.amount
            elif txn.transaction_type == TransactionType.DEDUCTION:
                self.fund_balance += txn.amount

            # Step 5: Mark as processed
            txn.status = TransactionStatus.PROCESSED
            self._processed_ids.add(txn.transaction_id)
            self.processed_transactions.append(txn)

            logger.info(
                " PROCESSED: %s | Remaining balance: ₹%s",
                txn, f"{self.fund_balance:,.2f}",
            )
            return True

        except InvalidTransactionError as e:
            # Validation failures are NOT retryable
            txn.status = TransactionStatus.FAILED
            txn.error_message = str(e)
            self.failed_transactions.append(txn)
            logger.error(" VALIDATION FAILED: %s", e)
            return False

        except InsufficientFundsError as e:
            # Insufficient funds -- may be retryable if more funds arrive
            txn.status = TransactionStatus.FAILED
            txn.error_message = str(e)
            self.recovery_queue.append(txn)
            logger.warning(" INSUFFICIENT FUNDS: %s -- queued for recovery", e)
            return False

        except PayrollProcessingError as e:
            # Processing errors -- retry if retryable
            txn.error_message = str(e)
            if e.retryable:
                self.recovery_queue.append(txn)
                logger.warning(
                    " PROCESSING ERROR (retryable): %s -- queued for retry", e
                )
            else:
                txn.status = TransactionStatus.FAILED
                self.failed_transactions.append(txn)
                logger.error(
                    " PROCESSING ERROR (non-retryable): %s", e
                )
            return False

    def _execute_transaction(self, txn: PayrollTransaction) -> None:
        """
        Simulates executing a transaction.

        In a real system, this would call a payment gateway API.
        Here we simulate occasional failures for demonstration.

        Raises:
            PayrollProcessingError: If the simulated processing fails.
        """
        # Simulate: transactions for employee 'EMP005' always fail
        # (simulating a gateway error for demo purposes)
        if txn.employee_id == "EMP005" and txn.retry_count < 2:
            raise PayrollProcessingError(
                txn.transaction_id,
                "Payment gateway timeout (simulated)",
                retryable=True,
            )

        logger.debug("Transaction %s executed successfully", txn.transaction_id)

    def process_batch(
        self, transactions: list[PayrollTransaction]
    ) -> dict[str, int]:
        """
        Process a batch of payroll transactions.

        Args:
            transactions: List of PayrollTransaction objects to process.

        Returns:
            Dictionary with counts of processed, failed, and queued
            transactions.
        """
        logger.info(
            "=" * 60 + "\n"
            "  BATCH PROCESSING STARTED -- %d transactions\n" + "=" * 60,
            len(transactions),
        )

        results = {"processed": 0, "failed": 0, "queued_for_retry": 0}

        for txn in transactions:
            logger.info("-" * 40)
            logger.info("Processing: %s", txn)

            success = self._process_single(txn)
            if success:
                results["processed"] += 1
            elif txn.status == TransactionStatus.FAILED:
                results["failed"] += 1
            else:
                results["queued_for_retry"] += 1

        logger.info(
            "=" * 60 + "\n"
            "  BATCH COMPLETE -- Processed: %d | Failed: %d | "
            "Queued: %d\n" + "=" * 60,
            results["processed"],
            results["failed"],
            results["queued_for_retry"],
        )

        return results

    def retry_failed_transactions(self) -> dict[str, int]:
        """
        Retry transactions in the recovery queue with exponential backoff.

        Each transaction is retried up to max_retries times. The backoff
        delay doubles with each attempt (simulated with log messages
        rather than actual sleep to keep the demo fast).

        Returns:
            Dictionary with counts of recovered and permanently failed
            transactions.
        """
        if not self.recovery_queue:
            logger.info("No transactions in recovery queue.")
            return {"recovered": 0, "permanently_failed": 0}

        logger.info(
            "=" * 60 + "\n"
            "  RETRY PHASE -- %d transactions to retry\n" + "=" * 60,
            len(self.recovery_queue),
        )

        results = {"recovered": 0, "permanently_failed": 0}

        # Copy the queue and clear it (retries may re-add items)
        retry_list = list(self.recovery_queue)
        self.recovery_queue.clear()

        for txn in retry_list:
            txn.retry_count += 1
            txn.status = TransactionStatus.RETRYING

            # Calculate backoff delay (simulated)
            backoff_seconds = 2 ** txn.retry_count
            logger.info(
                " RETRY #%d for %s (backoff: %ds simulated)",
                txn.retry_count, txn, backoff_seconds,
            )

            if txn.retry_count > self.max_retries:
                # Exceeded max retries -- permanent failure
                txn.status = TransactionStatus.FAILED
                self.failed_transactions.append(txn)
                results["permanently_failed"] += 1
                logger.error(
                    " PERMANENTLY FAILED after %d retries: %s",
                    self.max_retries, txn,
                )
                continue

            # Attempt to process again
            success = self._process_single(txn)
            if success:
                results["recovered"] += 1

        logger.info(
            "=" * 60 + "\n"
            "  RETRY COMPLETE -- Recovered: %d | Permanently Failed: %d\n"
            + "=" * 60,
            results["recovered"],
            results["permanently_failed"],
        )

        return results

    def generate_report(self) -> str:
        """
        Generate a summary report of all processed and failed transactions.

        Returns:
            A formatted string report.
        """
        lines = [
            "",
            "=" * 60,
            "  PAYROLL PROCESSING REPORT",
            "=" * 60,
            f"  Fund Balance Remaining : ₹{self.fund_balance:,.2f}",
            f"  Total Processed        : {len(self.processed_transactions)}",
            f"  Total Failed           : {len(self.failed_transactions)}",
            f"  Pending in Recovery    : {len(self.recovery_queue)}",
            "",
            "--- Processed Transactions ---",
        ]

        for txn in self.processed_transactions:
            lines.append(f"   {txn}")

        lines.append("")
        lines.append("--- Failed Transactions ---")

        for txn in self.failed_transactions:
            lines.append(f"   {txn}")
            lines.append(f"     Reason: {txn.error_message}")

        if self.recovery_queue:
            lines.append("")
            lines.append("--- Pending Recovery ---")
            for txn in self.recovery_queue:
                lines.append(f"   {txn}")

        lines.append("=" * 60)

        report = "\n".join(lines)
        return report


# ============================================================
# Main -- Run with Sample Data
# ============================================================

def main():
    """
    Demonstrate the payroll system with sample data showing both
    success and failure scenarios.
    """
    # Define valid employees
    valid_employees = {"EMP001", "EMP002", "EMP003", "EMP004", "EMP005"}

    # Initialize processor with ₹500,000 fund balance
    processor = PayrollProcessor(
        fund_balance=500_000.00,
        valid_employees=valid_employees,
        max_retries=3,
    )

    # Create sample transactions -- mix of valid and invalid
    today = datetime.now()
    transactions = [
        #  Valid salary transactions
        PayrollTransaction(
            employee_id="EMP001",
            amount=75_000.00,
            date=today,
            transaction_type=TransactionType.SALARY,
        ),
        PayrollTransaction(
            employee_id="EMP002",
            amount=82_000.00,
            date=today,
            transaction_type=TransactionType.SALARY,
        ),
        #  Valid bonus
        PayrollTransaction(
            employee_id="EMP003",
            amount=15_000.00,
            date=today,
            transaction_type=TransactionType.BONUS,
        ),
        #  Valid deduction
        PayrollTransaction(
            employee_id="EMP004",
            amount=5_000.00,
            date=today,
            transaction_type=TransactionType.DEDUCTION,
        ),
        #  Invalid: negative amount
        PayrollTransaction(
            employee_id="EMP001",
            amount=-10_000.00,
            date=today,
            transaction_type=TransactionType.SALARY,
        ),
        #  Invalid: unknown employee
        PayrollTransaction(
            employee_id="EMP999",
            amount=50_000.00,
            date=today,
            transaction_type=TransactionType.SALARY,
        ),
        #  Will fail initially (simulated gateway timeout for EMP005)
        PayrollTransaction(
            employee_id="EMP005",
            amount=60_000.00,
            date=today,
            transaction_type=TransactionType.SALARY,
        ),
        #  Insufficient funds (will exceed remaining balance)
        PayrollTransaction(
            employee_id="EMP003",
            amount=400_000.00,
            date=today,
            transaction_type=TransactionType.SALARY,
        ),
    ]

    # Phase 1: Process the batch
    print("\n" + "" * 30)
    print("  PHASE 1: INITIAL BATCH PROCESSING")
    print("" * 30)
    batch_results = processor.process_batch(transactions)

    # Phase 2: Retry failed transactions
    print("\n" + "" * 30)
    print("  PHASE 2: RETRY FAILED TRANSACTIONS")
    print("" * 30)
    retry_results = processor.retry_failed_transactions()

    # If there are still items in recovery, retry once more
    if processor.recovery_queue:
        print("\n" + "" * 30)
        print("  PHASE 2b: SECOND RETRY ATTEMPT")
        print("" * 30)
        retry_results_2 = processor.retry_failed_transactions()

    # Phase 3: Generate final report
    print("\n" + "" * 30)
    print("  PHASE 3: FINAL REPORT")
    print("" * 30)
    report = processor.generate_report()
    print(report)


if __name__ == "__main__":
    main()
