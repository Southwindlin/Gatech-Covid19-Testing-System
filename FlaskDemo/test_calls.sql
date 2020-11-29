-- S2
	-- register_student
		-- [GOOD]
	CALL register_student('lvossler3', 'laurenvossler@gatech.edu', 'Lauren', 'Vossler', 'East', 'Off-campus Apartment',  'iLoVE4400$');
        -- [BAD] username already exists
	CALL register_student('jlionel666', 'laurenvossler@gatech.edu', 'Lauren', 'Vossler', 'East', 'Off-campus Apartment',  'iLoVE4400$');

    -- register_employee
		-- [GOOD]
	CALL register_employee('sstentz3', 'sstentz3@gatech.edu', 'Samuel', 'Stentz', '9703312824', True, True, 'l@urEni$myLIFE2');
        -- [BAD] username already exists
	CALL register_employee('mgeller3', 'sstentz3@gatech.edu', 'Sammy', 'Zee', '9703312824', True, True, 'weLCome2Fl@v@Twn');

-- S4
-- Should show only negative test for given user between the given dates
call student_view_results('aallman302', 'negative', '2020-09-01', '2020-09-10');
call student_view_results('aallman302', 'negative', '2020-09-01', '2020-09-16');
call student_view_results('aallman302', 'negative', '2020-09-01', '2020-09-03');
-- Should show only postive test for given user between the given dates
call student_view_results('aallman302', 'positive', '2020-09-01', '2020-09-10');
call student_view_results('aallman302', 'positive', '2020-09-01', '2020-09-16');
call student_view_results('aallman302', 'positive', '2020-09-01', '2020-09-03');
-- Should show only pending test for given user between the given dates
call student_view_results('aallman302', 'pending', '2020-09-01', '2020-09-10');
call student_view_results('aallman302', 'pending', '2020-09-01', '2020-10-10');
-- Should show all test for given users between the given dates
call student_view_results('aallman302', NULL, '2020-09-01', '2020-09-10');
call student_view_results('aallman302', NULL, '2020-09-01', '2020-10-10');
call student_view_results('abernard224', NULL, '2020-09-01', '2020-10-10');
call student_view_results('jpark29', NULL, '2020-09-01', '2020-10-10');
-- Test should not fail for any null inputs
call student_view_results('aallman302', null, '2020-09-01', '2020-09-10');
call student_view_results('aallman302', 'all', null, '2020-09-10');
call student_view_results('aallman302', 'all', '2020-09-01', null);
call student_view_results('jpark29', 'all', '2020-09-01', '2020-09-10');
call student_view_results('abernard224', null, null, '2020-09-10');

-- S5
	-- explore_results
		-- [GOOD] test exists
		CALL  explore_results('100017');
		-- [GOOD] test doesn't exist
		CALL  explore_results('999999');
		-- [GOOD] test exists with all info
		CALL explore_result('100001');
		-- [GOOD] Processed_date and Processed_by fields are NULL
		CALL explore_result('100059');
		CALL explore_result('100049');
        
        -- [BAD]
        CALL explore_result(null);

-- S6
	-- aggregate_results
		-- [GOOD] all results
        CALL aggregate_results(NULL, NULL, NULL, NULL, NULL);

        -- [GOOD] just people who live on east
        CALL aggregate_results('East', NULL, NULL, NULL, NULL);

-- S7
	-- test_sign_up_filter
		-- [GOOD] Show all test options for mbob2
	CALL test_sign_up_filter('mbob2', NULL, NULL, NULL, NULL, NULL);
		-- [BAD]  Should show nothing as site not at same locaiton as student
	CALL test_sign_up_filter('mgeller3', 'Coda Building', NULL, NULL, NULL, NULL);
		-- [GOOD] Test date filters
	CALL test_sign_up_filter('gburdell1', 'North Avenue (Centenial Room)', '2020-10-01', '2020-10-06', NULL, NULL);
		-- [GOOD] Test time filters
	CALL test_sign_up_filter('gburdell1', NULL, NULL, NULL, '9:00:00', '13:00:00');

	-- test_sign_up
		-- [GOOD] Standard case
		CALL test_sign_up('pbuffay56', 'Bobby Dodd Stadium', '2020-09-16', '12:00:00', '12345');

		-- [BAD] User already has a pending test
		CALL test_sign_up('gburdell1', 'North Avenue (Centenial Room)', '2020-10-07', '10:00:00', '12346');

        -- [BAD] Appointment already has someone signed up
		CALL test_sign_up('pbuffay56', 'Bobby Dodd Stadium', '2020-09-10', '17:00:00', '100050');

        -- [BAD] Duplicate test id
		CALL test_sign_up('pbuffay56', 'Bobby Dodd Stadium', '2020-09-16', '12:00:00', '100050');


-- S8
	-- tests_processed
		-- [GOOD] Show all tests processed by ygao10
    	CALL tests_processed(NULL, NULL, NULL, 'ygao10');
		-- [GOOD] tests start_date filter
	CALL tests_processed('2020-09-03', NULL, NULL, 'jhilborn97');
		-- [GOOD] tests end_date and status filters
	CALL tests_processed(NULL, '2020-09-07', 'positive', 'ygao10');
-- S9
  -- view_pools
    -- [GOOD] standard, retrieve all pools
    CALL view_pools(NULL, NULL, NULL, NULL);

    -- [GOOD] standard all params
    CALL view_pools('1900-10-10', '2020-12-12', 'positive', 'jhilborn98');

    -- [GOOD] get all pools within 2 dates
    CALL view_pools('1900-10-10', '2020-12-12', NULL, NULL);

    -- [GOOD] gets all pools processed on or after 2020-09-05 (should include pending pools)
    CALL view_pools('2020-09-05', NULL, NULL, NULL);

    -- [GOOD] gets all pools processed on or before 2020-09-05 (should not include pending pools)
    CALL view_pools(NULL, '2020-09-05', NULL, NULL);

    -- [BAD] shouldn't retrieve anything because pool can't have a date and be pending
    CALL view_pools(NULL, '2020-09-05', 'pending', NULL);

    -- [GOOD] gets pools with jhilborn97 processor
    CALL view_pools(NULL, NULL, NULL, 'jhilborn97');

    -- [BAD] gets pools with firstlast99 processor (should retrieve nothing, this processor doesn't exist)
    CALL view_pools(NULL, NULL, NULL, 'firstlast99');

    -- [GOOD] gets pending pools
    CALL view_pools(NULL, NULL, 'pending', NULL);

    -- [BAD] gets pools with updating status (should retreive nothing, updating isn't a valid status)
    CALL view_pools(NULL, NULL, 'updating', NULL);
    
-- S10
  -- TEST DATA TO INSERT FOR THESE TESTS
    INSERT INTO POOL
    VALUES('88','pending',NULL,NULL);

    INSERT INTO APPOINTMENT
    VALUES ('dkim99','North Avenue (Centenial Room)','2020-12-12','12:00:00'),
    ('dschrute18','North Avenue (Centenial Room)','2020-12-12','13:00:00'),
    ('dsmith102','North Avenue (Centenial Room)','2020-12-12','14:00:00'),
    ('gburdell1','North Avenue (Centenial Room)','2020-12-12','15:00:00'),
    ('hpeterson55','North Avenue (Centenial Room)','2020-12-12','16:00:00'),
    ('jhalpert75','North Avenue (Centenial Room)','2020-12-12','17:00:00'),
    ('jpark29','North Avenue (Centenial Room)','2020-12-12','18:00:00'),
    ('jtribbiani27','North Avenue (Centenial Room)','2020-12-12','19:00:00'),
    ('kkapoor155','North Avenue (Centenial Room)','2020-12-12','20:00:00');

    INSERT INTO TEST
    VALUES ('100088','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','12:00:00'),
    ('100089','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','13:00:00'),
    ('100090','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','14:00:00'),
    ('100091','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','15:00:00'),
    ('100092','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','16:00:00'),
    ('100093','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','17:00:00'),
    ('100094','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','18:00:00'),
    ('100095','pending',NULL,'North Avenue (Centenial Room)','2020-12-12','19:00:00'),
    ('100096','pending','88','North Avenue (Centenial Room)','2020-12-12','20:00:00');

  -- DELETE VALUES INSERTED FOR TESTING (when need to reset or get rid of extra data)
    DELETE FROM TEST WHERE test_id >= '100088' AND test_id <= '100096';
    DELETE FROM APPOINTMENT WHERE site_name = 'North Avenue (Centenial Room)' AND appt_date = '2020-12-12' AND appt_time > '10:00:00';
    DELETE FROM POOL WHERE pool_id = '88';
    DELETE FROM POOL WHERE pool_id = '99';

  -- create_pool
    -- [GOOD] standard: test has null pool and pool doesn't exist yet
    CALL create_pool('99','100088');

    -- [BAD] pool already exists
    CALL create_pool('88','100088');

    -- [BAD] test has pool id already
    CALL create_pool('99','100096');

    -- [BAD] test id doesn't exist
    CALL create_pool('99','100100');

  -- assign_test_to_pool
    -- [GOOD] standard, test exists with null pool, pool exists with < 7 tests
    CALL create_pool('99','100088');
    CALL assign_test_to_pool('99','100089');

    -- [BAD] pool_id doesn't exist
    CALL assign_test_to_pool('99','100089');

    -- [BAD] test already assinged to a pool
    CALL create_pool('99','100088');
    CALL assign_test_to_pool('99','100096');

    -- [BAD] test id doesn't exist
    CALL create_pool('99','100088');
    CALL assign_test_to_pool('99','100100');

    -- [BAD] pool already has max tests (all should work until last call)
    CALL create_pool('99','100088');
    CALL assign_test_to_pool('99','100089');
    CALL assign_test_to_pool('99','100090');
    CALL assign_test_to_pool('99','100091');
    CALL assign_test_to_pool('99','100092');
    CALL assign_test_to_pool('99','100093');
    CALL assign_test_to_pool('99','100094');
    CALL assign_test_to_pool('99','100095');

-- S11
  -- process_pool and process_test
    -- TEST DATA TO INSERT FOR THESE TESTS
    INSERT INTO POOL
    VALUES('88','pending',NULL,NULL);

    INSERT INTO APPOINTMENT
    VALUES ('dkim99','North Avenue (Centenial Room)','2020-12-12','12:00:00'),
    ('dschrute18','North Avenue (Centenial Room)','2020-12-12','13:00:00'),
    ('dphilbin81','North Avenue (Centenial Room)','2020-12-12','14:00:00');

    INSERT INTO TEST
    VALUES ('100088','pending','88','North Avenue (Centenial Room)','2020-12-12','12:00:00'),
    ('100089','pending','88','North Avenue (Centenial Room)','2020-12-12','13:00:00'),
    ('100090','pending','88','North Avenue (Centenial Room)','2020-12-12','14:00:00');

    -- DELETE VALUES INSERTED FOR TESTING (when need to reset or get rid of extra data)
    DELETE FROM TEST WHERE test_id = '100088' OR test_id = '100089' OR test_id = '100090';
    DELETE FROM APPOINTMENT WHERE site_name = 'North Avenue (Centenial Room)' AND appt_date = '2020-12-12' AND appt_time > '10:00:00';
    DELETE FROM POOL WHERE pool_id = '88';

      -- [GOOD] standard input: process pool to be positive, then process tests to be pos/neg
      CALL process_pool('88', 'positive', '2020-12-14', 'jhilborn98');
      CALL process_test('100088', 'positive');
      CALL process_test('100089', 'negative');
      CALL process_test('100090', 'negative');

      -- [GOOD] standard input: process pool to be negative then all tests to be negative
      CALL process_pool('88', 'negative', '2020-12-14', 'jhilborn98');
      CALL process_test('100088', 'negative');
      CALL process_test('100089', 'negative');
      CALL process_test('100090', 'negative');

      -- [BAD] process test while parent pool still has pending status
      CALL process_test('100088', 'positive');

      -- [BAD] process tests as positve while pool is negative
      CALL process_pool('88', 'negative', '2020-12-14', 'jhilborn98');
      CALL process_test('100088', 'positive');

      -- [BAD] process tests with invalid status input
      CALL process_pool('88', 'positive', '2020-12-14', 'jhilborn98');
      CALL process_test('100088', 'invstatus');

      -- [BAD] process test that is already processed
      CALL process_pool('88', 'positive', '2020-12-14', 'jhilborn98');
      CALL process_test('100088', 'positive');
      CALL process_test('100088', 'negative');

      -- [BAD] process pool that is already processed
      CALL process_pool('88', 'negative', '2020-12-14', 'jhilborn98');
      CALL process_pool('88', 'positive', '2020-12-14', 'jhilborn98');

      -- [BAD] process pool with invalid status input
      CALL process_pool('88', 'invstatus', '2020-12-14', 'jhilborn98');

      -- [BAD] process pool with invalid lab tester
      CALL process_pool('88', 'positive', '2020-12-14', 'firstlast99');

      -- [BAD] process pool w/ invalid pool id
      CALL process_pool('8888', 'positive', '2020-12-14', 'firstlast99');

      -- [BAD] process test w/ invalid test id
      CALL process_test('999999', 'positive');
-- S12
  -- create_appointment
	-- Deletes test values from table
    DELETE FROM APPOINTMENT WHERE appt_date = '2020-11-14';

    -- [GOOD] standard, create new appointment
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:00');

    -- [BAD] invalid site name, should not insert anything
    CALL create_appointment("Square on Fifth", '2020-11-14', '12:00:00');

    -- [BAD] too many appointments for one day, should not insert 12:00:20
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:01');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:02');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:03');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:04');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:05');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:06');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:07');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:08');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:09');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:10');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:11');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:12');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:13');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:14');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:15');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:16');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:17');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:18');
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:19');

    -- Should not create this appointment in table
    CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:20');

-- S13
  -- view_appointments
	-- [GOOD] standard, retrieve all appointments
    CALL view_appointments(NULL, NULL, NULL, NULL, NULL, NULL);

    -- [GOOD] standard all params
    CALL view_appointments('Bobby Dodd Stadium', '2020-07-12', '2020-9-12', '07:00:00', '12:00:00', 0);

    -- [GOOD] get all appointments that take place within Bobby Dodd Stadium
    CALL view_appointments('Bobby Dodd Stadium', NULL, NULL, NULL, NULL, NULL);

    -- [GOOD] gets all appointments on or after 2020-09-10
    CALL view_appointments(NULL, '2020-09-10', NULL, NULL, NULL, NULL);

    -- [GOOD] gets all appointments on or before 2020-09-10
    CALL view_appointments(NULL, NULL, '2020-09-10', NULL, NULL, NULL);

    -- [BAD] shouldn't retrieve anything because since begin date must be smaller than end date
    CALL view_appointments(NULL, '2020-09-10', '2020-08-10', NULL, NULL, NULL);

    -- [GOOD] gets all appointments on or after 12:00:00
    CALL view_appointments(NULL, NULL, NULL, '12:00:00', NULL, NULL);

    -- [GOOD] gets all appointments on or after 12:00:00
    CALL view_appointments(NULL, NULL, NULL, NULL, '12:00:00', NULL);

    -- [BAD] gets appointments with 'Square On Fifth Apartments' site (should retrieve nothing, this site doesn't exist)
    CALL view_appointments('Square On Fifth Apartments', NULL, NULL, NULL, NULL, NULL);

    -- [GOOD] gets all available appointments
    CALL view_appointments(NULL, NULL, NULL, NULL, NULL, 1);

    -- [GOOD] gets all booked appointments
    CALL view_appointments(NULL, NULL, NULL, NULL, NULL, 0);

    -- [BAD] gets appointments with invalid availability (should retrieve nothing)
    CALL view_appointments(NULL, NULL, NULL, NULL, NULL, 3);


-- S14
  -- view_testers
    -- [GOOD] standard call
    CALL view_testers();

-- S15
  -- create_testing_site
    -- [GOOD] standard call
    CALL
    create_testing_site('Test Site 1','test st',
        'Atlanta','GA','30318','East','akarev16');

    -- [BAD] name is already in the DB (Works_on shouldn't be added)
    CALL
    create_testing_site('Curran St Parking Deck',
        'test st','Atlanta','GA','30318','East','akarev16');
    
    -- [BAD]
   CALL
    create_testing_site('Test Site 2',
        null,null,null,'30318','East','akarev16');

-- S16
  -- pool_metadata
    -- [GOOD] negative pool
    CALL pool_metadata('1');

    -- [GOOD] positive pool
    CALL pool_metadata('8');

    -- [BAD] pool_id doesn't exist
    CALL pool_metadata('987');
    
        -- [BAD] pool_id doesn't exist
    CALL pool_metadata(null);

  -- tests_in_pool
    -- [GOOD] negative pool
    CALL tests_in_pool('1');

    -- [GOOD] positive pool
    CALL tests_in_pool('8');

    -- [BAD] pool_id doesn't exist
    CALL tests_in_pool('987');

-- S17
  -- tester_assigned_sites
    -- [GOOD] tester has many sites
    CALL tester_assigned_sites('akarev16');

    -- [GOOD] tester has 1 site
    CALL tester_assigned_sites('pwallace51');

    -- [GOOD] tester has no sites
    CALL tester_assigned_sites('jrosario34');

  -- assign_tester
    -- [GOOD] standard call
    CALL assign_tester('akarev16', 'West Village');

    -- [BAD] user is not a tester
    CALL assign_tester('jtribbiani27', 'West Village');

    -- [BAD] site doesn't exist
    CALL assign_tester('akarev16', 'Alien Site');

  -- unassign_tester
    -- [GOOD] standard call
    CALL unassign_tester('dmcstuffins7', 'West Village');

    -- [BAD] tester isn't assigned to site
    CALL unassign_tester('akarev16', 'West Village');

    -- [BAD] trying to remove last tester (second one shouldn't be removed)
    CALL unassign_tester('dmcstuffins7', 'West Village');
    CALL unassign_tester('sstrange11', 'West Village');

  -- S18
	-- daily_results
		-- [GOOD]
		CALL daily_results();

