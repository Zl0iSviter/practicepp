-- ============================================================
-- functions.sql  –  PhoneBook v2
-- Includes Practice-8 functions + new Practice-9 function.
-- ============================================================

-- ─── Practice-8 functions (unchanged) ─────────────────────

CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone FROM phonebook p
    WHERE p.name  ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_phonebook(limit_val INT, offset_val INT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone FROM phonebook p
    ORDER BY p.id DESC
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;

-- ─── Practice-9 new function ──────────────────────────────

-- 3.4 c) search_contacts — searches name, email, AND all phone numbers
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INTEGER,
    name       VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    grp        VARCHAR,
    phone      VARCHAR,
    phone_type VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (c.id, ph.id)
           c.id,
           c.name,
           c.email,
           c.birthday,
           g.name  AS grp,
           ph.phone,
           ph.type AS phone_type
    FROM   contacts c
    LEFT   JOIN groups g  ON g.id  = c.group_id
    LEFT   JOIN phones ph ON ph.contact_id = c.id
    WHERE  c.name  ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%'
    ORDER BY c.id, ph.id;
END;
$$ LANGUAGE plpgsql;

-- Helper: paginated contacts with full detail
CREATE OR REPLACE FUNCTION get_contacts(
    p_limit  INT,
    p_offset INT,
    p_sort   VARCHAR DEFAULT 'name'   -- 'name' | 'birthday' | 'created_at'
)
RETURNS TABLE(
    id         INTEGER,
    name       VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    grp        VARCHAR,
    phones_agg TEXT,
    created_at TIMESTAMPTZ
) AS $$
DECLARE
    v_order TEXT;
BEGIN
    v_order := CASE p_sort
        WHEN 'birthday'   THEN 'c.birthday'
        WHEN 'created_at' THEN 'c.created_at'
        ELSE 'c.name'
    END;

    RETURN QUERY EXECUTE format(
        $q$
        SELECT c.id,
               c.name,
               c.email,
               c.birthday,
               g.name AS grp,
               STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', '
                          ORDER BY ph.id) AS phones_agg,
               c.created_at
        FROM   contacts c
        LEFT   JOIN groups g  ON g.id  = c.group_id
        LEFT   JOIN phones ph ON ph.contact_id = c.id
        GROUP BY c.id, g.name
        ORDER BY %s
        LIMIT  %s OFFSET %s
        $q$,
        v_order, p_limit, p_offset
    );
END;
$$ LANGUAGE plpgsql;

-- Helper: contacts filtered by group
CREATE OR REPLACE FUNCTION get_contacts_by_group(
    p_group  VARCHAR,
    p_limit  INT DEFAULT 50,
    p_offset INT DEFAULT 0
)
RETURNS TABLE(
    id         INTEGER,
    name       VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    phones_agg TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id,
           c.name,
           c.email,
           c.birthday,
           STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', '
                      ORDER BY ph.id)
    FROM   contacts c
    JOIN   groups g   ON g.id  = c.group_id AND g.name ILIKE p_group
    LEFT   JOIN phones ph ON ph.contact_id = c.id
    GROUP BY c.id
    ORDER BY c.name
    LIMIT  p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
