#!/bin/bash

echo "Script started"

set -Eeuo pipefail

# PATHS
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# LOAD CONFIG
set -a
source "$SCRIPT_DIR/config.env"
set +a

# INIT
DATE_PATH=$(date +%Y/%m/%d)
TIMESTAMP=$(date +%H%M%S)
RUN_AT=$(date)
FILE_NAME="backup_${TIMESTAMP}.sql"
COMPRESSED_FILE="${FILE_NAME}.gz"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/backup.log"
PG_DUMP_PATH="/c/Program Files/PostgreSQL/18/bin/pg_dump.exe"
EMAIL_HELPER="$SCRIPT_DIR/send_email.py"
CURRENT_STEP="Initialization"

mkdir -p "$LOG_DIR"

export PGPASSWORD="$DB_PASSWORD"

log_message() {
    echo "$1" >> "$LOG_FILE"
}

send_status_email() {
    local status="$1"
    local subject="$2"

    if [[ -z "${EMAIL:-}" ]]; then
        log_message "[WARN] EMAIL is not configured. Skipping ${status,,} email alert."
        return 0
    fi

    if [[ ! -f "$EMAIL_HELPER" ]]; then
        log_message "[WARN] $EMAIL_HELPER is missing. Skipping ${status,,} email alert."
        return 0
    fi

    local recent_logs
    recent_logs=$(tail -n 20 "$LOG_FILE" 2>/dev/null || true)

    if ! cat <<EOF | py -3 "$EMAIL_HELPER" --to "$EMAIL" --subject "$subject" >> "$LOG_FILE" 2>&1
Backup Status: $status
Database: $DB_NAME
Host: $DB_HOST
S3 Bucket: $S3_BUCKET
Backup File: $COMPRESSED_FILE
Current Step: $CURRENT_STEP
Run Started: $RUN_AT
Log File: $LOG_FILE

Recent Log Entries:
$recent_logs
EOF
    then
        log_message "[WARN] Email notification could not be sent."
    else
        log_message "[INFO] ${status} email alert sent to $EMAIL."
    fi
}

handle_failure() {
    local exit_code=$?

    log_message "[ERROR] Backup failed during step: $CURRENT_STEP"
    send_status_email "FAILED" "PostgreSQL Backup Failed - $TIMESTAMP"
    exit "$exit_code"
}

trap handle_failure ERR

log_message "=================================="
log_message "Backup Started: $RUN_AT"

# STEP 1: BACKUP
CURRENT_STEP="Database backup"
"$PG_DUMP_PATH" -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" > "$SCRIPT_DIR/$FILE_NAME" 2>> "$LOG_FILE"
log_message "[INFO] Backup completed"

# STEP 2: COMPRESS
CURRENT_STEP="Compression"
gzip "$SCRIPT_DIR/$FILE_NAME" 2>> "$LOG_FILE"
log_message "[INFO] Compression done"

# STEP 3: UPLOAD TO S3
CURRENT_STEP="S3 upload"
aws s3 cp "$SCRIPT_DIR/$COMPRESSED_FILE" "s3://$S3_BUCKET/backups/postgres/$DATE_PATH/" >> "$LOG_FILE" 2>&1
log_message "[INFO] Upload successful"

# STEP 4: CLEAN LOCAL FILE
CURRENT_STEP="Local cleanup"
rm -f "$SCRIPT_DIR/$COMPRESSED_FILE"
log_message "[INFO] Local cleanup done"

CURRENT_STEP="Completed"
log_message "Backup Completed Successfully: $(date)"
send_status_email "SUCCESS" "PostgreSQL Backup Succeeded - $TIMESTAMP"
log_message "=================================="
