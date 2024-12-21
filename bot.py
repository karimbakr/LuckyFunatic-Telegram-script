import aiohttp
import asyncio
from urllib.parse import parse_qs
import json
from colorama import Fore, Style, init
from datetime import datetime
import os
import importlib.util 
import pyfiglet
import  subprocess
import sys
libraries = ["httpx", "requests", "colorama", "rich", "pyfiglet"]
# تهيئة مكتبة colorama
init(autoreset=True)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_library_installed(library_name):
    """تحقق إذا كانت المكتبة مثبتة."""
    return importlib.util.find_spec(library_name) is not None

def install_libraries():
    for library in libraries:
        if is_library_installed(library):
            print(f"✅ {library} is already installed.")
            clear_screen()
        else:
            try:
                print(f"🔄 Installing {library}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", library])
                print(f"✅ {library} installed successfully!")
                clear_screen()
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {library}. Error: {e}")

install_libraries()
def create_gradient_banner(text):
    banner = pyfiglet.figlet_format(text, font='slant').splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)
        elif i < section_size * 2:
            print(colors[1] + line)
        else:
            print(colors[2] + line)

# دالة لطباعة معلومات حول القنوات الاجتماعية
def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]
        print(color + f'| {social}: {username} |')
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
def get_user_agent():
    return "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36 Telegram-Android/11.2.2 (Xiaomi M1908C3JGG; Android 12; SDK 31; AVERAGE)"

# دالة للحصول على التاريخ والوقت الحالي
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# قراءة البيانات من الملف وتحويلها إلى قاموس
def load_params_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()  # قراءة النص من الملف
        params = parse_qs(content)    # تحويل النص إلى قاموس
        # تحويل القيم من قوائم إلى نصوص
        params = {key: value[0] for key, value in params.items()}
    return params

# إرسال طلب تسجيل الدخول
async def send_request():
    url = "https://api2.funtico.com/api/lucky-funatic/login"
    
    # تحميل البيانات من ملف data.txt
    params = load_params_from_file("data.txt")

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, headers=headers) as response:
            response_text = await response.text()
            try:
                # تحويل الاستجابة إلى JSON
                response_json = json.loads(response_text)
                # استخراج الـ token من داخل data
                token = response_json.get("data", {}).get("token", "Token not found")
                #print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Wellcome Mr: {Fore.YELLOW}{token}")
                return token
            except json.JSONDecodeError:
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to decode JSON response")
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Response Text:", response_text)

# دالة لعرض بيانات المستخدم
async def get_user_data(token):
    url = "https://api2.funtico.com/api/lucky-funatic/user"

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    # تحويل الاستجابة إلى JSON
                    response_json = json.loads(response_text)
                    
                    # استخراج first name
                    first_name = response_json.get("data", {}).get("user", {}).get("firstName", "First name not found")
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Wellcom Sir: {Fore.YELLOW}[{first_name}]")
                except json.JSONDecodeError:
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to decode JSON response")
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Response Text:", response_text)
            else:
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to fetch user data. Status code: {response.status}")
                
# دالة غير متزامنة للحصول على بيانات الـ quest وتخزين الـ id في ملف
async def get_quests_and_save_id(token):
    url = "https://clicker.api.funtico.com/quests"

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    # تحويل الاستجابة إلى JSON
                    response_json = json.loads(response_text)
                    
                    # التأكد من أن الاستجابة تحتوي على قائمة
                    if isinstance(response_json, list):
                        # استخراج الـ id من البيانات وحفظها في ملف quest.txt
                        with open("quest.txt", "w") as file:
                            for quest in response_json:
                                quest_id = quest.get("id", "No ID found")
                                file.write(f"{quest_id}\n")
                        
                        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Quests IDs have been saved in quest.txt")
                    else:
                        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Expected a list of quests, but got something else.")
                except json.JSONDecodeError:
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to decode JSON response")
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Response Text:", response_text)
            else:
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to fetch quest data. Status code: {response.status}")
async def claim_daily_bonus(token):
    url = "https://api2.funtico.com/api/lucky-funatic/daily-bonus/claim"

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 400:
                response_text = await response.text()
                response_data = json.loads(response_text)  # تحليل JSON
                message = response_data.get("message", "Message not found")  # استخراج الرسالة
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Bonus Login: Failed ❌ {Style.BRIGHT}{message}")
            elif response.status == 200:
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Bonus Login: Successful ✅")
# دالة غير متزامنة لقراءة الـ quest IDs من الملف وتمريرها إلى دالة claim_join_x
async def process_quests(token):
    try:
        # قراءة القيم من ملف quest.txt
        with open("quest.txt", "r") as file:
            quest_ids = [line.strip() for line in file.readlines()]

        # تمرير القيم إلى دالة claim_join_x واحدة تلو الأخرى
        for quest_id in quest_ids:
            await claim_join_x(token, quest_id)
            
            # إضافة فترة انتظار بين كل طلب وآخر لتجنب الحظر
            print(f"{Fore.CYAN}[{get_current_time()}] {Fore.YELLOW}Waiting for 5 seconds before the next quest...")
            await asyncio.sleep(5)  # فترة الانتظار بالثواني

        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}All quests processed successfully.")

    except Exception as e:
        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}An error occurred: {e}")
        
# دالة غير متزامنة لقراءة الـ quest IDs من الملف وتمريرها إلى دالة claim_join_y
async def process_questss(token):
    try:
        # قراءة القيم من ملف quest.txt
        with open("quest.txt", "r") as file:
            quest_ids = [line.strip() for line in file.readlines()]

        # تمرير القيم إلى دالة claim_join_x واحدة تلو الأخرى
        for quest_id in quest_ids:
            await claim_join_y(token, quest_id)
            
            # إضافة فترة انتظار بين كل طلب وآخر لتجنب الحظر
            print(f"{Fore.CYAN}[{get_current_time()}] {Fore.YELLOW}Waiting for 5 seconds before the next quest...")
            await asyncio.sleep(5)  # فترة الانتظار بالثواني

        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}All quests processed successfully.")

    except Exception as e:
        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}An error occurred: {e}")

# دالة claim_join_x لتنفيذ العمل على كل quest ID (يمكنك تخصيص هذا بناءً على احتياجاتك)
async def claim_join_x(token, quest_id):
    url = f"https://api2.funtico.com/api/claim/{quest_id}"

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    response_json = json.loads(response_text)
                    # التأكد من أن الاستجابة تحتوي على "status"
                    if response_json.get("status") == "success":
                        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Quest {quest_id} completed successfully.")
                    else:
                        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to claim quest {quest_id}")
                except json.JSONDecodeError:
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to decode JSON response")
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Response Text:", response_text)
            else:
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to claim quest {quest_id}. Status code: {response.status}")

# دالة claim_join_y (مثل claim_join_x لكن يمكن تخصيصها بما يناسب)
async def claim_join_y(token, quest_id):
    url = f"https://api2.funtico.com/api/claim/{quest_id}"

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    response_json = json.loads(response_text)
                    # التأكد من أن الاستجابة تحتوي على "status"
                    if response_json.get("status") == "success":
                        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Quest {quest_id} completed successfully.")
                    else:
                        print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to claim quest {quest_id}")
                except json.JSONDecodeError:
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to decode JSON response")
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Response Text:", response_text)
            else:
                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}Failed to claim quest {quest_id}. Status code: {response.status}")
async def get_current_energy_balance(token):
    url = "https://clicker.api.funtico.com/game"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    response_json = json.loads(response_text)
                    #print(response_json)
                    # استخراج الطاقة الحالية من الاستجابة
                    current_energy = response_json['data']['energy'].get("currentEnergyBalance", "Energy not found")
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}You Energy:  [{current_energy}]")
                    blance =  response_json['data']['funz'].get("currentFunzBalance", "Energy not found")
                   # print(f"{Fore.YELLOW}blance: [{int(blance)}]")
                    if current_energy <= 50:
                    	print(f"{Fore.RED}Failed energy....")
                    	await asyncio.sleep(200)
                    return int(blance)
                except json.JSONDecodeError:
                    print(f"{Fore.RED}Failed to decode JSON response.")
                    print(f"{Fore.RED}Response: {response_text}")
            else:
                print(f"{Fore.RED}Failed to retrieve energy balance. Status code: {response.status}")
async def send_tap_request(token):
    while True:
        token = await send_request()
        url = "https://clicker.api.funtico.com/tap"
        payload = {
            "taps": 1
        }

        headers = {
            'User-Agent': get_user_agent(),
            'Accept': "application/json",
            'Content-Type': "application/json",
            'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            'sec-ch-ua-mobile': "?1",
            'authorization': f"Bearer {token}",
            'sec-ch-ua-platform': "\"Android\"",
            'origin': "https://clicker.funtico.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://clicker.funtico.com/",
            'accept-language': "en-US,en;q=0.9"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    response_text = await response.text()
                    print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}claim: [{await get_current_energy_balance(token)}]")
                    await asyncio.sleep(2)
                else:
                    print("Failed with status code:", response.status)
                
async def fetch_and_save_type(token):
    url = "https://clicker.api.funtico.com/boosters"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'content-type': "application/json",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # استخراج نوع الـ type
                booster_types = [item['type'] for item in data.get('data', []) if 'type' in item]

                # حفظ الأنواع في ملف خارجي
                with open('bost.txt', 'w', encoding='utf-8') as file:
                    for b_type in booster_types:
                        file.write(f"{b_type}\n")

                print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}Done fatch boost ")
            else:
                print(f"فشل في جلب البيانات. رمز الحالة: {response.status}")     
                


async def send_boosters(token):
    url = "https://clicker.api.funtico.com/boosters/activate"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://clicker.funtico.com",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://clicker.funtico.com/",
        'accept-language': "en-US,en;q=0.9"
    }

    while True:
        try:
            # قراءة القيم من ملف bost.txt
            with open("bost.txt", "r", encoding="utf-8") as file:
                booster_types = [line.strip() for line in file.readlines() if line.strip()]

            # إرسال الطلب لكل قيمة
            async with aiohttp.ClientSession() as session:
                for booster_type in booster_types:
                    payload = {"boosterType": booster_type}
                    async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}BoosterType: {booster_type} : Successful ✅")
                        else:
                            print(f"{Fore.CYAN}[{get_current_time()}] {Fore.RED}BoosterType: {booster_type} : In used")
                            

                    # فاصل زمني لتجنب الحظر
                    await asyncio.sleep(10)  # 10 ثوانٍ (يمكنك تغييرها)

            # انتظار 3 ساعات قبل التكرار
            print(f"{Fore.CYAN}[{get_current_time()}] {Fore.GREEN}All Booster is Done :  ✅ watting next bosster ...")
            await asyncio.sleep(3 * 60 * 60)  # 3 ساعات
        except Exception as e:
            print(f"حدث خطأ: {e}")

# تشغيل الدالة
                          
# الدالة الرئيسية لتشغيل العملية
async def main():
    create_gradient_banner("LuckyFunatic")  # عرض الشعار
    print_info_box([("Telegram", "https://t.me/YOU742"),("Click on linke ","to open"), ("Coder", "@Ke4oo")])  # معلومات وسائل التواصل
    token = await send_request()  # الحصول على الـ token بعد التسجيل
    if token != "Token not found":
        
        await get_user_data(token)  # الحصول على بيانات المستخدم
        await claim_daily_bonus(token)
        await get_quests_and_save_id(token)
        await fetch_and_save_type(token)
        await process_quests(token)
        await process_questss(token)
        
        await asyncio.gather(
            send_boosters(token),
            send_tap_request(token),
            
            
        )
# تشغيل السكربت

asyncio.run(main())