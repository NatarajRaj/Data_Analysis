AWS CLI commands:

1. DELETE ALL FILES FROM S3 BUCKET
aws s3 rm s3://natarajan-de-2026-bucket-1 --recursive

2. DELETE THE EMPTY S3 BUCKET
aws s3 rb s3://natarajan-de-2026-bucket-1

3. VERIFY BUCKET IS DELETED
aws s3 ls | grep natarajan-de-2026-bucket-1

4. CHECK IF ANY FILES REMAIN
aws s3 ls s3://natarajan-de-2026-bucket-1 --recursive

5. DROP ATHENA TABLE
aws athena start-query-execution \
    --query-string "DROP TABLE IF EXISTS lakehouse_demo.orders;" \
    --result-configuration OutputLocation=s3://natarajan-de-2026-bucket-1/athena-results/ \
    --region ap-south-2

6. DROP ATHENA DATABASE
aws athena start-query-execution \
    --query-string "DROP DATABASE IF EXISTS lakehouse_demo;" \
    --result-configuration OutputLocation=s3://natarajan-de-2026-bucket-1/athena-results/ \
    --region ap-south-2


 <!-- ------------------------------------------- -->

Billing and Cost Management:

<!-- Screenshot of AWS Billing page showing $0 cost attached -->


