from abc import abstractmethod

class IJsonSerializable:
    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def reset_from_info(self, info):
        pass
