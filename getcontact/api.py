from getcontact.requester import Requester


class GetContactAPI:
    def __init__(self, config, verbose, lock_logger):
        self.requester = Requester(config, verbose, lock_logger)

    def get_information_by_phone(self, phone):
        response = self.requester.get_phone_tags(phone)
        if response:
            result_tags = {"tags": [tag['tag'] for tag in response['result']['tags']]}
        else:
            result_tags = {"tags": []}

        self.requester.update_config()

        return result_tags
