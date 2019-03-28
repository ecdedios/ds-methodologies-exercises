USE telco_churn;
SHOW TABLES;
DESCRIBE contract_types;
DESCRIBE customers;

SELECT * FROM contract_types;

SELECT 	customer_id,
		tenure,
        monthly_charges,
        total_charges
FROM customers as c
JOIN contract_types as t
ON c.contract_type_id = t.contract_type_id
WHERE t.contract_type_id = '3';