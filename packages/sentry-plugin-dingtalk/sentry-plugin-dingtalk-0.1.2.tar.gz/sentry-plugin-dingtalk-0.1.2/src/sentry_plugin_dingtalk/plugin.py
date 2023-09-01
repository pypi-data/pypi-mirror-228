# coding: utf-8

import re
import json
import requests

from sentry.plugins.bases.notify import NotificationPlugin
from sentry_plugin_dingtalk import VERSION
from .forms import OptionsForm
from .template import parseConfig

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class dingtalkPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to dingtalk.
    """

    author = "ding"
    version = VERSION
    description = "DingTalk integrations for sentry."
    slug = "DingTalk-EX"
    title = "DingTalk-EX"
    conf_key = slug
    conf_title = title
    project_conf_form = OptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option("options", project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def get_tag_data(self, group, event):
        """
        获取基础数据，用于标签渲染
        """
        data = {
            "projectName": event.project.slug,
            "projectId": "{}".format(event.project_id or "--"),
            "eventId": event.event_id,
            "issuesUrl": group.get_absolute_url(event_id=event.event_id),
            "title": event.title,
            "message": event.message or event.title,
            "platform": event.platform,
            "datetime": event.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "release": event.release or "--",
            "url": event.get_tag("url") or "--",
            "environment": event.get_tag("environment") or "--",
        }
        return data

    def render_tag(self, event, tagData, temp):
        """
        渲染模板
        """

        def replaceTag(pattern):
            op = pattern.group("op")
            tag = pattern.group("tag")
            if op == "@":
                return event.get_tag(tag) or "--"
            return tagData.get(tag, "--")

        return re.sub(r"\{(?P<op>[@#])?(?P<tag>[^}]+)\}", replaceTag, temp)

    def parse_config(self, group):
        """
        解析配置和模板
        """
        options = self.get_option("options", group.project)
        markdowns = self.get_option("markdowns", group.project)
        return parseConfig(options, markdowns)

    def check_condition(self, tag, op, value):
        """
        条件判定
        """
        if op == "=" or op == "==":
            return tag == value
        if op == "!=":
            return tag != value
        if op == "in":
            return value in tag
        if op == "not in":
            return value in tag
        if op == "reg" and re.search(value, tag):
            return True
        if op == "not reg" and not re.search(value, tag):
            return True
        return False

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """

        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        tagData = self.get_tag_data(group, event)
        configList = self.parse_config(group)

        try:
            # 调试功能
            debugUrl = configList[0].get("debug")
            if debugUrl and re.search(r"https?:", debugUrl):
                data = {
                    "type": "debug",
                    "environment": tagData.get("environment", "-"),
                    "title": tagData.get("title", "-"),
                    "url": tagData.get("url", "-"),
                    "datetime": tagData.get("datetime", "-"),
                }
                requests.post(
                    url=debugUrl,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(data).encode("utf-8"),
                )
        except Exception:
            pass

        # 遍历配置列表，满足条件发生消息
        for item in configList:
            # 优先取 url 字段，然后才取 token 拼接
            url = item.get("url") or DingTalk_API.format(token=item.get("token"))
            title = item.get("title", "")
            markdown = item.get("markdown", "")
            # 条件字段处理
            condition = item.get("condition")
            tag = condition.get("tag")
            op = condition.get("op")
            value = condition.get("value")
            # 条件成立就发送消息
            if self.check_condition(self.render_tag(event, tagData, tag), op, value):
                # 标题字段渲染变量，如果为空就取 event.title 字段
                title = (
                    self.render_tag(event, tagData, title)
                    if title
                    else tagData.get("title", "--")
                )
                # 渲染模板内容
                text = self.render_tag(event, tagData, markdown)
                try:
                    requests.post(
                        url=url,
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(
                            {
                                "msgtype": "markdown",
                                "markdown": {"title": title, "text": text},
                                "at": {
                                    "atMobiles": [],
                                    "atUserIds": [],
                                    "isAtAll": False,
                                },
                            }
                        ).encode("utf-8"),
                    )
                except Exception:
                    pass
