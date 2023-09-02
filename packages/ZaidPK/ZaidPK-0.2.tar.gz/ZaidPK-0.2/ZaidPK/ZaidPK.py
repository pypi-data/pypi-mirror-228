import json , requests , os , re , json , random
from OneClick import Hunter
hd = str(Hunter.Services())
from uuid import uuid4
ud = str(uuid4())
from user_agent import generate_user_agent
gd = str(generate_user_agent())
import os , uuid , requests , random , re , json
from user_agent import *
def A_Gmail(email):
    url = 'https://android.clients.google.com/setup/checkavail'
    headers = {
        'Content-Length':'98',
		'Content-Type':'text/plain; charset=UTF-8',
		'Host':'android.clients.google.com',
		'Connection':'Keep-Alive',
		'user-agent':'GoogleLoginService/1.3(m0 JSS15J)',
    }
    data = json.dumps({
        'username':f'{email}',
		'version':'3',
		'firstName':'ZAID',
		'lastName':'Codeing'
    })
    response = requests.post(url,headers=headers,data=data)
    if response.json()['status'] == 'SUCCESS':
        return {'Status':'Available','ZAID':'@Bnddq'}
    else:
        return {'Status':'UnAvailable','ZAID':'@Bnddq'}
def A_Yahoo(email):
    email2 = email.split('@')[0]
    url2 = "https://login.yahoo.com/account/module/create?validateField=userId" 
    headers2 = {
	 'accept': '*/*',
	 'accept-encoding': 'gzip, deflate, br',
	 'accept-language': 'en-US,en;q=0.9',
	 'content-length': '7979',
	 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'cookie': 'A1=d=AQABBKsqRWQCEP0UsV5c9lOx8e5im2YNQ50FEgEBAQF8RmRPZAAAAAAA_eMAAA&S=AQAAApW5iPsgjBo-EVpzITncq1w; A3=d=AQABBKsqRWQCEP0UsV5c9lOx8e5im2YNQ50FEgEBAQF8RmRPZAAAAAAA_eMAAA&S=AQAAApW5iPsgjBo-EVpzITncq1w; A1S=d=AQABBKsqRWQCEP0UsV5c9lOx8e5im2YNQ50FEgEBAQF8RmRPZAAAAAAA_eMAAA&S=AQAAApW5iPsgjBo-EVpzITncq1w&j=WORLD; cmp=t=1682254514&j=0&u=1---; B=9qgodcpi4aalb&b=3&s=7t; GUC=AQEBAQFkRnxkT0IiCATl; AS=v=1&s=yWa5asCx&d=A64467c3b|dcjw_0n.2SoXBbaywfJ6pOKLuxGKrtyyLsUqPKnDloZ4PzLBcZineGWbyj4SSiaHVn.6gkyCaIlqSJGryRwnshefN43hbdPocziZnuN6cUMiC9Ls7jght5ak90PZbx8rt9nghZTUPpDYSsMNpii5aA9xWBEhMq__TTmv.rfLHzlCE8rgi5dk5PJouLBujcieRBtI7i.7PwU1jFkaeDhxE4dRMjpAQrjJKc6XqfbTBc5K9QaF6r1YVIVWHEpNrUzbZ_7sSzQ5QFoQNwVBgRzaFtm48hiQlg6S.xsMMdDWkw5xtlG7GZUC.V2jgWNgLScSwqCU_3ntveI_BrcuBy_XAXWQsUzNv3grKBv3qzhOMH3pl8DgTDV3wOo.GqdTtcsaaUn7O0i1hSoA0_EqNIXvRBBdePtBAjPWFZt6sK1Dy8S.kVvW9rIWxonS8GYw6jAw3FrkvM_xk8gxU4oKX1pk3h4m0iJVDQhlr0OOLGW7vBxnzYqidDFi01xQe608kLkJO9qx2X1Xv6XORvYJTNAOVfOMWV83D75M_7L4FOjog8f8F5EkOTU7LymG8GTXY2g4K1xBfGHyzAOPDv9NMjc0I_7wLdATcbn2axvwj5I2xiSqrxK8DYnqTVGqEt.tusj07ij4sobwY0FePNGjLOHICdau9tCajCSqBxtly23flz3iYPQ22Va6uuSaQ.c9mtXsBd0NTlWvlOc6zRdQK.uYkiCYg719UyeIFzDDWeFvQCbuBrstwX.zAkYz2YPaTs8ZGpogdgQ5OhaduuhR5jzvz2mmHXGh5fJ1kxfeClXFWbvCdu3T77mmXHxLGQpr3UZKnmiPO7VjxJoEd9SjYA_NFz9HPbvimmWgmv0DIXvdNvHKCQMYEUROQlk5XIH7oiQ1BtywZNvoWv1D7Q--~A',
	 'origin': 'https://login.yahoo.com',
	 'referer': 'https://login.yahoo.com/account/create?.lang=en-US&src=homepage&activity=ybar-signin&pspid=2023538075&.done=https%3A%2F%2Fwww.yahoo.com%2F&specId=yidregsimplified&done=https%3A%2F%2Fwww.yahoo.com%2F',
	 'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
	 'sec-ch-ua-mobile': '?0',
	 'sec-ch-ua-platform': '"Windows"',
	 'sec-fetch-dest': 'empty',
	 'sec-fetch-mode': 'cors',
	 'sec-fetch-site': 'same-origin',
	 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
	 'x-requested-with': 'XMLHttpRequest',
    }
    data2 = {
	 'specId': 'yidregsimplified',
	 'cacheStored': '',
	 'crumb': 'hrxAgkAZ5jX',
	 'acrumb': 'yWa5asCx',
	 'sessionIndex': '',
	 'done': 'https://www.yahoo.com/',
	 'googleIdToken': '',
	 'authCode': '',
	 'attrSetIndex': '0',
	 'multiDomain': '',
	 'tos0': 'oath_freereg|xa|en-JO',
	 'firstName': 'ZAID',
	 'lastName': 'coding', 
	 'userid-domain': 'yahoo',
	 'userId': f'{email2}',
	 'password': 'szdxfefdgfh',
	 'birthYear': '1998',
	 'signup': '',
    }
    response2 = requests.post(url2,headers=headers2,data=data2).text
    if '{"errors":[]}' in response2:
        return {'Status':'Available','ZAID':'@Bnddq'}
    else:
        return {'Status':'UnAvailable','ZAID':'@Bnddq'}
def A_Hotmail(email):
    url3 = f'https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=0&emailAddress={email}&_=1604288577990'
    headers3 = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
    response3 = requests.post(url3, headers=headers3).text
    if 'Neither' in response3:
        return {'Status':'Available','ZAID':'@Bnddq'}
    else:
        return {'Status':'UnAvailable','ZAID':'@Bnddq'}
def A_Aol(email):
    email3 = email.split('@')[0]
    url4 = "https://login.aol.com/account/module/create?validateField=yid"
    headers4 = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '18430',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'A1=d=AQABBAcaP2MCEDS0lcVAC7jDxca1x2QPSMAFEgEBAQFrQGNIYwAAAAAA_eMAAA&S=AQAAAk66bvBpHLzQZ0n3bQV7x6U; A3=d=AQABBAcaP2MCEDS0lcVAC7jDxca1x2QPSMAFEgEBAQFrQGNIYwAAAAAA_eMAAA&S=AQAAAk66bvBpHLzQZ0n3bQV7x6U; cmp=t=1665079824&j=0&u=1---; rxx=5dmbu5em0gs.2w52y1t9&v=1; AS=v=1&s=mE9oz2RU&d=A6340990f|BfPo7D7.2Soeua6Q5.JcZFuTeKDZd.VEwARWGa18pr8Nw39Pbg3lrVe2yFRyh3RRePi__A4A5bs6jgblICTjtwR23Xn2FaKNd3g4n2Nyoe0HUPOPhxc2_MkgSPb3Uv64NNH6b4oIbh0d6GPjVX.u1iE75NeNGVgDykpoV.GJb.ZOyA1hi3D079flz5FnGN3UPl4Jos.LGJjKE5jeRFZVRbTJyV_q0zmHwp0WmwaGpmtr2bKK2pVY_9dMpw5J1u9Wx0e_QeNBnAgpvDP_E02PBbuxEQQXAX0GF8IM_gu2g5D1CEPA15ailOgAaPTMDY7plQgXdP3cYarpT20WB0vRVdZXqvfsh7E.m8mX5QyFisDObrlDfLbh6nPbmjU_8BIyAHLvCBoCmF0u4BhXftXCqUgW5SadK6EzXKbn394dWjCdO0YJRStGJo_POkob5FNOWud6u3MY1IZS2ov3OD9LIoJy7w.mSCLZ.M84QgA0UgsGTrDOgTQJWeetwKIYy1RbR8lxFZr0IDwTLBAGflJkaNvnQqWxWbEjftCTvXH2CPXFaCRUnSObHQ2cP1Mb8kro2zkXtaUGmW_cD9oHxidsx6vaOfx4f_fSysGP5Aaa2z6NndXHWh_ium8B45ejj4MFh3F7my8_04UX4WjjiZIqGG0fXcLQxFrB1GY6Vnqo47oSmh4yBcZPV7eQ0CKATeJLshzj2SovAZcIdV1ptsKk9P.LVCZl6MeDskIxd5L6iixeCU6PMq84tz7Gmg6S~A; A1S=d=AQABBAcaP2MCEDS0lcVAC7jDxca1x2QPSMAFEgEBAQFrQGNIYwAAAAAA_eMAAA&S=AQAAAk66bvBpHLzQZ0n3bQV7x6U&j=WORLD',
        'origin': 'https://login.aol.com',
        'referer': 'https://login.aol.com/account/create?intl=uk&lang=en-gb&specId=yidReg&done=https%3A%2F%2Fwww.aol.com',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data4 = {
        'specId': 'yidreg',
        'cacheStored': '',
        'crumb': 'ks78hCqM4K.',
        'acrumb': 'mE9oz2RU',
        'done': 'https://www.aol.com',
        'googleIdToken': '',
        'authCode': '',
        'attrSetIndex': '0',
        'tos0': 'oath_freereg|uk|en-GB',
        'firstName': 'ZAID',
        'lastName': 'Coodeing',
        'yid': email3,
        'password': '1#$ZAID$#1wjdytesre',
        'shortCountryCode': 'IQ',
        'phone': '7716555876',
        'mm': '11',
        'dd': '1',
        'yyyy': '1998',
        'freeformGender': '',
        'signup': '',
    }
    response4 = requests.post(url4,headers=headers4,data=data4).text
    if ('{"errors":[]}') in response4:
        return {'Status':'Available','ZAID':'@Bnddq'}
    else:
        return {'Status':'UnAvailable','ZAID':'@Bnddq'}
def A_MailRu(email):
    url5 = 'https://account.mail.ru/api/v1/user/exists'
    headers5 = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    data5 = {
'email': str(email)
    }
    response5 = requests.post(url5,headers=headers5,data=data5).text
    if 'exists":false' in response5:
        return {'Status':'Available','ZAID':'@Bnddq'}
    else:
        return {'Status':'UnAvailable','ZAID':'@Bnddq'}
def CheckTik(email):
    url = "https://api2-19-h2.musical.ly/aweme/v1/passport/find-password-via-email/?app_language=ar&manifest_version_code=2018101933&_rticket=1656747775754&iid=7115676682581247750&channel=googleplay&language=ar&fp=&device_type=SM-A022F&resolution=720*1471&openudid=8c05dec470c7b7d5&update_version_code=2018101933&sys_region=IQ&os_api=30&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=280&carrier_region=IQ&ac=wifi&device_id=7023349253125604869&mcc_mnc=41805&timezone_offset=10800&os_version=11&version_code=880&carrier_region_v2=418&app_name=musical_ly&ab_version=8.8.0&version_name=8.8.0&device_brand=samsung&ssmix=a&pass-region=1&build_number=8.8.0&device_platform=android&region=SA&aid=1233&ts=1656747775&as=a1e67fbb4fffb246cf0244&cp=f2f02d6bfbffb36de1eomw&mas=01cd120efcb179ac1b331e5cecb80282052c2c4c0c66c66c2c4c46"
    headers = {
            'host':'api2-19-h2.musical.ly',
            'connection':'keep-alive',
            'cookie':'sstore-idc=maliva; store-country-co de=iq; odin_tt=056f31c10f8c82638f6d4d64669ad49e9c36d4946d5d596f433d7f2d75fa1592a21c201d712196d54ee4ae4e14ac8708eee32dc97c85c0a65510024ecc0698346f73ecab038b7160dbff96ced716b8af',
            'accept-Encoding':'gzip',
            'user-agent':'com.zhiliaoapp.musically/2018101933 (Linux; U; Android 11; ar_IQ; SM-A022F; Build/RP1A.200720.012; Cronet/58.0.2991.0)',
            'connection': 'close'        
    }
    data = f"app_language=ar&manifest_version_code=2018101933&_rticket=1656747775754&iid=7115676682581247750&channel=googleplay&language=ar&fp=&device_type=SM-A022F&resolution=720*1471&openudid=8c05dec470c7b7d5&update_version_code=2018101933&sys_region=IQ&os_api=30&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=280&email={email}&retry_type=no_retry&carrier_region=IQ&ac=wifi&device_id=7023349253125604869&mcc_mnc=41805&timezone_offset=10800&os_version=11&version_code=880&carrier_region_v2=418&app_name=musical_ly&ab_version=8.8.0&version_name=8.8.0&device_brand=samsung&ssmix=a&pass-region=1&build_number=8.8.0&device_platform=android&region=SA&aid=1233"
    res = requests.post(url,headers=headers,data=data).text
    if 'Sent successfully' in res:
        return {'Status':'OK','BY':'@Bnddq'}
    else :
        return {'Status':'FALSE','BY':'@Bnddq'}
def CheckInsta(email):
    url2 = 'https://i.instagram.com/api/v1/accounts/login/'
    headers2 = {
        'User-Agent':str(hd),
        'Accept':'*/*',
        'Cookie':'missing',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US',
        'X-IG-Capabilities':'3brTvw==',
        'X-IG-Connection-Type':'WIFI',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'i.instagram.com'        
    }
    data2 = {
        'uuid':ud,
        'password':'ZAID#tele=@F_F_X_F',
        'username':email,
        'device_id':ud,
        'from_reg':'false',
        '_csrftoken':'missing',
        'login_attempt_countn':'0'
    }
    res2 = requests.post(url2,headers=headers2,data=data2).text
    if ('"invalid_user"')in res2:
        return {'Status':'FALSE','BY':'@Bnddq'}
    elif ('"bad_password"') in res2:
        return {'Status':'OK','BY':'@Bnddq'}
    else:
        return {'Status':'FALSE','BY':'@Bnddq'}
def GetInfoTik(user):
    try:
        resp4 = requests.get(f'https://www.tiktok.com/@{user}').text
        getting = str(resp4.split('"UserModule":')[1]).split('"RecommendUserList"')[0]
        i1 = str(getting.split('id":"')[1]).split('",')[0]
        i2 = str(getting.split('nickname":"')[1]).split('",')[0]
        i3 = str(getting.split('signature":"')[1]).split('",')[0]
        i4 = str(getting.split('region":"')[1]).split('",')[0]
        i5 = str(getting.split('privateAccount":')[1]).split(',"')[0]
        i6 = str(getting.split('followerCount":')[1]).split(',"')[0]
        i7 = str(getting.split('followingCount":')[1]).split(',"')[0]
        i8 = str(getting.split('heart":')[1]).split(',"')[0]
        i9 = str(getting.split('videoCount":')[1]).split(',"')[0]
        return {'result':'true','user':'true','id':i1,'name':i2,'bio':i3,'code-country':i4,'private':i5,'followers':i6,'following':i7,'likes':i8,'video':i9,'By':'@Bnddq'}
    except IndexError :
        return {'result':'false','user':'false','By':'@Bnddq'}
def GetInfoInsta(user):
    try:
        url= f"https://i.instagram.com/api/v1/users/web_profile_info/?username={user}"
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'mid=Y3bGYwALAAHNwaKANMB8QCsRu7VA; ig_did=092BD3C7-0BB2-414B-9F43-3170EAED8778; ig_nrcb=1; shbid=1685054; shbts=1675191368.6684434090; rur=CLN; ig_direct_region_hint=ATN; csrftoken=Wcmc9xB0EWESej9SP16gSpt1nBYAsWs7; ds_user_id=6684434090',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': gd,
            'x-asbd-id': '198387',
            'x-csrftoken': 'Wcmc9xB0EWESej9SP16gSpt1nBYAsWs7',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0g7ECdkTdrXy37TE9AoSnMndccWbB1cqrccYOZSLfcb0pE',
            'x-instagram-ajax': '1006383249',
        }
        r4 = requests.get(url,headers=headers).json()
    except :
        return {'result':'false','user':'false','Tele':'@Bnddq'}
    f1 = str(r4['data']['user']['full_name'])
    f2 = str(r4['data']['user']['id'])
    f3 = str(r4['data']['user']['edge_followed_by']['count'])
    f4 = str(r4['data']['user']['edge_follow']['count'])
    f5 = str(r4['data']['user']['edge_owner_to_timeline_media']['count'])
    r5 = requests.get(f"https://o7aa.pythonanywhere.com/?id={f2}").json()
    r6 = r5['date']
    f6 = int(r6)-1
    try:
        hd5 = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            'Connection': 'Keep-Alive',
            'User-Agent': hd,
            'Accept-Language': 'en-US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': 'AQ==',
	    }
        d5 = {
            'ig_sig_key_version': '4',
            "user_id":f2
	    }
        u5 = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        r6 = requests.post(u5,headers=hd5,data=d5).json()
        f7 = r6['obfuscated_email']
        return {'result':'true','user':'true','name':f1,'id':f2,'followers':f3,'following':f4,'posts':f5,'date':f6,'reset':f7,'Tele':'@Bnddq'}
    except KeyError:
        return {'result':'true','user':'true','name':f1,'id':f2,'followers':f3,'following':f4,'posts':f5,'date':f6,'reset':'false','Tele':'@Bnddq'}
#def GetListInsta_FG(n5,sessionid):
    try:
        u6 = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={n5}'
        hd6 = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'mid=Y3bGYwALAAHNwaKANMB8QCsRu7VA; ig_did=092BD3C7-0BB2-414B-9F43-3170EAED8778; ig_nrcb=1; shbid=1685054; shbts=1675191368.6684434090; rur=CLN; ig_direct_region_hint=ATN; csrftoken=gLlFX76z8qqwDgmh8ZIp3uFhAeX4zKdO; ds_user_id=921803283; sessionid={sessionid}',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': generate_user_agent(),
            'x-asbd-id': '198387',
            'x-csrftoken': 'gLlFX76z8qqwDgmh8ZIp3uFhAeX4zKdO',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0g7ECdkTdrXy37TE9AoSnMndccWbB1cqrccYOZSLfcb0pE',
            'x-instagram-ajax': '1006383249',
        }
        r7 = requests.get(u6,headers=hd6).json()
    except json.decoder.JSONDecodeError:
        return {'Status':'False','Sessionid':'False'}
    try:
        id = str(r7['data']['user']['id'])
    except KeyError:
        print('user false')
        exit()
    os.system('clear')
    s1 = {'sessionid':sessionid}
    hd7 = {
    'Host': 'www.instagram.com',
    'User-Agent': Hunter.Services(),
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-IG-App-ID': '936619743392459',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/'+str(n5)+'/following/',
    'TE': 'Trailers'
    }
    ZAID22 = 0
    r8 = requests.get('https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"'+str(id)+'","include_reel":true,"fetch_mutual":false,"first":50}',headers=hd7,cookies=s1)
    while True:
        if str('"has_next_page":false,') in r8.text:
            try:
                nu = json.loads(r8.text)['data']['user']['edge_follow']['edges']
                if nu == '[]':
                    return {'Status':'False','Sessionid':'False'}
                for ns in nu:
                    n6 = str(ns["node"]["username"])
                pass
            except KeyboardInterrupt:
                pass
        else:
            if ZAID22 != 0:
                try:
                    end = re.findall(',"end_cursor":"(.*)"},"edges":', r8.text)
                    r8 = requests.get('https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"'+str(id)+'","include_reel":true,"fetch_mutual":false,"first":50,"after":"'+end[0]+'"}',headers=hd7,cookies=s1)
                    try:
                        nu = json.loads(r8.text)['data']['user']['edge_follow']['edges']
                    except KeyboardInterrupt:
                        pass
                    for ns in nu:
                        n6 = str(ns["node"]["username"])
                except KeyboardInterrupt:
                    pass
            else:
                try:
                    nu = json.loads(r8.text)['data']['user']['edge_follow']['edges']
                    for ns in nu:
                        n6 = str(ns["node"]["username"])
                    return {'Status':'Ok','Users':nu}
                except KeyboardInterrupt:
                    pass
                ZAID22 += 1
#def GetListInsta_FS(n5,sessionid):
    try:
        u6 = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={n5}'
        hd6 = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'mid=Y3bGYwALAAHNwaKANMB8QCsRu7VA; ig_did=092BD3C7-0BB2-414B-9F43-3170EAED8778; ig_nrcb=1; shbid=1685054; shbts=1675191368.6684434090; rur=CLN; ig_direct_region_hint=ATN; csrftoken=gLlFX76z8qqwDgmh8ZIp3uFhAeX4zKdO; ds_user_id=921803283; sessionid={sessionid}',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': generate_user_agent(),
            'x-asbd-id': '198387',
            'x-csrftoken': 'gLlFX76z8qqwDgmh8ZIp3uFhAeX4zKdO',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0g7ECdkTdrXy37TE9AoSnMndccWbB1cqrccYOZSLfcb0pE',
            'x-instagram-ajax': '1006383249',
        }
        r7 = requests.get(u6,headers=hd6).json()
    except json.decoder.JSONDecodeError:
        return {'Status':'False','Sessionid':'False'}
    try:
        id = str(r7['data']['user']['id'])
    except KeyError:
        print('user false')
        exit()
    os.system('clear')
    s1 = {'sessionid':sessionid}
    hd7 = {
    'Host': 'www.instagram.com',
    'User-Agent': Hunter.Services(),
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-IG-App-ID': '936619743392459',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/'+str(n5)+'/followers/',
    'TE': 'Trailers'
    }
    ZAID22 = 0
    r8 = requests.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"'+str(id)+'","include_reel":true,"fetch_mutual":true,"first":50}',headers=hd7,cookies=s1)
    while True:
        if str('"has_next_page":false,') in r8.text:
            try:
                nu = json.loads(r8.text)["data"]["user"]["edge_followed_by"]["edges"]
                if nu == '[]':
                    return {'Status':'False','Sessionid':'False'}
                for ns in nu:
                    n6 = str(ns["node"]["username"])
                pass
            except KeyboardInterrupt:
                pass
        else:
            if ZAID22 != 0:
                try:
                    end = re.findall(',"end_cursor":"(.*)"},"edges":', r8.text)
                    r8 = requests.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"'+str(id)+'","include_reel":true,"fetch_mutual":true,"first":50,"after":"'+end[0]+'"}|',headers=hd7,cookies=s1)
                    try:
                        nu = json.loads(r8.text)["data"]["user"]["edge_followed_by"]["edges"]
                    except KeyboardInterrupt:
                        pass
                    for ns in nu:
                        n6 = str(ns["node"]["username"])
                except KeyboardInterrupt:
                    pass
            else:
                try:
                    nu = json.loads(r8.text)["data"]["user"]["edge_followed_by"]["edges"]
                    for ns in nu:
                        n6 = str(ns["node"]["username"])
                    
                except KeyboardInterrupt:
                    pass
                ZAID22 += 1
                return {'Status':'Ok','Users':nu}
lii = 0
pp = 0
def GetListTik_FG(user):
    global lii,pp
    r = requests.get(f'https://www.tiktok.com/@{user}').text
    k = str(r.split('"UserModule":')[1]).split('"RecommendUserList"')[0]
    s = str(k.split('secUid":"')[1]).split('"')[0]
    id = str(k.split('"id":"')[1]).split('"')[0]
    url = 'https://www.tiktok.com/'
    headers = {'user-agent':str(generate_user_agent())}
    resp = requests.get(url,headers=headers).cookies.get_dict()
    tw = resp['ttwid']
    resp = requests.get(f'https://www.tiktok.com/api/search/user/full/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=0.95&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36%20Edg%2F112.0.1722.58&channel=tiktok_web&cookie_enabled=true&cursor=0&device_id=7167133500737406469&device_platform=web_pc&focus_state=true&from_page=search&history_len=12&is_fullscreen=false&is_page_visible=true&keyword={user}&os=windows&priority_region=&referer=&region=IQ&screen_height=864&screen_width=1536&tz_name=Asia%2FBaghdad&webcast_language=en&msToken=Jh2Un0eoRktVfI93pGX8cCnjRORmfpHcdVk3CX3iFej0oFwd4KkZbjtj4gVtMIcKhXsdNszAv59W5Hv4B1uqr4MEN1QLpDdyPbK0H_5XQxUIeebrnEz3m3lWx7RqYD-vYc_r2dD4dSnBoCz07w==&X-Bogus=DFSzswVLKvhANe8ktehWvBesEu3F&_signature=_02B4Z6wo00001nxbdaQAAIDD9Q7cROrxgA58W3EAAPti03',headers=headers)
    ms = resp.cookies.get_dict()['msToken']
    h = {
            'accept': '*/*',
            'accept-language':'ar-AE,ar-IQ;q=0.9,ar;q=0.8,en-US;q=0.7,en;q=0.6',
            'cookie':'passport_csrf_token=446c23e1b656077bd01b1f379ff01c64; passport_csrf_token_default=446c23e1b656077bd01b1f379ff01c64; tiktok_webapp_theme=dark; cookie-consent={"ga":true,"af":true,"fbp":true,"lip":true,"bing":true,"ttads":true,"reddit":true,"version":"v8"}; _ttp=2HZr0KnJ2pqKwJRyQ8myJ28Lpa8; __tea_cache_tokens_1988={"user_unique_id":"7160599742786815489","timestamp":1667850947815,"_type_":"default"}; passport_auth_status=c8fe9febc06f8f7a271309fa9e4f80e9,; passport_auth_status_ss=c8fe9febc06f8f7a271309fa9e4f80e9,; tt_csrf_token=CSVYu9wW-NbmqJ_cgNMHwEIItUNZGwDPM-hU; tt_chain_token=K01fXiH8q/IKwxFnx8jzcA==; _abck=951F354EE38142028A7429E8C92DB598~0~YAAQVvvOF6YBsxSFAQAAMc+wPgl24s0qz4P3iMup3WLL4PWyu/iF6+jb4qL2RfvMEKOGTv6dPfAH9AA2Hm+t/Z/Qn1TlkKHzKXk+KmuWj5d1dmCzqXD0BWgAUcMFCLRinQHou0lzh0ImXOw3B98dRIVnofWMwN8L8JxOErAxrQfi2JIEgTjNECxiZFYaqhpfLqyAUXBESaQxfCYfbNwLNwAAZvjpAfc1viGc/I9vlRIeVc2jYPA5/YUVwAytWPIOb2RuvdrXc2bfybwD3ffG0godURyE+r0QSJapjZK7kfVwbPGnVLal0dzAQM6MK2iDC5YhXugMYw9ZXB2CIaYRg4Cqy/t6BabKM9i+ZJgdvwWQQ6ljnk0pa1bKBsAYL79BxNMrQWccpQxQhUm9n09604O82PBKq8E=~-1~-1~-1; bm_sz=304AE404FA2929B0E90042E8314D20CA~YAAQVvvOF6kBsxSFAQAAMc+wPhIfC1eYkaU2YudlghSK8pNrkVcLYapeM/xrzvQbQkT9quFNwKNHsG4xkv6anwuDXn+BSd+gzoBWSdRZJscGEzPghGpbTStjyG61DtaJIqpkgjW7q6BEP37XgXgrWfHRdmoN5zraADDH7wpkIQ3UlBq5rj88cFl1IY4CUg2DSRugvtjKk+vcNV5AUjQ++v859Tv3vYF3Ga6m5lifIf0u50u/dC1xeVz0p4ew+7U21dwrDdNrai63bM7T9ArdMNk1q+2YK55FJU7tdQwtKtdLtnI=~4407620~4277556; ak_bmsc=EE17F7D340A941EB628DF68B5981EA8D~000000000000000000000000000000~YAAQVvvOF/8BsxSFAQAAS/SwPhJbeUd2XpuVnfaiGo9WDUNsMw3AUn4T4r4BtvFH6pwejSxQJ/K4aoQUK/hGU8InWjW8iSyWgKZxkNIl6lgAAvUdX8CiKcyfyQKJYfQcPDyxW6dnF6+VF2/BABsRcYTw9LUX6MjuhvgtLs1uh3AbWeHxdZFDhp/YYwjrPxoOEXgItQjGUSsxRhgRubItrsXwhW20gW9y+I7Eq22TORlAZOn+jyrl2bYH6C4yxD8yld+5OcSAQ3zKJfQLUjNj03BMgtlIyYT74OIh6GwUzgtjpGLUCzpqdeiOFZdfZApTnRoTK9J01CpUY+YxrThJKz4dScjK1V78LSd2CkfUakgFa7TXfZ1fgfPX/RW2nkWTe9SZtvDH3f62qd9b5oNojffOAM0fpnNeX06hNWSNDRRuiHOmv3m49PN2cJhknh753LdNdt81kj8LJ3SEe1y3sfHb0nPwafPExOaSSrXviHwj4+yLWrZw+dXy3Q==; sid_guard=5d52768f6a4a876314ea37244edfd0d0|1671794088|21600|Fri,+23-Dec-2022+17:14:48+GMT; uid_tt=9392403db19bcfc1eb8eb48532fd8d5e; uid_tt_ss=9392403db19bcfc1eb8eb48532fd8d5e; sid_tt=5d52768f6a4a876314ea37244edfd0d0; sessionid=5d52768f6a4a876314ea37244edfd0d0; sessionid_ss=5d52768f6a4a876314ea37244edfd0d0; sid_ucp_v1=1.0.0-KDM1ZGU2ODk4YzcyNDJkMzUxNWRiMTVlMzc3OTMyZTNlY2JlYWYwYWMKCRCom5adBhizCxADGgZtYWxpdmEiIDVkNTI3NjhmNmE0YTg3NjMxNGVhMzcyNDRlZGZkMGQw; ssid_ucp_v1=1.0.0-KDM1ZGU2ODk4YzcyNDJkMzUxNWRiMTVlMzc3OTMyZTNlY2JlYWYwYWMKCRCom5adBhizCxADGgZtYWxpdmEiIDVkNTI3NjhmNmE0YTg3NjMxNGVhMzcyNDRlZGZkMGQw; bm_sv=F556D2E15739C190D1B417337724D81E~YAAQVvvOF8ACsxSFAQAAaICxPhJ1QOpVK0jJSh0nuEay3Iz+L/0up1OoP09MVnndgBSzTjunJoYxBBQH4BTuDkQIQY+zt9kedbGoP5/7AUt2jVEq7DfEwQYdr31ZvZiHlhdU2Q5jwNvbZvNzQSokkwHoGbPqes9c4kV0ZGJuEuWc3pLurp0dkRkEBTY0UrcljYpQayw5/w7+4BlpmrMR5UAHElAGf2njGNpz3vRls+WGkTy9l8jRTCEseWkwnA9X~1; ttwid='+tw+'; odin_tt=70015f10b12827e4d2b9cce32ead78da9bd1f5af11487a83ba408d86d9a4fb55ec780a14ad91b601d9fe256fcb8160786311c12ef294e6bf285fbbf7eed8dff8080f26ed1bcedbdfca7244743dcbc60e; msToken='+ms+'; msToken='+ms+'; s_v_web_id=verify_lc0f2h1w_v9MWasYr_Uw4b_4j2o_8gdZ_QkWrSxI57MTt',
            'referer': f'https://www.tiktok.com/@{user}?item_id={id}',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A025F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
    }
    rt = requests.get(f'https://www.tiktok.com/api/user/list/?aid=1988&app_language=ar&app_name=tiktok_web&battery_info=0.88&browser_language=ar-EG&browser_name=Mozilla&browser_online=true&browser_platform=Linux%20aarch64&browser_version=5.0%20%28Linux%3B%20Android%2010%3B%20Infinix%20X690B%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Mobile%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=200&device_id=7227896390197003781&device_platform=web_mobile&focus_state=true&from_page=user&history_len=6&is_fullscreen=false&is_page_visible=true&maxCursor=0&minCursor=0&os=android&priority_region=&referer=https%3A%2F%2Fwww.tiktok.com%2Flogin%3Fenter_from%3Dhomepage_hot%26lang%3Dar%26redirect_url%3Dhttps%253A%252F%252Fwww.tiktok.com%252Fforyou%253Fitem_id%253D7216022215656262917&region=IQ&root_referer=https%3A%2F%2Fwww.google.com%2F&scene=21&screen_height=820&screen_width=360&secUid={s}&tz_name=Asia%2FBaghdad&verifyFp=verify_lh3ospm9_Reu7fKhn_mc4D_4qqD_BFQ3_dphns44cCPKG&webcast_language=ar',headers=h).json()['userList']
    g = 0
    for gt in rt:
        try:
            g+=1
        except IndexError:
            exit()
    return{'status':'ok','users':rt}
def GetListTik_RM():
    url = 'https://www.tiktok.com/'
    headers = {'user-agent':str(generate_user_agent())}
    resp = requests.get(url,headers=headers).cookies.get_dict()
    tw = resp['ttwid']
    resp = requests.get(f'https://www.tiktok.com/api/search/user/full/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=0.95&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36%20Edg%2F112.0.1722.58&channel=tiktok_web&cookie_enabled=true&cursor=0&device_id=7167133500737406469&device_platform=web_pc&focus_state=true&from_page=search&history_len=12&is_fullscreen=false&is_page_visible=true&keyword=Ahmed&os=windows&priority_region=&referer=&region=IQ&screen_height=864&screen_width=1536&tz_name=Asia%2FBaghdad&webcast_language=en&msToken=Jh2Un0eoRktVfI93pGX8cCnjRORmfpHcdVk3CX3iFej0oFwd4KkZbjtj4gVtMIcKhXsdNszAv59W5Hv4B1uqr4MEN1QLpDdyPbK0H_5XQxUIeebrnEz3m3lWx7RqYD-vYc_r2dD4dSnBoCz07w==&X-Bogus=DFSzswVLKvhANe8ktehWvBesEu3F&_signature=_02B4Z6wo00001nxbdaQAAIDD9Q7cROrxgA58W3EAAPti03',headers=headers)
    ms = resp.cookies.get_dict()['msToken']
    chars = 'qwertyuiopasdfghjklzxcvbnm'
    numbers = '12345'
    ch_nu = int(''.join(random.choice(numbers) for i in range(1)))
    ch_ch = str(''.join(random.choice(chars) for i in range(ch_nu)))
    url2 = f'https://www.tiktok.com/api/search/user/full/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=1&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36%20Edg%2F112.0.1722.68&channel=tiktok_web&cookie_enabled=true&cursor=0&device_id=7167133500737406469&device_platform=web_pc&focus_state=true&from_page=search&history_len=5&is_fullscreen=false&is_page_visible=true&keyword={ch_ch}&os=windows&priority_region=&referer=https%3A%2F%2Fwww.tiktok.com%2Flogout%3Fredirect_url%3Dhttps%253A%252F%252Fwww.tiktok.com%252Fforyou&region=IQ&root_referer=https%3A%2F%2Fwww.tiktok.com%2Fforyou&screen_height=864&screen_width=1536&tz_name=Asia%2FBaghdad&webcast_language=en&msToken=N7LASCNduT-MFKDAG_2vQV5KXknnx-LIiTJ8zJtyj1p8ifLDvVbX2DWTFel3Knplp2bFxalDAB9UyLdhDqbQSXUuRkTI5JH12kGMaVNpcIB7iKfjBpPehrTf894yWm5GACHz12r9jdyxylxOQ_Q=&X-Bogus=DFSzswVLZ1TANynytCAcZ-esEuf-&_signature=_02B4Z6wo00001bS8P3wAAIDAPemWnyqLqaW0vDvAAAl903'
    headers2 = {
        'accept': '*/*',
        'accept-language':'ar-AE,ar-IQ;q=0.9,ar;q=0.8,en-US;q=0.7,en;q=0.6',
        'cookie':'passport_csrf_token=446c23e1b656077bd01b1f379ff01c64; passport_csrf_token_default=446c23e1b656077bd01b1f379ff01c64; tiktok_webapp_theme=dark; cookie-consent={"ga":true,"af":true,"fbp":true,"lip":true,"bing":true,"ttads":true,"reddit":true,"version":"v8"}; _ttp=2HZr0KnJ2pqKwJRyQ8myJ28Lpa8; __tea_cache_tokens_1988={"user_unique_id":"7160599742786815489","timestamp":1667850947815,"_type_":"default"}; passport_auth_status=c8fe9febc06f8f7a271309fa9e4f80e9,; passport_auth_status_ss=c8fe9febc06f8f7a271309fa9e4f80e9,; tt_csrf_token=CSVYu9wW-NbmqJ_cgNMHwEIItUNZGwDPM-hU; tt_chain_token=K01fXiH8q/IKwxFnx8jzcA==; _abck=951F354EE38142028A7429E8C92DB598~0~YAAQVvvOF6YBsxSFAQAAMc+wPgl24s0qz4P3iMup3WLL4PWyu/iF6+jb4qL2RfvMEKOGTv6dPfAH9AA2Hm+t/Z/Qn1TlkKHzKXk+KmuWj5d1dmCzqXD0BWgAUcMFCLRinQHou0lzh0ImXOw3B98dRIVnofWMwN8L8JxOErAxrQfi2JIEgTjNECxiZFYaqhpfLqyAUXBESaQxfCYfbNwLNwAAZvjpAfc1viGc/I9vlRIeVc2jYPA5/YUVwAytWPIOb2RuvdrXc2bfybwD3ffG0godURyE+r0QSJapjZK7kfVwbPGnVLal0dzAQM6MK2iDC5YhXugMYw9ZXB2CIaYRg4Cqy/t6BabKM9i+ZJgdvwWQQ6ljnk0pa1bKBsAYL79BxNMrQWccpQxQhUm9n09604O82PBKq8E=~-1~-1~-1; bm_sz=304AE404FA2929B0E90042E8314D20CA~YAAQVvvOF6kBsxSFAQAAMc+wPhIfC1eYkaU2YudlghSK8pNrkVcLYapeM/xrzvQbQkT9quFNwKNHsG4xkv6anwuDXn+BSd+gzoBWSdRZJscGEzPghGpbTStjyG61DtaJIqpkgjW7q6BEP37XgXgrWfHRdmoN5zraADDH7wpkIQ3UlBq5rj88cFl1IY4CUg2DSRugvtjKk+vcNV5AUjQ++v859Tv3vYF3Ga6m5lifIf0u50u/dC1xeVz0p4ew+7U21dwrDdNrai63bM7T9ArdMNk1q+2YK55FJU7tdQwtKtdLtnI=~4407620~4277556; ak_bmsc=EE17F7D340A941EB628DF68B5981EA8D~000000000000000000000000000000~YAAQVvvOF/8BsxSFAQAAS/SwPhJbeUd2XpuVnfaiGo9WDUNsMw3AUn4T4r4BtvFH6pwejSxQJ/K4aoQUK/hGU8InWjW8iSyWgKZxkNIl6lgAAvUdX8CiKcyfyQKJYfQcPDyxW6dnF6+VF2/BABsRcYTw9LUX6MjuhvgtLs1uh3AbWeHxdZFDhp/YYwjrPxoOEXgItQjGUSsxRhgRubItrsXwhW20gW9y+I7Eq22TORlAZOn+jyrl2bYH6C4yxD8yld+5OcSAQ3zKJfQLUjNj03BMgtlIyYT74OIh6GwUzgtjpGLUCzpqdeiOFZdfZApTnRoTK9J01CpUY+YxrThJKz4dScjK1V78LSd2CkfUakgFa7TXfZ1fgfPX/RW2nkWTe9SZtvDH3f62qd9b5oNojffOAM0fpnNeX06hNWSNDRRuiHOmv3m49PN2cJhknh753LdNdt81kj8LJ3SEe1y3sfHb0nPwafPExOaSSrXviHwj4+yLWrZw+dXy3Q==; sid_guard=5d52768f6a4a876314ea37244edfd0d0|1671794088|21600|Fri,+23-Dec-2022+17:14:48+GMT; uid_tt=9392403db19bcfc1eb8eb48532fd8d5e; uid_tt_ss=9392403db19bcfc1eb8eb48532fd8d5e; sid_tt=5d52768f6a4a876314ea37244edfd0d0; sessionid=5d52768f6a4a876314ea37244edfd0d0; sessionid_ss=5d52768f6a4a876314ea37244edfd0d0; sid_ucp_v1=1.0.0-KDM1ZGU2ODk4YzcyNDJkMzUxNWRiMTVlMzc3OTMyZTNlY2JlYWYwYWMKCRCom5adBhizCxADGgZtYWxpdmEiIDVkNTI3NjhmNmE0YTg3NjMxNGVhMzcyNDRlZGZkMGQw; ssid_ucp_v1=1.0.0-KDM1ZGU2ODk4YzcyNDJkMzUxNWRiMTVlMzc3OTMyZTNlY2JlYWYwYWMKCRCom5adBhizCxADGgZtYWxpdmEiIDVkNTI3NjhmNmE0YTg3NjMxNGVhMzcyNDRlZGZkMGQw; bm_sv=F556D2E15739C190D1B417337724D81E~YAAQVvvOF8ACsxSFAQAAaICxPhJ1QOpVK0jJSh0nuEay3Iz+L/0up1OoP09MVnndgBSzTjunJoYxBBQH4BTuDkQIQY+zt9kedbGoP5/7AUt2jVEq7DfEwQYdr31ZvZiHlhdU2Q5jwNvbZvNzQSokkwHoGbPqes9c4kV0ZGJuEuWc3pLurp0dkRkEBTY0UrcljYpQayw5/w7+4BlpmrMR5UAHElAGf2njGNpz3vRls+WGkTy9l8jRTCEseWkwnA9X~1; ttwid='+tw+'; odin_tt=70015f10b12827e4d2b9cce32ead78da9bd1f5af11487a83ba408d86d9a4fb55ec780a14ad91b601d9fe256fcb8160786311c12ef294e6bf285fbbf7eed8dff8080f26ed1bcedbdfca7244743dcbc60e; msToken='+ms+'; msToken='+ms+'; s_v_web_id=verify_lc0f2h1w_v9MWasYr_Uw4b_4j2o_8gdZ_QkWrSxI57MTt',
        'referer': 'https://www.tiktok.com/search/user?q=its.veba&t=1671705430400',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A025F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
    }
    resp2 = requests.get(url2,headers=headers2).json()['user_list']
    return {'status':'ok','users':resp2}
def generate_tiktok_username():
        adjectives = ["happy", "sunny", "funny", "crazy", "cool"]
        nouns = ["cat", "dog", "bird", "rabbit", "fish"]
        numbers = random.randint(10, 99)
        
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        
        username = f"{adjective}_{noun}_{numbers}"
        return username
def check_tiktok_username(username):
        url = f"https://www.tiktok.com/@{username}"
        response = requests.get(url)
        
        if response.status_code == 200:
        	return True
        else:
            return False
def generate_instagram_username():
        adjectives = ["beautiful", "awesome", "lovely", "mysterious", "fierce"]
        nouns = ["sunset", "moon", "star", "ocean", "mountain"]
        numbers = random.randint(100, 999)
def check_instagram_username(username):
        url = f"https://www.instagram.com/{username}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            return True
        else:
            return False
def generate_youtube_username():
        adjectives = ["creative", "amazing", "talented", "brilliant", "fantastic"]
        nouns = ["artist", "musician", "vlogger", "gamer", "influencer"]
        numbers = random.randint(1000, 9999)
        
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        
        username = f"{adjective}_{noun}_{numbers}"
        return username
def check_youtube_username(username):
        url = f"https://www.youtube.com/{username}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return True
        else:
            return False
def get_email():
        s = ["@gmail.com" ,"@yahoo.com" ,"@hotmail.com" ,"@aol.com" ,"@outlook.com"]
        domin = random.choice(s)
        url = 'https://randommer.io/random-email-address'
        headers = {
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '239',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '.AspNetCore.Antiforgery.9TtSrW0hzOs=CfDJ8DJ-g9FHSSxClzJ5QJouzeI7-q_vZxCnhkeFlGapcHZgJbZ-aP87NSgO15EqlMTNlpWsrTtDK8Qo_FkcelUen-XMHT8ZaUCFeGiAhGS8O7Ny-7XLvjZQza8gyEX141ln397mg-FwkxUmh8CBjHv4QKw',
            'origin': 'https://randommer.io',
            'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()),
            'x-requested-with': 'XMLHttpRequest'}

        data = {
            'number': "1",'culture': 'en_US',
            '__RequestVerificationToken': 'CfDJ8DJ-g9FHSSxClzJ5QJouzeLi6tSHIeSyq6LHD-lqesWRBHZhI32LFnxMH163TgAQwwE7dRIDYclgxYfDODEZgqrDwuegjkOko7L88MqV4BLhOsmSdGm9gFbDalgtuV6lb3bhat9gHttOROyeP72M4aw',
            'X-Requested-With': 'XMLHttpRequest'}
        req = requests.post(url, headers=headers, data=data).text
        data = req.replace('[' ,'').replace(']' ,'').split(',')
        for i in data:
            eail = i.replace('"' ,'')
            ema = eail.split("@")[0]
            email = ema + domin
            return email
def csrf_token():
        headers = {"User-Agent": str(generate_user_agent())}
        with requests.Session() as azoz:
            url_tok = "https://www.instagram.com/"
            data = azoz.get(url_tok, headers=headers).content
            token = re.findall('{"config":{"csrf_token":"(.*)","viewer"', str(data))[0]
        return {'csrf_token' :str(token)}
def insta(email: str) -> str:
    	url = "https://i.instagram.com/api/v1/users/lookup/"
    	headers = {
			        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			        'Host': 'i.instagram.com',
			        'Connection': 'Keep-Alive',
			        'User-Agent': 'Instagram 6.12.1 Android (25/7.1.2; 160dpi; 383x680; LENOVO/Android-x86; 4242ED1; x86_64; android_x86_64; en_US)',
			        'Accept-Language': 'en-US',
			        'X-IG-Connection-Type': 'WIFI',
			        'X-IG-Capabilities': 'AQ==',}
    	data = 'signed_body=acd10e3607b478b845184ff7af8d796aec14425d5f00276567ea0876b1ff2630.%7B%22_csrftoken%22%3A%22rZj5Y3kci0OWbO8AMUi0mWwcBnUgnJDY%22%2C%22q%22%3A%22'+str(email)+'%22%2C%22_uid%22%3A%226758469524%22%2C%22guid%22%3A%22a475d908-a663-4895-ac60-c0ab0853d6df%22%2C%22device_id%22%3A%22android-1a9898fad127fa2a%22%2C%22_uuid%22%3A%22a475d908-a663-4895-ac60-c0ab0853d6df%22%7D&ig_sig_key_version=4'
    	res = requests.post(url, headers=headers, data=data).text
    	if '"status":"ok"' in res:
    		return {'status':'Success','email':True}
    	else:
    		return {'status':'error','email':False}
def get_tiktok_user_info(username):
    url = f"https://www.tiktok.com/@{username}?lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        user_info = {}
        user_info[" اسم "] 
        user_info["يوزر "]
        user_info[" سيرة ذاتية "]
        user_info[" عدد المتابعهم "]
        user_info[" عدد المتابعين "]
        user_info[" عدد مقاطع الحساب "]
        user_info[" عدد لايكات الحساب "]
        
        return user_info
    else:
        return None