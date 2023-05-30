from User.models import Config

# liff id = line_login.html,line-duplicate.html
# liff endpoint
# Webhook URL in Line Messaging API
# line url = register_done.html 

def line_config_info():
    config = Config.objects.all()
    if config.exists():
        line_data = {   
                        "channel_access_token":config[0].line_channel_access_token,
                        "user_id" : config[0].line_user_id,
                        "liff_id": config[0].line_liff_id,
                        "url_website": config[0].url_website,
                        "line_url": config[0].line_url,
                        "is_rtaf_authen": config[0].is_rtaf_authen
                    }
    else:
        line_data = {   
                        "channel_access_token":"",
                        "user_id" : "",
                        "liff_id": "",
                        "url_website": "",
                        "line_url": "",
                        "is_rtaf_authen": ""
                    }

    return line_data