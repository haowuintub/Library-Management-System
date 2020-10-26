import time

import pandas as pd
import os
import matplotlib.pyplot as plt

# 先定义一个配置类
# from Tools.scripts.treesync import input()


class Config:
    # 定义表一
    table1_url = "C:\\Users\\Shinelon\\Desktop\\untitled\\resource\\table1.csv"
    table1_header = ["书号", "书名", "出版社", "作者", "价格", "库存"]
    # 定义表二
    table2_url = "C:\\Users\\Shinelon\\Desktop\\untitled\\resource\\table2.csv"
    table2_header = ["学号", "书号", "借阅日期"]
    # 定义表三
    table3_url = "C:\\Users\\Shinelon\\Desktop\\untitled\\resource\\table3.csv"
    table3_header = ["学号", "姓名", "性别", "班级"]


class library_system(object):
    def __init__(self):
        print("图书馆系统初始化中...")
        self.input_table1_table2()
        self.book_table, self.borrow_table, self.student_table = self.get_info_from_file()
        print("图书馆系统初始化完成！")
        self.menu()

    def input_table1_table2(self):
        print("请输入图书馆藏书表")
        table1 = []
        print("输入藏书表:书号 书名 出版社 作者 价格 库存\n")
        x = input()('请输入数据：')
        while x != "exit\n":
            y = x.split()
            if len(y) != 6:
                x = input()('列数不一致\n请重新输入:')
            else:
                table1.append(y)
                x = input()('下一条记录:')
        print("请输入学生信息表")
        table3 = []
        print("输入学生表:学号 姓名 性别 班级\n")
        x = input()('请输入数据:')
        while x != "exit\n":
            y = x.split()
            if len(y) != 4:
                x = input()('数据列数不一致\n请重新输入:')
            else:
                table3.append(y)
                x = input()('下一条记录:')
        table1 = pd.DataFrame(table1)
        table3 = pd.DataFrame(table3)
        table1.to_csv(Config.table1_url, header=Config.table1_header, index=None)
        table3.to_csv(Config.table3_url, header=Config.table3_header, index=None)

    def get_info_from_file(self):
        book_table = pd.read_csv(Config.table1_url)
        borrow_table = []
        student_table = pd.read_csv(Config.table3_url)
        print("信息读取成功...")
        return book_table, borrow_table, student_table

    def save_file(self):
        self.book_table.to_csv(Config.table1_url, header=Config.table1_header, index=None)
        boo = pd.DataFrame(self.borrow_table)
        boo.to_csv(Config.table2_url, header=Config.table2_header, index=None)
        self.student_table.to_csv(Config.table3_url, header=Config.table3_header, index=None)
        print("保存文件成功")

    # 实现借阅功能：输入学号和书号，如果借阅成功（学号所对应的学生在表3中并且书号所对应的图书在表1中且库存大于等于1），修改表1和表2，并保存到文件
    def borrow(self, student_id, book_id):
        flag1 = True
        for i in range(len(self.student_table["学号"])):
            if int(self.student_table["学号"][i]) == int(student_id):
                print("查询到该学生")
                flag1 = False
                for j in range(len(self.book_table["书号"])):
                    if int(self.book_table["书号"][j]) == int(book_id) and int(self.book_table["库存"][j]) > 0:
                        print("库存充足")
                        self.book_table["库存"][j] = str(int(self.book_table["库存"][j]) - 1)
                        borrow = [student_id, book_id, time.strftime("%d/%m/%Y")]
                        self.borrow_table.append(borrow)
                        self.save_file()
                        break
            if not flag1:
                break
        if flag1:
            print("未查询到该学生")
        print("借阅图书")

    # 实现还书功能：从表2中删除该学生的借阅信息，并修改表1的库存信息，并保存到文件
    def let_back(self, student_id, book_id):
        for j in range(len(self.book_table["书号"])):
            if int(self.book_table["书号"][j]) == int(book_id):
                self.book_table["库存"][j] = str(int(self.book_table["库存"][j]) + 1)
                for i in range(len(self.borrow_table)):
                    if int(self.borrow_table[i][0]) == int(student_id) and int(self.borrow_table[i][1]) == int(book_id):
                        del self.borrow_table[i]
                        self.save_file()
                        break
                break

        print("还书")

    # 输入某书号，可以查询借阅该书的学生信息
    def find_by_book_id(self, book_id):
        stu_ids = set()
        # 先获取对应人的学号
        for i in range(len(self.borrow_table)):
            if int(self.borrow_table[i][1]) == int(book_id):
                stu_ids.add(int(self.borrow_table[i][0]))
        stu = []
        for i in range(len(self.student_table["学号"])):
            if int(self.student_table["学号"][i]) in stu_ids:
                stu.append(self.student_table.iloc[i])
        print("查询借了某本书的学生信息")
        print(stu)

    def sum_by_student_id(self, student_id):
        sum = 0
        for i in range(len(self.borrow_table)):
            if int(self.borrow_table[i][0]) == int(student_id):
                sum += 1
        print("统计某学生当前借书量" + str(sum))

    # 统计某出版社的藏书量，统计某学生当前借书量
    def sum_by_publish(self, publish_name):
        book_id = set()
        sum = 0
        for i in range(len(self.book_table["出版社"])):
            if str(self.book_table["出版社"][i]) == str(publish_name):
                book_id.add(int(self.book_table["出版社"][0]))
                sum += int(self.book_table["库存"][i])
        for i in range(len(self.borrow_table)):
            if self.borrow_table[i][1] in book_id:
                sum += 1
        print(str(publish_name) + "统计藏书量" + str(sum))
        return sum

    # 输入某学生姓名，可以查询该生的借阅图书信息
    def find_by_student_name(self, student_name):
        stu_id = set()
        for i in range(len(self.student_table["姓名"])):
            if str(self.student_table["姓名"][i]) == str(student_name):
                stu_id.add(int(self.student_table["学号"][i]))
                print("找到")
        book_id = set()
        res = []
        for i in range(len(self.borrow_table)):
            if int(self.borrow_table[i][0]) in stu_id:
                book_id.add(int(self.borrow_table[i][1]))
        for i in range(len(self.book_table["书号"])):
            if int(self.book_table["书号"][i]) in book_id:
                res.append(self.book_table.iloc[i])
        print("查询某学生的借书信息")
        print(res)

    # 获取各出版社的藏书量折线图
    def get_publish(self):
        pub = set()
        for i in range(len(self.book_table["出版社"])):
            pub.add(str(self.book_table["出版社"][i]))
        pubL = list(pub)
        x1 = range(len(pubL))
        numL = []
        for i in range(len(pubL)):
            numL.append(self.sum_by_publish(pubL[i]))
        plt.title('各出版社的藏书量折线图')
        plt.xlabel('出版社名字')
        plt.ylabel('藏书量')
        plt.plot(pubL, numL, 'r', label='藏书量')
        plt.xticks(x1, pubL, rotation=0)
        plt.legend()
        plt.grid()
        plt.show()
        # 利用第三方库matplotlib中的pyplot绘制统计图，如绘制各出版社的藏书量折线图，绘制各学生借书量的饼图等

    def get_stu(self):
        stu_id = set()
        for i in range(len(self.student_table["学号"])):
            stu_id.add(int(self.student_table["学号"][i]))
        stuL = list(stu_id)
        numL = []
        for i in range(len(stuL)):
            numL.append(self.sum_by_student_id(stuL[i]))

        plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
        plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
        plt.pie(numL, labels=stuL, autopct='%1.1f%%')  # 绘制饼图
        plt.title('2018年饼图')  # 绘制标题
        plt.show()

    # 1绘制各出版社的藏书量折线图，2绘制各学生借书量的饼图
    def show_diaglo(self, chos):
        if str(chos) == "1":
            self.get_publish()
        if str(chos) == '2':
            self.get_stu()
        print("展现图表")

    def cls(self):
        os.system("cls")

    def menu(self):
        level_1_choose = input()("按回车继续")
        while level_1_choose != "exit\n":
            self.cls()
            print("图书管理系统菜单\n")
            print("1 借阅功能 请输入： 1 学号 书号")
            print("2 还书功能 请输入： 2 学号 书号")
            print("3 查询学生借阅信息 请输入： 3 学生姓名")
            print("4 查询借该书的学生信息 请输入： 4 书号")
            print("5 统计某出版社的藏书量 请输入： 5 出版社名")
            print("6 统计某学生当前的借书量 请输入： 6 学生学号")
            print("7 绘图功能 请输入：7")
            level_1_choose = input()("请选择1-7你要选择的功能,输入exit退出")
            turn = True
            while turn:
                sp = level_1_choose.split()
                # 1-7
                if sp[0] == "1":
                    if len(sp) == 3:
                        self.borrow(sp[1], sp[2])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                elif sp[0] == "2":
                    if len(sp) == 3:
                        self.let_back(sp[1], sp[2])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                elif sp[0] == "3":
                    if len(sp) == 2:
                        self.find_by_student_name(sp[1])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                elif sp[0] == "4":
                    if len(sp) == 2:
                        self.find_by_book_id(sp[1])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                elif sp[0] == "5":
                    if len(sp) == 2:
                        self.sum_by_publish(sp[1])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                elif sp[0] == "6":
                    if len(sp) == 2:
                        self.sum_by_student_id(sp[1])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                elif sp[0] == "7":
                    if len(sp) == 2:
                        self.show_diaglo(sp[1])
                        turn = False
                    else:
                        turn = True
                        level_1_choose = input()("输入错误，请重新输入\n")
                else:
                    turn = True
                    level_1_choose = input()("输入错误，请重新输入\n")


if __name__ == '__main__':
    ls = library_system()