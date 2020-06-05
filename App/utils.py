
"""
# result
{
    "message":'',
    "data":'',
    "code":''
}
"""
def make_result(message=None,data=None,code=200):
    return {
        'message':message,
        'data':data,
        'code':code
    }
    

def allowed_file(filename,allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions