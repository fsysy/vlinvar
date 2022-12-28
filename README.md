# VLinvar

* Visualized cLinvar (VLinvar) is a useful tool for the interpretation of genetic variants. It change multiple charicteristics of variants, like the population minor allele frequency, in-silico prediction, variant types, into images based on the statistical characteristics of each genes. You would get useful insight from this tool.

+ Dev step 1 (2022-08-17)
I am trying to make some parsing tool for Clinvar, but the XML file of clinvar is very complicate. It is almost impossible to change the XML into CSV, because the data-size is too big and the hierachy of data structure is not appropriate. Also, the storage size of my current dev server is very small, so I cannot finish the parsing.
So, I change the server, and trying to use mysql.

this site is very useful for the initiation (https://pinggoopark.tistory.com/122)

the database name is clinvar.


# MySQL command
sudo mysql -u root

use clinvar;

show tables;

SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='CLINVARSET';

OR

SHOW COLUMNS FROM CLINVARSET;

ALTER TABLE CLINVARSET MODIFY CLINVARACCESSION_ACC varchar(20);

ALTER TABLE CLINVARSET CONVERT TO CHARACTER SET utf8;

ALTER TABLE `CLINVARSET` ADD `CHROMOSOME` VARCHAR(10) AFTER MEASURESET_ALTERNATE;

select column_name,data_type from information_schema.columns where table_name = 'CLINVARSET';



# MySQL data type
ClinvarSet
+------------------------------+-----------+
| column_name                  | data_type |
+------------------------------+-----------+
| ID                           | int       |
| SYMBOL                       | varchar   |
| STATUS                       | varchar   |
| TITLE                        | varchar   |
| DATECREATED                  | varchar   |
| DATELASTUPDATED              | varchar   |
| REFCLINVAR_ID                | varchar   |
| CLINVARACCESSION_ACC         | varchar   |
| CLINVARACCESSION_VERSION     | varchar   |
| CLINVARACCESSION_DATEUPDATED | varchar   |
| CLINVARRECORDSTATUS          | varchar   |
| CLINVARSIG_DATELASTEVALUATED | varchar   |
| CLINVARSIG_REVIEWSTATUS      | varchar   |
| CLINVARSIG_DESCRIPTION       | varchar   |
| MEASURESET_ID                | varchar   |
| MEASURESET_ACC               | varchar   |
| MEASURESET_VERSION           | varchar   |
| MEASURESET_PREFERRED         | varchar   |
| MEASURESET_ALTERNATE         | varchar   |
| CHROMOSOME                   | varchar   |
| POSITION                     | int       |
| REF                          | text      |
| ALT                          | text      |
| CLINVAR_ASSERT_ID            | varchar   |
+------------------------------+-----------+


CLINVARASSERTION
+------------------------------+------------+
| column_name                  | data_type  |
+------------------------------+------------+
| ID                           | varchar    |
| LOCALKEY                     | varchar    |
| SUBMITTER                    | varchar    |
| SUBMITTER_DATE               | varchar    |
| TITLE                        | varchar    |
| ACC                          | varchar    |
| ACC_VERSION                  | varchar    |
| ACC_TYPE                     | varchar    |
| ACC_ORGID                    | varchar    |
| ACC_DATE                     | varchar    |
| RECORDSTATUS                 | varchar    |
| CLINCALSIGNIFICANCE_LASTDATE | varchar    |
| REVIEWSTATUS                 | varchar    |
| DESCRIPTION                  | varchar    |
| COMMENT                      | text       |
| ASSERTION_TYPE               | varchar    |
| EXTDB                        | varchar    |
| EXTDB_ID                     | varchar    |
| SAMPLE                       | varchar    |
| SPECIES                      | varchar    |
| AFFECTEDSTATUS               | varchar    |
| METHODTYPE                   | varchar    |
| OBSERVED_DATA                | mediumtext |
| SYMBOL                       | varchar    |
+------------------------------+------------+





