from ..base import BaseAPI

class SendAll(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = 'https://api.weixin.qq.com/cgi-bin/message'

    def send(self, data):
        # https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Batch_Sends_and_Originality_Checks.html
        publish_url = self.base_url + '/mass/sendall?access_token=' + self.access_token
        return self.post(url=publish_url, data=data)
