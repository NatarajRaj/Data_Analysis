import argparse
import os
import smtplib
import sys
from email.message import EmailMessage


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Send backup status emails.")
    parser.add_argument("--to", required=True, dest="recipient")
    parser.add_argument("--subject", required=True)
    args = parser.parse_args()

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user or args.recipient)
    smtp_use_tls = parse_bool(os.getenv("SMTP_USE_TLS", "true"))

    missing = [
        name
        for name, value in {
            "SMTP_HOST": smtp_host,
            "SMTP_USER": smtp_user,
            "SMTP_PASSWORD": smtp_password,
        }.items()
        if not value
    ]

    if missing:
        print(
            f"Skipping email because required SMTP settings are missing: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    body = sys.stdin.read().strip()
    if not body:
        body = "Backup job completed. Check the backup log for details."

    message = EmailMessage()
    message["Subject"] = args.subject
    message["From"] = smtp_from
    message["To"] = args.recipient
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.ehlo()
        if smtp_use_tls:
            server.starttls()
            server.ehlo()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    print(f"Email sent to {args.recipient}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
