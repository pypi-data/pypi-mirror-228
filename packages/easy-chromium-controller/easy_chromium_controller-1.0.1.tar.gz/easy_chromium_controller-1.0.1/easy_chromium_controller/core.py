__author__ = "Gonzalo Fernandez Suarez"

# Utils
import os
import time
import difflib  # Search Better Match
from time import sleep
from enum import Enum
from .utils import KillAllChromiumProcessOnLinux, KillAllChromiumProcessOnWindows, Singleton, Log, Input
from PIL import Image, ImageDraw  # Captcha resolve dependecies

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

# Use Chromium
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.webdriver import ChromiumDriver

class Browser(metaclass=Singleton):
    """Objeto responsable de interactuar con el navegador.\n
    ``Solo existe una instancia de este objeto.``\n

    Dependencias:
        - La enumeracion de ventanas "BROWSER_WINDOWS" : necesario saber el numero de ventanas\n
          que se van a utilizar de antemano.\n

        - Variable de entorno "ENV" : decide si es headless o no.\n

    """
    def open(
        self,
        browser_windows: Enum,
        screenshots_path=os.path.dirname(os.path.abspath(__file__)) + "/screenshots",
        binary_location=os.path.dirname(os.path.abspath(__file__)),
        short_wait_scs=5,
        normal_wait_scs=10,
        long_wait_scs=20,
    ):
        # Browser atributes
        self.screenshots_path = screenshots_path
        self.browser_windows = browser_windows
        self.OS = os.getenv("OS") # "linux" | "win"
        # Browser config
        options = ChromiumOptions()
        # Disable logging
        options.add_argument("--disable-logging")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # Para que no pregunte por guardar contraseñas
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        # Tamaño y posicion de la ventana, para evitar errores en clicks
        # Docker config https://rstudio.github.io/chromote/reference/default_chrome_args.html
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--window-position=0,0")
        options.add_argument("--start-fullscreen")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-features=Translate")

        # Setup driver
        if self.OS == "linux":
            service = ChromiumService(binary_location + "/bin/linux/chromedriver")
            options.binary_location = binary_location + "/bin/linux/chrome/chromium"
            options.headless = True
        else:
            service = ChromiumService(binary_location + "\\bin\\win\\chromedriver.exe")
            options.binary_location = binary_location + "\\bin\\win\\chrome\\chromium.exe"
            options.headless = False

        browser_name = "chrome"
        vendor_prefix = "goog:"
        self.driver = ChromiumDriver(
            browser_name=browser_name,
            vendor_prefix=vendor_prefix,
            options=options,
            service=service,
        )

        # Setup waits
        self.normal_wait_scs = normal_wait_scs
        self.wait = WebDriverWait(self.driver, normal_wait_scs)
        self.shortWait = WebDriverWait(self.driver, short_wait_scs)
        self.longWait = WebDriverWait(self.driver, long_wait_scs)

        # Setup windows
        for i in range(len(browser_windows) - 1):
            self.__openNewWindow()
        self.switchToWindow(0)

    def goTo(self, url):
        self.driver.get(url)
        self._disableTransitions()
        
    def getURL(self):
        return self.driver.current_url

    def sleep(self, seconds: float):
        sleep(seconds)

    def findElement(self, by, value, wait="normal") -> WebElement:
        if wait == "short":
            return self.shortWait.until(EC.presence_of_element_located((by, value)))
        else:
            return self.wait.until(EC.presence_of_element_located((by, value)))

    def findElements(self, by, value, wait="normal"):
        if wait == "short":
            return self.shortWait.until(
                EC.presence_of_all_elements_located((by, value))
            )
        else:
            return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    def hiddeElement(self, by, value):
        elem = self.findElement(by, value)
        self.executeScript([elem], 'args[0].style.display = "none";')

    def click(self, by, value, wait="normal", maybe=False):
        def func():
            if wait in "long":
                self.longWait.until(EC.element_to_be_clickable((by, value))).click()
            elif maybe:
                self.shortWait.until(EC.element_to_be_clickable((by, value))).click()
            else:
                self.wait.until(EC.element_to_be_clickable((by, value))).click()

        if not maybe:
            return func()
        try:
            func()
        except:
            return

    def clickElem(self, element: WebElement):
        self.wait.until(EC.element_to_be_clickable(element)).click()

    def switchToFrame(self, by=By.XPATH, value="/html"):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((by, value)))
        """ self.driver.switch_to.frame(wait.until(EC.presence_of_element_located((by,value)))) """

    def waitForNewWindow(self):
        oldWindows = self.driver.window_handles
        self.wait.until(EC.new_window_is_opened(oldWindows))

    def waitForNumberWindows(self, number):
        self.wait.until(EC.number_of_windows_to_be(number))

    def switchToWindow(self, window):
        page_name = self.browser_windows(window).name
        self.driver.switch_to.window(self.driver.window_handles[window])

    def __openNewWindow(self):
        self.driver.execute_script("window.open();")

    """ def __closeWindow(self, window : BROWSER_WINDOWS):
        self.switchToWindow(window)
        self.driver.close() """

    def clearCurrentWindow(self):
        self.driver.get("about:blank")

    def waitForPageLoad(self):
        """
        Espera a que la pagina termine de cargar. \n
        """
        loaded = False
        start_time = time.time()
        while not loaded and time.time() - start_time < self.normal_wait_scs:
            loaded = self.executeScript(
                [], """return document.readyState === "complete";"""
            )
            self.sleep(1)

    def close(self):
        self.driver.quit()
        if self.OS == "linux":
            KillAllChromiumProcessOnLinux()
        else:
            KillAllChromiumProcessOnWindows()

    def printWindows(self):
        print(self.driver.window_handles)

    def fullScreenshot(self, imageName):
        """ScreenShot a la pantalla y lo guarda para que la API pueda acceder a el"""
        self.findElement(By.TAG_NAME, "body").screenshot(
            self.screenshots_path + "/" + imageName + ".png"
        )

    def elementScreenshot(self, By, value, imageName):
        """ScreenShot a un elemento y lo guarda para que la API pueda acceder a el"""
        self.findElement(By, value).screenshot(
            self.screenshots_path + "/" + imageName + ".png"
        )

    def executeScript(self, args=[], script=""):
        """Ejecuta un script de javascript y retorna el resultado. \n
        Para acceder a los argumentos dentro \n
        del script utilizar la constante "args". \n
        Ejemplo:
        ```js
            console.log(args[0]); // Imprime el primer argumento
        ```
        """
        scriptSetup = "const args = arguments[0];\n"
        return self.driver.execute_script(scriptSetup + script, args)

    def scrollIntoView(self, element: WebElement):
        """Hace scroll hasta que el elemento sea visible"""
        self.executeScript(
            [element],
            'args[0].scrollIntoView({ behavior: "instant", block: "center",  inline: "center" });',
        )

    def scrollToBottom(self):
        """Hace scroll hasta el final de la pagina"""
        self.executeScript([], "window.scrollTo(0, document.body.scrollHeight);")

    def scrollToTop(self):
        """Hace scroll hasta el principio de la pagina"""
        self.executeScript([], "window.scrollTo(0, 0);")

    def handleCaptcha(self, captcha_iframe_xPath: str):
        self.switchToFrame(By.XPATH, captcha_iframe_xPath)

        def solveCaptcha():
            # Prueba de que no eres un robot
            # Comprobamos si es de 3x3 o 4x4
            tiles_list = self.findElements(By.CLASS_NAME, "rc-imageselect-tile")
            if len(tiles_list) == 16:
                matrix_size = 4
                x_offset = 113
                y_offset = 103
            else:
                matrix_size = 3
                x_offset = 136
                y_offset = 134
            Log("Tamaño de captcha : ", matrix_size, " x ", matrix_size)
            self.fullScreenshot("robot_image")
            # Recortamos la imagen
            img = Image.open(self.screenshots_path + "/robot_image.png")
            draw = ImageDraw.Draw(img)
            count = 1
            for row in range(matrix_size):
                for col in range(matrix_size):
                    position = (4 + ((col) * x_offset), 127 + (row * y_offset))
                    text = "(" + str(count) + ")"
                    bbox = draw.textbbox(position, text)
                    draw.rectangle(bbox, fill="black")
                    draw.text(position, text, fill="red")
                    count += 1
            img.save(self.screenshots_path + "/robot_image_text.png", format="png")
            Log("Por favor, resuelve el captcha y pulsa enter")
            Log("imagen => <API URL>/image/robot_image_text")
            Log("Formato: numeros separados por puntos o comas ")
            blocks_to_click: list[int] = []
            while True:
                try:
                    str_input = Input()
                    if str_input == "":
                        continue
                    str_input = str_input.replace(" ", "").strip()
                    str_input = str_input.replace(",,", ",")
                    str_input = str_input.replace(".", ",")
                    str_input = str_input.split(",")
                    max = 1
                    min = 1
                    for number in str_input:
                        if int(number) > max:
                            max = int(number)
                        if int(number) < min:
                            min = int(number)
                        if int(number) not in blocks_to_click:
                            blocks_to_click.append(int(number))
                    if (max <= count - 1) and (min >= 1):
                        break
                    else:
                        raise Exception("Números fuera de rango")
                except Exception:
                    Log("Por favor, escribe un numero entre 1 y ", count - 1)
                    str_input = None
            Log("Clickando en los cuadrados: ", blocks_to_click)
            for index in blocks_to_click:
                tiles_list[index - 1].click()
                self.sleep(0.5)
            self.click(By.XPATH, '//*[@id="recaptcha-verify-button"]')
            Log("Comprobando...")
            self.sleep(6)
            try:
                tiles_list = self.findElements(
                    By.CLASS_NAME, "rc-imageselect-tile", wait="short"
                )
                if (not tiles_list) or (len(tiles_list) == 0):
                    raise Exception("Captcha resulto")
            except Exception:
                Log("Captcha resuelto  ✔️")
                return
            Log("Captcha no resuelto aún, intentando de nuevo")
            solveCaptcha()
            return

        solveCaptcha()
        self.switchToFrame()

    def markElement(self, element: WebElement, width=4, color="red"):
        self.executeScript(
            [element],
            'args[0].style.border = "' + str(width) + "px solid " + color + '";',
        )

    def _disableTransitions(self):
        """Desactiva las transiciones. Muy útil para antes de abrir pestañas con animaciones, etc..."""
        self.executeScript(
            [],
            """
            let css = ` * {
                -o-transition-property: none !important;
                -moz-transition-property: none !important;
                -ms-transition-property: none !important;
                -webkit-transition-property: none !important;
                transition-property: none !important;
                -o-transform: none !important;
                -moz-transform: none !important;
                -ms-transform: none !important;
                -webkit-transform: none !important;
                transform: none !important;
                -webkit-animation: none !important;
                -moz-animation: none !important;
                -o-animation: none !important;
                -ms-animation: none !important;
                animation: none !important;
            }`;
            head = document.head || document.getElementsByTagName('head')[0];
            style = document.createElement('style');
            head.appendChild(style);
            style.type = 'text/css';
            if (style.styleSheet){
            // This is required for IE8 and below.
                style.styleSheet.cssText = css;
            } else {
                style.appendChild(document.createTextNode(css));
            }
            """,
        )

    def clickBetterMatchButtonFromList(
        self,
        list_container_locator,
        target_buttons_locator,
        target_text: str,
        format_button_text=None,
    ):
        """
        Busca un botón con el texto mas similar a ``text`` dentro de la lista de pestañas ``tabs_list`` y lo clicka.\n
        Retorna true si lo encuentra, false si no.
        """
        container = self.findElement(
            list_container_locator[0], list_container_locator[1]
        )
        self.markElement(container)
        target_buttons = container.find_elements(
            target_buttons_locator[0], target_buttons_locator[1]
        )
        if (not target_buttons) or (len(target_buttons) == 0):
            return False
        if format_button_text:
            target_buttons_text = list(
                map(lambda x: format_button_text(x.text), target_buttons)
            )
        else:
            target_buttons_text = list(map(lambda x: x.text, target_buttons))
        better_matches = difflib.get_close_matches(
            target_text, target_buttons_text, n=1, cutoff=0.6
        )
        if better_matches:
            match = better_matches[0]
            match_index = target_buttons_text.index(match)
        else:
            return False
        self.scrollIntoView(target_buttons[match_index])
        self.clickElem(target_buttons[match_index])
        return True

    def clickBetterMatchButtonFromTabsList(
        self,
        tabs_container_locator,
        tabs_collapse_button_locator,
        target_buttons_locator,
        target_text: str,
        target_buttons_container_locator=None,
        list_container_locator=None,
    ):
        """
        Busca un botón con el texto mas similar a ``text`` dentro de la lista de pestañas ``tabs_list`` y lo clicka.
        Retorna true si lo encuentra, false si no.

        Hay dos formas de utilizarlo:

        1º . Los ``tabs_container`` envuelven el header y el contenido de cada pestaña, son el contenedor de cada sección.
            - Utilización: no se pasa ``list_container_locator`` y se pasa ``target_buttons_container_locator``.

        2º . Los ``tabs_container`` envuelven solo el header (``collapse_button``, ...). El contenido de cada pestaña esta\n
            dentro de ``list_container``.
            - Utilización: se pasa ``list_container_locator`` y no se pasa ``target_buttons_container_locator``.

        Si se utiliza ``list_container_locator`` se ignora ``target_buttons_container_locator`` y se busca directamente todo
        dentro de ``list_container_locator``.
        """
        if list_container_locator:
            list_container = self.findElement(
                list_container_locator[0], list_container_locator[1]
            )
            self.markElement(list_container)
            tabs_container_list = list_container.find_elements(
                tabs_container_locator[0], tabs_container_locator[1]
            )
        else:
            tabs_container_list = self.findElements(
                tabs_container_locator[0], tabs_container_locator[1]
            )
        # Lista de listas de botones, textos e indices de pestañas a la que pertenecen
        target_buttons = []
        target_buttons_text = []
        target_buttons_tab_index = []
        for index, tab in enumerate(tabs_container_list):
            collapseButton = tab.find_element(
                tabs_collapse_button_locator[0], tabs_collapse_button_locator[1]
            )
            self.scrollIntoView(tab)
            self.clickElem(collapseButton)
            if not list_container_locator:
                temp_buttons = tab.find_element(
                    target_buttons_container_locator[0],
                    target_buttons_container_locator[1],
                ).find_elements(target_buttons_locator[0], target_buttons_locator[1])
                self.scrollIntoView(temp_buttons[len(temp_buttons) - 1])
            else:
                self.scrollIntoView(tab)
                temp_buttons = list_container.find_elements(
                    target_buttons_locator[0], target_buttons_locator[1]
                )
            temp_buttons_text = list(map(lambda b: b.text, temp_buttons))
            temp_buttons_tab_index = list(map(lambda b: index, temp_buttons))
            target_buttons.extend(temp_buttons)
            target_buttons_text.extend(temp_buttons_text)
            target_buttons_tab_index.extend(temp_buttons_tab_index)
            if not list_container_locator:
                self.scrollIntoView(collapseButton)
                self.clickElem(collapseButton)

        # Buscamos el boton correspondiente al texto
        better_matches = difflib.get_close_matches(
            target_text, target_buttons_text, n=1, cutoff=0.5
        )
        if better_matches:
            match = better_matches[0]
            match_index = target_buttons_text.index(match)
        else:
            return False
        if not list_container_locator:
            self.scrollIntoView(
                tabs_container_list[target_buttons_tab_index[match_index]]
            )
            self.clickElem(tabs_container_list[target_buttons_tab_index[match_index]])
        target_button = target_buttons[match_index]
        self.scrollIntoView(target_button)
        # Click en el boton con el texto que buscamos
        self.clickElem(target_button)
        return True

    def mapListOfElements(self, container_locator, elements_locator, func) -> list:
        """
        Aplica una función a cada elemento de la lista y retorna una lista con los resultados. \n
        """
        container = self.findElement(container_locator[0], container_locator[1])
        self.markElement(container)
        elements = container.find_elements(elements_locator[0], elements_locator[1])
        return list(map(func, elements))

    def findElementInContainerWithText(
        self, container: WebElement, elements_locator, target_text
    ) -> WebElement:
        """
        Busca un elemento dentro de un contenedor que contenga el texto ``text``. \n
        Si no lo encuentra retorna None. \n
        """
        elements = container.find_elements(elements_locator[0], elements_locator[1])
        for element in elements:
            if target_text in element.text:
                return element
        return None
