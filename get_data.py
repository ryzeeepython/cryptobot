
import requests

class Get_Data:

    def get_data():
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
            'Origin': 'https://tradersdiaries.com',
            'Referer': 'https://tradersdiaries.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'X-Loading': 'none',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'lang': 'ru',
            'market': 'all',
        }

        response = requests.post('https://api.tradersdiaries.com/prod/signals/get-signals', headers=headers, json=json_data).json()  

        result =''
        for i in response:
            symbol = str(i['symbol'])
            market = str(i['market'])
            timeframe = str(i['timeframe'])
            price = str(i['price'])
            stop = str(i['stop'])
            side = str(i['side'])
            created = str(i['created'])
            if side != 'short':
                emoji = '🔴'
            else:
               emoji = '🟢' 
            result = result + emoji + symbol + ': ' + market +  '\n    buy: ' + price + '\n    sell: ' + stop + '\n    timeframe: ' + timeframe +'\n    created: ' +created +'\n\n'

        return result

