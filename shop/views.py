from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from config.settings import UPLOAD_DIR

# Create your views here.
from frame.cartdb import CartDB
from frame.custdb import CustDB
from frame.itemdb import ItemDB
from frame.error import ErrorCode

import logging
logger = logging.getLogger('users')
# logging.basicConfig(filename='logtest.log', encoding='utf-8', level=logging.WARNING)   # 파이썬 기본 로깅 시스템



def home(request):
    return render(request, 'home.html');

def login(request):
    return render(request, 'login.html')

def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    print('세션1:', request.session.keys())

    try:
        cust = CustDB().selectOne(id)      # id가 db에 없으면 이 부분에서 오류남
        if pwd == cust.pwd:      # 입력한 pwd와 저장된 cust.pwd의 정보가 같은 경우
            request.session['logincust']  = {'id': cust.id, 'name': cust.name}    # 사용자 정보를 세션에 저장
            print('세션2:', request.session.keys())
            next = 'home.html'
            context = None
        else:
            raise Exception
    except:
        next = 'error.html'
        context = {'msg': ErrorCode.e0003}

    return render(request, next, context)


def logout(request):
    if request.session['logincust'] != None:    # 로그인된 상태에서
        del request.session['logincust']        # logincust라는 키 값을 사전에서 삭제
        print('세션3:', request.session.keys())

    return render(request, 'home.html')

#---------------------------------------------------------------------------------------------------------

def inputcart(request):
    custid = request.GET['custid']
    itemid = request.GET['itemid']     # itemid, num은 문자열
    num = request.GET['num']
    CartDB().insert(custid, int(itemid), int(num))
    return redirect('itemlist')

def cartlist(request):
    custid = request.GET['custid']
    print(custid)
    cartlist = CartDB().selectCust(custid)     # 객체 리스트 반환
    print(cartlist)
    context = {'cartlist': cartlist}
    return render(request, 'cartlist.html', context);

#-----------------------------------------------------------------------------------------------------

def custlist(request):
    clist = CustDB().selectAll()
    context = {'clist': clist}
    return render(request, 'custlist.html', context);

def custdetail(request):
    id = request.GET['id']
    cust = CustDB().selectOne(id)
    context = {'cust': cust}
    return render(request, 'custdetail.html', context)

def custdelete(request):
    id = request.GET['id']
    CustDB().delete(id)
    return redirect('custlist')        # 삭제 후 custlist.html 페이지로 이동시킴. url name을 인수로 받음

def custupdate(request):
    id = request.GET['id']
    cust = CustDB().selectOne(id)
    context = {'cust': cust}
    return render(request, 'custupdate.html', context)

def custupdateimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    name = request.POST['name']
    CustDB().update(id, pwd, name)
    # custdetail?id=id01 주소로 이동하기 위해서 아래 과정 진행
    qstr = urlencode({'id': id})       # query string
    return HttpResponseRedirect('%s?%s' %('custdetail', qstr))

def custadd(request):
    return render(request, 'custadd.html');

def custaddimpl(request):
    id = request.POST['id']    # raise MultiValueDictKeyError(key) 오류
    pwd = request.POST['pwd']
    name = request.POST['name']
    try:
        CustDB().insert(id, pwd, name)
    except:
        context = {'msg': ErrorCode.e0001}
        return render(request, 'error.html', context)      # 에러 페이지로 이동. 에러났을 때는 return해서 여기서 함수가 끝남
    # 조회 화면으로 이동
    return redirect('custlist')

#-----------------------------------------------------------------------------------------------------------------------

def itemlist(request):
    ilist = ItemDB().selectAll()
    context = {'ilist': ilist}
    return render(request, 'itemlist.html', context)

def itemdetail(request):
    itemid = request.GET['id']     # itemid는 문자열
    item = ItemDB().selectOne(int(itemid))
    custid = request.session['logincust']['id']
    temp = '30ºC'
    weather = 'Sunny'
    logger.debug(custid + ', ' + item.name + ', ' + str(item.price) + ', ' + temp + ', ' + weather)

    # 파이썬 기본 로깅 시스템 - 기본 레벨인 warning 이상만 기록
    # logging.debug('디버그')
    # logging.info('인포')
    # logging.warning('워닝')
    # logging.error('에러')
    # logging.critical('크리티컬')

    context = {'item': item}
    return render(request, 'itemdetail.html', context)


def itemadd(request):
    return render(request, 'itemadd.html');

def itemaddimpl(request):
    name = request.POST['name']
    price = request.POST['price']

    if 'img' in request.FILES:      # 요청으로 받은 파일에 name="img"가 있는 경우
        img = request.FILES['img']
        # print(img, type(img))                 # 받은 파일 이름, django.core.files.uploadedfile.InMemoryUploadedFile
        # print(img.name, type(img.name))       # 받은 파일 이름, str
        # print(img._name, type(img._name))     # 받은 파일 이름, str

        fp = open('%s/%s' %(UPLOAD_DIR, img), 'wb')    # 이미지 파일은 바이너리
        for chunk in img.chunks():
            fp.write(chunk)
            fp.close()

    ItemDB().insert(name, int(price), img)      # price는 문자열이므로 int로 바꿔줌
    return redirect('itemlist')


def itemdelete(request):
    id = request.GET['id']
    ItemDB().delete(int(id))
    return redirect('itemlist')   # url name

def itemupdate(request):
    id = request.GET['id']
    item = ItemDB().selectOne(int(id))
    context = {'item': item}
    return render(request, 'itemupdate.html', context)

def itemupdateimpl(request):
    id = request.POST['id']
    name = request.POST['name']
    price = request.POST['price']
    oldimgname = request.POST['oldimgname']     # newimg와 별개로 oldimgname은 항상 전달되는 값이다.
    # print(id, name, price, oldimgname)

    imgname = ''     # newimg가 될 수도 있고 oldimgname이 될 수도 있다

    # print(request.FILES)               # <MultiValueDict: {'newimg': [<InMemoryUploadedFile: pants4.jpg (image/jpeg)>]}>
    if 'newimg' in request.FILES:        # request.FILES: 실제로 파일을 업로드 한 경우만 값이 있음
        newimg = request.FILES['newimg']
        # print(newimg)                  # pants4.jpg
        imgname = newimg.name            # 강사님은 newimg._name이라고 했는데 API 문서에 따라 .name으로 했음
        # print(imgname)                    # pants4.jpg
        # print(newimg.read())              # binary string - 파일이 클 때 메모리로 읽어들이려고 하면 시스템에 무리가 됨(비추)
        # print(newimg.chunks())            # InMemoryUploadedFile.chunks 객체 생성

        fp = open('%s/%s' % (UPLOAD_DIR, imgname), 'wb')   # 업로드 폴더에 해당 파일 이름으로 새파일 열기(기존 파일 있었으면 지워짐)
        for chunk in newimg.chunks():
            # print('chunk:', chunk)        # binary string - .read() 결과와 같다
            fp.write(chunk)
            fp.close()

    else:
        imgname = oldimgname

    ItemDB().update(int(id), name, int(price), imgname)
    qstr = urlencode({'id': id})
    # print(qstr)          # id=1010

    # return HttpResponseRedirect('%s?%s' %('itemdetail', qstr))
    # return HttpResponseRedirect('itemdetail?%s' %(qstr))
    return HttpResponseRedirect('itemdetail?id=%d' %(int(id)))   # 모두 동일한 결과

