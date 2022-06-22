import time
import os
import json
from hashlib import sha1
import re

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost, DeletePost
import frontmatter

# 获取已发布文章id列表
def get_posts():
    print(time.strftime('%Y-%m-%d-%H-%M-%S')+"开始从服务器获取文章列表...")
    posts = wp.call(GetPosts({'post_type': 'post', 'number': 1000000000}))
    post_link_id_list = []
    for post in posts:
        post_link_id_list.append({
            "id": post.id,
            "link": post.link
        })
    print(post_link_id_list)
    print(len(post_link_id_list))
    return post_link_id_list

# 创建post对象
def create_post_obj(title, content, link, post_status, terms_names_post_tag, terms_names_category):
    post_obj = WordPressPost()
    post_obj.title = title
    post_obj.content = content
    post_obj.link = link
    post_obj.post_status = post_status
    post_obj.comment_status = "open"
    print(post_obj.link)
    post_obj.terms_names = {
        #文章所属标签，没有则自动创建
        'post_tag': terms_names_post_tag,
         #文章所属分类，没有则自动创建
        'category': terms_names_category
    }

    return post_obj



# 新建文章
def new_post(title, content, link, post_status, terms_names_post_tag, terms_names_category):

    post_obj = create_post_obj(
        title = link, 
        content = content, 
        link = link, 
        post_status = post_status, 
        terms_names_post_tag = terms_names_post_tag, 
        terms_names_category = terms_names_category)
    # 先获取id
    id = wp.call(NewPost(post_obj))
    # 再通过EditPost更新信息
    edit_post(id, title, 
        content, 
        link, 
        post_status, 
        terms_names_post_tag, 
        terms_names_category)


# 更新文章
def edit_post(id, title, content, link, post_status, terms_names_post_tag, terms_names_category):
    post_obj = create_post_obj(
        title, 
        content, 
        link, 
        post_status, 
        terms_names_post_tag, 
        terms_names_category)
    res = wp.call(EditPost(id, post_obj))
    print(res)

# 删除文章
def delete_post(id):
    res = wp.call(DeletePost(id))
    print(res)

# 获取markdown文件中的内容
def read_md(file_path):
    content = ""
    metadata = {}
    with open(file_path) as f:
        post = frontmatter.load(f)
        content = post.content
        metadata = post.metadata
        print("==>>", post.content)
        print("===>>", post.metadata)
    return (content, metadata)

# 获取特定目录的markdown文件列表
def get_md_list(dir_path):
    md_list = []
    dirs = os.listdir(dir_path)
    for i in dirs:
        if os.path.splitext(i)[1] == ".md":   
            md_list.append(os.path.join(dir_path, i))
    print(md_list)
    return md_list

# 计算sha1
def get_sha1(filename):
    sha1_obj = sha1()
    with open(filename, 'rb') as f:
        sha1_obj.update(f.read())
    result = sha1_obj.hexdigest()
    print(result)
    return result

# 将字典写入文件
def write_dic_info_to_file(dic_info, file):
    dic_info_str = json.dumps(dic_info)   
    file = open(file, 'w')  
    file.write(dic_info_str)  
    file.close()
    return True

# 将文件读取为字典格式
def read_dic_from_file(file):
    file_byte = open(file, 'r') 
    file_info = file_byte.read()
    dic = json.loads(file_info)   
    file_byte.close()
    return dic 

# 获取md_sha1_dic

def get_md_sha1_dic(file):
    result = {}
    if(os.path.exists(file) == True):
        result = read_dic_from_file(file)
    else:
        write_dic_info_to_file({}, file)
    return result

# 重建md_sha1_dic,将结果写入.md_sha1
def rebuild_md_sha1_dic(file, md_dir):
    md_sha1_dic = {}

    md_list = get_md_list(md_dir)

    for md in md_list:
        key = os.path.basename(md)
        value = get_sha1(md)
        md_sha1_dic[key] = value

    md_sha1_dic["update_time"] =  time.strftime('%Y-%m-%d-%H-%M-%S')
    write_dic_info_to_file(md_sha1_dic, file)

def post_link_id_list_2_link_id_dic(post_link_id_list):
    link_id_dic = {}
    for post in post_link_id_list:
        link_id_dic[post["link"]] = post["id"]
    return link_id_dic


def href_info(link):
    return "<br/><br/><br/>\n\n\n\n## 本文永久更新地址: \n[" + link + "](" + link + ")"

# 在README.md中插入信息文章索引信息，更容易获取google的收录
def update_index_info_in_readme():
    # 获取_posts下所有markdown文件
    md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))
    # 生成插入列表
    insert_info = ""
    md_list.sort(reverse=True)
    # 读取md_list中的文件标题
    for md in md_list:
        (content, metadata) = read_md(md)
        title = metadata.get("title", "")
        insert_info = insert_info + "[" + title +"](" + "https://"+domain_name + "/p/" + os.path.basename(md).split(".")[0] +"/" + ")\n\n"
    # 替换 ---start--- 到 ---end--- 之间的内容

    insert_info = "---start---\n## 目录(" + time.strftime('%Y年%m月%d日') + "更新)" +"\n" + insert_info + "---end---"

    # 获取README.md内容
    with open (os.path.join(os.getcwd(), "README.md"), 'r', encoding='utf-8') as f:
        readme_md_content = f.read()

    print(insert_info)

    new_readme_md_content = re.sub(r'---start---(.|\n)*---end---', insert_info, readme_md_content)

    with open (os.path.join(os.getcwd(), "README.md"), 'w', encoding='utf-8') as f:
        f.write(new_readme_md_content)

    print("==new_readme_md_content==>>", new_readme_md_content)

    return True