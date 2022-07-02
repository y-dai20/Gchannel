def is_same_user(request_user, true_user):
    if request_user == true_user:
        return True
    
    return False

def get_reply_type_id(type):
    reply_type_id = ["つぶやき", "根拠", "確認", "要求", "現状", "その他"]
    if not type in reply_type_id:
        return -1
        
    return str(reply_type_id.index(type))