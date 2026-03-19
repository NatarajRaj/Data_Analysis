# Part 1 – Cost Analysis (Decision Making)

## Problem Statement

* Initial Database Size: **100 GB**
* Daily Growth: **2 GB/day**
* Retention Requirement: **30–90 days**
* Objective: Design a **cost-efficient, reliable, and maintainable backup strategy**

---

# Approach 1: Full Daily Backup

## Backup Strategy

* Take a **full database backup daily** using `pg_dump`
* Compress using gzip
* Store in S3 with date-based structure

---

## Retention Strategy

* Use **S3 Lifecycle Policy**
* Automatically delete backups older than **30–90 days**

---

## Restore Strategy

* Restore using a single backup file:

```bash id="g1l9ux"
psql db_name < backup.sql
```

---

## Evaluation

### Cost

* Stores full copy every day → higher storage usage
* Compression reduces size significantly
* Overall cost: **Moderate**

---

###  Restore Speed

* Very fast
* Single-step restore

---

###  Operational Complexity

* Low complexity
* Easy to automate and maintain

---

## Summary

```text id="r2b9xu"
Simple, reliable, and fast recovery but uses more storage
```

---

<!-- --------------------------------------------------------------------------------- -->

#  Approach 2: Incremental Backup

## Backup Strategy

* Take one **full backup initially**
* Store only **daily changes (2 GB/day)**
* Requires change tracking (CDC / logs)

---

##  Retention Strategy

* Retain:

  * Base full backup
  * Incremental backups for 30–90 days
* Delete old backup chains after retention period

---

##  Restore Strategy

* Restore process:

  1. Restore full backup
  2. Apply all incremental backups sequentially

---

##  Evaluation

###  Cost

* Stores only incremental changes
* Significantly lower storage usage
* Overall cost: **Low**

---

###  Restore Speed

* Slower restore
* Depends on multiple backup files

---

### Operational Complexity

* High complexity
* Requires:

  * Change tracking
  * Dependency management
  * Error handling

---

##  Summary

```text id="6r9l1n"
Cost-efficient but complex and slower recovery
```

---

#  Comparison

| Criteria      | Full Backup   | Incremental Backup |
| ------------- | ------------- | ------------------ |
| Backup Type   | Full snapshot | Change-based       |
| Cost          | Medium        | Low                |
| Restore Speed | Fast          | Slow               |
| Complexity    | Low           | High               |
| Reliability   | High          | Medium             |

---

#  Decision Making

##  Cheapest Long-Term

 **Incremental Backup**

* Stores only daily changes (2 GB/day)
* Reduces long-term storage cost significantly

---

##  Fastest to Restore

**Full Backup**

* Single backup file
* No dependency chain

---

##  Trade-off Analysis

| Factor          | Preferred Approach |
| --------------- | ------------------ |
| Cost Efficiency | Incremental        |
| Simplicity      | Full Backup        |
| Reliability     | Full Backup        |
| Recovery Speed  | Full Backup        |

---

#  Final Recommendation

 **Full Daily Backup (pg_dump + Compression + S3)**

---

## Justification

* Easy to implement and maintain
* Faster recovery during failures
* Lower operational risk
* Suitable for small-to-medium scale systems
* Meets assignment constraint (low cost, no complex infrastructure)

---

##  Retention Decision

* Use **S3 Lifecycle Policy**
* Automatically delete backups older than **30–90 days**
* Ensures cost optimization without manual intervention

---

# Final Decision

```text id="x4m2za"
Adopt Full Daily Backup with S3 lifecycle-based retention for a balance of simplicity, reliability, and acceptable cost
```

---

#  Conclusion

The selected approach prioritizes:

* **Reliability over aggressive cost savings**
* **Simplicity over complex engineering**
* **Fast recovery over storage optimization**

This ensures a **robust, maintainable, and cost-aware solution** aligned with real-world data engineering practices.
