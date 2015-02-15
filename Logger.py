import logging


class Logger(object):

    @property
    def logger(self):
        try:
            name = '.'.join([__name__, self.__class__.__name__, self.name])
        except AttributeError:
            name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)
