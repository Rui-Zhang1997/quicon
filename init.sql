create database if not exists polydata;

use polydata;

create table if not exists submissions (
    id char(6),
    subreddit varchar(125),
    title varchar(1000),
    author varchar(200),
    upvotes integer,
    downvotes integer,
    timePosted timestamp,
    primary key (id)
);

create table if not exists comments (
    id char(6),
    subreddit varchar(125),
    parentPost char(6),
    upvotes integer,
    downvotes integer,
    author varchar(200),
    content varchar(15000),
    time timestamp,
    primary key (id),
    foreign key (subreddit) references submissions(id)
);


