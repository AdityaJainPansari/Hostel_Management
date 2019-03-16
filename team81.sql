drop table if exists authenticate ;
drop table if exists admins ;
drop table if exists students ;
drop table if exists hostels ;
drop table if exists residents ;
drop table if exists dues ;
drop table if exists posts ;
drop table if exists comments ;
drop table if exists likes ;
drop table if exists dislikes ;
drop table if exists FAQs ;

create table authenticate (
username text primary key not null,
password text not null,
profile_pic boolean default 0
);

create table admins (
username text primary key not null UNIQUE,
phone char[10] not null,
of_what char[20] not null,
value char[20],
FOREIGN KEY (username) REFERENCES authenticate(username)
);

create table students (
username text primary key not null,
roll_no char[8] not null UNIQUE,
firstname varchar[50] not null,
lastname varchar[50] ,
phone char[10] not null ,
gaurdian varchar[80] not null,
gaurdian_phone char[10] not null,
batch char[4] not null,
FOREIGN KEY (username) REFERENCES authenticate(username)
);

create table hostels (
id integer primary key autoincrement,
name text not null UNIQUE,
phone char[11] not null,
warden text not null,
phone_warden char[10] not null,
ratings integer not null,
FOREIGN KEY (warden) REFERENCES authenticate(username)
);

create table residents (
username text primary key not null,
room_no varchar[5] not null,
roommates_roll_no char[8] UNIQUE,
hostel varchar[20] not null,
wing char[5] not null ,
CHECK (LENGTH(room_no)=3),
FOREIGN KEY (username) REFERENCES authenticate(username),
FOREIGN KEY (roommates_roll_no) REFERENCES students(roll_no),
FOREIGN KEY (hostel) REFERENCES hostels(name)
);

create table dues (
id integer primary key autoincrement,
username text not null,
description text not null,
hostel varchar[20] not null,
amount integer not null,
due_adding_date date not null,
paid boolean not null default 0,
FOREIGN KEY (username) REFERENCES authenticate(username),
FOREIGN KEY (hostel) REFERENCES hostels(name)
);

create table FAQs(
id integer primary key autoincrement,
question text not null,
answer text
);

create table posts (
post_id integer primary key autoincrement,
username text not null,
title varchar[50] not null,
description text not null,
groups varchar[20] not null,
post_date date not null,
likes integer default 0,
dislikes integer default 0,
FOREIGN KEY (username) REFERENCES authenticate(username)
);

create table likes (
post_id integer,
username text not null,
FOREIGN KEY (username) REFERENCES authenticate(username)
);

create table dislikes (
post_id integer,
username text not null,
FOREIGN KEY (username) REFERENCES authenticate(username)
);

create table comments (
id integer primary key autoincrement,
username text not null,
comment text not null,
post_id integer not null,
comment_date date not null,
FOREIGN KEY (username) REFERENCES authenticate(username),
FOREIGN KEY (post_id) REFERENCES posts(post_id)
);
