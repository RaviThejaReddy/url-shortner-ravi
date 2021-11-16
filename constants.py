make_short_url = """INSERT INTO public.short_url
(created, original_url, shorturl, total_hits)
VALUES (CURRENT_TIMESTAMP, %s, %s, 0);
"""

check_if_log_url_is_already_present = """
select 
    distinct shorturl, 
    count(shorturl) 
from 
    public.short_url 
where 
    original_url=%s 
group by 
    shorturl 
"""
get_long_url = """
select 
    original_url,
    total_hits
from 
    public.short_url 
where 
    shorturl=%s
"""
search_long_url = """
select 
    distinct original_url
from 
    public.short_url 
where 
  	original_url like %s
"""
update_total_hits = """
UPDATE public.short_url 
SET total_hits = %s
WHERE shorturl=%s"""
update_current_hit = """
UPDATE public.short_url_hit_data 
SET total_hits = %s
WHERE shorturl=%s"""
insert_into_hit_time_data = """
INSERT INTO public.short_url_hit_data
(shorturl, hit_time_stamp)
VALUES(%s, CURRENT_TIMESTAMP);
"""
get_total_hits_in_last_hour = """
select 
    count(*) 
from 
    public.short_url_hit_data 
where
    shorturl=%s and
    hit_time_stamp between current_timestamp - INTERVAL '1 HOUR' and current_timestamp 
"""