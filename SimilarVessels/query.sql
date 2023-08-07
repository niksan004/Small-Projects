DELIMITER //

DROP PROCEDURE IF EXISTS find_similar_vessels_new;
CREATE PROCEDURE find_similar_vessels_new()
BEGIN
	DECLARE done INT;
	DECLARE curr_imo INT;
    
    	DECLARE cur CURSOR FOR SELECT IMO FROM vessels WHERE TYPE LIKE 'A%' AND DEATH = 0;
    	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
	OPEN cur;
    
    	TRUNCATE TABLE similar;

	match_vessels: LOOP
		FETCH cur INTO curr_imo;
        
		IF done = 1 THEN
			LEAVE match_vessels;
		END IF;
        
	        SELECT @cur_gt := GT, @cur_loa := LOA, @cur_type := TYPE, @cur_built := BUILT FROM vessels WHERE IMO = curr_imo;
	        
	        INSERT INTO similar (IMO, SIMILAR, DELTA)
		SELECT 
			curr_imo,
	            	IMO,
			CASE 
				WHEN @cur_gt != 0 THEN ABS((CAST(@cur_gt AS SIGNED) * 10000 + CAST(@cur_built AS SIGNED)) - (CAST(GT AS SIGNED) * 10000 + CAST(BUILT AS SIGNED)))
	                	ELSE ABS((CAST(ROUND(@cur_loa) AS SIGNED) * 10000 + CAST(@cur_built AS SIGNED)) - (CAST(ROUND(LOA) AS SIGNED) * 10000 + CAST(BUILT AS SIGNED)))
			END AS DELTA
		FROM vessels
	        WHERE IMO != curr_imo AND TYPE = @cur_type AND DEATH = 0
	        ORDER BY DELTA
	        LIMIT 10;
	END LOOP;
	
	CLOSE cur;
END //

DELIMITER ;
