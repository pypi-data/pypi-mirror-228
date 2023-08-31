class Config():
    def __init__(self, username, pwd, server, db, 
                 echo=True, pool_size=10, max_overflow = 20):
        self._username = username
        self._pwd = pwd
        self._server = server
        self._db = db
        
        self.echo = echo
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        
    @property
    def url(self):
        return f"mssql+pymssql://{self._username}:{self._pwd}@{self._server}/{self._db}"
    