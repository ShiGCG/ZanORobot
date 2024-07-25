from pathlib import Path
import requests
import time

# 定义API的URL地址
urls = {
    "list": "http://c.zanao.com/sc-api/thread/v2/list",  # 获取列表的API地址
    "comment": "https://c.zanao.com/sc-api/comment/post",  # 发送评论的API地址
    'msg': 'http://c.zanao.com/sc-api/msg/list',  # 消息列表
    "cnt": "http://c.zanao.com/sc-api/msg/unum",  # 新回复的个数
    "read": "http://c.zanao.com/sc-api/msg/oneread",  # 读消息
    "comment_list": "http://c.zanao.com//sc-api/comment/list",  # 某个评论的评论链

}

# 存储用户认证信息的cookies
cookies = {
    'user_token': '...',
    'Hm_lvt_...': '...',
    'HMACCOUNT': '...',
    'Hm_lpvt_...': '{}'.format(time.time()),
    'SERVERID': '...'

}


s = requests.session()
s.keep_alive = False
s.proxies = {"https": "47.100.104.247:8080",
             "http": "36.248.10.47:8080", }  # 代理随便找的一个


def get_headers():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Host': 'c.zanao.com',
        "X-Sc-Platform": 'android',
        'X-Sc-Alias': 'xxx',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090b13) XWEB/9185 Flue'
    }
    return headers


def one_read(msg_id: int):
    url = urls['read']
    headers = get_headers()
    params = {
        'msg_id': msg_id,
        'isIOS': 'false'
    }
    res = requests.get(url=url, headers=headers,
                       params=params, cookies=cookies, verify=False)
    return res


def get_cnt_new_msg():
    url = urls["cnt"]
    headers = get_headers()
    params = {
        'isIOS': "false"
    }
    res = requests.get(cookies=cookies, url=url,
                       headers=headers, params=params, verify=False)
    return res.json()['data']['count']


def get_all_new_msg():
    url = urls['msg']
    headers = get_headers()
    params = {
        'isIOS': "false",
        'from_time': '0'
    }
    res = requests.get(cookies=cookies, url=url,
                       headers=headers, params=params, verify=False)
    all_msg = res.json()["data"]["list"]
    return all_msg


def post_reply(content, id, reply_comment_id, root_comment_id):
    '''
    回复指定的消息
    '''
    # id: thread_id
    # reply_comment_id: from_comment_info.comment_id
    # root_comment_id: from_comment_info.root_comment_id
    url = urls["comment"]
    headers = get_headers()
    data = {
        "id": id,
        "content": content,
        "reply_comment_id": reply_comment_id,
        "root_comment_id": root_comment_id,
        "cert_show": "0",
        "isIOS": "false"
    }
    print(data)
    response = requests.post(url, headers=headers,
                             data=data, cookies=cookies, verify=False, allow_redirects=False)
    return response


def get_comment_list(rcid, id=0, vuid=0):
    if id == 0:
        raise Exception(f'你必须指定id（帖子id）')
    # id: thread_id #帖子的id
    # rcid：comment_id/from_comment_info.comment_id
    url = urls['comment_list']
    headers = get_headers()
    params = {
        'id': id,
        'rcid': rcid,
        'vuid': vuid,
        'sign': "",  # 可以为空
        'url': "",  # 可以为空
        'isIOS': "false"
    }
    response = requests.get(url, headers=headers, params=params,
                            cookies=cookies, verify=False, allow_redirects=False)
    return response


def get_comment_list_str(rcid):
    '''
    调用评论链解析函数并解析成指定格式的字符串
    '''
    res = get_comment_list(rcid=rcid)
    all_msg = res.json()["data"]["list"]
    result_strings = []
    for comment in all_msg:
        # 打印主评论
        result_strings.append(f"{comment['nickname']} 评论了自己：
                              {comment['content']}，评论内容：{comment['content']}")

        # 如果有回复
        if 'reply_list' in comment:
            for reply in comment['reply_list']:
                # 打印回复
                result_strings.append(f"{reply['nickname']} 回复了 {reply['reply_nickname']} 的评论：
                                      {comment['content']}，回复内容：{reply['content']}")
    return "\n".join(result_strings)


if __name__ == '__main__':
    pass
