import os
from urllib.parse import urlparse

from wordpress_xmlrpc import Client
import markdown

from utils import (
    get_posts,
    post_link_id_list_2_link_id_dic,
    get_md_sha1_dic,
    get_sha1,
    get_md_list,
    read_md,
    href_info,
    new_post,
    edit_post,
    delete_post,
    rebuild_md_sha1_dic,
    update_index_info_in_readme
)
# from wordpress_xmlrpc import Client, WordPressPost
# from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost, DeletePost
# from urllib.parse import urlparse
# import frontmatter
# import time
# import os
# from hashlib import sha1
# import json
# import markdown
# import re

# config_file_txt = ""

# if((os.path.exists(os.path.join(os.getcwd(), "diy_config.txt")) == True)):
#     config_file_txt = os.path.join(os.getcwd(), "diy_config.txt")
# else:
#     config_file_txt = os.path.join(os.getcwd(), "config.txt")

# config_info = {}


# with open (config_file_txt, 'rb') as f:
#     config_info = json.loads(f.read())


# username = config_info["USERNAME"]
# password = config_info["PASSWORD"]
# xmlrpc_php = config_info["XMLRPC_PHP"]

def main():
    # 1. 获取网站数据库中已有的文章列表
    post_link_id_list = get_posts()
    print(post_link_id_list)
    link_id_dic = post_link_id_list_2_link_id_dic(post_link_id_list)
    link_id_dic = {key.split('/')[-2]: value for (key,value) in link_id_dic.items()}
    print(link_id_dic)
    # wp_links = [link.split('/')[-1] for link in link_id_dic.keys()]

    # 2. 获取md_sha1_dic
    # 查看目录下是否存在md_sha1.txt,如果存在则读取内容；
    # 如果不存在则创建md_sha1.txt,内容初始化为{}，并读取其中的内容；
    # 将读取的字典内容变量名，设置为 md_sha1_dic
    md_sha1_dic = get_md_sha1_dic(os.path.join(os.getcwd(), ".md_sha1"))

    # 3. 开始同步
    # 读取_posts目录中的md文件列表
    md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))

    for md in md_list:
        # 计算md文件的sha1值，并与md_sha1_dic做对比
        sha1_key =  os.path.basename(md)
        sha1_value = get_sha1(md)
        # 如果sha1与md_sha1_dic中记录的相同，则打印：XX文件无需同步;
        if((sha1_key in md_sha1_dic.keys()) and (sha1_value == md_sha1_dic[sha1_key])):
            print(md+"无需同步")
        # 如果sha1与md_sha1_dic中记录的不同，则开始同步
        else:
            # 读取md文件信息
            (content, metadata) = read_md(md)
            # 获取title
            title = metadata.get("title", "")
            terms_names_post_tag = metadata.get("tags",  domain_name)
            terms_names_category = metadata.get("categories", domain_name)
            post_status = "publish"
            link = sha1_key.split(".")[0]
            content = markdown.markdown(content + href_info("https://"+domain_name+"/p/"+link+"/"), extensions=['tables', 'fenced_code'])
            # 如果文章id不存在,则直接新建
            if link not in link_id_dic.keys():
                print(f'Creating new post {md}')
                new_post(title, content, link, post_status, terms_names_post_tag, terms_names_category)
            # 如果文章有id, 则更新文章
            else:
                # 获取id
                print(f'Updating existing post {md}')
                id = link_id_dic[link]
                edit_post(id, title, content, link, post_status, terms_names_post_tag, terms_names_category)

    # 如果_posts中的markdown被删除，则删除对应的post
    for md in md_sha1_dic.keys():
        if md == 'update_time':
            continue
        md_list_basename = [os.path.basename(md) for md in md_list]
        if md not in md_list_basename:
            print(f'Deleting post {md}')
            link = md.split(".")[0]
            id = link_id_dic[link]
            delete_post(id)

    # 4. 重建md_sha1_dic
    rebuild_md_sha1_dic(os.path.join(os.getcwd(), ".md_sha1"), os.path.join(os.getcwd(), "_posts"))

    # 5. 将链接信息写入insert_index_info_in_readme
    update_index_info_in_readme()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
xmlrpc_php = os.getenv('XMLRPC_PHP')
enable_deletion = os.getenv('ENABLE_DELETION')

# try:
#     if(os.environ["USERNAME"]):
#         username = os.environ["USERNAME"]

#     if(os.environ["PASSWORD"]):
#         password = os.environ["PASSWORD"]

#     if(os.environ["XMLRPC_PHP"]):
#         xmlrpc_php = os.environ["XMLRPC_PHP"]
# except:
#     print("无法获取github的secrets配置信息,开始使用本地变量")


url_info = urlparse(xmlrpc_php)

global domain_name
domain_name = url_info.netloc

global wp
wp = Client(xmlrpc_php, username, password)

if __name__=='__main__':
    main()