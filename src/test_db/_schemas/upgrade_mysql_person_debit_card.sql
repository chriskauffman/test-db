
ALTER TABLE person_debit_card DROP INDEX card_number;
ALTER TABLE person_debit_card MODIFY COLUMN card_number text;
