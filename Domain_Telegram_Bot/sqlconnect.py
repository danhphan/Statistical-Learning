import datetime
import pymssql


domain_live_conn = pymssql.connect("abc.domain.com.au", "USERNAME", "PASSWORD", "DomainLive")
domain_live_cursor = domain_live_conn.cursor()
def get_listing_views(current_time):
    previous_time = current_time - datetime.timedelta(hours=1)

    last_push = previous_time.strftime("%Y-%m-%d %H:%M:%S")

    domain_live_cursor.execute("""SELECT distinct vw.SaleID, vw.feature_name, CAST(dl.feature_instances as varchar(8000)) as 'feature_instances'
                               FROM domgrpdw.dbo.dq_sale_feature_extraction_master_vw vw WITH (nolock)                              
                               JOIN domgrpdw.dbo.dq_sale_feature_extraction_detail dl WITH (nolock) on dl.SaleID = vw.SaleID and dl.execution_date = vw.execution_date
                               join DomainLive.dbo.Sale_Live sl WITH (nolock) on vw.SaleID = sl.SaleID
                               WHERE sl.Address_State = 'NSW' and vw.is_primary =1 and feature_name in ('beach_view', 'bridge_view',
                               'canal_view', 'cbd_view', 'city_view', 'coastline_view', 'garden_view', 'golf_view', 
                               'harbour_view', 'island_view', 'lake_view', 'mountain_view', 'park_view', 'river_view',
                               'sea_view', 'skyline_view', 'sports_ground_view', 'valley_view', 'waterfront_view') and vw.insert_date > '%s'""" % last_push)

    listing_views = domain_live_cursor.fetchall()
    return listing_views