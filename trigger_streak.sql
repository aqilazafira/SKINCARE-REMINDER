CREATE TRIGGER timelines_update_streak AFTER INSERT ON timelines FOR EACH ROW BEGIN
    DECLARE last_date DATE;
    DECLARE days_diff INT;

    -- ambil timeline sebelumnya
    SELECT DATE(date)
    INTO last_date
    FROM timelines
    WHERE user_id = NEW.user_id
    ORDER BY date DESC
    LIMIT 1 OFFSET 1;

    -- hitung selisih hari
    IF last_date IS NOT NULL THEN
        SET days_diff = DATEDIFF(DATE(NEW.date), last_date);
        
        -- jika gap 1 hari, tambah streak
        IF days_diff = 1 THEN
            UPDATE users
            SET streak = streak + 1
            WHERE id = NEW.user_id;
        -- jika gap lebih dari 1 hari, reset streak ke 1
        ELSE
            UPDATE users
            SET streak = 1
            WHERE id = NEW.user_id;
        END IF;
    ELSE
        -- timeline pertama, mulai streak dari 1
        UPDATE users
        SET streak = 1
        WHERE id = NEW.user_id;
    END IF;
END