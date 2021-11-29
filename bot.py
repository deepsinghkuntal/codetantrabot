from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from termcolor import colored
import stdiomask

#twilio
from twilio.rest import Client

account_sid = "ACd621bbcae9f2c8e4aab3378eb674506a"
auth_token = 'd00a7dca49cdaac9a8cac9d56d351a29'




ID = input('[+]Enter Username\n')
PASSWORD = stdiomask.getpass(prompt='Enter Password:\n')
frequency = 3


def add(hour, val):
    return str(int(hour) + val)


#get current time
def ryt_now():
    cur_time = time.localtime()
    cur_time=time.strftime("%H:%M:%S",cur_time)
    return cur_time

#get hour form ryt_now()
def get_time():
    cur_time = ryt_now()
    hour, mn, sec = cur_time.split(':')
    if int(mn) >= 40:
        hour = str((int(hour) + 1))
    return hour


#login to codetantra
def do_login(username, password):

    id_field = driver.find_element_by_xpath("//input[@placeholder='Username']")
    pass_field = driver.find_element_by_xpath("//input[@placeholder='Password']")

    id_field.send_keys(username)
    pass_field.send_keys(password)

    pass_field.send_keys(Keys.RETURN)
    message = driver.find_element_by_xpath("//a[@title='Click here to view Meetings']")
    message.send_keys(Keys.RETURN)


def process_hr(cur_hr, minutes):
    if int(cur_hr) > 12:
        cur_hr = str((int(cur_hr) - 12))
    cur = str((minutes + 60) % 60)
    if len(cur) < 2:
        cur = '0' + cur
    return cur_hr + ':' + cur


def send_sms(at):
    twilio_number = '+12087389649'
    target_number = '+917983686747'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = "Boss I have joind your class "+ at,
        from_= twilio_number,
        to = target_number
    )


    


# check for classes from cur time t in order t - 1, t, t + 1
# handle false positive of night
# can be more efficient
def check_for_class(hour):
    print(colored('Checking for ongoing class', 'cyan'))
    for cur_hr in [add(hour, -2), add(hour, -1), hour, add(hour, 1)]:
        for minutes in range(0, 60):
            val = process_hr(cur_hr, minutes)
            # print('Checking class at', val)
            try:
                path = "//div[@data-start='" + val + "']"
                current_class = driver.find_element_by_xpath(path)
                extra_check = current_class.get_attribute('data-full')
                if len(extra_check) > 8:
                    continue
                print(val, ' - Class Found')
                current_class.find_element_by_xpath("./../..").send_keys(Keys.RETURN)
                return val
            except:
                pass
    return False


def do_polls():
    poll_number = 1
    print(colored('[+] Starting poll daemon', 'green'))
    # print('End time estimated:', cur_hour)
    driver.switch_to.frame(driver.find_element_by_id('frame'))
    while True:
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[starts-with(@aria-labelledby,"pollAnswerLabel")]')))
            element.click()
            print('[+]', poll_number, 'poll(s) marked.')
            poll_number += 1
        except:
            pass
        if int(ryt_now().split(':')[1]) == 5:
            return


def join():
    try:
        # wait = WebDriverWait(driver, 3600)
        # wait.until(EC.visibility_of_element_located(By.ID("//a[@role='button']")))
        driver.find_element_by_class_name('btn').send_keys(Keys.RETURN)
        time.sleep(6)
        driver.switch_to.frame(driver.find_element_by_id('frame'))
        driver.find_element_by_xpath('//button[@aria-label="Microphone"]').send_keys(Keys.RETURN)
        time.sleep(20)
        driver.find_element_by_xpath('//button[@aria-label="Echo is audible"]').send_keys(Keys.RETURN)
        driver.switch_to.default_content()
        return True
    except:
        driver.quit()
        print(colored('[-] Join Button not available. Retrying in 3 minutes', 'red', attrs=['reverse', 'blink']))
        time.sleep(3 * 60)
        return False


def abort():
    print(colored('[-] Aborting', 'red'))
    driver.quit()
    exit(0)


#reply in chatbox(not working)
def chatbox():
    driver.find_element_by_xpath('//button[@aria-label="Users and messages toggle"]').send_keys(Keys.RETURN)
    time.sleep(5)
    driver.find_element_by_xpath('//div[@data-test="chatButton"]').send_keys(Keys.RETURN)
    reply = driver.find_element_by_xpath('//textarea[@placeholder="Send message to Public Chat"]')
    sendtext = "ok"
    reply.send_keys(sendtext)
    reply.send_keys(Keys.ENTER)
    return 


have_class = False
while True:
    chrome_options = webdriver.ChromeOptions()
    # uncomment line below to hide the class tab
    #chrome_options.headless = True
    chrome_options.add_argument("--mute-audio")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver.minimize_window()
    driver.get("http://myclass.lpu.in")

    try:
        do_login(ID, PASSWORD)
    except:
        print(colored('[-] Probably your credentials are invalid', 'red'))
        abort()

    hr = get_time()
    if int(hr) >= 20:
        print(colored('[-] No classes are scheduled after 8 pm', 'cyan', attrs=['reverse', 'blink']))
        abort()

    have_class = check_for_class(hr)

    if have_class and join():
        do_polls()
        send_sms(process_hr)
        driver.quit()
        time.sleep(60)
        print(colored('[+] Refreshing Daemon For other classes', 'cyan'))
    else:
        print(colored("[+] No ongoing lectures found at", 'blue'), colored(ryt_now(), 'blue'))
        driver.quit()
        print(colored('[+] Sleeping for', 'blue'), colored(frequency, 'blue'), colored('minutes', 'blue'))
        time.sleep(frequency * 60)
    
    if have_class and join():
        chatbox()
        print( 'replyed')
    else:
        print("class have not been joined")
