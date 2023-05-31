def mobileBrowser (request):
    mobile_browser = False
    is_mob=request.user_agent.is_mobile # returns False
    is_tab=request.user_agent.is_tablet # returns False
    is_pc=request.user_agent.is_pc # returns True
    if(is_mob == True):
        mobile_browser = True
    else:
        mobile_browser = False
    return mobile_browser