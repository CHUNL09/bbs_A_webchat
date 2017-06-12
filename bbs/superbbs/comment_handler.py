import datetime
def addnode(comment,tree_dic):
    if comment.parent_comment is None:
        tree_dic[comment]={}
    else:
        for k,v in tree_dic.items():
            if k==comment.parent_comment:
                tree_dic[k][comment]={}
            else:
                addnode(comment,v)

def comment_rendering(comment_list,tree_dic,offset):
    offset+=5
    for k,v in tree_dic.items():
        # print('----k----',k.id,k.parent_comment or -1)
        # print('----v----',v)
        if k.parent_comment is None:
            comment_line="<div class='comment_node root_comment' sid='%s' pid='-1' style='margin-left:0px'>"%(k.id)+"<span style='color: #5bc0de;'>"+\
                         k.user.name+"</span><span>"+k.comment+"</span><span>"+k.date.strftime("%Y-%m-%d %H:%M:%S")+"</span>"\
                        "<a href='javascript:void(0)' class='add_comment'><span class='glyphicon glyphicon-comment' aria-hidden='true'>评论</span></a><a href='javascript:void(0)' class='comment_thumb'><span class='glyphicon glyphicon-thumbs-up'aria-hidden='true'>"+str(k.children.count())+"</span></a>" \
                        "<div id='add_area'></div></div>"
        else:
            comment_line="<div class='comment_node' sid='%s' pid='%s' style='margin-left:%spx'>"%(k.id,k.parent_comment.id,offset)+"<span style='color: #5bc0de;'>"+\
                         k.user.name+"</span><span>"+k.comment+"</span><span>"+k.date.strftime("%Y-%m-%d %H:%M:%S")+"</span>"\
                          "<a href='javascript:void(0)' class='add_comment'><span class='glyphicon glyphicon-comment' aria-hidden='true'>评论</span></a><a href='javascript:void(0)' class='comment_thumb'><span class='glyphicon glyphicon-thumbs-up'aria-hidden='true'>"+str(k.children.count())+"</span></a>" \
                          "<div id='add_area'></div></div>"
        # tmp_dic={k.id:comment_line}
        comment_list.append(comment_line)
        if len(v)!=0:
            comment_rendering(comment_list,v,offset)
    return comment_list

def build_tree(comment_set):
    tree_dic={}
    for comment in comment_set:
        addnode(comment,tree_dic)
    comment_list=[]
    res=comment_rendering(comment_list,tree_dic,0)
    return res