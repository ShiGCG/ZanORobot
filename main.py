import time
import random
import Logger
import ZanaoSpider
import ZanaoRobot


class MsgData():
    def __init__(self,
                 id,
                 msg_id,
                 content,
                 reply_comment_id,
                 root_comment_id,
                 reply_user_nickname) -> None:

        # id: thread_id
        # msg_id: msg_id
        # content: from_comment_info.content
        # reply_comment_id: from_comment_info.comment_id
        # root_comment_id: from_comment_info.root_comment_id
        # reply_user_nickname: from_user_info.nickname

        self.id = id
        self.msg_id = msg_id
        self.content = content
        self.reply_comment_id = reply_comment_id
        self.root_comment_id = root_comment_id
        self.reply_user_nickname = reply_user_nickname

        if (root_comment_id == "0"):
            self.root_comment_id = reply_comment_id

    def __str__(self):
        return "id:{}\nmsg_id:{}\nnickname{}\ncontent:{}\nreply_comment_id:{}\nroot_comment_id:{}"\
            .format(self.id, self.msg_id, self.reply_comment_id, self.content, self.reply_comment_id, self.root_comment_id)


def get_unread_post() -> list[MsgData]:
    '''
    构建MsgData
    虽然可以用api获取有几条未读消息，但是返回的json数据中没用的信息太多
    '''
    result = []
    list = ZanaoSpider.get_all_new_msg()
    for msg in list:
        if (msg['is_read'] == "0"):
            result.append(MsgData(
                id=msg["thread_id"],
                msg_id=msg['msg_id'],
                content=msg['from_comment_info']['content'],
                reply_comment_id=msg["from_comment_info"]["comment_id"],
                root_comment_id=msg['from_comment_info']['root_comment_id'],
                reply_user_nickname=msg['from_user_info']['nickname'],
            ))
    print("获取到{}条未回复的消息".format(len(result)))
    return result


logger = Logger.Logger("log/log.txt")


while True:
    try:
        unread = get_unread_post()
        for msg in unread:
            print(msg)
            history = ZanaoSpider.get_comment_list_str(
                rcid=msg.reply_comment_id)
            question = (f'这是之前的对话：\n{history}\n这是新的回复:
                        {msg.reply_user_nickname}:{msg.content}\n请你做简短的回复')
            reply = ZanaoRobot.ask(question=question)
            # reply = "测试 {}".format(time.time())
            r = ZanaoSpider.post_reply(
                id=msg.id, content=reply, root_comment_id=msg.root_comment_id, reply_comment_id=msg.reply_comment_id)
            r = ZanaoSpider.one_read(msg.msg_id)#回复完必须调用这个
            time.sleep(random.randint(5, 10))#随机睡几秒
            temp = "问题：{}\n回复: {}".format(msg, reply)
            logger.log(temp)
        time.sleep(random.randint(10, 20))
    except Exception as e:
        logger.log("发生错误...{}".format(e))
        exit(-1)
