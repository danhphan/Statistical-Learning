
import logging
import json
import pymssql
import datetime

def get_listing(bot, update, args):
    listing_id = args[0]
    url = "http://domain.com.au/" + listing_id
    bot.send_message(chat_id='@domainausnews', text="http://domain.com.au/" + listing_id)



# Set types of views. Default is 4 - All views
view_type = 4
def send_listing_vews(bot, job):
    listing_dic = {}
    listing_all_dic = {}
    current_time = datetime.datetime.now()
    listing_views = get_listing_views(current_time)

    show_views = "all views"
    if view_type == 1:
        show_views = "city_view"
    elif view_type == 2:
        show_views = "sea_view"
    elif view_type == 3:
        show_views = "lake_view"
    else:
        show_views = "all views"

    for item in listing_views:
        sale_id, views, instance = item

        if str(views) == show_views:
            if sale_id in listing_dic:
                listing_dic[sale_id][0].append(views)
            else:
                listing_dic[sale_id] = [[views], instance]
        else:
            if sale_id in listing_all_dic:
                listing_all_dic[sale_id][0].append(views)
            else:
                listing_all_dic[sale_id] = [[views], instance]

    listing_show_dic = {}
    if show_views == "all views":
        listing_show_dic = listing_all_dic
    else:
        listing_show_dic = listing_dic

    # Set top number of properties
    max_num = 3
    if len(listing_show_dic) < max_num:
        max_num = len(listing_show_dic)

    text_html = '<b>On ' + current_time.strftime('%d %B %Y') + ', from ' + str(int(datetime.datetime.now().strftime('%H')) - 1) + current_time.strftime(':%M') + ' to ' + current_time.strftime('%H:%M') + \
                ", there is top " + str(max_num ) + ' ' + show_views + " properties in Postcode " + str(post_code) + ", including:</b>"
    bot.send_message(chat_id='@domainviews', text=text_html, parse_mode='HTML')

    for sale_id in listing_show_dic:
        views = list(set(listing_show_dic[sale_id][0]))
        instance = json.loads(listing_show_dic[sale_id][1])
        description = "This property has " + ', '.join(list(instance.keys()))

        bot.send_message(chat_id='@domainviews', text="http://domain.com.au/" + str(sale_id) + ' ' + description)
        max_num = max_num - 1
        if max_num == 0:
            return
        print([sale_id, ', '.join(views), ', '.join(list(instance.keys()))])
