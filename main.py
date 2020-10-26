# 创建一个dict，存放图书
books={"C Programming":{"id":1,"price":100.00},
       "C++ Programming":{"id":2,"price":200.00},
       "Java Programming":{"id":3,"price":300.00},
       "Python Programming":{"id":4,"price":400.00}
       }
# 创建一个list
menu=["1、add a new book","2、modify the bookshelf","3、delete the bookshelf","4、query the bookshelf","5、exit the system"]

# 系统启动+菜单展示
def start():
    print("Welcome to the library management system")
    # 菜单展示
    for i in menu:
        print("**%s**" % i)
    choose()

# 功能选择
def choose():
    choosenum = input("Please select a option：")
    # 添加新书
    if choosenum=="1":
        print("Adding a new book...")
        while True:
            add_bookname = input("Input the title of the book to be added:")
            # 如果图书馆已经有这本书
            if ifexist(bookname=add_bookname):
                s=input("There is already this book！\nPlease input 0 to re-select the function, input 1 to continue adding a new book：")
                # 输入0回到choose（）
                if s=="0":
                    return choose()
                # 输入1停止剩余的语句，继续下一次的循环
                elif s=="1":
                    continue
                else:
                    print("Input error, has been exited！")
                    # 退出系统
                    exit()
            # 如果图书馆没有这本书，跳出while循环
            else:
                break
        while True:
            add_bookid = input("Please enter the shelf number to be placed:")
            # 如果书架号已经被占用
            if ifexist(bookid=add_bookid):
                s=input("This bookshelf is already occupied!\nPlease input 0 to reselect the function, input 1 to continue adding bookshelf：")
                if s=="0":
                    return choose()
                elif s=="1":
                    continue
                else:
                    print("Input error, has been exited！")
                    exit()
            # 如果书架号没有被占用，跳出while循环
            else:
                break
        # 输入书的价格
        add_bookprice=input("Please input the price of the book：")
        # 创建一个dict
        add_bookidprice={"id":add_bookid,"price":add_bookprice}
        # 往图书馆中添加新书
        newbook(add_bookname,**add_bookidprice)
        # 展示所有的图书
        showbooks(**books)
    # 修改书架
    elif choosenum=="2":
        # 输入书名
        update_bookname=input("Please input the title of the book to be modified：")
        # 对着书名，修改其书架号和价格
        updatebook(update_bookname)
    # 删除书架
    elif choosenum=="3":
        # 输入书名
        del_bookname = input("Please select the title of the book to be deleted：")
        # 删除这本书的所有的记录
        deletebook(del_bookname)
    # 查询书架
    elif choosenum=="4":
        # 展示所有的图书
        showbooks(**books)
    # 退出系统
    elif choosenum=="5":
        print("Exit system！")
        # 退出系统
        exit()
    else:
        # 输入的功能不是1、2、3、4、5，抛出“输入的参数有误”
        if isinstance(choosenum, str):
            raise TypeError("Incorrect input parameters！")
        else:
            # 退出系统
            exit()

# 修改书架
def updatebook(bookname):
    # 查看书本是否已经存在
    if ifexist(bookname=bookname):
        num=input("What do you want to modify? Input 1 to modify the shelf number, input 2 to modify the price, input other to exit：")
        # 修改书的书架号
        if num=="1":
            while True:
                updatebook_id=input("Which bookshelf do you want to put on？：")
                # 查看书架号是否被占用
                if ifexist(bookid=updatebook_id):
                    print("This bookshelf is full！")
                    # 停止剩下的语句，继续下一次循环
                    continue
                else:
                    # 修改书架号
                    books[bookname]["id"]=int(updatebook_id)
                    print("Successfully modify the bookshelf number！")
                    # 展示所有的图书
                    showbooks(**books)
        # 修改书的价格
        elif num=="2":
            updatebook_price=float(input("Input new price："))
            # 修改输的价格
            books[bookname]["price"]=updatebook_price
            print("Price modified successfully！")
            # 展示所有的图书
            showbooks(**books)
        else:
            # 退出系统
            exit()
    # 图书馆没有这本书，返回主键面
    else:
        print("The library does not have this book！")
        return choose()
#删除书架
def deletebook(bookname):
    # 查看图书馆是否有这本书
    if ifexist(bookname=bookname):
        # 删除这本书
        books.pop(bookname)
        print("Deleted%s" % bookname)
        # 返回主键面
        return choose()
    else:
        print("The library does not have this book！")
        return choose()

# 新书存入图书馆
def newbook(bookname,**kwargs):
    # 新书存入图书馆中
    books[bookname]=kwargs
    print("Added successfully！")

# 展示图书馆的所有的图书
def showbooks(**kwargs):
    # 遍历books
    for i in kwargs:
        print("name=%s,id=%d,price=%.2f" % (i,int(books[i]["id"]),float(books[i]["price"])))
    # 遍历完返回主键面
    return choose()

# 判断书名或者id是否存在于图书馆系统中
def ifexist(bookname='',bookid=''):
    # 书名不为空
    if bookname != '':
        # 如果图书馆有这本书，返回True
        if bookname in books:
            return True
        # 图书馆没有这本书，返回False
        else:
            return False
    else:
        # 遍历一个dict
        for i in books:
            # 如果输入参数bookid等于某个图书馆书架的id，返回True
            if int(bookid)==books[i]['id']:
                return True
        return False
# 程序启动
start()