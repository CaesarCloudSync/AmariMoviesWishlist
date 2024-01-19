class CaesarCreateTables:
    def __init__(self) -> None:
        self.wishlistfields = ("movie","themoviedbid","broadcasttype")

        

    def create(self,caesarcrud):
        caesarcrud.create_table("movieid",self.wishlistfields,
        ("varchar(255) NOT NULL","INT NOT NULL","varchar(255) NOT NULL"),
        "amarimovieswishlist")

