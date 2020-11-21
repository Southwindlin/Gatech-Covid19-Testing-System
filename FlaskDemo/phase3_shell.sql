/*
CS4400: Introduction to Database Systems
Fall 2020
Phase III Template

Team ##
Team Member Name (GT username)
Team Member Name (GT username)
Team Member Name (GT username)
Team Member Name (GT username)

Directions:
Please follow all instructions from the Phase III assignment PDF.
This file must run without error for credit.
*/


-- ID: 2a
-- Author: lvossler3
-- Name: register_student
DROP PROCEDURE IF EXISTS register_student;
DELIMITER //
CREATE PROCEDURE register_student(
		IN i_username VARCHAR(40),
        IN i_email VARCHAR(40),
        IN i_fname VARCHAR(40),
        IN i_lname VARCHAR(40),
        IN i_location VARCHAR(40),
        IN i_housing_type VARCHAR(20),
        IN i_password VARCHAR(40)
)
BEGIN

-- Type solution below


-- End of solution
END //
DELIMITER ;

-- ID: 2b
-- Author: lvossler3
-- Name: register_employee
DROP PROCEDURE IF EXISTS register_employee;
DELIMITER //
CREATE PROCEDURE register_employee(
		IN i_username VARCHAR(40),
        IN i_email VARCHAR(40),
        IN i_fname VARCHAR(40),
        IN i_lname VARCHAR(40),
        IN i_phone VARCHAR(10),
        IN i_labtech BOOLEAN,
        IN i_sitetester BOOLEAN,
        IN i_password VARCHAR(40)
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;

-- ID: 4a
-- Author: Aviva Smith
-- Name: student_view_results
DROP PROCEDURE IF EXISTS `student_view_results`;
DELIMITER //
CREATE PROCEDURE `student_view_results`(
    IN i_student_username VARCHAR(50),
	IN i_test_status VARCHAR(50),
	IN i_start_date DATE,
    IN i_end_date DATE
)
BEGIN
	DROP TABLE IF EXISTS student_view_results_result;
    CREATE TABLE student_view_results_result(
        test_id VARCHAR(7),
        timeslot_date date,
        date_processed date,
        pool_status VARCHAR(40),
        test_status VARCHAR(40)
    );
    INSERT INTO student_view_results_result

    -- Type solution below

		SELECT t.test_id, t.appt_date, p.process_date, p.pool_status , t.test_status
        FROM Appointment a
            LEFT JOIN Test t
                ON t.appt_date = a.appt_date
                AND t.appt_time = a.appt_time
                AND t.appt_site = a.site_name
            LEFT JOIN Pool p
                ON t.pool_id = p.pool_id
        WHERE i_student_username = a.username
            AND (i_test_status = t.test_status OR i_test_status IS NULL)
            AND (i_start_date <= t.appt_date OR i_start_date IS NULL)
            AND (i_end_date >= t.appt_date OR i_end_date IS NULL);

    -- End of solution
END //
DELIMITER ;

-- ID: 5a
-- Author: asmith457
-- Name: explore_results
DROP PROCEDURE IF EXISTS explore_results;
DELIMITER $$
CREATE PROCEDURE explore_results (
    IN i_test_id VARCHAR(7))
BEGIN
    DROP TABLE IF EXISTS explore_results_result;
    CREATE TABLE explore_results_result(
        test_id VARCHAR(7),
        test_date date,
        timeslot time,
        testing_location VARCHAR(40),
        date_processed date,
        pooled_result VARCHAR(40),
        individual_result VARCHAR(40),
        processed_by VARCHAR(80)
    );
    INSERT INTO explore_results_result

    -- Type solution below

        SELECT * FROM User;

    -- End of solution
END$$
DELIMITER ;

-- ID: 6a
-- Author: asmith457
-- Name: aggregate_results
DROP PROCEDURE IF EXISTS aggregate_results;
DELIMITER $$
CREATE PROCEDURE aggregate_results(
    IN i_location VARCHAR(50),
    IN i_housing VARCHAR(50),
    IN i_testing_site VARCHAR(50),
    IN i_start_date DATE,
    IN i_end_date DATE)
BEGIN
    DROP TABLE IF EXISTS aggregate_results_result;
    CREATE TABLE aggregate_results_result(
        test_status VARCHAR(40),
        num_of_test INT,
        percentage DECIMAL(6,2)
    );

    INSERT INTO aggregate_results_result

    -- Type solution below

    SELECT * FROM User;

    -- End of solution
END$$
DELIMITER ;


-- ID: 7a
-- Author: lvossler3
-- Name: test_sign_up_filter
DROP PROCEDURE IF EXISTS test_sign_up_filter;
DELIMITER //
CREATE PROCEDURE test_sign_up_filter(
    IN i_username VARCHAR(40),
    IN i_testing_site VARCHAR(40),
    IN i_start_date date,
    IN i_end_date date,
    IN i_start_time time,
    IN i_end_time time)
BEGIN
    DROP TABLE IF EXISTS test_sign_up_filter_result;
    CREATE TABLE test_sign_up_filter_result(
        appt_date date,
        appt_time time,
        street VARCHAR (40),
        city VARCHAR(40),
        state VARCHAR(2),
        zip VARCHAR(5),
        site_name VARCHAR(40));
    INSERT INTO test_sign_up_filter_result

    -- Type solution below

    SELECT * FROM User;

    -- End of solution

    END //
    DELIMITER ;

-- ID: 7b
-- Author: lvossler3
-- Name: test_sign_up
DROP PROCEDURE IF EXISTS test_sign_up;
DELIMITER //
CREATE PROCEDURE test_sign_up(
		IN i_username VARCHAR(40),
        IN i_site_name VARCHAR(40),
        IN i_appt_date date,
        IN i_appt_time time
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;

-- Number: 8a
-- Author: lvossler3
-- Name: tests_processed
DROP PROCEDURE IF EXISTS tests_processed;
DELIMITER //
CREATE PROCEDURE tests_processed(
    IN i_start_date date,
    IN i_end_date date,
    IN i_test_status VARCHAR(10),
    IN i_lab_tech_username VARCHAR(40))
BEGIN
    DROP TABLE IF EXISTS tests_processed_result;
    CREATE TABLE tests_processed_result(
        test_id VARCHAR(7),
        pool_id VARCHAR(10),
        test_date date,
        process_date date,
        test_status VARCHAR(10) );
    INSERT INTO tests_processed_result
    -- Type solution below

        SELECT * FROM User;

    -- End of solution
    END //
    DELIMITER ;

-- ID: 9a
-- Author: ahatcher8@
-- Name: view_pools
DROP PROCEDURE IF EXISTS view_pools;
DELIMITER //
CREATE PROCEDURE view_pools(
    IN i_begin_process_date DATE,
    IN i_end_process_date DATE,
    IN i_pool_status VARCHAR(20),
    IN i_processed_by VARCHAR(40)
)
BEGIN
    DROP TABLE IF EXISTS view_pools_result;
    CREATE TABLE view_pools_result(
        pool_id VARCHAR(10),
        test_ids VARCHAR(100),
        date_processed DATE,
        processed_by VARCHAR(40),
        pool_status VARCHAR(20));

    INSERT INTO view_pools_result
-- Type solution below

    SELECT * FROM User;

-- End of solution
END //
DELIMITER ;

-- ID: 10a
-- Author: ahatcher8@
-- Name: create_pool
DROP PROCEDURE IF EXISTS create_pool;
DELIMITER //
CREATE PROCEDURE create_pool(
	IN i_pool_id VARCHAR(10),
    IN i_test_id VARCHAR(7)
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;

-- ID: 10b
-- Author: ahatcher8@
-- Name: assign_test_to_pool
DROP PROCEDURE IF EXISTS assign_test_to_pool;
DELIMITER //
CREATE PROCEDURE assign_test_to_pool(
    IN i_pool_id VARCHAR(10),
    IN i_test_id VARCHAR(7)
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;

-- ID: 11a
-- Author: ahatcher8@
-- Name: process_pool
DROP PROCEDURE IF EXISTS process_pool;
DELIMITER //
CREATE PROCEDURE process_pool(
    IN i_pool_id VARCHAR(10),
    IN i_pool_status VARCHAR(20),
    IN i_process_date DATE,
    IN i_processed_by VARCHAR(40)
)
BEGIN
-- Type solution below

    SELECT pool_status
    INTO @curr_status
    FROM POOL
    WHERE pool_id = i_pool_id;

    IF
        ((@curr_status = 'pending') AND (i_pool_status = 'positive' OR i_pool_status = 'negative'))
    THEN
        UPDATE POOL
        SET pool_status = i_pool_status, process_date = i_process_date, processed_by = i_processed_by
        WHERE pool_id = i_pool_id;
    END IF;


-- End of solution
END //
DELIMITER ;

-- ID: 11b
-- Author: ahatcher8@
-- Name: process_test
DROP PROCEDURE IF EXISTS process_test;
DELIMITER //
CREATE PROCEDURE process_test(
    IN i_test_id VARCHAR(7),
    IN i_test_status VARCHAR(20)
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;

-- ID: 12a
-- Author: dvaidyanathan6
-- Name: create_appointment

DROP PROCEDURE IF EXISTS create_appointment;
DELIMITER //
CREATE PROCEDURE create_appointment(
	IN i_site_name VARCHAR(40),
    IN i_date DATE,
    IN i_time TIME
)
sp_main: BEGIN
-- Type solution below
    -- First get the tester who is working in this site
      -- get the current tester number who are working on this site
      set @testerNum = (select count(distinct sitetester_username)
from SITETESTER join WORKING_AT on sitetester_username = WORKING_AT.username
where WORKING_AT.site = i_site_name);

     if (select count(*) from Appointment where site_name = i_site_name) >= 10 * @testerNum then leave sp_main; end if;
     
     insert into Appointment values (null, i_site_name,i_date,i_time);
-- End of solution
END //
DELIMITER ;

-- check if its right
-- SELECT * FROM covidtest_fall2020.Appointment;
-- CALL create_appointment("Bobby Dodd Stadium", '2020-11-14', '12:00:00');
-- SELECT * FROM covidtest_fall2020.Appointment;


-- ID: 13a
-- Author: dvaidyanathan6@
-- Name: view_appointments
DROP PROCEDURE IF EXISTS view_appointments;
DELIMITER //
CREATE PROCEDURE view_appointments(
    IN i_site_name VARCHAR(40),
    IN i_begin_appt_date DATE,
    IN i_end_appt_date DATE,
    IN i_begin_appt_time TIME,
    IN i_end_appt_time TIME,
    IN i_is_available INT  -- 0 for "booked only", 1 for "available only", NULL for "all"
)
BEGIN
    DROP TABLE IF EXISTS view_appointments_result;
    CREATE TABLE view_appointments_result(

        appt_date DATE,
        appt_time TIME,
        site_name VARCHAR(40),
        location VARCHAR(40),
        username VARCHAR(40));

    INSERT INTO view_appointments_result
-- Type solution below

select appt_date, appt_time,timeRange.site_name,location, timeRange.username
     from  (select * from (select *  from APPOINTMENT 
     where appt_date >= i_begin_appt_date and appt_date <= i_end_appt_date) as dateRange 
     where appt_time>=i_begin_appt_time and appt_time <= i_end_appt_time) as timeRange join SITE on timeRange.site_name = SITE.site_name
where (CASE
    WHEN i_is_available = 0 THEN timeRange.username is not null
    WHEN i_is_available = 1 THEN timeRange.username is null
    else (timeRange.username is null) or (timeRange.username is not null)
    END);


-- End of solution
END //
DELIMITER ;
-- CALL view_appointments('Bobby Dodd Stadium', '2020-07-12', '2020-9-12', '07:00:00', '12:00:00', 0);
-- select * from view_appointments_result;
-- CALL view_appointments('Bobby Dodd Stadium', NULL, NULL, NULL, NULL, NULL);


select * from view_appointments_result;
-- ID: 14a
-- Author: kachtani3@
-- Name: view_testers
DROP PROCEDURE IF EXISTS view_testers;
DELIMITER //
CREATE PROCEDURE view_testers()
BEGIN
    DROP TABLE IF EXISTS view_testers_result;
    CREATE TABLE view_testers_result(

        username VARCHAR(40),
        name VARCHAR(80),
        phone_number VARCHAR(10),
        assigned_sites VARCHAR(255));

    INSERT INTO view_testers_result
-- Type solution below

select testerInfo.username, testerInfo.name, testerInfo.phone_num as phone_number, group_concat(WORKING_AT.Site  order by WORKING_AT.Site) as assigned_sites
from (select emUser.username,phone_num, concat(concat(fname,' '),lname) as name
from SITETESTER join (select *
from employee join user on EMPLOYEE.emp_username = user.username) as emUser on SITETESTER.sitetester_username = emUser.username) as testerInfo left outer join WORKING_AT on testerInfo.username = WORKING_AT.username
group by testerInfo.username;

-- End of solution
END //
DELIMITER ;

-- call view_testers();
-- select * from view_testers_result;


-- ID: 15a
-- Author: kachtani3@
-- Name: create_testing_site
DROP PROCEDURE IF EXISTS create_testing_site;
DELIMITER //
CREATE PROCEDURE create_testing_site(
	IN i_site_name VARCHAR(40),
    IN i_street varchar(40),
    IN i_city varchar(40),
    IN i_state char(2),
    IN i_zip char(5),
    IN i_location varchar(40),
    IN i_first_tester_username varchar(40)
)
sp_main:BEGIN
-- Type solution below

-- first check whether such user exist
if (select count(*)
from SITETESTER
where sitetester_username = i_first_tester_username) <= 0 then leave sp_main; end if;


insert into covidtest_fall2020.SITE values (i_site_name,i_street,i_city,i_state,i_zip,i_location);
insert into covidtest_fall2020.WORKING_AT values (i_first_tester_username,i_site_name);
-- End of solution
END //
DELIMITER ;

-- CALL create_testing_site('Test Site 1','test st', 'Atlanta','GA','30318','East','akarev16');
-- SELECT * FROM covidtest_fall2020.SITE;
-- SELECT * FROM covidtest_fall2020.WORKING_AT;

-- ID: 16a
-- Author: kachtani3@
-- Name: pool_metadata
DROP PROCEDURE IF EXISTS pool_metadata;
DELIMITER //
CREATE PROCEDURE pool_metadata(
    IN i_pool_id VARCHAR(10))
BEGIN
    DROP TABLE IF EXISTS pool_metadata_result;
    CREATE TABLE pool_metadata_result(
        pool_id VARCHAR(10),
        date_processed DATE,
        pooled_result VARCHAR(20),
        processed_by VARCHAR(100));

    INSERT INTO pool_metadata_result
-- Type solution below

    select POOL.pool_id, POOL.process_date as date_processed, POOL.pool_status as pooled_result, concat(concat(fname,' '),lname) as processed_by
    from POOL left outer join USER on POOL.processed_by = USER.username
    where pool_id = i_pool_id;

-- End of solution
END //
DELIMITER ;

-- CALL pool_metadata('1');
-- select * from pool_metadata_result;


-- ID: 16b
-- Author: kachtani3@
-- Name: tests_in_pool
DROP PROCEDURE IF EXISTS tests_in_pool;
DELIMITER //
CREATE PROCEDURE tests_in_pool(
    IN i_pool_id VARCHAR(10))
BEGIN
    DROP TABLE IF EXISTS tests_in_pool_result;
    CREATE TABLE tests_in_pool_result(
        test_id varchar(7),
        date_tested DATE,
        testing_site VARCHAR(40),
        test_result VARCHAR(20));

    INSERT INTO tests_in_pool_result
-- Type solution below

    SELECT * FROM User;

-- End of solution
END //
DELIMITER ;

-- ID: 17a
-- Author: kachtani3@
-- Name: tester_assigned_sites
DROP PROCEDURE IF EXISTS tester_assigned_sites;
DELIMITER //
CREATE PROCEDURE tester_assigned_sites(
    IN i_tester_username VARCHAR(40))
BEGIN
    DROP TABLE IF EXISTS tester_assigned_sites_result;
    CREATE TABLE tester_assigned_sites_result(
        site_name VARCHAR(40));

    INSERT INTO tester_assigned_sites_result
-- Type solution below

    SELECT * FROM User;

-- End of solution
END //
DELIMITER ;

-- ID: 17b
-- Author: kachtani3@
-- Name: assign_tester
DROP PROCEDURE IF EXISTS assign_tester;
DELIMITER //
CREATE PROCEDURE assign_tester(
	IN i_tester_username VARCHAR(40),
    IN i_site_name VARCHAR(40)
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;


-- ID: 17c
-- Author: kachtani3@
-- Name: unassign_tester
DROP PROCEDURE IF EXISTS unassign_tester;
DELIMITER //
CREATE PROCEDURE unassign_tester(
	IN i_tester_username VARCHAR(40),
    IN i_site_name VARCHAR(40)
)
BEGIN
-- Type solution below


-- End of solution
END //
DELIMITER ;


-- ID: 18a
-- Author: lvossler3
-- Name: daily_results
DROP PROCEDURE IF EXISTS daily_results;
DELIMITER //
CREATE PROCEDURE daily_results()
BEGIN
	DROP TABLE IF EXISTS daily_results_result;
    CREATE TABLE daily_results_result(
		process_date date,
        num_tests int,
        pos_tests int,
        pos_percent DECIMAL(6,2));
	INSERT INTO daily_results_result
    -- Type solution below

    SELECT * FROM User;

    -- End of solution
    END //
    DELIMITER ;














