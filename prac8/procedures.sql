CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE phonebook
    SET phone = p_phone
    WHERE name = p_name;

    IF NOT FOUND THEN
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        
        IF phones[i] ~ '^[0-9]+$' THEN
            INSERT INTO phonebook(name, phone)
            VALUES (names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Wrong phone: % - %', names[i], phones[i];
        END IF;

    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_user(val TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = val OR phone = val;
END;
$$;
