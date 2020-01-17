from catscore.http.request import CatsRequest
from catscore.lib.logger import CatsLogging as logging

class DetailSite:
    def __init__(self, request: CatsRequest, url):
        """[summary]

        Arguments:
            request {CatsRequest} -- [description]
            url {[type]} -- [description]
        """
        self.url = url
        self.soup = request.get(url=url, response_content_type="html").content

    @property
    def pr_comment(self):
        pr_comment_wrap = self.soup.find("div", {"class": "pr-comment-wrap"})
        if pr_comment_wrap != None:
            pr_comment_title = pr_comment_wrap.find("h3", {"class": "pr-comment-title"}).text
            pr_comment_first = pr_comment_wrap.find("span", {"class": "pr-comment__first"}).text
        else:
            logging.error(f"{self.url} comment_wrap is None")
            pr_comment_title = ""
            pr_comment_first = ""
        return {"pr_comment_title": pr_comment_title, "pr_comment_first": pr_comment_first}
