CREATE schema mlaas;

create sequence unq_num_seq increment 1;

SELECT setval('unq_num_seq', 1);

CREATE TABLE mlaas.parent_activity_tbl (
	parent_activity_id int8 NULL,
	parent_activity_name text NULL,
	tab_id int8 NULL,
	PRIMARY KEY(parent_activity_id)
);

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
	check_type int8 NULL,
	PRIMARY KEY(activity_id),
	CONSTRAINT fk_parent_activity
      FOREIGN KEY(parent_activity_id) 
	  REFERENCES mlaas.parent_activity_tbl(parent_activity_id)
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
	created_on timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY("index"),
	CONSTRAINT fk_activity
      FOREIGN KEY(activity_id) 
	  REFERENCES mlaas.activity_master_tbl(activity_id)
);

CREATE TABLE mlaas.menu_tbl (
	id int8 NULL,
	modulename text NULL,
	menuname text NULL,
	parent_id float8 NULL,
	url text NULL,
	icon text NULL,
	PRIMARY KEY(id)
);

CREATE TABLE mlaas.user_auth_tbl (
	uid bigserial NOT NULL,
	user_name text NULL,
	"password" text NULL,
	PRIMARY KEY(uid)
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
	uid int8 NOT NULL,
    created_on timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY(profile_id),
	CONSTRAINT fk_player_user
      FOREIGN KEY(uid) 
	  REFERENCES mlaas.user_auth_tbl(uid)
);

--Create subscription table
CREATE TABLE mlaas.subscription_plan_tbl (
    sub_id bigserial NOT NULL,
    menu_id int8 NULL,
    plan_name text NULL,
    plan_desc text NULL,
    plan_type text NULL,
	uid int8 NOT NULL,
    created_on timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY(sub_id),
	CONSTRAINT fk_sub_user
      FOREIGN KEY(uid) 
	  REFERENCES mlaas.user_auth_tbl(uid)
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
	uid int8 NOT NULL,
    created_on timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY(video_id),
	CONSTRAINT fk_vid_user
      FOREIGN KEY(uid) 
	  REFERENCES mlaas.user_auth_tbl(uid)
);

--Create video master table
CREATE TABLE mlaas.video_reaction_tbl (
	vr_id bigserial NOT NULL, 
    video_id int8 NOT NULL,
    likes int8 NULL,
    unlikes int8 NULL,
    victory int8 NULL,
    frustration int8 NULL,
    anger int8 NULL,
	comment text NULL,
    uid int8 NOT NULL,
    created_on timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT fk_video_key
    FOREIGN KEY(video_id) 
	REFERENCES mlaas.video_master_tbl(video_id)
);
--Create video master table
CREATE TABLE mlaas.player_history_tbl (
	ph_id bigserial NOT NULL,
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
uid int8 NOT NULL,
created_on timestamptz NOT NULL DEFAULT now(),
CONSTRAINT fk_ph_user
      FOREIGN KEY(uid) 
	  REFERENCES mlaas.user_auth_tbl(uid)
);

--Insert menu_tbl
Insert into  mlaas.menu_tbl values (1,'Admin','Videos Master',null,null,' mdi-database-import');
Insert into  mlaas.menu_tbl values (2,'User','Profile',null,null,' mdi-database-import');
Insert into  mlaas.menu_tbl values (3,'User','Plan',null,null,null);
Insert into  mlaas.menu_tbl values (4,'User','Explore',null,null,null);
Insert into  mlaas.menu_tbl values (5,'User','Highlights',null,null,'mdi-database-sync');
Insert into  mlaas.menu_tbl values (6,'User','Chat',null,null,null);
Insert into  mlaas.menu_tbl values (7,'User','Stats',null,null,null);
Insert into  mlaas.menu_tbl values (8,'Product','Product',null,null,null);
Insert into  mlaas.menu_tbl values (9,'Product','About us',null,null,null);
Insert into  mlaas.menu_tbl values (10,'Product','Privacy Policy',null,null,null);

--Insert user_auth_tbl
Insert into mlaas.user_auth_tbl values('admin','admin');
Insert into mlaas.user_auth_tbl values('adarsh','adarsh');
Insert into mlaas.user_auth_tbl values('vishal','vishal');
Insert into mlaas.user_auth_tbl values('jay','jay');
Insert into mlaas.user_auth_tbl values('chirag','chirag');
Insert into mlaas.user_auth_tbl values('mehul','mehul');


--Insert parent_activity_tbl
Insert into mlaas.parent_activity_tbl values(1,'Admin',1);
Insert into mlaas.parent_activity_tbl values(2,'User Profile',2);
Insert into mlaas.parent_activity_tbl values(3,'Video Reaction',3);
Insert into mlaas.parent_activity_tbl values(4,'Chat',2);
Insert into mlaas.parent_activity_tbl values(5,'Subscription Plan',2);
Insert into mlaas.parent_activity_tbl values(6,'Explore Search',2);
Insert into mlaas.parent_activity_tbl values(7,'Static Page',1);



--Insert activity master
-- COLUMNS => "index", activity_id, activity_name, activity_description, "language", operation, code, parent_activity_id, user_input, check_typ
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_1','Add Video','You have created Video','US','Create',0,1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_2','Delete Video','You have deleted Video','US','Delete',0,1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_3','Create Sport Category','You have Sport Category','US','Create',0,1,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'in_4','Delete Sport Category','You have deleted Sport Category','US','Delete',0,1,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'ur_5','User Sign Up','User Profile','US','Update',0,2,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ur_6','Forgot Password','Forgot Password','US','Select',0,2,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ur_7','Player History','Player Statistics','US','Ended',0,2,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_8','Like','Video reaction Like','US','Ignore',0,3,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_9','Un Like','Video reaction un like','US','Started',0,3,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_10','Victory','Video reaction victory','US','Ended',0,3,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_11','Frustraction','Video reaction frustration','US','Ended',0,3,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'rc_12','Anger','Video reaction anger','US','Ended',0,3,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_13','Chat','Chat','US','Ended',0,4,0,0);

Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_14','Trial','Subscription Plan Trial','US','Ended',0,5,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_15','Explore','Subscription Plan Explore','US','Ended',0,5,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_16','Advance','Subscription Plan Advance','US','Ended',0,5,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'sp_17','Premium','Subscription Plan Premium','US','Ended',0,5,0,0);


Insert into mlaas.activity_master_tbl values (DEFAULT,'ep_18','Explore','Search and Explore','US','Ended',0,6,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ab_19','About','About','US','Ended',0,7,0,0);
Insert into mlaas.activity_master_tbl values (DEFAULT,'ab_20','Term and Condition','Term and Condition','US','Ended',0,7,0,0);