# Easy Chromium Controller 🌐

Easy Chromium Controller is a Python package that simplifies web scraping tasks by providing an easy-to-use interface for controlling Chromium browsers. It removes the complexity of setting up and configuring Selenium, while also offering additional features and general methods to streamline web scraping workflows.

## Installation 🚀

You can install Easy Chromium Controller via pip:

```bash
pip install easy-chromium-controller
```

## Getting Started 🛠️

Here's a simple example of how to use the Browser class, which is the core of this package:

```python
from easy_chromium_controller import Browser

# Setup windows
class Windows(Enum):
  GOOGLE = 0

# Get Browser instance
browser = Browser()
# Initialize Browser (Open Chromium)
browser.open(browser_windows=Windows)

# Navigate to a website
browser.goTo("https://google.com")

# Find and interact with elements on the webpage
element = browser.findElement(By.XPATH, "//input[@name='q']")
element.send_keys("Web scraping with Easy Chromium Controller")

# Perform other web scraping actions as needed

# Close the browser when done
browser.close()
```

## Documentation 📖

### Browser Class

Class responsible for interacting with the browser. Only one instance of this object exists.

## Required

- The enumeration of windows `browser_windows`: necessary to know the number of windows to be used in advance. It should start from 0 and increase one by one.

- Environment variable `OS`: to indicate the operating system ("linux" or "win").

## Methods

### function ```open```

```python
def open(
    self,
    browser_windows: Enum,
    screenshots_path=os.path.dirname(os.path.abspath(__file__)) + "/screenshots",
    binary_folder=os.path.dirname(os.path.abspath(__file__)),
    short_wait_scs=5,
    normal_wait_scs=10,
    long_wait_scs=20,
    headless=False,
    disable_logging=False,
    disable_save_passwords=False,
    incognito=False,
    start_maximize=False,
    start_fullscreen=False,
    window_size=None,
    window_position=None,
    configForDocker=False,
    disable_translate=False,
)
```
Opens an instance of the browser.

### function ```goTo```
```python
def goTo(self, url) -> None
```
Navigates to a specified URL.

### function ```getURL```
```python
def getURL(self) -> str
```
Gets the current URL of the browser.

### function ```sleep```
```python
def sleep(self, seconds: float)
```
Makes the script wait for the specified time in seconds.

### function ```findElement```
```python
def findElement(self, by, value, wait="normal") -> WebElement
```
Finds an element on the page based on the specified criteria.

### function ```findElements```
```python
def findElements(self, by, value, wait="normal")
```
Finds multiple elements on the page based on the specified criteria.

### function ```hideElement```
```python
def hideElement(self, by, value)
```
Hides an element on the page.

### function ```click```
```python
def click(self, by, value, wait="normal", maybe=False)
```
Clicks on an element on the page.

### function ```clickElem```
```python
def clickElem(self, element: WebElement)
```
Clicks on a WebElement.

### function ```switchToFrame```
```python
def switchToFrame(self, by=By.XPATH, value="/html")
```
Switches the context to the specified frame.

### function ```waitForNewWindow```
```python
def waitForNewWindow(self)
```
Waits for a new browser window to open.

### function ```waitForNumberWindows```
```python
def waitForNumberWindows(self, number)
```
Waits for a specific number of browser windows to be open.

### function ```switchToWindow```
```python
def switchToWindow(self, window=None)
```
Switches focus to a specific browser window.

### function ```clearCurrentWindow```
```python
def clearCurrentWindow(self)
```
Clears the content of the current window.

### function ```waitForPageLoad```
```python
def waitForPageLoad(self)
```
Waits for the current page to finish loading.

### function ```close```
```python
def close(self)
```
Closes the browser instance.

### function ```fullScreenshot```
```python
def fullScreenshot(self, imageName)
```
Captures a full-page screenshot.

### function ```elementScreenshot```
```python
def elementScreenshot(self, By, value, imageName)
```
Captures a screenshot of a specific element.

### function ```executeScript```
```python
def executeScript(self, args=[], script="")
```
Executes a JavaScript script on the page.

### function ```scrollIntoView```
```python
def scrollIntoView(self, element: WebElement)
```
Scrolls to make an element visible.

### function ```scrollToBottom```
```python
def scrollToBottom(self)
```
Scrolls to the bottom of the page.

### function ```scrollToTop```
```python
def scrollToTop(self)
```
Scrolls to the top of the page.

### function ```handleCaptcha```
```python
def handleCaptcha(self, captcha_iframe_xPath: str)
```
Solves a captcha on a web page.

### function ```markElement```
```python
def markElement(self, element: WebElement, width=4, color="red")
```
Marks an element on the page with a colored border.

### function ```_disableTransitions```
```python
def _disableTransitions(self)
```
Disables transitions on the page.

### function ```clickBetterMatchButtonFromList```
```python
def clickBetterMatchButtonFromList(
    self,
    list_container_locator,
    target_buttons_locator,
    target_text: str,
    format_button_text=None,
)
```
Clicks on a button with similar text from a list of buttons.

### function ```clickBetterMatchButtonFromTabsList```
```python
def clickBetterMatchButtonFromTabsList(
    self,
    tabs_container_locator,
    tabs_collapse_button_locator,
    target_buttons_locator,
    target_text: str,
    target_buttons_container_locator=None,
    list_container_locator=None,
)
```
Clicks on a button with similar text from a list of tabs.

### function ```mapListOfElements```
```python
def mapListOfElements(self, container_locator, elements_locator, func) -> list
```
Applies a function to each element in a list and returns a list of results.

### function ```findElementInContainerWithText```
```python
def findElementInContainerWithText(
    self, container: WebElement, elements_locator, target_text
) -> WebElement
```
Finds an element within a container that contains the specified text.

### function ```handleCaptcha```
```python
def handleCaptcha(self, captcha_iframe_xPath: str)
```
Solves a captcha on a web page.

<hr>

Enjoy web scraping with Easy Chromium Controller! 🕸️