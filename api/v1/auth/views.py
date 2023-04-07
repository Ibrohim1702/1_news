import datetime
import random

from rest_framework.generics import GenericAPIView
from regis.models import User, Otp
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import base64
import uuid


class RegisView(GenericAPIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data

        nott = ["phone", 'password', 'username', 'first_name', 'last_name']
        s = ''
        for i in nott:
            for i in nott:
                if i not in data:
                    s += f" {i} "
        if s:
            return Response({
                "Error": f"datada {s} polyalar toldirilmagan"
            })

        # if i not in data:
        #     return Response({
        #         "Error": f'{i} toldirilmagan'
        #     })

        if len(data['phone']) != 12:
            return Response({"Error": "Telefon + qoyilmagan holatda 12 ta bolishi kere"})

        if not data['phone'].isdigit():
            return Response({"Error": "Telefon sonlada boladiyu harp "})

        if len(data['password']) < 6:
            return Response({"Error": "parol juda oddiy va parol 6 ta simvoldan kop bolishi kere"})

        user = User.objects.create_user(
            phone=data['phone'],
            password=data.get('password', ''),
            username=data.get('username', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
        )

        return Response({
            "Success": "foydalanuvchi ro`yxatdan otdi",
            "user": user
        })


class LoginView(GenericAPIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        # if 'phone' not in data or 'password' not in data:
        #     return Response({
        #         "Error": "data to'lliq emas"
        #     })

        nott = 'phone' if 'phone' not in data else 'password' if 'password' not in data else None
        if nott:
            return Response({
                "Error": f"{nott} to'ldirilmagan"
            })
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            return Response({
                "Error": "Bu raqamga tegishli user topilmadi"
            })
        if not user.check_password(data['password']):
            return Response({
                "Error": "Parol Xato"
            })

        # datada yana nimadirlar kirib kesa qogan ishlar shu yerda qilinadi
        # tokenlar tekshiruvi

        token = Token.objects.get_or_create(user=user)[0]

        return Response({
            "Success": token.key,
            'user': user.format()
        })


class AuthOne(GenericAPIView):
    """bu api sms chiqarib yuborish uchun"""

    def post(self, requests, *args, **kwargs):
        data = requests.data
        if 'phone' not in data:
            return Response({
                "Error": "phone to'ldirilmagan"
            })
        start = 100000
        end = 999999
        son = random.randint(start, end)
        # smsga o'tib sms chiqib foydalanuvchidan keladi

        token = uuid.uuid4().__str__() + "$" + str(son) + '$' + uuid.uuid4().__str__()

        shifr = base64.b64encode(token.encode()).decode()
        otp = Otp.objects.create(
            key=shifr,
            phone=data['phone'],
            step='one'
        )

        # sms bo'p chiqib ketad
        # for i in range(5):
        #     shifr = base64.b64encode(str(shifr).encode())
        # print(b"958624")  # binar
        # unshifr = 'YidZaWRaYVdSYVlWZFNVVlZyVmtaTlJsRjNWVzVLVGxVeVRUbEtkejA5Snc9PSc='
        # for i in range(4):
        #     unshifr = base64.b64decode(unshifr).decode()
        #     print(unshifr)

        return Response({
            "otp": son,
            # "token": token,
            "otp_token": otp.key,
            # "unshifr": unshifr
        })


class AuthTwo(GenericAPIView):
    """bu api smsdagi maxfiy kodni tekshirish"""

    def post(self, requests, *args, **kwargs):
        data = requests.data
        if 'sms' not in data or 'token' not in data:
            return Response({
                "Error": "data toliq emas  "
            })
        otp = Otp.objects.filter(key=data['token']).first()
        if not otp:
            return Response({
                "Error": "Token xato"
            })
        if otp.is_expired:
            return Response({
                "Error": "Token eskirgan"
            })
        now = datetime.datetime.now(datetime.timezone.utc)

        if (now-otp.created).total_seconds() >=  120:
            otp.is_expired = True
            otp.save()
            return Response({
                "Error": "Otp uchun berilgan voxt tugad"
            })


        deshifr = base64.b64decode(otp.key).decode()
        son = deshifr.split('$')[1]
        if str(son) != str(data['sms']):
            otp.tries = otp.tries + 1
            otp.save()
            return Response({
                "Error": "parol xato kim bilan oynashvotganin blmayapsa"
            })

        user = User.objects.filter(phone=otp.phone).first()

        return Response({
            "is_registered": user is not None
        })






