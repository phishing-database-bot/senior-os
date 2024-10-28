from dataclasses import dataclass, field
from typing import List


@dataclass
class SwebConfiguration:
    urlsForWebsites: List[str] = field(default_factory=lambda: ["https://irozhlas.cz/",
                                                                "https://edition.cnn.com/",
                                                                "https://www.vut.cz/",
                                                                "https://google.com/",
                                                                "https://www.aktualne.cz/",
                                                                "https://www.denik.cz/"])
    
    picturePaths: List[str] = field(default_factory=lambda: ["../sconf/images/SWEB-EXIT.png",
                                                             "../sconf/images/SWEB-WWW1.png",
                                                            "../sconf/images/SWEB-WWW2.png",
                                                            "../sconf/images/SWEB-WWW3.png",
                                                            "../sconf/images/SWEB-WWW4.jpg",
                                                            "../sconf/images/SWEB-WWW5.png",
                                                            "../sconf/images/SWEB-WWW6.png"])
    sendPhishingWarning: bool = True
    phishingFormular: bool = True
    seniorWebsitePosting: bool = True
    allowedWebsites: List[str] = field(default_factory=lambda: ["https://seznam.cz",
                                                                "https://google.com",
                                                                "https://vut.cz"])
