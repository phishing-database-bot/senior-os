# Frameworks from PyQt5 libraries
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QToolBar, QWidget
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QSize, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy
# Library for creating channel for monitoring input keyboard
from PyQt5.QtWebChannel import QWebChannel

from src.utils.url_blocker import URLBlocker
from src.phish.update_phishing import PhishingDatabaseModificationChecker
from src.language.language_translator import Translator
from src.utils.monitor_provider import GetMonitorHeightAndWidth
from src.phish.notification_email import NotificationFillTextToPhishing
from src.browser.browser_core import MyWebEnginePage
# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)

## static size of the button
BUTTON_WIDTH = 244
BUTTON_HEIGHT = 107

# static size of the toolbar
TOOLBAR_WIDTH = 1360
TOOLBAR_HEIGHT = 117


class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self, input_url, _dataProvider, global_dataProvider):
        super(MyBrowser,self).__init__()
        # Set window flags to customize window behavior
        # Remove standard window controls
        # Set window flags to customize window behavior

        self._dataProvider = _dataProvider
        self.global_dataProvider = global_dataProvider
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.main_browser = QWebEngineView()
        # Set cutstom page to open new page in the same browser
        self.my_custom_page = MyWebEnginePage(self.main_browser)
        self.my_custom_page.urlChangedSignal.connect(self.on_url_changed_my_custom_page)
        # Configuration for open in Mobile
        # Value for mobile user agent
        mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        self.my_custom_page.setUserAgent(mobile_user_agent)
        # Add my custom page to browser
        self.main_browser.setPage(self.my_custom_page)
        self.setCentralWidget(self.main_browser)
        # Default page is configured as vut.cz
        # Check if input URL is contained HTTP or HTTPS
        if input_url.startswith("https") or input_url.startswith("http"):
            self.main_browser.setUrl(QUrl(input_url))
        else:
            self.main_browser.setUrl(QUrl("http://" + input_url))
        # Parameter for changging language on application
        self.language_translator = Translator(_dataProvider, global_dataProvider)
        # Parameter for getting monitor heigght ad width
        self.get_monitor_height_and_width = GetMonitorHeightAndWidth()
        # Create notification when connection and input text to phishing page
        self.notification_fill_text = NotificationFillTextToPhishing()
        self.my_custom_page.channel.registerObject("notification_fill_text",self.notification_fill_text)
        # Load URL blocker and logger
        #self.data_in_my_config_data = my_config_data
        #path_to_phishing_database =_dataProvider.phishingDatabase
        #path_to_allowed_website = _dataProvider.allowedURL
        #path_to_phishing_database = my_config_data["phishing_database"]["path"]
        self.url_blocker = URLBlocker(_dataProvider.phishingDatabase,_dataProvider.allowedURL)
    
        
        # Check if phishing database is up to date
        phishing_database_check_update = PhishingDatabaseModificationChecker(_dataProvider)
        phishing_database_check_update.check_and_update_if_needed()
        
        # Initialization pygame mixer  for play sounds
        ##pygame.mixer.init()
        # Sound control attribute
   
        # Get height and width from class GetHeightAndWidthInfo
        self.buttons_width_info = BUTTON_WIDTH
        ##self.buttons_width_info = self.get_monitor_height_and_width.get_width_button()

        self.buttons_height_info = BUTTON_HEIGHT
        ##self.buttons_height_info =self.get_monitor_height_and_width.get_height_button()
        
        # Get my parametr from file
        self.color_info_menu = "#e5e5e5"
        self.color_info_app = "#FFFFFF"
        self.color_info_button_unselected = "#797979"
        self.color_info_button_selected = "#00ff00"
        
        # Get path for images
        #self.path_to_image_exit = my_config_data["image"]["sweb_image_exit"]
        #self.path_to_image_exit = _dataProvider.get_sweb_configuration().picturePaths[0]

        #(_dataProvider.get_sweb_configuration().picturePaths[0])

        self.path_to_image_exit = _dataProvider.picturePaths[0]
        self.path_to_image_www1 = _dataProvider.picturePaths[1]
        self.path_to_image_www2 = _dataProvider.picturePaths[2]
        self.path_to_image_www3 = _dataProvider.picturePaths[3]
        self.path_to_image_www4 = _dataProvider.picturePaths[4]
        self.path_to_image_www5 = _dataProvider.picturePaths[5]
        self.path_to_image_www6 = _dataProvider.picturePaths[6]


        # Create a toolbar for saving menu and buttons
        self.menu_1_toolbar = QToolBar("MENU 1")
        self.addToolBar(self.menu_1_toolbar)
        self.menu_1_toolbar.setMovable(False)

        # Load permitted websites from URLBlocker class
        self.permitted_website_list = self.url_blocker.load_permitted_website_from_sconf(_dataProvider.allowedURL)

        # Create a toolbar for saving menu and buttons
        self.menu_2_toolbar = QToolBar("MENU 2")
        self.addToolBar(self.menu_2_toolbar)
        self.menu_2_toolbar.setMovable(False)
        #self.menu_2_toolbar.setFixedSize(1600, 117)

        # Add the buttons to the toolbar
        #self.setup_initial_menu_2()
       

        """
        # Add a spacer to the left of the toolbar
        left_spacer = QWidget()
        left_spacer.setFixedWidth(left_spacer_width)
        self.menu_2_toolbar.addWidget(left_spacer)
        self.addToolBarBreak()
        """
        self.toolbar_space = QToolBar("Spacer")
        # Set the spacer height

        self.addToolBar(self.toolbar_space)
        self.toolbar_space.setMovable(False)
        self.toolbar_space.setVisible(False)
        self.addToolBarBreak()
        
        # Set a style for Menu 1 toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for Menu 2 toolbar
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for URL toolbar
        self.setup_initial_menu_1()
        self.setup_initial_menu_2()

        # Set disvisible for menu 2
        self.menu_2_toolbar.setVisible(False)
        
        # Create toolbar for saving URL
        self.url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(self.url_toolbar)
        self.url_toolbar.setMovable(False)
        
        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        # Change the parameter of URL bar
        self.url_bar.setStyleSheet(f"""
        QToolBar {{
                background-color: {self.color_info_menu};
        }}
        QLineEdit {{
            border: 2px solid black;
            height: {self.buttons_height_info}px;
            font-family: 'Google Sans';
            font-size: {int(self.buttons_height_info/3)}px;
            font-weight: 'Regular';
            background-color: {self.color_info_app};         
        }}        
        """)
        
        # When text of URL is changed, check for URL Phishing
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_toolbar.addWidget(self.url_bar)
        
        # Initially make URL toolbar visible
        # This method is used for Address option -> hide and show url bar
        self.url_toolbar.setVisible(False)
        # Parameter for toggle phishing
        self.toggle_phishing_webpage = False
        # Configure audio and for hovering buttons, menus and options
        # Run this methods for the set Current language in Translator
        self.update_ui_text()
        ##Tarik
        #self.update_ui_audio()
        self.main_browser.urlChanged.connect(self.security_against_phishing)
        # Apply changing text after finishing load
        #self.main_browser.loadFinished.connect(self.finished_load_web_page)
    
    def on_url_changed_my_custom_page(self, url):
        # Load the new URL in the existing browser window
        self.main_browser.setUrl(url)
        
    def setup_initial_menu_1(self):
        """
        Sets up the initial configuration for the first menu, including buttons 
        for various web navigation and a search feature. Configures button 
        properties, layouts, icons, and click events.
        """

        # Calculate the left and right spacers to center the toolbar
        total_screen_width = self.get_monitor_height_and_width.get_width_screen()
        left_spacer_width = (total_screen_width - TOOLBAR_WIDTH) // 2
      

        left_spacer = QWidget()
        left_spacer.setFixedWidth(left_spacer_width)
        self.menu_1_toolbar.addWidget(left_spacer)
        
       
        # Create first Menu
        self.menu1_button = QPushButton(self)
        # Create Menu QvBoxLayout
        menu1_news_layout = QVBoxLayout(self.menu1_button)
        self.menu1_new_text_label = QLabel("MENU 1", self.menu1_button)
        menu1_news_layout.addWidget(self.menu1_new_text_label)
        # Align text in the center
        menu1_news_layout.setAlignment(self.menu1_new_text_label, Qt.AlignCenter)

        # Change to hand when click cursor
        self.menu1_button.setCursor(Qt.PointingHandCursor)
        self.menu1_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_1_toolbar.addWidget(self.menu1_button)

        # Add Exit button
        self.menu1Exit = QPushButton(self)
        # Create Home QvBoxLayout
        menu1Exit_layout = QVBoxLayout(self.menu1Exit)
        # Set Icon for Exit
        menu1Exit_icon = QIcon(self.path_to_image_exit)
        menu1Exit_label = QLabel(self.menu1Exit)
        menu1Exit_label.setPixmap(menu1Exit_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1Exit_layout.addWidget(menu1Exit_label)
        # Align text and icon in the center
        menu1Exit_layout.setAlignment(menu1Exit_label,Qt.AlignCenter)
        self.menu1Exit.clicked.connect(self.close)
        self.menu1Exit.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1Exit)


        '''
        # Add back button
        self.back_btn = QPushButton(self)
        self.back_btn.setFixedSize(360, 210)  # Set size to 360x210
        back_layout = QVBoxLayout(self.back_btn)
        # Set icon for Language
        back_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        back_label = QLabel(self.back_btn)
        back_label.setPixmap(back_icon.pixmap(QSize(int(self.buttons_width_info/(2)),int(self.buttons_height_info/(2)))))
        back_layout.addWidget(back_label)
        # Change to hand when click cursor
        self.back_btn.setCursor(Qt.PointingHandCursor)
        # Align text and icon in the center
        back_layout.setAlignment(back_label,Qt.AlignCenter)
        self.back_btn.clicked.connect(self.main_browser.back)
        self.menu_1_toolbar.addWidget(self.back_btn)
        
         # Add a blank space between two button
        spacer3 = QWidget()
        spacer3.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer3)
        
        '''

        # Add Menu1_WWW1 button
        self.menu1WWW1 = QPushButton(self)
        menu1WWW1_layout = QVBoxLayout(self.menu1WWW1)
        # Icon for Ceska televize
        #menu1WWW1_icon = QIcon(_dataProvider.get_sweb_configuration().picturePaths[1])
        menu1WWW1_icon = QIcon(self.path_to_image_www1)
        menu1WWW1_label = QLabel(self.menu1WWW1)
        menu1WWW1_label.setPixmap(menu1WWW1_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW1_layout.addWidget(menu1WWW1_label)
        # Align icon in the center
        menu1WWW1_layout.setAlignment(menu1WWW1_label,Qt.AlignCenter)
        self.menu1WWW1.clicked.connect(self.navigate_www1)
        self.menu1WWW1.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW1)
        
       
        # Add Menu1_WWW2 button
        self.menu1WWW2 = QPushButton(self)
        menu1WWW2_layout = QVBoxLayout(self.menu1WWW2)
        # Icon for Irozhlas
        menu1WWW2_icon = QIcon(self.path_to_image_www2)
        menu1WWW2_label = QLabel(self.menu1WWW2)
        menu1WWW2_label.setPixmap(menu1WWW2_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW2_layout.addWidget(menu1WWW2_label)
        # Align icon in the center
        menu1WWW2_layout.setAlignment(menu1WWW2_label,Qt.AlignCenter)
        self.menu1WWW2.clicked.connect(self.navigate_www2)
        self.menu1WWW2.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW2)


        # Add Menu1_WWW3 button
        self.menu1_WWW3 = QPushButton(self)
        menu1WWW3_layout = QVBoxLayout(self.menu1_WWW3)
        # Icon for Ceska televize
        menu1WWW3_icon = QIcon(self.path_to_image_www3)
        menu1WWW3_label = QLabel(self.menu1_WWW3)
        menu1WWW3_label.setPixmap(menu1WWW3_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW3_layout.addWidget(menu1WWW3_label)
        # Align icon in the center
        menu1WWW3_layout.setAlignment(menu1WWW3_label,Qt.AlignCenter)
        self.menu1_WWW3.clicked.connect(self.navigate_www3)
        self.menu1_WWW3.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1_WWW3)
        
    

    def setup_initial_menu_2(self):
        """
        Sets up the initial configuration for the second menu, including buttons 
        for various web navigation and a search feature. Configures button 
        properties, layouts, icons, and click events.
        """
        # Calculate the left and right spacers to center the toolbar
        total_screen_width = self.get_monitor_height_and_width.get_width_screen()
        left_spacer_width = (total_screen_width - TOOLBAR_WIDTH) // 2

        left_spacer = QWidget()
        left_spacer.setFixedWidth(left_spacer_width)
        self.menu_2_toolbar.addWidget(left_spacer)
        # Create second Menu2
        self.menu2_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu2_news_layout = QVBoxLayout(self.menu2_button)
        self.menu2_new_text_label = QLabel("MENU 2", self.menu2_button)
        
        menu2_news_layout.addWidget(self.menu2_new_text_label)
        # Set the font color for menu2
 
        # Align text and icon in the center
        menu2_news_layout.setAlignment(self.menu2_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu2_button.setCursor(Qt.PointingHandCursor)
        # Show menu 2 when clicked
        self.menu2_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_2_toolbar.addWidget(self.menu2_button)

        # Add Menu2_WWW4 button
        self.menu2WWW4 = QPushButton(self)
        menu2WWW4_layout = QVBoxLayout(self.menu2WWW4)
        # Icon for idnes
        menu2WWW4_icon = QIcon(self.path_to_image_www4)
        menu2WWW4_label = QLabel(self.menu2WWW4)
        menu2WWW4_label.setPixmap(menu2WWW4_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW4_layout.addWidget(menu2WWW4_label)
        # Align text and icon in the center
        menu2WWW4_layout.setAlignment(menu2WWW4_label,Qt.AlignCenter)
        self.menu2WWW4.clicked.connect(self.navigate_www4)
        self.menu2WWW4.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW4)

        # Add Menu2_WWW5 button
        self.menu2WWW5 = QPushButton(self)
        menu2WWW5_layout = QVBoxLayout(self.menu2WWW5)
        # Icon for aktualne.cz
        menu2WWW5_icon = QIcon(self.path_to_image_www5)
        menu2WWW5_label = QLabel(self.menu2WWW5)
        menu2WWW5_label.setPixmap(menu2WWW5_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW5_layout.addWidget(menu2WWW5_label)
        # Align text and icon in the center
        menu2WWW5_layout.setAlignment(menu2WWW5_label,Qt.AlignCenter)
        self.menu2WWW5.clicked.connect(self.navigate_www5)
        self.menu2WWW5.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW5)
        
        # Add Menu2_WWW6 button
        self.menu2WWW6 = QPushButton(self)
        menu2WWW6_layout = QVBoxLayout(self.menu2WWW6)
        # Icon for denik.cz
        menu2WWW6_icon = QIcon(self.path_to_image_www6)
        menu2WWW6_label = QLabel(self.menu2WWW6)
        menu2WWW6_label.setPixmap(menu2WWW6_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW6_layout.addWidget(menu2WWW6_label)
        # Align text and icon in the center
        menu2WWW6_layout.setAlignment(menu2WWW6_label,Qt.AlignCenter)
        self.menu2WWW6.clicked.connect(self.navigate_www6)
        self.menu2WWW6.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW6)
        
        # Add Menu2_Address button
        self.menu2Address = QPushButton(self)
        # Create Home QvBoxLayout
        menu2Address_layout = QVBoxLayout(self.menu2Address)
        self.menu2_addres_new_text_label = QLabel("Search", self.menu2_button)
        self.menu2_addres_new_text_label.setAlignment(Qt.AlignCenter)
        menu2Address_layout.addWidget(self.menu2_addres_new_text_label)
        # Align text and icon in the center
        menu2Address_layout.setAlignment(self.menu2_addres_new_text_label,Qt.AlignCenter)
        
        self.menu2Address.clicked.connect(self.toggle_url_toolbar)
        self.menu2Address.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2Address)
        
    


    # Set default style for Toolbar
    def default_style_toolbar(self):

        """
        Generates a CSS style string for customizing the appearance of a QToolBar and its child widgets.
        The style string includes:
        - Transparent background and border for QToolBar.
        - White text color for QPushButton and QLabel.
        - Custom styling for QPushButton, including:
        - Rounded corners with a 3px radius.
        - 1px solid border with color #797979.
        - Background color #949494.
        - Margins of 10px on top, bottom, and left, and 12px on the right.
        - Font size of 40px, regular weight, and 'Google Sans' font family.
        - Width of 244px and height of 107px.
        - Hover effect for QPushButton with a background color change to #00ff00.
        - Custom font styling for QPushButton QLabel with a font size of 40px, regular weight, and 'Google Sans' font family.
        Returns:
            str: A CSS style string for the QToolBar and its child widgets.
        """

       ## toolbar_text_config = MenuBarTextConfiguration()
        
        style_string = f"""
            QToolBar {{
            border: 0px solid transparent;
            background-color: transparent;
            spacing: 0px;
            width: {TOOLBAR_WIDTH}px;
            high: {TOOLBAR_HEIGHT}px;
            
            
            
            }}
            QPushButton QLabel {{
                color: #FFFFFF;
            }}
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border-radius: 3px;
                border: 1px solid #797979;
                background-color: #949494 ; 
                margin: 10px 12px 10px 10px;                 
                font-size: 40px;
                font-weight: 'Regular';
                
            
                font-family: 'Google Sans';
                width: 244px;
                height: 107px;
            }}
            
            QPushButton:hover {{
                background-color: #00ff00; 
            }}
            
            QPushButton QLabel {{
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Google Sans';
            }}
        """
        
        return style_string
    
    # Set default style for Toolbar
    def phishing_style_toolbar(self):
        alert_style_string = f"""
            QToolBar {{
            border: 0px solid transparent;
            background-color: transparent;
            spacing: 0px;
            width: {TOOLBAR_WIDTH}px;
            high: {TOOLBAR_HEIGHT}px;
            }}
            QPushButton QLabel {{
                color: #FFFFFF;
            }}
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border-radius: 3px;
                border: 1px solid #797979;
                background-color: #F90000;   
                margin: 10px 12px 10px 10px;                 
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Google Sans';
                width: 244px;
                height: 107px;
                
            }}
            
            QPushButton:hover {{
                background-color: #00ff00; 
            }}
            
            QPushButton QLabel {{
                font-size: 40px;
                font-weight: 'Regular';
                font-family: 'Google Sans';
            }}
        """
        
        return alert_style_string
    
    # This method control HTML injection to web page
    # Function: Zoom in, block input text and zoom text
    def finished_load_web_page(self):
        """
        Handles the completion of a web page load in the browser.
        This method performs the following actions:
        - Retrieves the current URL from the browser.
        - Checks if the URL is in the list of permitted websites.
        - Adjusts the zoom factor of the browser.
        - Injects HTML content based on the URL and configuration settings.
        """

        # Get url value from browser
        url_in_browser_value = self.main_browser.url().toString()
        #senior_website_posting_option = self.data_in_my_config_data["advanced_against_phishing"]["senior_website_posting"]

        senior_website_posting_option = self._dataProvider.seniorWebsitePosting
        
        # Get permitted websites list from sgive
        permitted_website_list = self.permitted_website_list
        # Check if it is permitted website
        check_result = any(permitted_website in url_in_browser_value for permitted_website in permitted_website_list)
        if check_result:
            if "homepage.html" not in url_in_browser_value:
                self.main_browser.setZoomFactor(1)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(250, lambda: self.html_injection_to_web_content())

        elif self.toggle_phishing_webpage:
            self.main_browser.setZoomFactor(1)
            # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
            QTimer.singleShot(250, lambda: self.html_injection_to_phishing_web_content())
        else:
            
            if senior_website_posting_option:
                self.main_browser.setZoomFactor(1)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(250, lambda: self.html_injection_to_web_content_strict())
            else:
                return
            
    # This method is applied for connection to phishing web page
    def html_injection_to_phishing_web_content(self):
        """
        Injects JavaScript into the web page to capture and send input field data to a Qt WebChannel.
        """

        injection_javasript = """
        var script = document.createElement('script');
        <!-- Define and call script qtwebchannel-->
        script.src = 'qrc:///qtwebchannel/qwebchannel.js';
        script.onload = function() {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.notification_fill_text = channel.objects.notification_fill_text;
                <!-- Elements for capturing text are defined HERE!!!-->
                document.querySelectorAll('input[type="text"], input[type="email"], input[type="search"], input[type="password"], input[type="tel"], input[type="url"],input[enterkeyhint="search"], textarea').forEach(function(element) {
                    element.addEventListener('change', function() {
                        <!-- Define data with two parameter: one for saved text, one for url-->
                        var data = {value: element.value, url: window.location.href};
                        <!-- Parse text to channel in type of JSON text-->
                        window.notification_fill_text.receiveData(JSON.stringify(data));
                    });
                });
            });
        };
        document.head.appendChild(script);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # This method is used for changing font in HTML content
    def html_injection_to_web_content(self):
        """
        Injects JavaScript into the web content to modify the styles of specific HTML elements.
        The injected script targets paragraph, div, article, span, and header elements (h3, h4, h5)
        and adjusts their font size and line height based on their tag name.
        """
        injection_javasript = """
        <!-- Change only paragraph, article, span and header elements with lower levels--> 
        var all_changed_content_tag = ['p', 'div', 'article', 'span', 'h3', 'h4', 'h5'];
        <!-- Create a function to change content style-->
        var change_content_style = function(element) {
            <!-- Method includes will return value in UPPERCASE>
            if (['H3', 'H4', 'H5', 'A'].includes(element.tagName)) {
                <!-- Header with bigger size-->
                element.style.fontSize = '20px';
                element.style.lineHeight = '1.0';
            }
            <!-- Method includes will return value in UPPERCASE>
            else if (['P', 'DIV', 'ARTICLE', 'SPAN'].includes(element.tagName)) {
                <!-- Content with smaller size>
                element.style.fontSize = '17px';
                element.style.lineHeight = '1.1';
            }
            Array.from(element.children).forEach(change_content_style);
        }
        change_content_style(document.body);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # This method is used for changing font and block input in HTML content
    # !!!Apply for not permiited website
    def html_injection_to_web_content_strict(self):
        """
        Injects JavaScript into the web page to disable input fields and 
        modify the style of specific HTML elements.
        """

        injection_javasript = """
        <!-- Declare tags for prohibiting input text to textfill-->
        var prohibited_tag_input = document.querySelectorAll('input, textarea, div.input');
        <!-- Disable input field in webpage-->
        prohibited_tag_input.forEach(function(input) {
            <!-- True == input value is disabled-->
            input.disabled = true;
        });
        <!-- Change only paragraph, article, span and header elements with lower levels--> 
        var all_changed_content_tag = ['p', 'div', 'article', 'span', 'h3', 'h4', 'h5'];
        <!-- Create a function to change content style-->
        var change_content_style = function(element) {
            <!-- Method includes will return value in UPPERCASE>
            if (['H3', 'H4', 'H5', 'A'].includes(element.tagName)) {
                <!-- Header with bigger size-->
                element.style.fontSize = '20px';
                element.style.lineHeight = '1.0';
            }
            <!-- Method includes will return value in UPPERCASE>
            else if (['P', 'DIV', 'ARTICLE', 'SPAN'].includes(element.tagName)) {
                <!-- Content with smaller size>
                element.style.fontSize = '17px';
                element.style.lineHeight = '1.1';
            }
            Array.from(element.children).forEach(change_content_style);
        }
        change_content_style(document.body);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # Show full screen without Minimizing or Moving
    def show_app_full_screen(self):
        self.showFullScreen()
        
    # Method use for disable menu when click to another menu
    def toggle_between_toolbar(self):
        """
        Toggles the visibility between two toolbars, menu_1_toolbar and menu_2_toolbar.
        """

        # Toggle visibility of toolbars
        if self.menu_1_toolbar.isVisible():
            self.menu_1_toolbar.setVisible(False)
            self.menu_2_toolbar.setVisible(True)
        else:
            self.menu_2_toolbar.setVisible(False)
            self.menu_1_toolbar.setVisible(True)
        
    # Method for get current language and update default language in app
    # If translate button is clicked, change to other language and audio
    
    def toggle_supported_language(self):
        """
        Toggles the supported language in the language translator and updates the UI text.
        """

        self.language_translator.toggle_supported_language()
        self.update_ui_text()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_text(self):
            """
            Updates the UI text labels with translated text for menu items.
            """
            
            self.menu1_new_text_label.setText(self.language_translator.get_translated_text("menu1"))
            self.menu2_new_text_label.setText(self.language_translator.get_translated_text("menu2"))
            self.menu2_addres_new_text_label.setText(self.language_translator.get_translated_text("menu2Address"))

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"

    # QpushButton can be set HoverLeave and HoverEnter event with "widget"
    # Play sound when usesr hovers on button longer than 5 seconds
    '''Tarik
    def setup_hover_sound_value(self, input_widget, hover_time,path_to_sound):
        # Using Qtimer to set clock
        input_widget.hover_timer = QTimer()
        input_widget.hover_timer.setInterval(hover_time)
        # Run only one times when hover
        input_widget.hover_timer.setSingleShot(True)
        input_widget.hover_timer.timeout.connect(lambda: self.play_sound_for_button(path_to_sound))
        # Install event to widget -> Event is comefrom eventFilter
        input_widget.installEventFilter(self)
    '''
    # Set event for leave and enter button -> Using only with QpushButton
    def eventFilter(self, watched, event):
        """
        Filters events for the watched object and handles hover events.
        Args:
            watched: The object being watched.
            event: The event being filtered.
        Returns:
            bool: True if the event should be filtered out, False otherwise.
        """

        if event.type() == QEvent.HoverEnter:
            watched.hover_timer.start()
        elif event.type() == QEvent.HoverLeave:
            watched.hover_timer.stop()
            # Stop sound immediately
            self.stop_sound_for_button()
        return super().eventFilter(watched, event)
    
    
    # Stop sound immediately when button is leaved hover
    ## TODO delete
    def stop_sound_for_button(self):
        if self.sound_mixer_control_for_button:
            self.sound_mixer_control_for_button.stop()
            self.sound_mixer_control_for_button = None
        
    # This method is set for visible and invisible URL bar
    def toggle_url_toolbar(self):
        """
        Toggles the visibility of the URL toolbar and the toolbar space in the main browser.
        """
        if self.global_dataProvider.protectionLevel != 3:
            self.main_browser.setUrl(QUrl("about:blank"))
            self.url_toolbar.setVisible(not self.url_toolbar.isVisible())
            self.toolbar_space.setVisible(not self.toolbar_space.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        """
        Navigates the browser to the URL entered in the URL bar. If the URL does not contain a dot,
        it performs a Google search. If the URL does not start with a scheme, it defaults to HTTPS.
        """

        # Get url from URL toobal
        url_in_bar_value = self.url_bar.text().strip()

        if self.global_dataProvider.protectionLevel == 2:
            web_url = self.url_blocker.find_url_with_value(url_in_bar_value)
            
            if web_url != "None":

                # Set default style for toolbar
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                
                # Set visible after navitigation
                self.url_toolbar.setVisible(False)
                self.toolbar_space.setVisible(False)
                # Set url bar as clean
                self.url_bar.clear()
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(web_url)) 
            else:
                print("URL is not permitted")
                    
        else:
            #If "." is not contained in URL
            if "." not in url_in_bar_value:
                url_in_bar_value = "https://www.google.com/search?q=" + url_in_bar_value
            # If in URl not http or https, connect with HTTPS
            if "://" not in url_in_bar_value:
                url_in_bar_value = "https://" + url_in_bar_value
            
            # Set default style for toolbar
            self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
            self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
            
            # Set visible after navitigation
            self.url_toolbar.setVisible(False)
            self.toolbar_space.setVisible(False)
            # Set url bar as clean
            self.url_bar.clear()
            # Connect to URL after entering
            self.main_browser.setUrl(QUrl(url_in_bar_value))
    
    # Method for security against phishing    
    def security_against_phishing(self,qurl):
        """
        Checks the given URL for phishing threats and updates the browser's UI and logs accordingly.
        Parameters:
        qurl (QUrl): The URL to be checked for phishing threats.
        """
        # Get url from QURL
        url_in_browser_value = qurl.toString()
        if url_in_browser_value.endswith('/'):
            if self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True                   
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
            else:
                self.toggle_phishing_webpage = False
                # Set default style for toolbar
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
        elif not url_in_browser_value.endswith('/'):
            if "about:blank" in url_in_browser_value:
                self.toggle_phishing_webpage = False
                return
            #elif "google.com" in url_in_browser_value:
                #self.toggle_phishing_webpage = False
                #self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                #self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with level 6 INFORMATIONAL
                #self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
                # Connect to URL after entering
                #self.main_browser.setUrl(QUrl(url_in_browser_value))
            elif self.url_blocker.is_url_blocked(url_in_browser_value):
                self.toggle_phishing_webpage = True
                ## My comment
                ##self.play_sound_for_button(self.path_to_alert_phishing_music)
                # Log with level 5 when connected to phishing
                #self.url_logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Connection to Phishing server {url_in_browser_value}')
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
            else:
                self.toggle_phishing_webpage = False
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with LEVEL 6 INFORMATIONAL
                #self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
        self.main_browser.loadFinished.connect(self.finished_load_web_page)
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www1(self):
        self.main_browser.setUrl(QUrl(self._dataProvider.urlsForWebsites[0]))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        
    # Method for connect to the irozhlas.cz
    def navigate_www2(self):
        self.main_browser.setUrl(QUrl(self._dataProvider.urlsForWebsites[1]))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the vut.cz
    def navigate_www3(self):
        self.main_browser.setUrl(QUrl(self._dataProvider.urlsForWebsites[2]))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
    # Method for connect to the idnes.cz
    def navigate_www4(self):
        self.main_browser.setUrl(QUrl(self._dataProvider.urlsForWebsites[3]))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)



    # Method for connect to the aktualne.cz
    def navigate_www5(self):
        self.main_browser.setUrl(QUrl(self._dataProvider.urlsForWebsites[4]))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the denik.cz
    def navigate_www6(self):
        self.main_browser.setUrl(QUrl(self._dataProvider.urlsForWebsites[5]))
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
