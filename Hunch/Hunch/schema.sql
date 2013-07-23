drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  name text not null,
  rating integer not null,
  liked_bool integer not null
);