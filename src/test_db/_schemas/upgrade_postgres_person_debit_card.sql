
ALTER TABLE person_debit_card DROP CONSTRAINT person_debit_card_card_number_key;
ALTER TABLE person_debit_card ALTER COLUMN card_number DROP NOT NULL;
