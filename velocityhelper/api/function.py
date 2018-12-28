
class Function(object):
    ISOPACH = 'isopach'
    ISOCHRON = 'isochron'
    ISOCHRONOWTSEC = 'isochronOWTsec'
    VINT = 'vint'
    MISSING = 'missing'

    def __init__(self):
        self.index = 0
        self.row = 0
        self.top = ""
        self.base = ""
        #well tops to check against for missing
        self.markersList = []