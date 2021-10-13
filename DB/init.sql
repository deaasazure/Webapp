CREATE schema mlaas;

create sequence unq_num_seq increment 1;

SELECT setval('unq_num_seq', 1);

CREATE TABLE mlaas.activity_master_tbl (
	"index" serial NOT NULL,
	activity_id text NULL,
	activity_name text NULL,
	activity_description text NULL,
	"language" text NULL,
	operation text NULL,
	code int8 NULL,
	parent_activity_id int8 NULL,
	user_input int8 NULL,
	check_type int8 NULL
);


CREATE TABLE mlaas.menu_tbl (
	id int8 NULL,
	modulename text NULL,
	menuname text NULL,
	parent_id float8 NULL,
	url text NULL,
	icon text NULL
);

CREATE TABLE mlaas.parent_activity_tbl (
	parent_activity_id int8 NULL,
	parent_activity_name text NULL,
	tab_id int8 NULL
);

CREATE TABLE mlaas.player_profile_tbl (
	profile_id bigserial NOT NULL,
	player_name text NULL,
	type text NULL,
	category text NULL,
	player_role text NULL,
	dob timestamptz NULL,
	team_name text NULL,
	founded_since text NULL,
	profile_pict_path text NULL,
	user_name text NULL,
    created_on timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE mlaas.user_auth_tbl (
	uid int8 NULL,
	user_name text NULL,
	"password" text NULL
);


--Create activity_deatil table
CREATE TABLE mlaas.activity_detail_tbl (
    "index" bigserial NOT NULL,
    activity_id text NULL,
    user_name text NULL,
    profile_id int8 NULL,
    video_id int8 NULL,
    activity_description text NULL,
    start_time timestamp NOT NULL DEFAULT now(),
    end_time timestamp NULL,
    column_id text NULL,
    "parameter" text NULL,
	created_on timestamptz NOT NULL DEFAULT now()
);

--Create subscription table
CREATE TABLE mlaas.subscription_plan_tbl (
    sub_id bigserial NOT NULL,
    menu_id int8 NULL,
    plan_name text NULL,
    plan_desc text NULL,
    plan_type text NULL,
	user_name text NULL,
    created_on timestamptz NOT NULL DEFAULT now()
);


--Create video master table
CREATE TABLE mlaas.video_master_tbl (
    video_id bigserial NOT NULL,
    video_name text NULL,
    file_name text NULL,
    file_size int8 NULL,
    file_path text NULL,
	file_visibility text NULL,
    file_description text NULL,
	user_name text NULL,
    created_on timestamptz NOT NULL DEFAULT now()
);

--Create video master table
CREATE TABLE mlaas.video_reaction_tbl (
    video_id int8 NOT NULL,
    likes int8 NULL,
    unlikes int8 NULL,
    victory int8 NULL,
    frustration int8 NULL,
    anger int8 NULL,
	comment text NULL,
    user_name text NULL,
    created_on timestamptz NOT NULL DEFAULT now()
);
--Create video master table
CREATE TABLE mlaas.player_history_tbl (
    profile_id int8 NOT NULL,
    weight text NULL,
    height text NULL,
    activity_start_year text NULL,
non_registered text NULL,
city text NULL,
country text NULL,
team_level int8 NULL,
current_season text NULL,
team_ranking int8 NULL,
team_points int8 NULL,
win_count int8 NULL,
loss_count int8 NULL,
draw_count int8 NULL,
coach  text NULL,
role text NULL,
manager  text NULL,
games_played int8 NULL,
games_started int8 NULL,
minutes_played int8 NULL,
game_winning_goal_count  int8 NULL,
game_winning_assist int8 NULL,
goal_count  int8 NULL,
assists_count int8 NULL,
shots_count int8 NULL,
shots_on_goal int8 NULL,
penalty_kick_goals int8 NULL,
penalty_kick_attempts int8 NULL,
blocked_shots_count int8 NULL,
steal_count int8 NULL,
red_card_count  int8 NULL,
yellow_card_count  int8 NULL,
saves_count int8 NULL,
catches_and_punches_count int8 NULL,
goals_allowed  int8 NULL,
saved_penalty int8 NULL,
user_name text NULL,
created_on timestamptz NOT NULL DEFAULT now()
);

--Insert menu_tbl
Insert into  mlaas.menu_tbl values (2,'Admin','Videos Master',null,null,' mdi-database-import');
Insert into  mlaas.menu_tbl values (2,'User','Profile',null,null,' mdi-database-import');
Insert into  mlaas.menu_tbl values (3,'User','Plan',null,null,null);
Insert into  mlaas.menu_tbl values (4,'User','Explore',null,null,null);
Insert into  mlaas.menu_tbl values (5,'User','Highlights',null,null,'mdi-database-sync');
Insert into  mlaas.menu_tbl values (6,'User','Chat',null,null,null);
Insert into  mlaas.menu_tbl values (7,'User','Stats',null,null,null);
Insert into  mlaas.menu_tbl values (8,'Product','Product',null,null,null);
Insert into  mlaas.menu_tbl values (8,'Product','About us',null,null,null);
Insert into  mlaas.menu_tbl values (8,'Product','Privacy Policy',null,null,null);

--Insert user_auth_tbl
Insert into mlaas.user_auth_tbl values(1,'mehul','mehul');
Insert into mlaas.user_auth_tbl values(2,'adarsh','adarsh');
Insert into mlaas.user_auth_tbl values(3,'vishal','vishal');
Insert into mlaas.user_auth_tbl values(4,'jay','jay');
Insert into mlaas.user_auth_tbl values(5,'chirag','chirag');
Insert into mlaas.user_auth_tbl values(6,'shivangi','shivangi');



--Insert parent_activity_tbl
Insert into mlaas.parent_activity_tbl values(1,'Admin',1);
Insert into mlaas.parent_activity_tbl values(2,'Sign Up',2);
Insert into mlaas.parent_activity_tbl values(3,'Video Reaction',3);
Insert into mlaas.parent_activity_tbl values(4,'User Profile',4);
Insert into mlaas.parent_activity_tbl values(5,'Chat',2);
Insert into mlaas.parent_activity_tbl values(6,'Subscription Plan',2);
Insert into mlaas.parent_activity_tbl values(7,'Player Stats',2);
Insert into mlaas.parent_activity_tbl values(8,'Explore Search',2);
Insert into mlaas.parent_activity_tbl values(9,'Static Page',1);




--Insert activity master
-- COLUMNS => "index", activity_id, activity_name, activity_description, "language", operation, code, parent_activity_id, user_input, check_typ
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_2','Delete Video','You have deleted Video','US','Delete',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_3','Create Sport Category','You have Sport Category','US','Create',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_1','Add Video','You have created Video','US','Create',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_4','Delete Sport Category','You have deleted Sport Category','US','Delete',0,-1,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'ur_5','User Profile','User Profile','US','Update',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ur_6','Forgot Password','Forgot Password','US','Select',0,-1,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_7','Like','Video reaction Like','US','Ignore',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_8','Un Like','Video reaction un like','US','Started',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_9','Victory','Video reaction victory','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_10','Frustraction','Video reaction frustration','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_11','Anger','Video reaction anger','US','Ended',0,-1,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_12','Trial','Subscription Plan Trial','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_13','Explore','Subscription Plan Explore','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_14','Advance','Subscription Plan Advance','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_15','Premium','Subscription Plan Premium','US','Ended',0,-1,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'ps_16','Player Stats','Player Statistics','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ep_17','Explore','Search and Explore','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ab_18','About','About','US','Ended',0,-1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ab_19','Term and Condition','Term and Condition','US','Ended',0,-1,0,0);
