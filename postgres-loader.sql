-- postgresql nfbc adp export loader
-- 
-- once you've run the spider, you may load the results into postgresql
-- using this script.

drop table if exists nfbcadp;

create table nfbcadp (
  id serial
  , nfbc_id integer
  , player_url text
  , player_name text
  , team_name text
  , pos text
  , avg_pick numeric
  , min_pick integer
  , max_pick integer
)
;

-- load adp data scraped by crawler
copy nfbcadp (
  nfbc_id
  , player_url
  , player_name
  , team_name
  , pos
  , avg_pick
  , min_pick
  , max_pick
)
from '/path/to/spider/output.csv'
with csv header
;

-- delete duplicate player entries
-- note:
--  data collected in "page count" mode will,
--  somewhat amazingly, include duplicates.
--  here, we rely on the natural order
--  (yeah, i know) for the correct values -
--  in testing, this was (also somewhat amazingly)
--  the only reliable method.
delete from nfbcadp
where
  id in (
    select
      id
    from (
      select
        id
        , nfbc_id
        , row_number() over (partition by player_url) as rn
        , player_url
      from
        nfbcadp
      order by
        nfbc_id
    ) dupes
  where
    dupes.rn > 1
)
;
