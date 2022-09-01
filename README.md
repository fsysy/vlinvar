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
